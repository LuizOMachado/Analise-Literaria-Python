import sys
import re
import time
from ddgs import DDGS
from curl_cffi import requests
from bs4 import BeautifulSoup


from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.status import Status
from rich.rule import Rule
from rich.align import Align

console = Console()

class ConsultorLiterario:
    def __init__(self):
       
        self.session = requests.Session(impersonate="chrome110")
        self.headers = {
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/"
        }

    def exibir_banner(self):
        
        banner = Panel(
            Align.center("[bold yellow]CONSULTOR LITERÁRIO[/bold yellow]\n[cyan][/cyan]"),
            border_style="bright_blue",
            padding=(1, 2)
        )
        console.print(banner)

    def obter_nome_livro(self):
       
        if len(sys.argv) > 1:
            return " ".join(sys.argv[1:])
        return Prompt.ask("[bold cyan]Qual livro você deseja pesquisar hoje?[/bold cyan]")

    def buscar_referencias(self, nome_livro):
        
        query = f'site:skoob.com.br/pt/book/ "{nome_livro}"'
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=3)
                for r in results:
                    url = r['href']
                   
                    match = re.search(r'/book/(\d+)', url)
                    if match:
                        return url, match.group(1)
        except Exception as e:
            console.print(f"[red]Erro na busca externa: {e}[/red]")
        return None, None

    def extrair_conteudo(self, url_principal, book_id):
        
        try:
          
            res_main = self.session.get(url_principal, headers=self.headers, timeout=15)
            soup_main = BeautifulSoup(res_main.text, 'lxml')
            
            titulo = soup_main.find('h1').get_text(strip=True) if soup_main.find('h1') else "Título não identificado"
            nota = soup_main.find('span', class_='bg-success').get_text(strip=True) if soup_main.find('span', class_='bg-success') else "N/A"
            
           
            sinopse_elem = soup_main.find('p', class_='text-contrast')
            sinopse = sinopse_elem.get_text(strip=True) if sinopse_elem else "Sinopse não encontrada."

            
            url_resenhas = f"https://www.skoob.com.br/pt/book/{book_id}/reviews"
            console.print(f"[dim] Debug: Acessando subpágina de resenhas: {url_resenhas}[/dim]")
            
            res_reviews = self.session.get(url_resenhas, headers=self.headers, timeout=15)
            soup_reviews = BeautifulSoup(res_reviews.text, 'lxml')
            
            resenhas = self._parse_comentarios(soup_reviews, sinopse)

            
            if not resenhas:
                console.print("[yellow]  Aviso: Nenhuma resenha na subpágina. Tentando extração na página principal...[/yellow]")
                resenhas = self._parse_comentarios(soup_main, sinopse)

            return {
                "titulo": titulo,
                "nota": nota,
                "sinopse": sinopse,
                "resenhas": resenhas[:10] 
            }
        except Exception as e:
            console.print(f"[bold red]Falha na extração de dados: {e}[/bold red]")
            return None

    def _parse_comentarios(self, soup, sinopse_referencia):
        """Localiza resenhas completas e evita duplicidade com a sinopse."""
        comentarios = []
        
        seletores = soup.select('div#corpo-resenha') or soup.find_all('p', class_='text-contrast')
        
        for item in seletores:
            texto = item.get_text(strip=True)
           
            if len(texto) > 150 and texto[:100] not in sinopse_referencia:
               
                texto_limpo = texto.replace("Ler mais", "").replace("...", "").strip()
                if texto_limpo not in comentarios:
                    comentarios.append(texto_limpo)
        
        return comentarios

    def formatar_saida(self, dados):
        """Interface final ajustada para evitar erros de tipo e melhorar UX."""
        
        console.print() 
        console.print(Rule(f"[bold green]DADOS COLETADOS: {dados['titulo']}[/bold green]", style="bright_magenta"))
        
        console.print(f"\n[bold white]Avaliação Geral:[/bold white] [bold yellow]⭐ {dados['nota']}[/bold yellow]")
        
       
        console.print("\n[bold cyan] SINOPSE[/bold cyan]")
        console.print(Panel(f"[italic white]{dados['sinopse']}[/italic white]", border_style="cyan", padding=(1, 2)))
        
       
        console.print()
        console.print(Rule("[bold yellow]OPINIÃO DOS LEITORES (TEXTO ÍNTEGRO)[/bold yellow]", style="yellow"))
        
        if not dados['resenhas']:
            console.print("[red]Não foi possível recuperar resenhas completas para este título.[/red]")
        else:
            for idx, r in enumerate(dados['resenhas'], 1):
                
                console.print(
                    Panel(
                        f"[white]{r}[/white]",
                        title=f"[bold blue]Comentário #{idx}[/bold blue]",
                        title_align="left",
                        border_style="dim"
                    )
                )
        
        
        console.print()
        console.print(Rule(style="bright_blue"))
        console.print(Align.right("[bold green] Pesquisa finalizada com sucesso![/bold green]"))
        console.print()

def main():
    app = ConsultorLiterario()
    app.exibir_banner()
    
    nome_busca = app.obter_nome_livro()
    
    with Status("[bold green]Vasculhando as prateleiras do Skoob...", console=console) as status:
        url_livro, book_id = app.buscar_referencias(nome_busca)
        
        if not url_livro or not book_id:
            status.stop()
            console.print(f"\n[bold red] Ops! Não encontramos o livro '{nome_busca}' no banco de dados.[/bold red]")
            return

        dados = app.extrair_conteudo(url_livro, book_id)
        
        if dados:
            status.stop()
            app.formatar_saida(dados)

if __name__ == "__main__":
    main()
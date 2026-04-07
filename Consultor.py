import sys
import re
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
            Align.center("[bold yellow]CONSULTOR LITERÁRIO[/bold yellow]\n[cyan]"),
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
                        return url
        except Exception as e:
            console.print(f"[red]Erro na busca externa: {e}[/red]")
        return None

    def extrair_conteudo(self, url_principal):
        try:
            res_main = self.session.get(url_principal, headers=self.headers, timeout=15)
            soup_main = BeautifulSoup(res_main.text, 'lxml')
            
            titulo_elem = soup_main.find('h1')
            titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Título não identificado"
            
            autor = "Autor desconhecido"
            if titulo_elem:
                autor_elem = titulo_elem.find_next('a')
                if autor_elem:
                    autor = autor_elem.get_text(strip=True)

            nota_elem = soup_main.find('span', class_='bg-success')
            nota = nota_elem.get_text(strip=True) if nota_elem else "N/A"
            
            sinopse_elem = soup_main.find('p', class_='text-contrast')
            sinopse = sinopse_elem.get_text(strip=True) if sinopse_elem else "Sinopse não encontrada."

            return {
                "titulo": titulo,
                "autor": autor,
                "nota": nota,
                "sinopse": sinopse
            }
        except Exception as e:
            console.print(f"[bold red]Falha na extração de dados: {e}[/bold red]")
            return None

    def formatar_saida(self, dados):
        
        console.print() 
        
        
        console.print(Rule("[bold green]LIVRO ENCONTRADO[/bold green]", style="bright_magenta"))
        console.print() 
        
       
        console.print(Align.center(f"[bold cyan]{dados['titulo']}[/bold cyan]"))
        
        
        console.print(Align.center(f"[italic white]{dados['autor']}[/italic white]"))
        console.print() 
        
        
        console.print(Align.center(f"[bold white]Avaliação Geral:[/bold white] [bold yellow]⭐ {dados['nota']}[/bold yellow]"))
        console.print()
        
       
        console.print(Align.center("[bold cyan]SINOPSE[/bold cyan]"))
        console.print(Panel(f"[italic white]{dados['sinopse']}[/italic white]", border_style="cyan", padding=(1, 2)))
        
        console.print()
        console.print(Rule(style="bright_blue"))
        console.print(Align.right("[bold green]Pesquisa finalizada com sucesso![/bold green]"))
        console.print()

def main():
    app = ConsultorLiterario()
    app.exibir_banner()
    
    nome_busca = app.obter_nome_livro()
    
    with Status("[bold green]Vasculhando as prateleiras do Skoob...", console=console) as status:
        url_livro = app.buscar_referencias(nome_busca)
        
        if not url_livro:
            status.stop()
            console.print(f"\n[bold red] Ops! Não encontramos o livro '{nome_busca}' no banco de dados.[/bold red]")
            return

        dados = app.extrair_conteudo(url_livro)
        
        if dados:
            status.stop()
            app.formatar_saida(dados)

if __name__ == "__main__":
    main()

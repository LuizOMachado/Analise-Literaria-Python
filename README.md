## Projeto: Consultor Literário (Web Scraping 

# ​O que é o projeto?
​Sabe quando você ouve falar de um livro e quer saber rápido se ele vale o seu tempo? Normalmente, você teria que abrir o navegador, digitar o site do Skoob, pesquisar o título, clicar no livro certo e rolar várias páginas.

​O Consultor Literário faz todo esse "trabalho braçal" por você. É como se você tivesse um assistente pessoal que corre até a biblioteca, identifica o autor, verifica a nota e volta com um resumo pronto em questão de segundos.

# ​Por que ele é útil? (O Problema e a Solução)

​O Problema: Pesquisar livros manualmente é demorado e cheio de distrações. Além disso, ao procurar a sinopse em sites comuns, você corre o risco de ler "spoilers" sem querer nas resenhas dos usuários.

​A Solução: Uma ferramenta onde você apenas digita o nome do livro e recebe, de forma limpa e centralizada:

​O nome do Autor.

​A nota oficial (reputação do livro).

​A sinopse completa.

​Privacidade Visual: Sem anúncios e sem o risco de ler comentários que estraguem a história (spoilers).

# Como a "mágica" acontece?
​O programa funciona através de três pilares:

​O Mensageiro (curl_cffi + DDGS): O programa usa o motor de busca do DuckDuckGo para localizar o livro exato no Skoob e age como um "usuário fantasma", acessando as informações sem precisar abrir um navegador pesado.

​O Tradutor Inteligente (BeautifulSoup): O site original tem muitos elementos. O programa funciona como um filtro que ignora o lixo visual e "pesca" apenas o que interessa: título, autor, nota e a sinopse.

​O Organizador (Python + Rich): Ele pega essas informações e as organiza de um jeito bonito, centralizado e fácil de ler no terminal do seu computador.

# Como utilizar?
​No terminal, instale as bibliotecas necessárias:

pip install -r requirements.txt

​Inicie a consulta: 

python Consultor.py

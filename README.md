## Projeto: Consultor Literário (Web Scraping Skoob)


# O que é o projeto?
Sabe quando você ouve falar de um livro e quer saber rápido se ele vale o seu tempo? Normalmente, você teria que abrir o navegador, digitar o site do Skoob, pesquisar o título, clicar no livro certo e rolar várias páginas para ler o que as pessoas acharam.
O Consultor Literário faz todo esse "trabalho braçal" por você. É como se você tivesse um assistente pessoal que corre até a biblioteca, lê as melhores partes e volta com um resumo pronto em questão de segundos.
# Por que ele é útil? (O Problema e a Solução)
O Problema: Pesquisar opiniões de livros manualmente é demorado e cheio de distrações. Você gasta mais tempo clicando e esperando páginas carregarem do que analisando se o livro é bom.

A Solução: Uma ferramenta onde você apenas digita o nome do livro e recebe, instantaneamente:

A nota oficial (reputação do livro).

As 10 opiniões mais recentes de quem já leu.

# Como a "mágica" acontece?
O programa funciona através de três pilares:

O Mensageiro (Requests): O programa age como um "usuário fantasma". Ele vai até o site do Skoob de forma invisível, sem precisar abrir uma janela de navegador pesada, e pede as informações da página.

O Tradutor Inteligente (BeautifulSoup): O site original é uma bagunça de códigos e anúncios. O programa funciona como um filtro que ignora o lixo visual e "pesca" apenas o que interessa: o título, a nota e o texto das resenhas.

O Organizador (Python): Ele pega essas informações "pescadas" e as organiza de um jeito bonito e fácil de ler na tela do seu computador.

# As Etapas de Construção
Estou construindo esse projeto em passos lógicos para garantir que ele seja robusto:

Fase 1 (O Mapa): Ensinar o programa a transformar o nome do livro em um endereço de internet válido.

Fase 2 (A Busca): Fazer o "robô" entrar no site e identificar qual é o livro exato entre vários resultados.

Fase 3 (A Coleta): O trabalho pesado de ler as notas e copiar os comentários de forma automática.

Fase 4 (O Acabamento): Deixar o programa "inteligente" para que, se você digitar um nome errado, ele te avise educadamente em vez de simplesmente parar de funcionar.

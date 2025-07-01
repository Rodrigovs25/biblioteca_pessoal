## Membros do grupo

- Lucas Araujo Magesty
- Rodrigo Viana Souza

## Descrição do sistema

O sistema de gerenciamento de biblioteca pessoal foi desenvolvido com o objetivo de organizar a leitura de livros de forma simples, funcional e acessível via linha de comando. 

Com ele, o usuário pode registrar obras literárias, técnicas ou acadêmicas, mantendo informações como título, autor, ano de publicação e ISBN. Além disso, o usuário pode avaliar os livros lidos com notas de 1 a 5.

O sistema permite gerenciar uma biblioteca pessoal com as seguintes funcionalidades:
- Adicionar livros(Título, autor, ano, ISBN)
- Remover livros por meio do ISBN
- Marcar livros como lido/não lido
- Pesquisar livros por título, autor, ano e ISBN
- Listar todos os livros, os livros lidos, não lidos e por avaliação
- Avaliar os livros lidos com notas de 1 a 5
- Gera um relatório sobre os livros
- Guardar dados em arquivo JSON

## Teste
- main.py: para testar algumas funcionalidades, tem um menu e acessar um arquivo json para fazer as operações
- data/exemplo.json: arquivo com alguns livros

## Tecnologias utilizadas

- Python 3.11
- Pytest para testes automatizados
- GitHub Actions para CI/CD (testes automáticos em Linux, Windows e MacOS)
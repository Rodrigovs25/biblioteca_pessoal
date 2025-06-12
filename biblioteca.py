import json
import os

class Livro:
    def __init__(self, titulo, autor, ano, isbn, lido=False, avaliacao=None):
        if not titulo or not autor or not isbn:
            raise ValueError("Título, autor e ISBN são obrigatórios.")
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.lido = lido
        self.avaliacao = avaliacao

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "isbn": self.isbn,
            "lido": self.lido,
            "avaliacao": self.avaliacao
        }

class Biblioteca:
    def __init__(self, arquivo_dados="data/livros.json"):
        self.arquivo_dados = arquivo_dados
        self.livros = []
        self._carregar()

    def adicionar_livro(self, livro):
        if any(l.isbn == livro.isbn for l in self.livros):
            raise ValueError("Livro com este ISBN já existe.")
        self.livros.append(livro)
        self._salvar()

    def remover_livro(self, isbn):
        livro = self.buscar_por_isbn(isbn)
        if livro:
            self.livros.remove(livro)
            self._salvar()
        else:
            raise ValueError("Livro não encontrado.")

    def marcar_como_lido(self, isbn):
        livro = self.buscar_por_isbn(isbn)
        if livro:
            livro.lido = True
            self._salvar()
        else:
            raise ValueError("Livro não encontrado.")

    def marcar_como_nao_lido(self, isbn):
        livro = self.buscar_por_isbn(isbn)
        if livro:
            livro.lido = False
            self._salvar()
        else:
            raise ValueError("Livro não encontrado.")
    
    def avaliar_livro(self, isbn, nota):
        livro = self.buscar_por_isbn(isbn)
        if not livro:
            raise ValueError("Livro não encontrado.")
        if not livro.lido:
            raise ValueError("Só é possível avaliar livros que já foram lidos.")
        if not isinstance(nota, int) or nota < 1 or nota > 5:
            raise ValueError("A avaliação deve ser um número inteiro entre 1 e 5.")
        livro.avaliacao = nota
        self._salvar()

    def listar_livros(self):
        return self.livros

    def listar_livros_lidos(self):
        return [l for l in self.livros if l.lido]

    def listar_livros_nao_lidos(self):
        return [l for l in self.livros if not l.lido]

    def buscar_por_titulo(self, titulo):
        return [l for l in self.livros if titulo.lower() in l.titulo.lower()]

    def buscar_por_autor(self, autor):
        return [l for l in self.livros if autor.lower() in l.autor.lower()]
    
    def buscar_por_ano(self, ano):
        return [l for l in self.livros if l.ano == ano]

    def buscar_por_isbn(self, isbn):
        for l in self.livros:
            if l.isbn == isbn:
                return l
        return None

    def _salvar(self):
        os.makedirs(os.path.dirname(self.arquivo_dados), exist_ok=True)
        with open(self.arquivo_dados, "w", encoding="utf-8") as f:
            json.dump([l.to_dict() for l in self.livros], f, indent=4)

    def _carregar(self):
        if os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, "r", encoding="utf-8") as f:
                livros_json = json.load(f)
                self.livros = [
                    Livro(
                        titulo=l["titulo"],
                        autor=l["autor"],
                        ano=l["ano"],
                        isbn=l["isbn"],
                        lido=l["lido"],
                        avaliacao=l.get("avaliacao")
                    )
                    for l in livros_json
                ]

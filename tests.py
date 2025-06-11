import pytest
import os
import shutil
from biblioteca import Biblioteca, Livro

@pytest.fixture
def biblioteca_temp():
    # Usa um arquivo de teste temporário
    temp_arquivo = "tests/temp_livros.json"
    if os.path.exists(temp_arquivo):
        os.remove(temp_arquivo)
    biblio = Biblioteca(arquivo_dados=temp_arquivo)
    yield biblio
    if os.path.exists(temp_arquivo):
        os.remove(temp_arquivo)

def test_adicionar_livro(biblioteca_temp):
    livro = Livro("Titulo A", "Autor A", 2020, "12345")
    biblioteca_temp.adicionar_livro(livro)
    assert len(biblioteca_temp.listar_livros()) == 1

def test_adicionar_livro_invalido():
    with pytest.raises(ValueError):
        Livro("", "Autor B", 2021, "54321")

def test_remover_livro(biblioteca_temp):
    livro = Livro("Titulo B", "Autor B", 2021, "54321")
    biblioteca_temp.adicionar_livro(livro)
    biblioteca_temp.remover_livro("54321")
    assert len(biblioteca_temp.listar_livros()) == 0

def test_remover_livro_inexistente(biblioteca_temp):
    with pytest.raises(ValueError):
        biblioteca_temp.remover_livro("99999")

def test_marcar_como_lido(biblioteca_temp):
    livro = Livro("Titulo C", "Autor C", 2022, "22222")
    biblioteca_temp.adicionar_livro(livro)
    biblioteca_temp.marcar_como_lido("22222")
    assert biblioteca_temp.buscar_por_isbn("22222").lido is True

def test_marcar_como_nao_lido(biblioteca_temp):
    livro = Livro("Titulo D", "Autor D", 2023, "33333", lido=True)
    biblioteca_temp.adicionar_livro(livro)
    biblioteca_temp.marcar_como_nao_lido("33333")
    assert biblioteca_temp.buscar_por_isbn("33333").lido is False

def test_buscar_por_titulo(biblioteca_temp):
    livro = Livro("Python Avançado", "Autor E", 2020, "44444")
    biblioteca_temp.adicionar_livro(livro)
    resultado = biblioteca_temp.buscar_por_titulo("python")
    assert len(resultado) == 1

def test_buscar_por_autor(biblioteca_temp):
    livro = Livro("Livro X", "Autor Famoso", 2020, "55555")
    biblioteca_temp.adicionar_livro(livro)
    resultado = biblioteca_temp.buscar_por_autor("famoso")
    assert len(resultado) == 1

def test_buscar_por_isbn(biblioteca_temp):
    livro = Livro("Livro Y", "Autor Y", 2020, "66666")
    biblioteca_temp.adicionar_livro(livro)
    resultado = biblioteca_temp.buscar_por_isbn("66666")
    assert resultado is not None

def test_listar_livros(biblioteca_temp):
    livro1 = Livro("Livro 1", "Autor 1", 2019, "77777")
    livro2 = Livro("Livro 2", "Autor 2", 2018, "88888")
    biblioteca_temp.adicionar_livro(livro1)
    biblioteca_temp.adicionar_livro(livro2)
    assert len(biblioteca_temp.listar_livros()) == 2

def test_persistencia(biblioteca_temp):
    livro = Livro("Persistencia", "Autor Persistente", 2024, "99999")
    biblioteca_temp.adicionar_livro(livro)
    nova_biblioteca = Biblioteca(arquivo_dados="tests/temp_livros.json")
    assert len(nova_biblioteca.listar_livros()) == 1

def test_nao_adicionar_isbn_duplicado(biblioteca_temp):
    livro1 = Livro("Livro Original", "Autor Orig", 2020, "101010")
    livro2 = Livro("Livro Duplicado", "Autor Dup", 2021, "101010")
    biblioteca_temp.adicionar_livro(livro1)
    with pytest.raises(ValueError):
        biblioteca_temp.adicionar_livro(livro2)

def test_listar_livros_lidos(biblioteca_temp):
    livro1 = Livro("Lido 1", "Autor", 2020, "202020", lido=True)
    livro2 = Livro("Nao Lido", "Autor", 2021, "303030", lido=False)
    biblioteca_temp.adicionar_livro(livro1)
    biblioteca_temp.adicionar_livro(livro2)
    assert len(biblioteca_temp.listar_livros_lidos()) == 1

def test_listar_livros_nao_lidos(biblioteca_temp):
    livro1 = Livro("Lido 1", "Autor", 2020, "404040", lido=True)
    livro2 = Livro("Nao Lido", "Autor", 2021, "505050", lido=False)
    biblioteca_temp.adicionar_livro(livro1)
    biblioteca_temp.adicionar_livro(livro2)
    assert len(biblioteca_temp.listar_livros_nao_lidos()) == 1

def test_buscar_por_isbn_inexistente(biblioteca_temp):
    resultado = biblioteca_temp.buscar_por_isbn("000000")
    assert resultado is None

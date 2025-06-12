import pytest
import os
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

def test_buscar_por_ano(biblioteca_temp):
    livro1 = Livro("Livro Antigo", "Autor A", 2000, "A1")
    livro2 = Livro("Livro Recente", "Autor B", 2020, "B2")
    livro3 = Livro("Outro Recente", "Autor C", 2020, "C3")

    biblioteca_temp.adicionar_livro(livro1)
    biblioteca_temp.adicionar_livro(livro2)
    biblioteca_temp.adicionar_livro(livro3)

    resultado_2020 = biblioteca_temp.buscar_por_ano(2020)
    resultado_2000 = biblioteca_temp.buscar_por_ano(2000)
    resultado_1990 = biblioteca_temp.buscar_por_ano(1990)

    assert len(resultado_2020) == 2
    assert len(resultado_2000) == 1
    assert len(resultado_1990) == 0

def test_avaliar_livro_lido(biblioteca_temp):
    livro = Livro("Avaliável", "Autor", 2024, "77777", lido=True)
    biblioteca_temp.adicionar_livro(livro)
    biblioteca_temp.avaliar_livro("77777", 4)
    assert biblioteca_temp.buscar_por_isbn("77777").avaliacao == 4

def test_avaliacao_fora_do_intervalo(biblioteca_temp):
    livro = Livro("Com Nota Inválida", "Autor", 2024, "99999", lido=True)
    biblioteca_temp.adicionar_livro(livro)
    with pytest.raises(ValueError):
        biblioteca_temp.avaliar_livro("99999", 0)  # abaixo do mínimo
    with pytest.raises(ValueError):
        biblioteca_temp.avaliar_livro("99999", 6)  # acima do máximo

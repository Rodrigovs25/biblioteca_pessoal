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

def test_remover_um_entre_varios(biblioteca_temp):
    livro1 = Livro("Livro 1", "Autor", 2020, "L1")
    livro2 = Livro("Livro 2", "Autor", 2021, "L2")
    livro3 = Livro("Livro 3", "Autor", 2022, "L3")
    
    biblioteca_temp.adicionar_livro(livro1)
    biblioteca_temp.adicionar_livro(livro2)
    biblioteca_temp.adicionar_livro(livro3)
    
    biblioteca_temp.remover_livro("L2")
    
    isbns = [l.isbn for l in biblioteca_temp.listar_livros()]
    assert "L2" not in isbns
    assert "L1" in isbns and "L3" in isbns

def test_atualizar_avaliacao_livro(biblioteca_temp):
    livro = Livro("Livro para Avaliar", "Autor", 2024, "AV1", lido=True, avaliacao=3)
    biblioteca_temp.adicionar_livro(livro)
    
    biblioteca_temp.avaliar_livro("AV1", 5)  # Atualiza nota
    
    livro_atualizado = biblioteca_temp.buscar_por_isbn("AV1")
    assert livro_atualizado.avaliacao == 5

def test_listar_por_avaliacao_limiar(biblioteca_temp):
    livro1 = Livro("Ruim", "Autor", 2020, "R1", lido=True, avaliacao=2)
    livro2 = Livro("Bom", "Autor", 2021, "B1", lido=True, avaliacao=4)
    livro3 = Livro("Excelente", "Autor", 2022, "E1", lido=True, avaliacao=5)
    
    biblioteca_temp.adicionar_livro(livro1)
    biblioteca_temp.adicionar_livro(livro2)
    biblioteca_temp.adicionar_livro(livro3)
    
    resultado = biblioteca_temp.listar_livros_por_avaliacao(4)
    titulos = [l.titulo for l in resultado]
    
    assert "Bom" in titulos
    assert "Excelente" in titulos
    assert "Ruim" not in titulos

def test_avaliar_apos_marcar_como_nao_lido(biblioteca_temp):
    livro = Livro("Livro Fluxo Reverso", "Autor", 2025, "REV1", lido=True)
    biblioteca_temp.adicionar_livro(livro)
    
    # Avalia normalmente
    biblioteca_temp.avaliar_livro("REV1", 4)
    assert biblioteca_temp.buscar_por_isbn("REV1").avaliacao == 4
    
    # Marca como não lido
    biblioteca_temp.marcar_como_nao_lido("REV1")
    assert biblioteca_temp.buscar_por_isbn("REV1").lido is False

    # Tenta reavaliar
    with pytest.raises(ValueError):
        biblioteca_temp.avaliar_livro("REV1", 5)


def test_fluxo_completo_sistema(biblioteca_temp):
    livro = Livro("Fluxo E2E", "Autor", 2025, "E2E")
    biblioteca_temp.adicionar_livro(livro)
    
    biblioteca_temp.marcar_como_lido("E2E")
    biblioteca_temp.avaliar_livro("E2E", 5)
    
    resultado = biblioteca_temp.listar_livros_por_avaliacao(5)
    assert len(resultado) == 1
    assert resultado[0].titulo == "Fluxo E2E"
    
    resumo = biblioteca_temp.relatorio_resumo()
    assert resumo["total_livros"] == 1
    assert resumo["total_lidos"] == 1
    assert resumo["media_avaliacao_lidos"] == 5

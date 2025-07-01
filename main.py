from biblioteca import Livro, Biblioteca

def menu():
    b = Biblioteca("data/exemplo.json")

    while True:
        print("\n=== Menu da Biblioteca (Exemplo) ===")
        print("1. Listar todos os livros")
        print("2. Buscar por título")
        print("3. Listar livros por avaliação mínima")
        print("4. Ver relatório resumo")
        print("5. Avaliar livro")
        print("6. Remover livro")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            livros = b.listar_livros()
            if livros:
                for l in livros:
                    print(f"{l.titulo} - {l.autor} ({l.ano}) - ISBN: {l.isbn} - Lido: {l.lido} - Avaliação: {l.avaliacao}")
            else:
                print("Nenhum livro cadastrado.")

        elif opcao == "2":
            titulo = input("Título para buscar: ")
            resultado = b.buscar_por_titulo(titulo)
            if resultado:
                for l in resultado:
                    print(f"{l.titulo} - {l.autor} ({l.ano}) - ISBN: {l.isbn} - Avaliação: {l.avaliacao}")
            else:
                print("Nenhum livro encontrado.")

        elif opcao == "3":
            nota_min = int(input("Nota mínima (1 a 5): "))
            resultado = b.listar_livros_por_avaliacao(nota_min)
            if resultado:
                for l in resultado:
                    print(f"{l.titulo} - Avaliação: {l.avaliacao}")
            else:
                print("Nenhum livro encontrado com essa avaliação mínima.")

        elif opcao == "4":
            resumo = b.relatorio_resumo()
            print("\n=== Relatório Resumo ===")
            print(f"Total de livros: {resumo['total_livros']}")
            print(f"Total lidos: {resumo['total_lidos']}")
            print(f"Total não lidos: {resumo['total_nao_lidos']}")
            print(f"Média de avaliação dos lidos: {resumo['media_avaliacao_lidos']}")

        elif opcao == "5":
            isbn = input("ISBN do livro: ")
            nota = int(input("Nota (1 a 5): "))
            try:
                b.avaliar_livro(isbn, nota)
                print("Avaliação registrada.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "6":
            isbn = input("ISBN do livro a remover: ")
            try:
                b.remover_livro(isbn)
                print("Livro removido.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "7":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()

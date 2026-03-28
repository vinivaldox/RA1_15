# Nome | apelido no Github | link do Github
# Andrei de Carvalho Bley | TODO: inserir usuario/apelido do github aqui
# Vinicius Cordeiro Vogt | vinivaldox | https://github.com/vinivaldox
# Vitor Matias Percegona Bilbao | TODO: inserir usuario/apelido do github aqui

# Grupo: RA1 15
# Aluno 4: Interface do Usuário e Integração Final

import sys
from analisador_lexico import parseExpressao, ler_arquivo


def exibirResultados(resultados: list) -> None:
    """Exibe os resultados das expressões.

    Parameters
    ----------
    resultados : list
        Lista de resultados (float)
    """
    print("\n" + "=" * 70)
    print("RESULTADOS DAS EXPRESSOES")
    print("=" * 70)

    for i, resultado in enumerate(resultados, 1):
        if resultado is not None:
            print(f"Linha {i}: {resultado:.1f}")
        else:
            print(f"Linha {i}: ERRO")

    print("=" * 70 + "\n")


def salvarAssembly(assembly: str, nome_arquivo: str = "saida.s") -> None:
    """Salva código Assembly em arquivo.

    Parameters
    ----------
    assembly : str
        Código Assembly a salvar
    nome_arquivo : str
        Nome do arquivo de saída
    """
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(assembly)
        print(f"Assembly salvo em: {nome_arquivo}")
    except IOError as e:
        print(f"Erro ao salvar Assembly: {e}")


def main():
    """Função principal - Integra todos os alunos.

    Fluxo:
    1. Lê arquivo (Aluno 3)
    2. Para cada linha:
       a. Tokeniza (Aluno 1)
       b. Executa (Aluno 2)
       c. Gera Assembly (Aluno 3)
    3. Exibe e salva resultados
    """

    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_teste.txt>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]

    print(f"\n{'=' * 70}")
    print("COMPILADOR RPN → ASSEMBLY ARMv7")
    print(f"{'=' * 70}")
    print(f"Arquivo: {nome_arquivo}\n")

    try:
        # Lê arquivo
        linhas = ler_arquivo(nome_arquivo)
        print(f"{len(linhas)} linhas lidas\n")

        resultados = []
        assembly_completo = ""

        # Processa cada linha
        for i, linha in enumerate(linhas, 1):
            print(f"Linha {i}: {linha}")

            try:
                # Aluno 1: Tokenização
                tokens = parseExpressao(linha)
                print(f"Tokenização OK ({len(tokens)} tokens)")

                # Aluno 2: Execução (assumindo que existe a função)
                # resultado = executarExpressao(tokens)
                # print(f"  ✓ Resultado: {resultado}")
                # resultados.append(resultado)

                # Aluno 3: Geração Assembly (assumindo que existe a função)
                # assembly = gerarAssembly(tokens)
                # assembly_completo += assembly + "\n"
                # print(f"  ✓ Assembly gerado\n")

            except Exception as e:
                print(f"Erro: {e}\n")
                resultados.append(None)

        # Exibe resultados
        if resultados:
            exibirResultados(resultados)

        # Salva Assembly
        if assembly_completo:
            salvarAssembly(assembly_completo)

        print("Compilação concluída!\n")

    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

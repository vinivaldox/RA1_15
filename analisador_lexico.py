# Nome | apelido no Github | link do Github
# Andrei de Carvalho Bley | TODO: inserir usuario/apelido do github aqui
# Vinicius Cordeiro Vogt | vinivaldox | https://github.com/vinivaldox
# Vitor Matias Percegona Bilbao | TODO: inserir usuario/apelido do github aqui

# Grupo: RA1 15


def ler_arquivo(nome_arquivo: str) -> list:
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
    return linhas


if __name__ == "__main__":
    nome_arquivo = "teste_1.txt"
    linhas = ler_arquivo(nome_arquivo)
    for linha in linhas:
        print(linha)

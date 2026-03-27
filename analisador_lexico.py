# Nome | apelido no Github | link do Github
# Andrei de Carvalho Bley | TODO: inserir usuario/apelido do github aqui
# Vinicius Cordeiro Vogt | vinivaldox | https://github.com/vinivaldox
# Vitor Matias Percegona Bilbao | TODO: inserir usuario/apelido do github aqui

# Grupo: RA1 15
from dataclasses import dataclass


@dataclass
class Token:
    """Classe que representa os atributos de um token"""

    tipo: str  # "NUMERO", "OPERADOR", "PARENTESE", "COMANDO"
    valor: str  # O valor real do token. Exemplo, "3", "+", "(", "MEM"


def ler_arquivo(nome_arquivo: str) -> list:
    """Abre arquivo.txt e retorna uma lista com as linhas contidas dentro do arquivo aberto.

    Parameters
    ----------
    nome_arquivo : str
        Nome do arquivo a ser aberto, deve conter a extensão .txt

    Returns
    -------
    list
        Lista com as linhas contidas dentro do arquivo aberto
    """

    if not nome_arquivo.endswith(".txt"):
        raise ValueError("O nome do arquivo deve conter a extensão .txt")

    with open(nome_arquivo, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
    return linhas


if __name__ == "__main__":
    nome_arquivo = "teste_1.txt"
    linhas = ler_arquivo(nome_arquivo)
    for linha in linhas:
        print(linha)

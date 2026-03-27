'''
Vou explicar como essa função da funfando, pega  braba:
Temos um try catch para tratar o erro de nome de arquivo (como o prof quer)

'''


def lerArquivo(nomeArquivo):
    try:
        with open(nomeArquivo, 'r') as arquivo:
            #le sem aquebra de linha
            linhas = [linha.strip() for linha in arquivo.readlines()]
            print(f"Arquivo '{nomeArquivo}' lido com sucesso!")
            return linhas
    except FileNotFoundError:
        print(f"Erro: Não foi possível abrir o arquivo '{nomeArquivo}'. Verifique o caminho.")
        return []
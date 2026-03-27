def lerArquivo(nomeArquivo):
    try:
        with open(nomeArquivo, 'teste_1.txt') as arquivo:
            #le sem aquebra de linha
            linhas = [linha.strip() for linha in arquivo.readlines()]
            print(f"Arquivo '{nomeArquivo}' lido com sucesso!")
            return linhas
    except FileNotFoundError:
        print(f"Erro: Não foi possível abrir o arquivo '{nomeArquivo}'. Verifique o caminho.")
        return []
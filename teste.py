#testando com token manual, sempre que ver ")" na expressao
tokens = ["(", "3.14", "2.0", "+", ")"]
tokens2 = ["(", "11.8", "2,0", "%", ")"]

#pega os token e adiciona numa pilha até encontrar ")", que significa que a operação acabou, então desempilha em uma lista até achar o "("
#que significa que chegou no início da expressão
def executarExpressao(tokens):
    pilha = []

    for i in tokens:
        if i != ")":
            pilha.append(i)
        else:
            elementos = []

            while pilha and pilha[-1] != "(":
                elementos.append(pilha.pop())

            pilha.pop()  #remove "("
            elementos.reverse() #corrige ordem

            print("Expressão encontrada:", elementos)

    return pilha
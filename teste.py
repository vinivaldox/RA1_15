#testando com token manual, sempre que ver ")" na expressao
tokens = ["(", "3.14", "2.0", "+", ")"]
tokens2 = ["(", "11.8", "2,0", "%", ")"]
tokens3 =["(", "(", "1", "2", "+", ")", "3", "/", ")"]

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

            if len(elementos) == 3:
                op1 = elementos[0]
                op2 = elementos[1]
                op = elementos[2]

                subexpressao = {        #dicionario da operação
                    "op1": op1,     #operante1
                    "op2": op2,     #operante2
                    "op": op        #operador
                }

                pilha.append(subexpressao)
                
            else:
                print("ERRO: subexpressão inválida: ", elementos)

    return pilha

print(executarExpressao(tokens3))

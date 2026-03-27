#testando com token manual, sempre que ver ")" na expressao
tokens = ["(", "3.14", "2.0", "+", ")"]
tokens2 = ["(", "11.8", "2,0", "%", ")"]
tokens3 =["(", "(", "1", "2", "+", ")", "3", "/", ")"]

tokenfalho = ["1", "2", "+", ")"] #teste faltando parentesis
tokenfalho2 = ["(", "1", "+", ")"]#teste faltando operando (2 elementos)
tokenfalho3 = ["(", "1", "2", "3", "+", ")"]#teste com elementos demais
tokenfalho4 = ["(", "1", "2", "&", ")"] #teste operador invalido
tokenfalho5 = ["(", "+", "1", "2", ")"] 

tokensMEM = ["(", "MEM", "2", "+", ")"]
tokensRES = ["(", "5", "RES", "*", ")"]

tokensdefMEM = ["(", "2", "MEM", ")"]



#pega os token e adiciona numa pilha até encontrar ")", que significa que a operação acabou, então desempilha em uma lista até achar o "("
#que significa que chegou no início da expressão
def executarExpressao(tokens, memoria, resultados):
    pilha = []
    operadores = ["+", "-", "*", "/", "//", "%", "^"]

    for i in tokens:
        if i != ")":
            pilha.append(i)
        else:
            elementos = []

            while pilha and pilha[-1] != "(":
                elementos.append(pilha.pop())

            if not pilha:                                   #validação de lista vazia provavelmente erro no ()
                print("ERRO...parêntesis")
                return None

            pilha.pop()  #remove 1 "("
            elementos.reverse() #corrige ordem

            # caso (N RES)
            if len(elementos) == 2 and elementos[1] == "RES":
                subexpressao = {
                    "tipo": "res_get",
                    "indice": elementos[0]
                }
                pilha.append(subexpressao)
                continue

            # caso (V MEM)
            if len(elementos) == 2 and elementos[1] == "MEM":
                subexpressao = {
                    "tipo": "mem_set",
                    "valor": elementos[0],
                    "memoria": "MEM"
                }
                pilha.append(subexpressao)
                continue 
        


            if len(elementos) != 3:                         #validação se segue o formato de -> operando1, operando2, operador
                print("ERRO: subexpressão inválida: ", elementos)
                return None

            #define os operandos e o operador
            op1 = elementos[0]
            op2 = elementos[1]
            op = elementos[2]
                
            if op not in operadores:
                print("ERRO: operador inválido: ", op)
                return None

            subexpressao = {        #dicionario da operação
                "tipo": "operacao",
                "op1": op1,     #operando1
                "op2": op2,     #operando2
                "op": op        #operador
            }

            pilha.append(subexpressao) #monta a subexpressão
                
    if len(pilha) != 1:
        print("ERRO... má formataçao")
        return None

    return pilha[0]


print(executarExpressao(tokens, {}, []))
print(executarExpressao(tokens2, {}, []))
print(executarExpressao(tokensRES, {}, []))
print(executarExpressao(tokensMEM, {}, []))
print(executarExpressao(tokensdefMEM, {}, []))
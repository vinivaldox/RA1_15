def is_variavel(token):
    """
    Verifica se o token recebido é uma variavel de memória (apenas letras maiusculas), porem a variável de memória não pode ser RES
    Retorna Falso caso não seja verdade
    """
    if token == "RES":
        return False
    else:
        return token.isalpha() and token.isupper()


def is_numero(token):
    """
    Aqui será verificado se o token é um número tentando converter para float, tanto para padronizar quanto para verificar
    ou seja, se tentar transformar uma letra em float, acusará erro e retornará falso
    """
    try:
        float(token)
        return True
    except ValueError:
        return False
    

operadores = {"+", "-", "*", "/", "//", "%", "^"}

def executarExpressao(tokens, memoria, historico):
    """
    Monta uma árvore de operações a partir dos tokens do Aluno 1
    
    """
    pilha = []

    for token in tokens:
        tipo  = token["tipo"]
        valor = token["valor"]

        # Parêntese de abertura — empilha como marcador do início
        if tipo == "PARENTESIS" and valor == "(":
            pilha.append("(")

        # Número — empilha como float
        elif tipo == "NUMERO":
            pilha.append(float(valor))

        # Operador 
        elif tipo == "OPERADOR":
            pilha.append(valor)

        # Variável de memória — empilha o nome
        elif tipo == "VARIAVEL":
            pilha.append(valor)

        # RES 
        elif tipo == "ESPECIAL" and valor == "RES":
            pilha.append("RES")

        # parêntese de fechamento 
        elif tipo == "PARENTESIS" and valor == ")":
            elementos = []

            # Desempilha tudo até encontrar o "("
            while pilha and pilha[-1] != "(":
                elementos.append(pilha.pop())

            if not pilha:
                print("ERRO: parênteses desbalanceados")
                return None

            pilha.pop()       # remove o "("
            elementos.reverse()  # corrige a ordem

            # get_mem é para ler algo na memória
            if len(elementos) == 1 and is_variavel(str(elementos[0])):
                no = {
                    "tipo": "mem_get",
                    "variavel": elementos[0]
                }

            # buscar algo no histórico
            elif len(elementos) == 2 and elementos[1] == "RES":
                no = {
                    "tipo": "res_get",
                    "indice": elementos[0]
                }

            # mem_set é quando define um valor na memoria
            elif len(elementos) == 2 and is_variavel(str(elementos[1])):
                no = {
                    "tipo": "mem_set",  
                    "valor": elementos[0],
                    "variavel": elementos[1]
                }

            # caso normal a b +
            elif len(elementos) == 3 and elementos[2] in operadores:
                no = {
                    "tipo": "operacao",
                    "op1": elementos[0],
                    "op2": elementos[1],
                    "op": elementos[2]
                }

            else:
                print("ERRO: subexpressão inválida:", elementos)
                return None

            pilha.append(no)  # empilha o nó montado

    if len(pilha) != 1:
        print("ERRO: expressão mal formada")
        return None

    return pilha[0]

tokens1 = [
    {"tipo": "PARENTESIS", "valor": "("},
    {"tipo": "NUMERO",     "valor": "3.0"},
    {"tipo": "NUMERO",     "valor": "2.0"},
    {"tipo": "OPERADOR",   "valor": "+"},
    {"tipo": "PARENTESIS", "valor": ")"}
]


tokens2 = [
    {"tipo": "PARENTESIS", "valor": "("},
    {"tipo": "PARENTESIS", "valor": "("},
    {"tipo": "NUMERO",     "valor": "1"},
    {"tipo": "NUMERO",     "valor": "2"},
    {"tipo": "OPERADOR",   "valor": "+"},
    {"tipo": "PARENTESIS", "valor": ")"},
    {"tipo": "NUMERO",     "valor": "3"},
    {"tipo": "OPERADOR",   "valor": "/"},
    {"tipo": "PARENTESIS", "valor": ")"}
]


tokens3 = [
    {"tipo": "PARENTESIS", "valor": "("},
    {"tipo": "NUMERO",     "valor": "10.5"},
    {"tipo": "VARIAVEL",   "valor": "CONTA"},
    {"tipo": "PARENTESIS", "valor": ")"}
]


tokens4 = [
    {"tipo": "PARENTESIS", "valor": "("},
    {"tipo": "VARIAVEL",   "valor": "CONTA"},
    {"tipo": "PARENTESIS", "valor": ")"}
]


tokens5 = [
    {"tipo": "PARENTESIS", "valor": "("},
    {"tipo": "NUMERO",     "valor": "2"},
    {"tipo": "ESPECIAL",   "valor": "RES"},
]

print(executarExpressao(tokens1, {}, []))
print(executarExpressao(tokens2, {}, []))
print(executarExpressao(tokens3, {}, []))
print(executarExpressao(tokens4, {}, []))
print(executarExpressao(tokens5, {}, []))
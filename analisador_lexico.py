# Nome | apelido no Github | link do Github
# Andrei de Carvalho Bley | TODO: inserir usuario/apelido do github aqui
# Vinicius Cordeiro Vogt | vinivaldox | https://github.com/vinivaldox
# Vitor Matias Percegona Bilbao | TODO: inserir usuario/apelido do github aqui

# Grupo: RA1 15
from dataclasses import dataclass


@dataclass
class Token:
    """Classe que representa os atributos de um token"""

    tipo: str  # "NUMERO", "OPERADOR", "PARENTESE", "COMANDO", "VARIAVEL"
    valor: str  # O valor real do token. Exemplo, "3", "+", "(", "MEM"

    def to_dict(self) -> dict:
        """Converte o Token para um dicionário.

        Returns
        -------
        dict
            Dicionário com as chaves 'tipo' e 'valor'
        """
        return {"tipo": self.tipo, "valor": self.valor}


def estado_inicial(caractere: str, contexto: dict) -> str:
    # TODO: Adicionar docstr para estado_inicial

    # paretneses, tem retorno imediato
    if caractere == "(":
        contexto["tokens"].append(Token("PARENTESE", "("))
        return "inicial"
    elif caractere == ")":
        contexto["tokens"].append(Token("PARENTESE", ")"))
        return "inicial"

    # ignora espaços e tabs
    elif caractere in " \t":
        return "inicial"

    # digitos de um numero
    elif caractere.isdigit():
        contexto["buffer"] = caractere
        return "numero"

    # letras para um comando ou variavel
    elif caractere.isalpha():
        contexto["buffer"] = caractere
        return "letra"

    # operadores simples, tem retorno imediato
    elif caractere == "+":
        contexto["tokens"].append(Token("OPERADOR", "+"))
        return "inicial"
    elif caractere == "*":
        contexto["tokens"].append(Token("OPERADOR", "*"))
        return "inicial"
    elif caractere == "%":
        contexto["tokens"].append(Token("OPERADOR", "%"))
        return "inicial"
    elif caractere == "^":
        contexto["tokens"].append(Token("OPERADOR", "^"))
        return "inicial"

    # TODO: Ver se tem numero negativo nessa atividade
    # verificar se o "-" é um operador de subtração ou um sinal de número negativo
    elif caractere == "-":
        contexto["buffer"] = "-"
        return "valida_menos"

    # operador complexo, podendo ser "/" ou "//", então precisa de um estado de validação
    elif caractere == "/":
        contexto["buffer"] = "/"
        return "valida_divisao"

    # entrada invalida
    else:
        msg = f"Caractere inválido: '{caractere}'"
        raise ValueError(msg)


def estado_numero(caractere: str, contexto: dict) -> str:
    # continua acumulando dígitos
    if caractere.isdigit():
        contexto["buffer"] += caractere
        return "numero"

    # encontrou ponto decimal - valida se já tem um ponto
    elif caractere == ".":
        if "." in contexto["buffer"]:
            msg = f"Número malformado: dois pontos - '{contexto['buffer']}'"
            raise ValueError(msg)
        contexto["buffer"] += caractere
        return "numero"

    # espaço - termina o número
    elif caractere in " \t":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = ""
        return "inicial"

    # parêntese - termina número e processa parêntese
    elif caractere in "()":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = ""
        return "inicial"

    # operador - termina número e processa operador
    elif caractere in "+*/%^":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = ""
        return "inicial"

    elif caractere == "-":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = ""
        return "valida_menos"

    # "/" - precisa validar se é "/" ou "//"
    elif caractere == "/":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = "/"
        return "valida_divisao"

    # inválido
    else:
        msg = f"Caractere inválido em número: '{contexto['buffer']}{caractere}'"
        raise ValueError(msg)


def estado_valida_menos(caractere: str, contexto: dict) -> str:
    # "-" DIRETO em dígito = número negativo
    if caractere.isdigit():
        contexto["buffer"] += caractere  # "-" + dígito
        return "numero"

    elif caractere in " \t":
        contexto["tokens"].append(Token("OPERADOR", "-"))
        contexto["buffer"] = ""
        return "inicial"  # Volta e ignora o espaço

    # "-" SEGUIDO de parêntese = é operador
    elif caractere in "()":
        contexto["tokens"].append(Token("OPERADOR", "-"))
        contexto["buffer"] = "-"
        return "inicial"

    # TODO: inserir validação de ponto aqui para numeros como -.8 ??
    else:
        msg = f"Caractere inválido após '-': '{caractere}'"
        raise ValueError(msg)


def estado_valida_divisao(caractere: str, contexto: dict) -> str:
    if caractere in "/":
        contexto["tokens"].append(Token("OPERADOR", "//"))
        contexto["buffer"] = ""
        return "inicial"

    else:
        contexto["tokens"].append(Token("OPERADOR", "/"))
        contexto["buffer"] = ""
        return estado_inicial(caractere, contexto)


def estado_letra(caractere: str, contexto: dict) -> str:
    if caractere.isalpha():
        contexto["buffer"] += caractere
        return "letra"

    elif caractere in " \t":
        _criar_token_comando_ou_variavel(contexto)
        return "inicial"

    elif caractere in "()+-*/%^":
        _criar_token_comando_ou_variavel(contexto)
        return estado_inicial(caractere, contexto)

    # "/" precisa validar se é "//"
    elif caractere == "/":
        _criar_token_comando_ou_variavel(contexto)
        contexto["buffer"] = "/"
        return "valida_divisao"

    # "-" precisa validar se é número negativo ou operador
    elif caractere == "-":
        _criar_token_comando_ou_variavel(contexto)
        contexto["buffer"] = ""
        return "valida_menos"

    else:
        msg = f"Caractere inválido em comando: '{contexto['buffer']}{caractere}'"
        raise ValueError(msg)


def _criar_token_comando_ou_variavel(contexto: dict):
    if not contexto["buffer"]:
        return

    comandos = {"MEM", "RES"}

    if contexto["buffer"].upper() in comandos:
        contexto["tokens"].append(Token("COMANDO", contexto["buffer"]))
    else:
        contexto["tokens"].append(Token("VARIAVEL", contexto["buffer"]))

    contexto["buffer"] = ""


def parseExpressao(linha: str) -> list:
    # Inicia contexto vazio
    contexto = {"buffer": "", "tokens": []}
    estado_atual = "inicial"

    # Mapeia nome do estado para sua função
    estados = {
        "inicial": estado_inicial,
        "numero": estado_numero,
        "letra": estado_letra,
        "valida_menos": estado_valida_menos,
        "valida_divisao": estado_valida_divisao,
    }

    # Processa cada caractere da linha
    for caractere in linha:
        # Pega a função do estado atual
        funcao_estado = estados[estado_atual]
        # Chama a função e recebe o próximo estado (como string)
        estado_atual = funcao_estado(caractere, contexto)

    # Ao final da linha, emite token pendente no buffer (se houver)
    if contexto["buffer"]:
        # Verifica se é número ou comando/variável
        if contexto["buffer"][0].isdigit() or (
            contexto["buffer"][0] == "-" and len(contexto["buffer"]) > 1
        ):
            contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        else:
            _criar_token_comando_ou_variavel(contexto)

    return contexto["tokens"]


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
        msg = f"O nome do arquivo '{nome_arquivo}' é inválido. O nome do arquivo deve conter a extensão .txt"
        raise ValueError(msg)

    with open(nome_arquivo, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
    return linhas


if __name__ == "__main__":
    nome_in = "teste_1.txt"
    nome_out = "token.txt"
    linhas = ler_arquivo(nome_in)

    with open(nome_out, "w", encoding="utf-8") as arquivo_saida:
        for i, linha in enumerate(linhas, 1):
            print(f"Linha {i}: {linha}")
            try:
                tokens = parseExpressao(linha)
                dict_out = [token.to_dict() for token in tokens]
                # Escreve dict_out como uma linha no arquivo
                arquivo_saida.write(str(dict_out) + "\n")
            except Exception as e:
                print(f"ERRO: {e}")
                # arquivo_saida.write(f"ERRO: {e}\n")

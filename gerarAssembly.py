def gerarAssembly(_tokens_):
    #Recebe uma lista de tokens e retorna o código Assembly (ARMv7 em 64-bits)
    
    #.data
    codigo_data = ".data\n"
    codigo_data += "    .align 3  @ Alinhamento obrigatorio para 64 bits\n"
    codigo_data += "    memoria_res: .space 800  @ Espaco para o historico (N RES)\n"
    #.text
    codigo_text = "\n.text\n.global main\nmain:\n"
    variaveis_criadas = []
    contador_literais = 0
    for token in _tokens_:
        if token in ("(", ")"):
            continue
        elif token in ("+", "-", "*", "/"):
            codigo_text += f"    @ Operacao: {token}\n"
            codigo_text += "    VPOP {d1}  @ Desempilha B (segundo numero)\n"
            codigo_text += "    VPOP {d2}  @ Desempilha A (primeiro numero)\n"
            if token == "+":
                codigo_text += "    VADD.F64 d0, d2, d1\n"
            elif token == "-":
                codigo_text += "    VSUB.F64 d0, d2, d1\n"
            elif token == "*":
                codigo_text += "    VMUL.F64 d0, d2, d1\n"
            elif token == "/":
                codigo_text += "    VDIV.F64 d0, d2, d1\n"     
            codigo_text += "    VPUSH {d0} @ Empilha o resultado\n"
        elif token in ("//", "%", "^"):
            codigo_text += f"    @ Operacao complexa: {token}\n"
            codigo_text += "    @ TODO: Adicionar subrotina para divisao inteira, resto ou potencia\n"
        elif token == "MEM":
            codigo_text += "    @ TODO: Logica para armazenar/ler memoria\n"
        elif token == "RES":
            codigo_text += "    @ TODO: Logica para ler do historico (memoria_res)\n"  
        else:
            if token[0].isalpha() and token not in ("MEM", "RES"):
                if token not in variaveis_criadas:
                    codigo_data += f"    var_{token}: .double 0.0\n"
                    variaveis_criadas.append(token)
                codigo_text += f"    @ Encontrou a variavel {token}\n"
            else:
                nome_literal = f"num_{contador_literais}"
                codigo_data += f"    {nome_literal}: .double {token}  @ Salva o numero na memoria\n"
                
                codigo_text += f"    @ Carrega operando: {token}\n"
                codigo_text += f"    LDR r0, ={nome_literal}  @ Pega o endereco do numero\n"
                codigo_text += "    VLDR.F64 d0, [r0]        @ Carrega o valor 64 bits para FPU\n"
                codigo_text += "    VPUSH {d0}               @ Empilha o numero\n"
                contador_literais += 1
    codigo_text += "    BX lr @ Fim do main\n"
    return codigo_data + codigo_text
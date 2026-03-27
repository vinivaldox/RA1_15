'''
 explicando:
função responsável por traduzir tokens RPN em formato de dicionário para ARMv7 (formato pedido pelo prof).
a geração é dividida em duas seções principais:
.data: trabalha com a alocalçao estática das constantes, com literais (64bits) e vars
.text: faz a logica das op matemáticas usando a FPU e os registradosres d
'''




def gerarAssembly(_tokens_):
    
    #.data 
    codigo_data = ".data\n"
    codigo_data += "    .align 3\n"
    codigo_data += "    memoria_res: .space 800\n"
    codigo_data += "    const_um: .double 1.0\n"
    
    #.text
    codigo_text = "\n.text\n.global main\nmain:\n"

    variaveis_criadas = []
    contador_literais = 0
    contador_loops = 0  

    for token_dict in _tokens_:
        tipo = token_dict.get("tipo")
        valor = token_dict.get("valor")

        if tipo == "PARENTESIS":
            continue
            
        #operacoes
        elif tipo == "OPERADOR" and valor in ("+", "-", "*", "/"):
            codigo_text += "    VPOP {d1}\n"
            codigo_text += "    VPOP {d2}\n"
            
            if valor == "+":
                codigo_text += "    VADD.F64 d0, d2, d1\n"
            elif valor == "-":
                codigo_text += "    VSUB.F64 d0, d2, d1\n"
            elif valor == "*":
                codigo_text += "    VMUL.F64 d0, d2, d1\n"
            elif valor == "/":
                codigo_text += "    VDIV.F64 d0, d2, d1\n"
                
            codigo_text += "    VPUSH {d0}\n"
            
        #divisao
        elif tipo == "OPERADOR" and valor in ("//", "%"):
            codigo_text += "    VPOP {d1}\n"
            codigo_text += "    VPOP {d2}\n"
            codigo_text += "    VCVT.S32.F64 s1, d1\n"
            codigo_text += "    VCVT.S32.F64 s2, d2\n"
            codigo_text += "    VMOV r1, s1\n"
            codigo_text += "    VMOV r0, s2\n"
            codigo_text += "    SDIV r2, r0, r1\n"
            
            if valor == "//":
                codigo_text += "    VMOV s0, r2\n"
            else: 
                codigo_text += "    MLS r3, r2, r1, r0\n"
                codigo_text += "    VMOV s0, r3\n"
                
            codigo_text += "    VCVT.F64.S32 d0, s0\n"
            codigo_text += "    VPUSH {d0}\n"

        #potencia
        elif tipo == "OPERADOR" and valor == "^":
            codigo_text += "    VPOP {d1}\n"
            codigo_text += "    VPOP {d2}\n"
            codigo_text += "    VCVT.S32.F64 s1, d1\n"
            codigo_text += "    VMOV r1, s1\n"
            codigo_text += "    LDR r0, =const_um\n"
            codigo_text += "    VLDR.F64 d0, [r0]\n"
            
            codigo_text += f"loop_pot_{contador_loops}:\n"
            codigo_text += "    CMP r1, #0\n"
            codigo_text += f"    BLE fim_pot_{contador_loops}\n"
            codigo_text += "    VMUL.F64 d0, d0, d2\n"
            codigo_text += "    SUB r1, r1, #1\n"
            codigo_text += f"    B loop_pot_{contador_loops}\n"
            codigo_text += f"fim_pot_{contador_loops}:\n"
            codigo_text += "    VPUSH {d0}\n"
            contador_loops += 1
            
        #RES
        elif tipo == "ESPECIAL" and valor == "RES":
            codigo_text += "    VPOP {d1}\n"
            codigo_text += "    VCVT.S32.F64 s1, d1\n"
            codigo_text += "    VMOV r1, s1\n"
            codigo_text += "    LSL r1, r1, #3\n"
            codigo_text += "    LDR r0, =memoria_res\n"
            codigo_text += "    ADD r0, r0, r1\n"
            codigo_text += "    VLDR.F64 d0, [r0]\n"
            codigo_text += "    VPUSH {d0}\n"
            
        #VAR
        elif tipo == "VARIAVEL":
            if valor not in variaveis_criadas:
                codigo_data += f"    var_{valor}: .double 0.0\n"
                variaveis_criadas.append(valor)
            codigo_text += f"    LDR r0, =var_{valor}\n"
            codigo_text += "    VLDR.F64 d0, [r0]\n"
            codigo_text += "    VPUSH {d0}\n"
                
        #NUM
        elif tipo == "NUMERO":
            nome_literal = f"num_{contador_literais}"
            codigo_data += f"    {nome_literal}: .double {valor}\n"
            codigo_text += f"    LDR r0, ={nome_literal}\n"
            codigo_text += "    VLDR.F64 d0, [r0]\n"
            codigo_text += "    VPUSH {d0}\n"
            contador_literais += 1

    codigo_text += "    BX lr\n"
    
    return codigo_data + codigo_text



#------------
#bloco de teste
#------------
if __name__ == "__main__":
    #(3.0 2.0 +)
    tokens1 = [
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "NUMERO",     "valor": "3.0"},
        {"tipo": "NUMERO",     "valor": "2.0"},
        {"tipo": "OPERADOR",   "valor": "+"},
        {"tipo": "PARENTESIS", "valor": ")"}
    ]
    
    #((1 2 +) 3 /)
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
    
    #alvar memória -> (10.5 CONTA)
    tokens3 = [
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "NUMERO",     "valor": "10.5"},
        {"tipo": "VARIAVEL",   "valor": "CONTA"},
        {"tipo": "PARENTESIS", "valor": ")"}
    ]
    
    #ler memória -> (CONTA)
    tokens4 = [
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "VARIAVEL",   "valor": "CONTA"},
        {"tipo": "PARENTESIS", "valor": ")"}
    ]
    
    #histórico -> (2 RES)
    tokens5 = [
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "NUMERO",     "valor": "2"},
        {"tipo": "ESPECIAL",   "valor": "RES"},
        {"tipo": "PARENTESIS", "valor": ")"}
    ]

    todos_os_tokens = tokens1 + tokens2 + tokens3 + tokens4 + tokens5

    print("Gerando Assembly para todos os casos...")
    resultado_assembly = gerarAssembly(todos_os_tokens)
    nome_do_arquivo = "teste_completo.s"
    with open(nome_do_arquivo, "w") as f:
        f.write(resultado_assembly)
        
    print(f"sucesso! '{nome_do_arquivo}'.")
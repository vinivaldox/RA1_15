# RA1_15 - Compilador RPN → ARMv7 Assembly

## Informações do Projeto

- **Matéria**: Linguagens Formais e Compiladores
- **Professor**: Frank
- **Faculdade**: PUCPR (Pontifícia Universidade Católica do Paraná)
- **Grupo**: RA1_15

## Descrição

Implementação de um compilador que processa expressões em notação RPN (Reverse Polish Notation) e gera código Assembly ARMv7 para a arquitetura Cpulator ARMv7 DEC1-SOC v16.1.

## Características

- **Aluno 1**: Analisador Léxico (DFA - Autômato Finito Determinístico)
- **Aluno 2**: Processador de Expressões RPN com gerenciamento de memória
- **Aluno 3**: Gerador de código Assembly ARMv7
- **Aluno 4**: Interface do usuário e integração de módulos

## Operações Suportadas

- Operadores aritméticos: `+`, `-`, `*`, `/`, `//` (div. inteira), `%` (módulo), `^` (potência)
- Comandos: `MEM` (salvar em memória), `RES` (recuperar resultado anterior)
- Números em ponto flutuante (IEEE 754 64-bit)

## Como Executar

```bash
python main.py <arquivo_teste.txt>
```

**Exemplo**:
```bash
python main.py teste_1.txt
```

## Arquivos de Saída

- `token.txt`: Lista de tokens gerados pelo analisador léxico
- `saida.s`: Código Assembly ARMv7 gerado

## Estrutura de Arquivos

- `analisador_lexico.py`: Implementação da análise léxica (Aluno 1)
- `geren_memo.py`: Processador RPN e gerenciador de memória (Aluno 2)
- `gerarAssembly.py`: Gerador de código Assembly (Aluno 3)
- `main.py`: Orquestrador e interface (Aluno 4)
- `teste_1.txt`, `teste_2.txt`, `teste_3.txt`: Arquivos de teste

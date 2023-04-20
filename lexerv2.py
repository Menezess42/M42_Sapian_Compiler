from sapians import Sapians
from my_parser import Parser
import numpy as np

'''code = [
    ["program prog1;"],
    ["int x;"],
    ["float y;"],
    ["char c;"],
    ["string s;"],
    [""],
    ["x := 2 + 3 * 4;"],
    ["y := 3.14;"],
    ["c := 'a';"],
    ['s := "hello, world!";'],
    [""],
    ["if (x >= 10) {"],
    ["y = y / 2;"],
    ["} else {"],
    ["y = y * 2;"],
    ["}"],
    [""],
    ["for (int i = 0; i < x; i = i + 1) {"],
    ["c = c + 1;"],
    ["}"],
    [""],
    ["while (y > 1.0) {"],
    ["y = y - 1.0;"],
    ["}"],
    [""],
    ["end;"],
]
code2 = [["c = 'a';"], ['s = "hello, world!";']]'''


# Função que realiza o parsing dos tokens
class Lexer:
    def __init__(self, code):
        self.code = code
        self.i = 0

    @staticmethod
    def verifier(c):
        if c.isspace():
            return False
        elif c == "(":
            return False
        elif c == ")":
            return False
        elif c == "{":
            return False
        elif c == "}":
            return False
        elif c == ";":
            return False
        return True

    def lexer(self):
        # Inicializa a lista de tokens
        tokens = []
        programa = np.array(self.code)
        tokens_list = np.array(self.code)
        tokens_list = tokens_list.tolist()
        error_lists = []
        y, x = programa.shape
        for i in range(len(tokens_list)):
            tokens_list[i][0] = ""
            error_lists.append([""])
        # Inicializa as variáveis auxiliares
        token = ""
        state = "start"
        sapian = Sapians()
        flag = True
        # Percorre todos os caracteres do programa
        for line in range(y):
            vector = []
            if programa[line, 0] == " " or programa[line, 0] == "":
                line += 1
            else:
                self.i = 0
                program = programa[line, 0]
                token = ""
                state = "start"
                i = 0
                flag_cs = True
                while i < len(program):
                    # Obtém o caractere atual
                    c = program[i]
                    # Executa a ação correspondente ao estado atual
                    if state == "start":
                        # Verifica se é uma letra ou um underline, indicando um possível identificador
                        if c.isalpha():
                            token += c
                            state = "identifier"
                            i += 1
                        # Verifica se é um dígito, indicando uma possível constante numérica
                        elif c.isdigit():
                            token += c
                            state = "number"
                            i += 1
                        # Verifica se é um espaço em branco, ignorando-o
                        elif c.isspace() or (program[i - 1] + c) in [
                            "<=",
                            ">=",
                            ":=",
                            "!=",
                            "&&",
                            "||",
                        ]:
                            i += 1
                            continue
                        # Verifica se é um operador ou símbolo
                        elif sapian.isInOperators(c):
                            # Se o próximo caractere também é um operador, forma um operador de dois caracteres
                            if i + 1 < len(program) and sapian.isInOperators(
                                c + program[i + 1]
                            ):
                                i += 1
                                c += program[i]
                                tokens.append((sapian.getTokenOperator(c), c))
                                tokens_list[line].append(
                                    (sapian.getTokenOperator(c), c)
                                    # f"{sapian.getTokenOperator(c)} {c}"
                                )
                                i += 1
                            else:
                                try:
                                    tokens.append((sapian.getTokenOperator(c), c))
                                    tokens_list[line].append(
                                        (sapian.getTokenOperator(c), c)
                                        # f"{sapian.getTokenOperator(c)} {c}"
                                    )
                                    i += 1
                                    if (
                                        sapian.getTokenOperator(c) == "QUOTE"
                                        and flag_cs == True
                                    ):
                                        state = "char"
                                        flag_cs = False
                                    elif (
                                        sapian.getTokenOperator(c) == "DOUBLE_QUOTE"
                                        and flag_cs == True
                                    ):
                                        state = "string"
                                        flag_cs = False
                                except KeyError:
                                    flag = False
                                    state = "error"
                                    token = c
                                    i += 1
                        else:
                            state = "error"
                            token = c
                            i += 1
                    elif state == "error":
                        if self.verifier(c):
                            token += c
                            i += 1
                        else:
                            flag = False
                            error_lists[line].append(
                                (f"ERROR: line {line+1}", f"invalid caracter {token}")
                            )
                            token = ""
                            state = "start"
                    elif state == "string":
                        if c != '"':
                            token += c
                            i += 1
                        else:
                            tokens.append(
                                (sapian.getTokenContant("const_string"), token)
                            )
                            tokens_list[line].append(
                                (sapian.getTokenContant("const_string"), token)
                                # f'{sapian.getTokenContant("const_string")} {token}'
                            )
                            token = ""
                            state = "start"
                    elif state == "char":
                        if c != "'":
                            token += c
                            i += 1
                        else:
                            tokens.append((sapian.getTokenContant("const_char"), token))
                            tokens_list[line].append(
                                (sapian.getTokenContant("const_char"), token)
                                # f'{sapian.getTokenContant("const_char")} {token}'
                            )
                            token = ""
                            state = "start"
                            # i -= 1
                    elif state == "identifier":
                        # Verifica se é um caractere alfanumérico ou um underline, continuando o identificador
                        if c.isalnum():
                            token += c
                            i += 1
                        # Se não, o identificador terminou
                        else:
                            # Verifica se é uma palavra-chave
                            if sapian.isInKeyWords(token):
                                tokens.append((sapian.getTokenKeyWord(token), token))
                                tokens_list[line].append(
                                    (sapian.getTokenKeyWord(token), token)
                                    # f"{sapian.getTokenKeyWord(token)} {token}"
                                )
                            else:
                                tokens.append(("IDENTIFIER", token))
                                tokens_list[line].append(  # f"IDENTIFIER {token}")
                                    ("IDENTIFIER", token)
                                )
                            token = ""
                            state = "start"
                    elif state == "number":
                        # Verifica se é um dígito, continuando a constante numérica
                        if c.isdigit():
                            token += c
                            i += 1
                        # Verifica se é um ponto, indicando uma constante numérica em ponto flutuante
                        elif c == ".":
                            token += c
                            state = "float_number"
                            i += 1
                        # Se não, a constante numérica terminou
                        else:
                            tokens.append((sapian.getTokenContant("const_int"), token))
                            tokens_list[line].append(
                                (sapian.getTokenContant("const_int"), token)
                                # f'{sapian.getTokenContant("const_int")} {token}'
                            )
                            token = ""
                            state = "start"
                            # Volta o índice em uma unidade para processar o caractere atual novamente
                    elif state == "float_number":
                        # Verifica se é um dígito, continuando a parte fracionária da constante em ponto flutuante
                        if c.isdigit():
                            token += c
                            i += 1
                        # Se não, a constante em ponto flutuante terminou
                        else:
                            tokens.append(
                                (sapian.getTokenContant(("const_float")), token)
                            )
                            tokens_list[line].append(
                                # f'{sapian.getTokenContant("const_float")} {token}'
                                (sapian.getTokenContant("const_float"), token)
                            )
                            token = ""
                            state = "start"
                            # Volta o índice em uma unidade para processar o caractere atual novamente
                    else:
                        return (
                            False,
                            f"ERRO: Invalid state '{state}' on the line {line+1}",
                        )

                # Verifica se ainda há um token pendente para ser processado
                if token:
                    # Verifica se é uma constante numérica inteira
                    if state == "number":
                        tokens.append((sapian.getTokenContant(("const_int")), token))
                        tokens_list[line].append(
                            # f'{sapian.getTokenContant("const_int")} {token}'
                            (sapian.getTokenContant("const_int"), token)
                        )
                    # Verifica se é uma constante numérica em ponto flutuante
                    elif state == "float_number":
                        tokens.append((sapian.getTokenContant(("const_float")), token))
                        tokens_list[line].append(
                            # f'{sapian.getTokenContant("const_float")} {token}'
                            (sapian.getTokenContant("const_float"), token)
                        )
                    # Verifica se é uma constante de caractere
                    elif state == "char":
                        tokens.append((sapian.getTokenContant(("const_char")), token))
                        tokens_list[line].append(
                            # f'{sapian.getTokenContant("const_char")} {token}'
                            (sapian.getTokenContant("const_char"), token)
                        )
                    # Verifica se é uma constante de string
                    elif state == "string":
                        tokens.append((sapian.getTokenContant("const_string"), token))
                        tokens_list[line].append(
                            # f'{sapian.getTokenContant("const_string")} {token}'
                            (sapian.getTokenContant("const_string"), token)
                        )
                    # Verifica se é uma palavra-chave
                    elif sapian.isInKeyWords(token):
                        tokens.append((sapian.getTokenKeyWord(token), token))
                        tokens_list[line].append(
                            # f"{sapian.getTokenKeyWord(token)} {token}"arquivo
                            (sapian.getTokenKeyWord(token), token)
                        )
                    # Se não, é um identificador
                    elif state == "error":
                        flag = False
                        error_lists[line].append(
                            (f"ERROR: line {line+1}", f"invalid caracter {token}")
                        )
                    else:
                        tokens.append(("IDENTIFIER", token))
                        tokens_list[line].append(f"IDENTIFIER {token}")

        for i in range(len(tokens_list)):
            tokens_list[i].remove("")
        for i in range(len(error_lists)):
            error_lists[i].remove("")
        tokens_list = np.array(tokens_list)
        error_lists = np.array(error_lists)
        return flag, tokens_list, error_lists



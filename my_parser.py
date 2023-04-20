'''code = [
    [
        ("PROGRAM", "program"),
        ("IDENTIFIER", "prog1"),
        ("SEMICOLON", ";"),
    ],
    [("INT", "int"), ("EQUAL", "x"), ("SEMICOLON", ";")],
    [("FLOAT", "float"), ("IDENTIFIER", "y"), ("SEMICOLON", ";")],
    [("CHAR", "char"), ("IDENTIFIER", "c"), ("SEMICOLON", ";")],
    [("STRING", "string"), ("IDENTIFIER", "s"), ("SEMICOLON", ";")],
    [
        ("IDENTIFIER", "x"),
        ("ATRIBUITION", ":="),
        ("INTEGER_CONST", "2"),
        ("PLUS", "+"),
        ("INTEGER_CONST", "3"),
        ("TIMES", "*"),
        ("INTEGER_CONST", "4"),
        ("SEMICOLON", ";"),
    ],
    [
        ("IDENTIFIER", "y"),
        ("ATRIBUITION", ":="),
        ("FLOAT_CONST", "3.14"),
        ("SEMICOLON", ";"),
    ],
    [
        ("IDENTIFIER", "y"),
        ("ATRIBUITION", ":="),
        ("FLOAT_CONST", "3.14"),
        ("SEMICOLON", ";"),
    ],
    [
        ("IDENTIFIER", "c"),
        ("ATRIBUITION", ":="),
        ("QUOTE", "'"),
        ("CHAR_CONST", "a"),
        ("QUOTE", "'"),
        ("SEMICOLON", ";"),
    ],
    [
        ("IDENTIFIER", "s"),
        ("ATRIBUITION", ":="),
        ("DOUBLE_QUOTE", '"'),
        ("STRING_CONST", "hello, world!"),
        ("DOUBLE_QUOTE", '"'),
        ("SEMICOLON", ";"),
    ],
    [
        ("IF", "if"),
        ("LEFT_PAREN", "("),
        ("IDENTIFIER", "x"),
        ("GREATER_EQUAL", ">="),
        ("INTEGER_CONST", "10"),
        ("RIGHT_PAREN", ")"),
        ("LEFT_BRACE", "{"),
    ],
    [
        ("IDENTIFIER", "y"),
        ("ATRIBUITION", ":="),
        ("IDENTIFIER", "y"),
        ("DIVIDE", "/"),
        ("INTEGER_CONST", "2"),
        ("SEMICOLON", ";"),
    ],
    [("RIGHT_BRACE", "}"), ("ELSE", "else"), ("LEFT_BRACE", "{")],
    [
        ("IDENTIFIER", "y"),
        ("ATRIBUITION", ":="),
        ("IDENTIFIER", "y"),
        ("TIMES", "*"),
        ("INTEGER_CONST", "2"),
        ("SEMICOLON", ";"),
    ],
    [("RIGHT_BRACE", "}")],
    [
        ("FOR", "for"),
        ("LEFT_PAREN", "("),
        ("INT", "int"),
        ("IDENTIFIER", "i"),
        ("ATRIBUITION", ":="),
        ("INTEGER_CONST", "0"),
        ("SEMICOLON", ";"),
        ("IDENTIFIER", "i"),
        ("LESS", "<"),
        ("IDENTIFIER", "x"),
        ("SEMICOLON", ";"),
        ("IDENTIFIER", "i"),
        ("ATRIBUITION", ":="),
        ("IDENTIFIER", "i"),
        ("PLUS", "+"),
        ("INTEGER_CONST", "1"),
        ("RIGHT_PAREN", ")"),
        ("LEFT_BRACE", "{"),
    ],
    [
        ("IDENTIFIER", "c"),
        ("ATRIBUITION", ":="),
        ("IDENTIFIER", "c"),
        ("PLUS", "+"),
        ("INTEGER_CONST", "1"),
        ("SEMICOLON", ";"),
    ],
    [("RIGHT_BRACE", "}")],
    [
        ("WHILE", "while"),
        ("LEFT_PAREN", "("),
        ("IDENTIFIER", "y"),
        ("GREATER", ">"),
        ("FLOAT_CONST", "1.0"),
        ("RIGHT_PAREN", ")"),
        ("LEFT_BRACE", "{"),
    ],
    [
        ("IDENTIFIER", "y"),
        ("ATRIBUITION", ":="),
        ("IDENTIFIER", "y"),
        ("MINUS", "-"),
        ("FLOAT_CONST", "1.0"),
        ("SEMICOLON", ";"),
    ],
    [("RIGHT_BRACE", "}")],
    [("END", "end"), ("SEMICOLON", ";")],
]
'''

class Parser:
    def __init__(self, code):
        self.code = code
        self.current_token = "PROGRAM"
        self.current_word = "program"
        self.position = 0
        self.pass_token = None
        self.pass_word = None
        self.pass_position = 0
        self.tokens = []
        self.pass_tokens = []
        self.pass_words = []
        self.msg = ""
        self.line = []
        for i in range(len(code)):
            self.line.append(len(code[i]))
            for j in range(len(code[i])):
                if code[i][j] != []:
                    self.tokens.append(code[i][j])

    def error(self, menssage):
        line = self.line[0]
        i = 0
        while self.position > line:
            i += 1
            line += self.line[i]
        self.msg += f"ERROR in Line {i+1}:\n\t{menssage}\n"

    def eat(self, expected_token):
        if self.current_token == expected_token:
            self.position += 1
            if self.position < len(self.tokens):
                token, word = self.tokens[self.position]
                # token = self.tokens[self.position]
                self.pass_token = self.current_token
                self.pass_word = self.current_word
                self.pass_tokens.append(self.pass_token)
                self.pass_words.append(self.pass_word)
                self.current_token = token
                self.current_word = word
                self.pass_position = self.position
        else:
            self.error(f"Palavra ou simbolo inesperado: {self.current_word}")

    def programa(self):
        self.eat("PROGRAM")
        self.identificador()
        self.eat("SEMICOLON")
        while self.current_token in ["CHAR", "STRING", "INT", "FLOAT"]:
            self.declaracao()
        while self.current_token in ["IDENTIFIER", "IF", "FOR", "WHILE"]:
            self.comando()
        self.eat("END")
        self.eat("SEMICOLON")

    def comando(self):
        if self.current_token == "IDENTIFIER":
            self.atribuicao()
        elif self.current_token == "IF":
            self.estrutura_condicional()
        elif self.current_token in ["FOR", "WHILE"]:
            self.estrutura_repeticao()

    def estrutura_repeticao(self):
        if self.current_token == "FOR":
            self.eat("FOR")
            self.eat("LEFT_PAREN")
            self.eat("INT")
            self.atribuicao()
            self.expressao()
            self.eat("SEMICOLON")
            self.identificador()
            self.eat("ATRIBUITION")
            self.expressao()
            self.eat("RIGHT_PAREN")
            self.eat("LEFT_BRACE")
            while self.current_token in ["IDENTIFIER", "IF", "FOR", "WHILE"]:
                self.comando()
            self.eat("RIGHT_BRACE")
        elif self.current_token == "WHILE":
            self.eat("WHILE")
            self.eat("LEFT_PAREN")
            self.expressao()
            self.eat("RIGHT_PAREN")
            self.eat("LEFT_BRACE")
            while self.current_token in ["IDENTIFIER", "IF", "FOR", "WHILE"]:
                self.comando()
            self.eat("RIGHT_BRACE")

    def estrutura_condicional(self):
        self.eat("IF")
        self.eat("LEFT_PAREN")
        self.expressao()
        self.eat("RIGHT_PAREN")
        self.eat("LEFT_BRACE")
        while self.current_token in ["IDENTIFIER", "IF", "FOR", "WHILE"]:
            self.comando()
        self.eat("RIGHT_BRACE")
        if self.current_token == "ELSE":
            self.eat("ELSE")
            self.eat("LEFT_BRACE")
            while self.current_token in ["IDENTIFIER", "IF", "FOR", "WHILE"]:
                self.comando()
            self.eat("RIGHT_BRACE")

    def atribuicao(self):
        self.identificador()
        self.eat("ATRIBUITION")
        if self.current_token == "QUOTE":
            self.eat("QUOTE")
            self.eat("CHAR_CONST")
            self.eat("QUOTE")
        elif self.current_token == "DOUBLE_QUOTE":
            self.eat("DOUBLE_QUOTE")
            self.eat("STRING_CONST")
            self.eat("DOUBLE_QUOTE")
        else:
            self.expressao()
        self.eat("SEMICOLON")

    def expressao(self):
        self.termo()
        while self.current_token in ["PLUS", "MINUS", "TIMES", "DIVIDE"]:
            self.eat(self.current_token)
            self.termo()
        while self.current_token in [
            "LESS",
            "LESS_EQUAL",
            "GREATER",
            "GREATER_EQUAL",
            "EQUAL",
            "NOT_EQUAL",
        ]:
            self.eat(self.current_token)
            self.expressao()

    def termo(self):
        self.fator()
        while self.current_token in ["PLUS", "MINUS", "TIMES", "DIVIDE"]:
            self.eat(self.current_token)
            self.fator()
        while self.current_token in ["AND", "OR"]:
            self.eat(self.current_token)
            self.termo()

    def fator(self):
        if self.current_token in ["INTEGER_CONST", "FLOAT_CONST"]:
            self.eat(self.current_token)
        elif self.current_token == "IDENTIFIER":
            self.eat("IDENTIFIER")
        else:
            self.error(
                f'SINTAX ERROR: esperado contant, identificador ou "(" após {self.pass_word}'
            )

    def declaracao(self):
        tipes = ["CHAR", "STRING", "INT", "FLOAT"]
        if self.current_token in tipes:
            self.eat(self.current_token)
            self.identificador()
            self.eat("SEMICOLON")
        else:
            self.error("Declaracao invalida")

    def identificador(self):
        if self.current_token == "IDENTIFIER":
            self.eat("IDENTIFIER")
        else:
            self.error(f"Esperado o identificador mas veio {self.current_word}")

    def parser(self):
        self.programa()
        if self.msg == "":
            self.msg += "Return 0\n\t"
        return self.msg


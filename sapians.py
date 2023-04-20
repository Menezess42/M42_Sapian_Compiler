class Sapians:
    def __init__(self):
        # Definição das palavras-chave
        self.keywords = {
            "program": "PROGRAM",
            "char": "CHAR",
            "string": "STRING",
            "int": "INT",
            "float": "FLOAT",
            "if": "IF",
            "else": "ELSE",
            "for": "FOR",
            "while": "WHILE",
            "end": "END",
        }

        # Definição dos operadores e símbolos
        self.operators = {
            "+": "PLUS",
            "-": "MINUS",
            "*": "TIMES",
            "/": "DIVIDE",
            "<": "LESS",
            ">": "GREATER",
            "<=": "LESS_EQUAL",
            ">=": "GREATER_EQUAL",
            ":=": "ATRIBUITION",
            "=": "EQUAL",
            "!=": "NOT_EQUAL",
            "&&": "AND",
            "||": "OR",
            ";": "SEMICOLON",
            "(": "LEFT_PAREN",
            ")": "RIGHT_PAREN",
            "{": "LEFT_BRACE",
            "}": "RIGHT_BRACE",
            "'": "QUOTE",
            '"': "DOUBLE_QUOTE",
        }

        # Definição dos tipos de constante
        self.const_types = {
            "const_int": "INTEGER_CONST",
            "const_float": "FLOAT_CONST",
            "const_string": "STRING_CONST",
            "const_char": "CHAR_CONST",
        }

    def isInKeyWords(self, word):
        if word in self.keywords:
            return True
        else:
            return False

    def getTokenKeyWord(self, word):
        return self.keywords[word]

    def isInOperators(self, c):
        for key in self.operators:
            if c in key:
                return True
        return False

    def getTokenOperator(self, word):
        return self.operators[word]

    def isInConst_types(self, word):
        if word in self.const_types:
            return True
        else:
            return False

    def getTokenContant(self, word):
        return self.const_types[word]


from .lexer import Lexer
from .tokens import TokenType
from .parser import Parser
from .generator import Generator

class Compiler:
    def compile(self, code):
        tokens = Lexer(code).tokenize()

        for token in tokens:
            print(token)

        tree = Parser(tokens).parse()
        python_code = Generator().generate(tree)

        header = "import sys; sys.setrecursionlimit(10000)\n"
        return header + python_code
    

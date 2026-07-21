from .lexer import Lexer
from .tokens import TokenType


class Compiler:

    def compile(self, code):

        lexer = Lexer(code)

        tokens = lexer.tokenize()

        for token in tokens:
            print(token)

        output = []

        i = 0

        while i < len(tokens):

            token = tokens[i]

            if token.type == TokenType.NEWLINE:
                i += 1
                continue


            # Variable assignment
            if token.type == TokenType.IDENTIFIER:

                if i + 2 < len(tokens):

                    if tokens[i + 1].type == TokenType.ASSIGN:

                        value = tokens[i + 2]

                        if value.type == TokenType.STRING:

                            output.append(
                                f'{token.value} = "{value.value}"'
                            )

                        elif value.type == TokenType.NUMBER:

                            output.append(
                                f'{token.value} = {value.value}'
                            )

                        i += 3
                        continue
                    
            # Print statement
            if token.type == TokenType.PRINT:

                value = tokens[i + 1]

                if value.type == TokenType.STRING:

                    output.append(
                        f'print("{value.value}")'
                    )

                elif value.type == TokenType.IDENTIFIER:

                    output.append(
                        f'print({value.value})'
                    )

                i += 2
                continue


            i += 1


        return "\n".join(output)

from pyplus.tokens import Token, TokenType


class Lexer:

    def __init__(self, source):
        self.source = source

    def tokenize(self):

        tokens = []

        for line_number, line in enumerate(
            self.source.splitlines(),
            start=1
        ):

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue


            # Variable assignment
            if ":=" in line:

                name, value = line.split(":=", 1)

                tokens.append(
                    Token(
                        TokenType.IDENTIFIER,
                        name.strip(),
                        line_number,
                        1
                    )
                )

                tokens.append(
                    Token(
                        TokenType.ASSIGN,
                        ":=",
                        line_number,
                        len(name)
                    )
                )

                value = value.strip()

                if value.startswith('"') and value.endswith('"'):

                    tokens.append(
                        Token(
                            TokenType.STRING,
                            value[1:-1],
                            line_number,
                            len(name)+3
                        )
                    )

                elif value.isdigit():

                    tokens.append(
                        Token(
                            TokenType.NUMBER,
                            int(value),
                            line_number,
                            len(name)+3
                        )
                    )

            elif line.startswith("print "):

                tokens.append(
                    Token(
                        TokenType.PRINT,
                        "print",
                        line_number,
                        1
                    )
                )

                text = line[6:].strip()

                if text.startswith('"') and text.endswith('"'):

                    tokens.append(
                        Token(
                            TokenType.STRING,
                            text[1:-1],
                            line_number,
                            7
                        )
                    )

                else:

                    tokens.append(
                        Token(
                            TokenType.IDENTIFIER,
                            text,
                            line_number,
                            7
                        )
                    )


            tokens.append(
                Token(TokenType.NEWLINE, None, line_number)
            )


        tokens.append(Token(TokenType.EOF))

        return tokens

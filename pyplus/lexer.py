from .tokens import Token, TokenType
from dataclasses import dataclass as dc
import sys

@dc
class Lexer:
    source   : str
    position : int = 0
    line     : int = 1
    column   : int = 1


    KEYWORDS = {
        "function": TokenType.FUNCTION,
        "end": TokenType.END,
        "return": TokenType.RETURN,
        "if": TokenType.IF,
        "True": TokenType.TRUE,
        "False": TokenType.FALSE,
    }

    def peek(self):
        if self.position + 1 < len(self.source):
            return self.source[self.position + 1]

        return ""

    def advance(self):
        self.position += 1
        self.column   += 1


    def tokenize(self):
        tokens = []

        while self.position < len(self.source):
            char = self.source[self.position]

            match char:
                # Spaces
                case " " | "\t":
                    self.advance()

                # New lines
                case "\n":
                    self.advance()
                    self.line += 1
                    self.column = 1

                # Strings
                case '"':
                    tokens.append(
                        self.read_string()
                    )

                # Numbers
                case x if x.isdigit():
                    tokens.append(
                        self.read_number()
                    )

                # Identifiers / keywords
                case x if x.isalpha() or x == "_":
                    tokens.append(
                        self.read_identifier()
                    )

                # ==
                case "=" if self.peek() == "=":
                    tokens.append(
                        Token(
                            TokenType.EQUAL,
                            "==",
                            self.line,
                            self.column
                        )
                    )

                    self.advance()
                    self.advance()

                # !=
                case "!" if self.peek() == "=":
                    tokens.append(
                        Token(
                            TokenType.NOT_EQUAL,
                            "!=",
                            self.line,
                            self.column
                        )
                    )

                    self.advance()
                    self.advance()

                # Assignment :=
                case ":" if self.peek() == "=":
                    tokens.append(
                        Token(
                            TokenType.ASSIGN,
                            ":=",
                            self.line,
                            self.column
                        )
                    )

                    self.advance()
                    self.advance()

                # <=
                case "<" if self.peek() == "=":
                    tokens.append(
                        Token(
                            TokenType.LESS_EQUAL,
                            "<=",
                            self.line,
                            self.column
                        )
                    )

                    self.advance()
                    self.advance()

                # >=
                case ">" if self.peek() == "=":
                    tokens.append(
                        Token(
                            TokenType.GREATER_EQUAL,
                            ">=",
                            self.line,
                            self.column
                        )
                    )

                    self.advance()
                    self.advance()

                # <
                case "<":
                    tokens.append(
                        Token(
                            TokenType.LESS,
                            "<",
                            self.line,
                            self.column
                        )
                    )

                    self.advance()

                # >
                case ">":
                    tokens.append(
                        Token(
                            TokenType.GREATER,
                            ">",
                            self.line,
                            self.column
                            )
                        )

                    self.advance()

                # Operators / Parentheses / Comma
                case op if op in "+-*/(),":
                    tokens.append(Token(
                            {
                                "+": TokenType.PLUS,
                                "-": TokenType.MINUS,
                                "*": TokenType.STAR,
                                "/": TokenType.SLASH,
                                "(": TokenType.LPAREN,
                                ")": TokenType.RPAREN,
                                ",": TokenType.COMMA,
                            }[op],
                            op,
                            self.line,
                            self.column
                    ))

                    self.advance()

                case _:
                    print(f"Error: Unexpected character '{char}' at {self.line}:{self.column}")
                    sys.exit(1)

        tokens.append(Token(TokenType.EOF))
        return tokens

    def read_number(self):
        start = self.column
        number = ""

        while (
            self.position < len(self.source)
            and self.source[self.position].isdigit()
        ):

            number += self.source[self.position]
            self.advance()

        return Token(
            TokenType.NUMBER,
            int(number),
            self.line,
            start
        )


    def read_string(self):
        start = self.column

        self.advance()   # Skip opening quote

        text = ""

        while (
            self.position < len(self.source)
            and self.source[self.position] != '"'
        ):

            text += self.source[self.position]
            self.advance()

        self.advance()   # Skip closing quote

        return Token(
            TokenType.STRING,
            text,
            self.line,
            start
        )


    def read_identifier(self):
        start = self.column
        word = ""

        while (
            self.position < len(self.source)
            and (
                self.source[self.position].isalnum()
                or self.source[self.position] == "_"
            )
        ):

            word += self.source[self.position]
            self.advance()

        token_type = self.KEYWORDS.get(
            word,
            TokenType.IDENTIFIER
        )

        return Token(
            token_type,
            word,
            self.line,
            start
        )



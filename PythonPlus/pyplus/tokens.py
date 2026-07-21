from enum import Enum, auto


class TokenType(Enum):
    PRINT = auto()

    IDENTIFIER = auto()

    STRING = auto()
    NUMBER = auto()

    ASSIGN = auto()      # :=

    NEWLINE = auto()
    EOF = auto()


class Token:
    def __init__(self, token_type, value=None, line=1, column=1):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return (
            f"{self.type.name}({self.value}) "
            f"[{self.line}:{self.column}]"
        )

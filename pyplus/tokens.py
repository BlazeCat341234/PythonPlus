from enum import Enum, auto
from dataclasses import dataclass as dc
from typing import Any


class TokenType(Enum):
    PRINT           = auto()

    IDENTIFIER      = auto()
    IF              = auto()

    STRING          = auto()
    NUMBER          = auto()

    ASSIGN          = auto() # :=

    PLUS            = auto()
    MINUS           = auto()
    STAR            = auto()
    SLASH           = auto()

    TRUE            = auto()
    FALSE           = auto()
    
    LPAREN          = auto()
    RPAREN          = auto()
    COMMA           = auto()

    FUNCTION        = auto()
    END             = auto()

    RETURN          = auto()
    EOF             = auto()

    EQUAL           = auto() # ==
    NOT_EQUAL       = auto() # !=

    LESS            = auto() # <
    LESS_EQUAL      = auto() # <=

    GREATER         = auto() # >
    GREATER_EQUAL   = auto() # >=


@dc
class Token:
    type   : Any
    value  : Any = None
    line   : int = 1
    column : int = 1

    def __repr__(self):
        return (
            f"{self.type.name}({self.value}) "
            f"[{self.line}:{self.column}]"
        )

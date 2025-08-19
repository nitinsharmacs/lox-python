from enum import Enum


class TokenType(Enum):
    pass


class Token:
    def __init__(self, type: TokenType, line: int, literal: any, lexeme: str):
        self.type = type
        self.line = line
        self.literal = literal
        self.lexeme = lexeme

    def __str__(self):
        return self.type + " " + self.lexeme + " " + self.literal


class Scanner:
    def __init__(self, code):
        pass

    def scan_tokens(self) -> list[Token]:
        return []

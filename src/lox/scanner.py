import typing
from src.lox.token import Token, TokenType


class SyntaxError(Exception):
    def __init__(self, line: int, char: str, *args):
        self.msg = "Unexpected character"
        self.line = line
        self.char = char
        super().__init__(f"Line: {self.line}, {self.msg}: {self.char}", *args)


class Scanner:
    def __init__(self, source_code: str):
        self.source_code: str = source_code
        self.tokens: list[Token] = []

        # locators
        self.start = 0
        self.current = 0
        self.line = 1

        self.errors: list[SyntaxError] = []

    def has_more(self) -> bool:
        return self.current < len(self.source_code)

    def advance(self) -> str:
        char = self.source_code[self.current]
        self.current += 1
        return char

    def add_token(self, token_type: TokenType, literal: typing.Any = None):
        lexeme = self.source_code[self.start : self.current]
        self.tokens.append(Token(token_type, self.line, literal, lexeme))

    def scan_token(self):
        char = self.advance()

        match char:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case _:
                error = SyntaxError(self.line, char)
                self.errors.append(error)
                print(error)

    def scan_tokens(self) -> list[Token]:
        while self.has_more():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, self.line, None, ""))

        return self.tokens

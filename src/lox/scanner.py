import typing
from src.lox.token import Token, TokenType


class TokenError(Exception):
    def __init__(self, line: int, char: str, msg=None, *args):
        self.msg = msg or "Unexpected character"
        self.line = line
        self.char = char
        super().__init__(f"Line: {self.line}, {self.msg}: {self.char}", *args)


class UnterminatedStringError(TokenError):
    def __init__(self, line, *args):
        self.line = line
        self.msg = "Unterminated string"
        super().__init__(line, "", self.msg, *args)


class Scanner:
    def __init__(self, source_code: str):
        self.source_code: str = source_code
        self.tokens: list[Token] = []

        # locators
        self.start = 0
        self.current = 0
        self.line = 1

        self.errors: list[TokenError] = []

    def has_more(self) -> bool:
        return self.current < len(self.source_code)

    def advance(self) -> str:
        char = self.source_code[self.current]
        self.current += 1
        return char

    def match(self, expected: str) -> bool:
        if self.has_more():
            if self.source_code[self.current] == expected:
                self.current += 1
                return True
            else:
                return False

        return False

    def add_token(self, token_type: TokenType, literal: typing.Any = None):
        lexeme = self.source_code[self.start : self.current]
        self.tokens.append(Token(token_type, self.line, literal, lexeme))

    def exhaust_line(self):
        while self.peek() != "\n" and self.has_more():
            self.advance()

    def peek(self) -> str:
        if self.has_more():
            return self.source_code[self.current]
        return "\0"

    def peek_next(self) -> str:
        if self.current + 1 < len(self.source_code):
            return self.source_code[self.current + 1]
        return "\0"

    def scan_string(self):
        while self.has_more():
            char = self.peek()

            if char == '"':
                break
            if char == "\n":
                return self.errors.append(UnterminatedStringError(self.line))

            self.advance()
        else:
            return self.errors.append(UnterminatedStringError(self.line))

        value = self.source_code[self.start + 1 : self.current]

        self.advance()

        self.add_token(TokenType.STRING, value)

    def scan_number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        self.add_token(
            TokenType.NUMBER, float(self.source_code[self.start : self.current])
        )

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
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case "/":
                if self.match("/"):
                    self.exhaust_line()
                else:
                    self.add_token(TokenType.SLASH)
            case '"':
                self.scan_string()
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case _:
                if char.isdigit():
                    self.scan_number()
                else:
                    error = TokenError(self.line, char)
                    self.errors.append(error)
                    print(error)

    def scan_tokens(self) -> list[Token]:
        while self.has_more():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, self.line, None, ""))

        return self.tokens

from src.lox.token import Token


class RuntimeException(Exception):
    def __init__(self, token: Token, msg: str, *args):
        self.token = token
        super().__init__(f"'{token.lexeme}' at line {token.line}, {msg}", *args)


class DivideByZeroException(RuntimeException):
    pass


class ReferenceException(RuntimeException):
    pass


class BreakException(Exception):
    pass

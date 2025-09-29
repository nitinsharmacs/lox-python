from src.lox.ast import Expr, Grouping
from src.lox.ast import Binary, Literal, Unary
from src.lox.token import Token, TokenType


class SyntaxError(Exception):
    def __init__(self, token: Token, msg: str, *args):
        self.token = token
        super().__init__(f"Line: {token.line}, {msg}", *args)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.current = 0
        self.tokens = tokens
        self.errors = []

    ## parsing infrastructure

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self):
        return self.tokens[self.current - 1]

    def peek(self):
        return self.tokens[self.current]

    def is_at_end(self):
        return self.tokens[self.current].type == TokenType.EOF

    def check(self, token_type: TokenType) -> bool:
        return False if self.is_at_end() else self.peek().type == token_type

    def match_any(self, *tokens_type: list[TokenType]) -> bool:
        for type in tokens_type:
            if self.check(type):
                self.advance()
                return True
        return False

    ## end of parsing infrastructure

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        """
        Rule implementation.
        equality -> comparision (("=="|"!=") comparision)*
        """
        expr = self.comparision()

        while self.match_any(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            right_operand = self.comparision()
            expr = Binary(expr, operator, right_operand)

        return expr

    def comparision(self) -> Expr:
        """
        Rule implementation.
        comparision -> term ((">" | "<" | ">=" | "<=") term)*
        """
        expr = self.term()

        while self.match_any(
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right_operand = self.term()
            expr = Binary(expr, operator, right_operand)

        return expr

    def term(self) -> Expr:
        """
        Rule implementation.
        term -> factor (("+"|"-") factor)*
        """
        expr = self.factor()

        while self.match_any(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right_operand = self.term()
            expr = Binary(expr, operator, right_operand)

        return expr

    def factor(self) -> Expr:
        """
        Rule implementation.
        factor -> unary (("*"|"/") unary)*
        """
        expr = self.unary()

        while self.match_any(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right_operand = self.unary()
            expr = Binary(expr, operator, right_operand)

        return expr

    def unary(self) -> Expr:
        """
        Rule implementation.
        unary -> ("-"|"!") unary
                | primary
        """

        if self.match_any(TokenType.MINUS, TokenType.BANG):
            operator = self.previous()
            operand = self.unary()
            return Unary(operator, operand)

        return self.primary()

    def primary(self) -> Expr:
        """
        Rule implementation.
        primary -> STRING | NUMBER | "true" | "false" | "nil"
                   | "( expression ")"
        """

        if self.match_any(TokenType.TRUE):
            return Literal(True)
        if self.match_any(TokenType.FALSE):
            return Literal(False)
        if self.match_any(TokenType.NIL):
            return Literal("nil")
        if self.match_any(TokenType.STRING, TokenType.NUMBER):
            return Literal(self.previous().literal)

        if self.match_any(TokenType.LEFT_PAREN):
            expr = self.expression()

            if self.check(TokenType.RIGHT_PAREN):
                return Grouping(expr)
            else:
                return self.errors.append(
                    SyntaxError(self.peek(), "Expected closing ')'.")
                )

        self.errors.append(SyntaxError(self.peek(), "Expected expression."))

    def synchronize(self):
        """
        Synchronize the parser at the point where valid sequence of token continues. Skips the non valid sequence of token until valid ones come.
        """
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            match self.peek():
                case TokenType.CLASS:
                    return
                case TokenType.FUN:
                    return
                case TokenType.VAR:
                    return
                case TokenType.FOR:
                    return
                case TokenType.IF:
                    return
                case TokenType.WHILE:
                    return
                case TokenType.PRINT:
                    return
                case TokenType.RETURN:
                    return
            self.advance()

    def parse(self) -> Expr:
        return self.expression()

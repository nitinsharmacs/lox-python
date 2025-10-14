from src.lox.ast_printer import AstPrinter
from src.lox.expr import Assignment, Expr, Grouping, Logical, Variable
from src.lox.expr import Binary, Literal, Unary
from src.lox.stmt import (
    BlockStmt,
    ExprStmt,
    IfStmt,
    PrintStmt,
    Stmt,
    VarDeclStmt,
    WhileStmt,
)
from src.lox.token import Token, TokenType


class SyntaxError(Exception):
    def __init__(self, token: Token, msg: str, *args):
        self.token = token
        super().__init__(f"at line {token.line}, {msg}", *args)


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

    def match_any(self, *tokens_type: TokenType) -> bool:
        for token_type in tokens_type:
            if self.check(token_type):
                self.advance()
                return True
        return False

    ## end of parsing infrastructure

    def declaration(self) -> Stmt | None:
        """
        Rule implementation.
        declaration -> varDecl
                       | statement
        """
        try:
            if self.match_any(TokenType.VAR):
                return self.var_declaration()

            return self.statement()
        except Exception as exp:
            self.synchronize()

    def var_declaration(self) -> Stmt:
        """
        Rule implementation.
        varDecl -> "var" IDENTIFIER ("=" expression)? ";"
        """
        identifier = self.consume(
            TokenType.IDENTIFIER, "Expect a variable name."
        )

        initializer = None
        if self.match_any(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")

        return VarDeclStmt(identifier, initializer)

    def statement(self) -> Stmt:
        """
        Rule implementation.
        statement -> printStmt
                     | exprStmt
                     | blockStmt
                     | ifStmt
                     | whileStmt
                     | forStmt
        """
        if self.match_any(TokenType.PRINT):
            return self.print_stmt()

        if self.match_any(TokenType.LEFT_BRACE):
            return BlockStmt(self.block_stmt())

        if self.match_any(TokenType.IF):
            return self.if_stmt()

        if self.match_any(TokenType.WHILE):
            return self.while_stmt()

        if self.match_any(TokenType.FOR):
            return self.for_stmt()

        return self.expr_stmt()

    def print_stmt(self) -> Stmt:
        """
        Rule implementation.
        print_stmt -> "print" expression ";"
        """
        expr = self.expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")

        return PrintStmt(expr)

    def expr_stmt(self) -> Stmt:
        """
        Rule implemenation.
        expr_stmt -> expression ";"
        """
        expr = self.expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after expression.")

        return ExprStmt(expr)

    def block_stmt(self) -> list[Stmt]:
        """
        Rule implementation.
        blockStmt -> "{" declaraction* "}"
        """
        statements = []
        while not (self.check(TokenType.RIGHT_BRACE) or self.is_at_end()):
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expected '}' to close block.")

        return statements

    def if_stmt(self) -> Stmt:
        """
        Rule implementation.
        ifStmt -> "if" "(" expression ")" statement
                  ("else" statement)?
        """
        self.consume(TokenType.LEFT_PAREN, "Expected '( after if.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ') after if condition.")

        then_branch = self.statement()
        else_branch = None

        if self.match_any(TokenType.ELSE):
            else_branch = self.statement()

        return IfStmt(condition, then_branch, else_branch)

    def while_stmt(self) -> Stmt:
        """
        Rule implementation.
        whileStmt -> "while" "(" expression ")" statement
        """

        self.consume(TokenType.LEFT_PAREN, "Expected '( after while.")
        condition = self.expression()
        self.consume(
            TokenType.RIGHT_PAREN, "Expected ') after while condition."
        )
        body = self.statement()

        return WhileStmt(condition, body)

    def for_stmt(self) -> Stmt:
        """
        Rule implementation.
        forStmt -> "for" "(" (varDecl | exprStmt | ";")
                    expression? ";"
                    expression? ")" statement
        """
        self.consume(TokenType.LEFT_PAREN, "Expected '( after for.")

        initializer = None
        if not self.match_any(TokenType.SEMICOLON):
            if self.match_any(TokenType.VAR):
                initializer = self.var_declaration()
            else:
                initializer = self.expr_stmt()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()

        self.consume(
            TokenType.SEMICOLON, "Expected ';' after for loop condition."
        )

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()

        self.consume(TokenType.RIGHT_PAREN, "Expected ') after for clause.")

        body = self.statement()

        if increment is not None:
            body = BlockStmt([body, ExprStmt(increment)])

        body = WhileStmt(
            condition if condition is not None else Literal(True), body
        )

        if initializer is not None:
            body = BlockStmt([initializer, body])

        return body

    def expression(self) -> Expr:
        """
        Rule implementation.
        expression -> assignment
        """
        return self.assignment()

    def assignment(self) -> Expr:
        """
        Rule implementation.
        assignment -> IDENTIFIER "=" assignment
                      | logical_or
        """
        expr = self.logical_or()

        if self.match_any(TokenType.EQUAL):
            token = self.previous()
            if type(expr) is Variable:
                value = self.assignment()
                return Assignment(expr.name, value)
            self.errors.append(
                SyntaxError(
                    token, "Invalid assignment. Did you mean to use '=='?"
                )
            )

        return expr

    def logical_or(self) -> Expr:
        """
        Rule implementation.
        logical_or -> logical_and ("or" logical_and)*
        """
        left = self.logical_and()

        if self.match_any(TokenType.OR):
            token = self.previous()
            right = self.logical_and()
            return Logical(left, token, right)

        return left

    def logical_and(self) -> Expr:
        """
        Rule implementation.
        logical_and -> equality ("and" equality)*
        """
        left = self.equality()

        if self.match_any(TokenType.AND):
            token = self.previous()
            right = self.equality()
            return Logical(left, token, right)

        return left

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
            right_operand = self.factor()
            expr = Binary(expr, operator, right_operand)

        return expr

    def factor(self) -> Expr:
        """
        Rule implementation.
        factor -> unary (("*"|"/") unary)*
        """
        expr = self.unary()

        while self.match_any(TokenType.SLASH, TokenType.STAR):
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
        primary -> STRING | NUMBER
                   | "true" | "false"
                   | "nil"
                   | "( expression ")"
                   | IDENTIFIER
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
            self.consume(TokenType.RIGHT_PAREN, "Expected closing ')'.")
            return Grouping(expr)

        if self.match_any(TokenType.IDENTIFIER):
            return Variable(self.previous())

        error = SyntaxError(self.peek(), "Expected expression.")
        self.errors.append(error)

        raise error

    def consume(self, token_type: TokenType, error_msg: str) -> Token:
        """
        Consume the current token. Store error if token type does not match.
        """

        if self.match_any(token_type):
            return self.previous()

        error = SyntaxError(self.previous(), error_msg)
        self.errors.append(error)

        raise error

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

    def parse(self) -> list[Stmt]:
        statements = []

        while not self.is_at_end():
            statements.append(self.declaration())

        return statements

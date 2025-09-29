from abc import ABC, abstractmethod
from src.lox.common import Visitor
from src.lox.token import Token, TokenType


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinary(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnary(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteral(self)


class Grouping(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visitGrouping(self)

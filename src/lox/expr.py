from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from src.lox.token import Token, TokenType


class ExprVisitor(ABC):
    @abstractmethod
    def visit_binary(self, expr) -> Expr:
        pass

    @abstractmethod
    def visit_unary(self, expr) -> Expr:
        pass

    @abstractmethod
    def visit_grouping(self, expr) -> Expr:
        pass

    @abstractmethod
    def visit_literal(self, expr) -> Expr:
        pass

    @abstractmethod
    def visit_variable(self, expr) -> Expr:
        pass


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor) -> Any:
        pass


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)

    def __str__(self):
        return self.left.__str__() + self.operator.lexeme + self.right.__str__()


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

    def __str__(self):
        return str(self.value)


class Grouping(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_grouping(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_variable(self)

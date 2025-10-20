from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from src.lox.token import Token, TokenType

if TYPE_CHECKING:
    from src.lox.stmt import Stmt


class ExprVisitor(ABC):
    @abstractmethod
    def visit_binary(self, expr: Binary):
        pass

    @abstractmethod
    def visit_unary(self, expr: Unary):
        pass

    @abstractmethod
    def visit_grouping(self, expr: Grouping):
        pass

    @abstractmethod
    def visit_literal(self, expr: Literal):
        pass

    @abstractmethod
    def visit_variable(self, expr: Variable):
        pass

    @abstractmethod
    def visit_assignment(self, expr: Assignment):
        pass

    @abstractmethod
    def visit_logical(self, expr: Logical):
        pass

    @abstractmethod
    def visit_call(self, expr: Call):
        pass

    @abstractmethod
    def visit_anonymous_fn(self, expr: AnonymousFnExpr):
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


class Assignment(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_assignment(self)


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_logical(self)


class Call(Expr):
    def __init__(
        self,
        callee: Expr,
        arguments: list[Expr],
        token: Token,
    ) -> None:
        self.callee = callee
        self.arguments = arguments
        self.token = token

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_call(self)


class AnonymousFnExpr(Expr):
    def __init__(self, params: list[Token], body: list[Stmt]) -> None:
        self.params = params
        self.body = body

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_anonymous_fn(self)

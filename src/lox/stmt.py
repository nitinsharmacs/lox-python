from __future__ import annotations

from abc import ABC, abstractmethod

from src.lox.expr import Expr


class StmtVisitor(ABC):
    @abstractmethod
    def visit_expr_stmt(self, expr_stmt: ExprStmt):
        pass

    @abstractmethod
    def visit_print_stmt(self, print_stmt: PrintStmt):
        pass


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor):
        pass


class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_expr_stmt(self)


class PrintStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_print_stmt(self)

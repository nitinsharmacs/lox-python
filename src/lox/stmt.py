from __future__ import annotations

from abc import ABC, abstractmethod

from src.lox.expr import Expr
from src.lox.token import Token


class StmtVisitor(ABC):
    @abstractmethod
    def visit_expr_stmt(self, stmt: ExprStmt):
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: PrintStmt):
        pass

    @abstractmethod
    def visit_var_decl_stmt(self, stmt: VarDeclStmt):
        pass


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor):
        pass


class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_expr_stmt(self)


class PrintStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_print_stmt(self)


class VarDeclStmt(Stmt):
    def __init__(self, identifier: Token, expr: Expr | None):
        self.identifier = identifier
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_var_decl_stmt(self)

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

    @abstractmethod
    def visit_block_stmt(self, stmt: BlockStmt):
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt: IfStmt):
        pass

    @abstractmethod
    def visit_while_stmt(self, stmt: WhileStmt):
        pass

    @abstractmethod
    def visit_break_stmt(self, stmt: BreakStmt):
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


class BlockStmt(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements = statements

    def accept(self, visitor: StmtVisitor):
        visitor.visit_block_stmt(self)


class IfStmt(Stmt):
    def __init__(
        self,
        condition: Expr,
        then_branch: Stmt,
        else_branch: Stmt | None = None,
    ) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: StmtVisitor):
        visitor.visit_if_stmt(self)


class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: Stmt) -> None:
        self.condition = condition
        self.body = body

    def accept(self, visitor: StmtVisitor):
        visitor.visit_while_stmt(self)


class BreakStmt(Stmt):
    def __init__(self) -> None:
        pass

    def accept(self, visitor: StmtVisitor):
        visitor.visit_break_stmt(self)

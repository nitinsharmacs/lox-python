from src.lox.exceptions import ReferenceException
from src.lox.expr import (
    AnonymousFnExpr,
    Assignment,
    Binary,
    Call,
    Expr,
    ExprVisitor,
    GetExpr,
    Grouping,
    Literal,
    Logical,
    SetExpr,
    Unary,
    Variable,
)
from src.lox.stmt import (
    BlockStmt,
    BreakStmt,
    ClassDeclStmt,
    ExprStmt,
    FunDeclStmt,
    IfStmt,
    PrintStmt,
    ReturnStmt,
    Stmt,
    StmtVisitor,
    VarDeclStmt,
    WhileStmt,
)
from src.lox.token import Token


class Resolver(StmtVisitor, ExprVisitor):
    def __init__(self) -> None:
        self.scopes: list[dict] = []
        self.errors = []
        self.bindings = {}
        self.resolving_fun = False

    def new_error(self, token: Token, msg) -> Exception:
        error = ReferenceException(token, msg)
        self.errors.append(error)
        return error

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, variable: Token):
        if len(self.scopes) == 0:
            return

        if self.scopes[-1].get(variable.lexeme) is not None:
            self.new_error(
                variable,
                f"A variable named '{variable.lexeme}' already present.",
            )
        self.scopes[-1][variable.lexeme] = False

    def define(self, variable: Token):
        if len(self.scopes) == 0:
            return

        self.scopes[-1][variable.lexeme] = True

    def resolve_expr(self, expr: Expr):
        expr.accept(self)

    def resolve_stmt(self, stmt: Stmt):
        stmt.accept(self)

    def resolve_stmts(self, stmts: list[Stmt]):
        for stmt in stmts:
            self.resolve_stmt(stmt)

    def resolve_local_var(self, expr: Expr, var: Token):
        scopes = list(enumerate(self.scopes))
        scopes.reverse()
        rel = len(self.scopes) - 1
        for i, scope in scopes:
            if scope.get(var.lexeme):
                self.bindings[expr] = rel - i
                return

    def visit_block_stmt(self, stmt: BlockStmt):
        self.begin_scope()

        self.resolve_stmts(stmt.statements)

        self.end_scope()

    def visit_var_decl_stmt(self, stmt: VarDeclStmt):
        self.declare(stmt.identifier)

        if stmt.expr is not None:
            self.resolve_expr(stmt.expr)

        self.define(stmt.identifier)

    def visit_variable(self, expr: Variable):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) == False:
            self.new_error(
                expr.name,
                f"Can't access '{expr.name.lexeme}' before initialization.",
            )

        self.resolve_local_var(expr, expr.name)

    def visit_assignment(self, expr: Assignment):
        self.resolve_expr(expr.value)
        self.resolve_local_var(expr, expr.name)

    def visit_fun_decl(self, stmt: FunDeclStmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_expr(stmt.declaration)

    def visit_anonymous_fn(self, expr: AnonymousFnExpr):
        prev_fn_status = self.resolving_fun
        self.resolving_fun = True
        self.begin_scope()

        for param in expr.params:
            self.declare(param)
            self.define(param)

        self.resolve_stmts(expr.body)

        self.end_scope()
        self.resolving_fun = prev_fn_status

    def visit_class_decl(self, stmt: ClassDeclStmt):
        self.declare(stmt.name)
        self.define(stmt.name)

    def visit_expr_stmt(self, stmt: ExprStmt):
        self.resolve_expr(stmt.expr)

    def visit_if_stmt(self, stmt: IfStmt):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve_stmt(stmt.else_branch)

    def visit_while_stmt(self, stmt: WhileStmt):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)

    def visit_print_stmt(self, stmt: PrintStmt):
        self.resolve_expr(stmt.expr)

    def visit_return_stmt(self, stmt: ReturnStmt):
        if self.resolving_fun is False:
            self.new_error(stmt.token, "Can't return from top-level code.")

        if stmt.value is not None:
            self.resolve_expr(stmt.value)

    def visit_break_stmt(self, stmt: BreakStmt):
        pass

    def visit_call(self, expr: Call):
        self.resolve_expr(expr.callee)

        for arg in expr.arguments:
            self.resolve_expr(arg)

    def visit_binary(self, expr: Binary):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_grouping(self, expr: Grouping):
        self.resolve_expr(expr.expr)

    def visit_literal(self, expr: Literal):
        pass

    def visit_logical(self, expr: Logical):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_unary(self, expr: Unary):
        self.resolve_expr(expr.right)

    def visit_get_expr(self, expr: GetExpr):
        self.resolve_expr(expr.object)

    def visit_set_expr(self, expr: SetExpr):
        self.resolve_expr(expr.object)
        self.resolve_expr(expr.value)

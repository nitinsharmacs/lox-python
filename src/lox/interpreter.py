# type: ignore

from ast import And
import operator
from typing import Any
from src.lox.ast_printer import stringify
from src.lox.callable import Callable
from src.lox.env import Environment
from src.lox.expr import (
    Assignment,
    Binary,
    Call,
    Expr,
    ExprVisitor,
    Grouping,
    Literal,
    Logical,
    Unary,
    Variable,
)
from src.lox.natives import set_natives
from src.lox.stmt import (
    BlockStmt,
    BreakStmt,
    IfStmt,
    Stmt,
    StmtVisitor,
    VarDeclStmt,
    WhileStmt,
)
from src.lox.token import TokenType, Token


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


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.errors: [Exception] = []
        self.env_global = Environment()

        set_natives(self.env_global)

        self.env = self.env_global

    def evaluate(self, stmt: Stmt | Expr):
        return stmt.accept(self)

    ## ----------- statements start ----------------
    def visit_var_decl_stmt(self, stmt: VarDeclStmt):
        value = None
        if stmt.expr is not None:
            value = self.evaluate(stmt.expr)

        self.env.put(stmt.identifier.lexeme, value)

    def visit_variable(self, expr: Variable):
        try:
            return self.env.get(expr.name.lexeme)
        except Exception as _:
            raise ReferenceException(expr.name, "Undefined Variable.")

    def visit_expr_stmt(self, expr_stmt):
        self.evaluate(expr_stmt.expr)

    def visit_print_stmt(self, print_stmt):
        result = self.evaluate(print_stmt.expr)
        print(stringify(result))

    def visit_block_stmt(self, stmt: BlockStmt):
        self.execute_block(stmt.statements, Environment(self.env))

    def execute_block(self, statements: list[Stmt], env: Environment):
        previous = self.env
        self.env = env
        try:
            for statement in statements:
                self.evaluate(statement)
        finally:
            self.env = previous

    def visit_if_stmt(self, stmt: IfStmt):
        if self.evaluate(stmt.condition):
            self.evaluate(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.evaluate(stmt.else_branch)

    def visit_while_stmt(self, stmt: WhileStmt):
        try:
            while self.evaluate(stmt.condition):
                self.evaluate(stmt.body)
        except Exception as exc:
            pass

    def visit_break_stmt(self, stmt: BreakStmt):
        raise BreakException()

    ## ----------- statements end -------------------

    ## ----------- expressions start ----------------
    def visit_assignment(self, expr: Assignment):
        try:
            self.env.assign(expr.name.lexeme, self.evaluate(expr.value))
        except Exception as excp:
            raise ReferenceException(
                expr.name, "Cannot assign to undefined Variable."
            )

    def visit_call(self, expr: Call) -> Any:
        callee = self.evaluate(expr.callee)

        if not isinstance(callee, Callable):
            raise RuntimeException(
                expr.token, "Only functions and classes are callable."
            )

        if len(expr.arguments) > callee.arity:
            raise RuntimeException(
                expr.token,
                f"Expected {callee.arity} arguments, but got {len(expr.arguments)}",
            )

        args = map(self.evaluate, expr.arguments)

        return callee.call(self, list(args))

    def visit_literal(self, expr: Literal):
        return expr.value

    def visit_grouping(self, expr: Grouping):
        return self.evaluate(expr.expr)

    def visit_binary(self, expr: Binary):
        left_operand = self.evaluate(expr.left)
        right_operand = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.PLUS:
                if self.all_type(str, left_operand, right_operand):
                    return left_operand + right_operand

                if self.all_type(float, left_operand, right_operand):
                    return left_operand + right_operand

                raise RuntimeException(
                    expr.operator, "Either numbers or strings permitted."
                )
            case TokenType.MINUS:
                self.assert_numerical_operands(
                    expr.operator, left_operand, right_operand
                )
                return left_operand - right_operand
            case TokenType.SLASH:
                self.assert_numerical_operands(
                    expr.operator, left_operand, right_operand
                )
                if right_operand == 0:
                    raise DivideByZeroException(
                        expr.operator, "Divide by zero not permitted."
                    )
                return left_operand / right_operand
            case TokenType.STAR:
                self.assert_numerical_operands(
                    expr.operator, left_operand, right_operand
                )
                return left_operand * right_operand
            case TokenType.GREATER:
                self.assert_numerical_operands(
                    expr.operator, left_operand, right_operand
                )
                return left_operand > right_operand
            case TokenType.LESS:
                self.assert_numerical_operands(
                    expr.operator, left_operand, right_operand
                )
                return left_operand < right_operand
            case TokenType.GREATER_EQUAL:
                self.assert_numerical_operands(
                    expr.operator, left_operand, right_operand
                )
                return left_operand >= right_operand
            case TokenType.LESS_EQUAL:
                self.assert_numerical_operands(
                    expr.operator, left_operand, right_operand
                )
                return left_operand <= right_operand
            case TokenType.EQUAL_EQUAL:
                return left_operand == right_operand
            case TokenType.BANG_EQUAL:
                return left_operand != right_operand

    def visit_logical(self, expr: Logical):
        left_result = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if left_result:
                return left_result
        elif expr.operator.type == TokenType.AND:
            if not left_result:
                return left_result

        return self.evaluate(expr.right)

    def visit_unary(self, expr: Unary):
        match expr.operator.type:
            case TokenType.MINUS:
                return -(self.evaluate(expr.right))
            case TokenType.BANG:
                return not self.evaluate(expr.right)

    ## ----------- expressions end ----------------

    def interpret(self, stmts: list[Stmt]):
        try:
            for stmt in stmts:
                self.evaluate(stmt)
        except RuntimeException as exp:
            self.errors = [exp]

    def reset_errors(self):
        self.errors = []

    @staticmethod
    def assert_numerical_operands(token: Token, left, right):
        if type(left) is float and type(right) is float:
            return

        raise RuntimeException(token, "Only numbers permitted.")

    @staticmethod
    def all_type(_type, *values) -> bool:
        for value in values:
            if type(value) is not _type:
                return False
        return True

    @property
    def has_error(self):
        return len(self.errors) > 0

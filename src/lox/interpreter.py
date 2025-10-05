from src.lox.ast import Binary, Expr, Grouping, Literal, Unary
from src.lox.common import Visitor
from src.lox.token import TokenType, Token


class RuntimeException(Exception):
    def __init__(self, token: Token, msg: str, *args):
        self.token = token
        super().__init__(f"Char '{token.lexeme}' at line: {token.line}, {msg}", *args)


class DivideByZeroException(RuntimeException):
    pass


class Interpreter(Visitor):
    def __init__(self):
        self.errors = []

    def evaluate(self, ast: Expr):
        return ast.accept(self)

    def visitLiteral(self, expr: Literal):
        return expr.value

    def visitGrouping(self, expr: Grouping):
        return self.evaluate(expr.expr)

    def visitBinary(self, expr: Binary):
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

    def visitUnary(self, expr: Unary):
        match expr.operator.type:
            case TokenType.MINUS:
                return -(self.evaluate(expr.right))
            case TokenType.BANG:
                return not self.evaluate(expr.right)

    def interpret(self, ast: Expr):
        try:
            return self.evaluate(ast)
        except RuntimeException as exp:
            self.errors = [exp]

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

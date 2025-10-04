from src.lox.ast import Binary, Expr, Grouping, Literal, Unary
from src.lox.common import Visitor
from src.lox.token import TokenType


class Interpreter(Visitor):
    def evaluate(self, ast: Expr):
        return ast.accept(self)

    def visitLiteral(self, expr: Literal):
        return expr.value

    def visitGrouping(self, expr: Grouping):
        return self.evaluate(expr.expr)

    def visitBinary(self, expr: Binary):
        left_op = self.evaluate(expr.left)
        right_op = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.PLUS:
                return left_op + right_op
            case TokenType.MINUS:
                return left_op - right_op
            case TokenType.SLASH:
                return left_op / right_op
            case TokenType.STAR:
                return left_op * right_op

    def visitUnary(self, expr: Unary):
        match expr.operator.type:
            case TokenType.MINUS:
                return -(self.evaluate(expr.right))
            case TokenType.BANG:
                return not self.evaluate(expr.right)

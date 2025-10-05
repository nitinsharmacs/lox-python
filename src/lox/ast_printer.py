from src.lox.common import Visitor
from src.lox.ast import Binary, Expr, Grouping, Literal, Unary
from src.lox.token import Token, TokenType


class AstPrinter(Visitor):
    def print(self, expr: Expr):
        print(expr.accept(self))

    def visitBinary(self, expr: Binary):
        return self.__print(expr.operator.lexeme, expr.left, expr.right)

    def visitUnary(self, expr: Unary):
        return self.__print(expr.operator.lexeme, expr.right)

    def visitLiteral(self, expr: Literal):
        return stringify(expr.value)

    def visitGrouping(self, expr: Grouping):
        return self.__print("group", expr.expr)

    def __print(self, name, *exprs: Expr):
        result = "("
        result += str(name)

        for expr in exprs:
            result += " "
            result += expr.accept(self)

        result += ")"
        return result


if __name__ == "__main__":
    ast1 = Binary(
        Literal(Token(TokenType.NUMBER, 0, 1, "1")),
        Token(TokenType.PLUS, 1, None, "+"),
        Literal(Token(TokenType.NUMBER, 0, 1, "1")),
    )
    printer = AstPrinter()
    printer.print(ast1)

    ast2: Expr = Binary(
        Unary(
            Token(TokenType.MINUS, "1", None, "-"),
            Literal(Token(TokenType.NUMBER, 1, 123, "123")),
        ),
        Token(TokenType.STAR, "1", None, "+"),
        Grouping(Literal(Token(TokenType.NUMBER, 1, 45.67, "45.67"))),
    )

    printer.print(ast2)


def print_errors(errors: list[Exception]):
    for error in errors:
        print(error)


def stringify(value):
    if value == None:
        return "nil"
    if type(value) is float:
        str_equiv = str(value)
        if str_equiv.endswith(".0"):
            return str_equiv[:-2]
    if type(value) is bool:
        if value:
            return "true"
        else:
            return "false"

    return str(value)

from src.lox.expr import Binary, Expr, ExprVisitor, Grouping, Literal, Unary
from src.lox.token import Token, TokenType


class AstPrinter(ExprVisitor):
    def print(self, expr: Expr):
        print(expr.accept(self))

    def visit_binary(self, expr: Binary):
        return self.__print(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary(self, expr: Unary):
        return self.__print(expr.operator.lexeme, expr.right)

    def visit_literal(self, expr: Literal):
        return stringify(expr.value)

    def visit_grouping(self, expr: Grouping):
        return self.__print("group", expr.expr)

    def __print(self, name, *exprs: Expr):
        result = "("
        result += str(name)

        for expr in exprs:
            result += " "
            result += expr.accept(self)

        result += ")"
        return result

    def visit_variable(self, expr) -> Expr:
        raise NotImplementedError


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
            Token(TokenType.MINUS, 1, None, "-"),
            Literal(Token(TokenType.NUMBER, 1, 123, "123")),
        ),
        Token(TokenType.STAR, 1, None, "+"),
        Grouping(Literal(Token(TokenType.NUMBER, 1, 45.67, "45.67"))),
    )

    printer.print(ast2)


def print_errors(errors: list[Exception]):
    for error in errors:
        msg = str(error)
        error_type = str(error.__class__.__name__)
        print(error_type + ": " + msg)


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

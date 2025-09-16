from src.lox.token import Token

# expression     → literal
#                | unary
#                | binary
#                | grouping ;

# literal        → NUMBER | STRING | "true" | "false" | "nil" ;
# grouping       → "(" expression ")" ;
# unary          → ( "-" | "!" ) expression ;
# binary         → expression operator expression ;
# operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
#                | "+"  | "-"  | "*" | "/" ;


class Expr:
    pass


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right


class Unary(Expr):
    def __init__(self, operator, right):
        self.left: Token = operator
        self.right: Expr = right


class Literal(Expr):
    def __init__(self, value):
        self.value: Token = value


class Grouping(Expr):
    def __init__(self, expr):
        self.expr: Expr = expr

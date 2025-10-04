import sys

from src.lox.ast_printer import AstPrinter
from src.lox.interpreter import Interpreter
from src.lox.parser import Parser
from src.lox.scanner import Scanner


def print_errors(errors: list[Exception]):
    for error in errors:
        print(error)


def run(code: str):
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()

    if len(scanner.errors) > 0:
        return

    parser = Parser(tokens)
    ast = parser.parse()

    if len(parser.errors) > 0:
        print_errors(parser.errors)
        return

    interpreter = Interpreter()
    print(interpreter.evaluate(ast))
    # AstPrinter().print(ast)


def run_file(file: str):
    with open(file, "r", encoding="utf-8") as _file:
        run(_file.read())


def start_repl():
    while True:
        line = input("> ")
        if line is None:
            break
        run(line)


def main(args: list[str]):
    arg_size = len(args)

    if arg_size > 1:
        print("Usage: plox [script]")
        sys.exit(64)
    elif arg_size == 1:
        run_file(args[0])
    else:
        start_repl()


if __name__ == "__main__":
    main(sys.argv[1:])

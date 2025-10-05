import sys

from src.lox.ast_printer import AstPrinter, print_errors, stringify
from src.lox.interpreter import Interpreter
from src.lox.parser import Parser
from src.lox.scanner import Scanner

had_errors = False
had_runtime_errors = False


def run(code: str):
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()

    global had_errors
    global had_runtime_errors

    if len(scanner.errors) > 0:
        print_errors(parser.errors)
        had_errors = True
        return

    parser = Parser(tokens)
    ast = parser.parse()

    if len(parser.errors) > 0:
        had_errors = True
        print_errors(parser.errors)
        return

    interpreter = Interpreter()
    result = interpreter.interpret(ast)

    if interpreter.has_error:
        print_errors(interpreter.errors)
        had_runtime_errors = True
        return

    print(stringify(result))


def run_file(file: str):
    with open(file, "r", encoding="utf-8") as _file:
        run(_file.read())
        if had_errors:
            sys.exit(65)
        if had_runtime_errors:
            sys.exit(70)


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

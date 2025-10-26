import sys

from src.lox.ast_printer import print_errors
from src.lox.interpreter import Interpreter
from src.lox.parser import Parser
from src.lox.resolver import Resolver
from src.lox.scanner import Scanner


class Lox:
    def __init__(self):
        self.had_errors = False
        self.had_runtime_errors = False
        self.resolver = Resolver()
        self.interpreter = Interpreter()

    def run(self, code: str):
        self.interpreter.reset_errors()

        scanner = Scanner(code)
        tokens = scanner.scan_tokens()

        if len(scanner.errors) > 0:
            print_errors(scanner.errors)
            self.had_errors = True
            return

        parser = Parser(tokens)
        stmts = parser.parse()

        if len(parser.errors) > 0:
            self.had_errors = True
            print_errors(parser.errors)
            return

        self.resolver.resolve_stmts(stmts)

        if len(self.resolver.errors) > 0:
            self.had_errors = True
            print_errors(self.resolver.errors)
            return

        self.interpreter.set_bindings(self.resolver.bindings)
        self.interpreter.interpret(stmts)

        if self.interpreter.has_error:
            print_errors(self.interpreter.errors)
            self.had_runtime_errors = True
            return

    def run_file(self, file: str):
        with open(file, "r", encoding="utf-8") as _file:
            self.run(_file.read())
            if self.had_errors:
                sys.exit(65)
            if self.had_runtime_errors:
                sys.exit(70)

    def start_repl(self):
        while True:
            line = input("> ")
            if line is None:
                break
            self.run(line)


def main(args: list[str]):
    arg_size = len(args)

    lox = Lox()

    if arg_size > 1:
        print("Usage: plox [script]")
        sys.exit(64)
    elif arg_size == 1:
        lox.run_file(args[0])
    else:
        lox.start_repl()


if __name__ == "__main__":
    main(sys.argv[1:])

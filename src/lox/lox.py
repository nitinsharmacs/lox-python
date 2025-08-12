import sys


def run(code: str):
    print(code)


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

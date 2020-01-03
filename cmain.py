#! /usr/local/bin/python3
import sys
import argparse

from logic import interpreter


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Python3.7 implementation Befunge-98 interpretator')
        self.parser.add_argument('program', type=str, help='program file')


if __name__ == '__main__':
    args = Parser().parser.parse_args()

    interpreter = interpreter.Interpreter()

    try:
        interpreter.init_interpreter(args.program)
    except FileNotFoundError:
        print("File is empty or doesn't exist", file=sys.stderr)
        sys.exit(1)

    interpreter.run()

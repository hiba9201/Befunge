#! /usr/local/bin/python3

import Interpreter
import sys


if __name__ == '__main__':
    interpreter = Interpreter.Interpreter()
    if len(sys.argv) < 2:
        print("Not enough arguments")
    interpreter.start(sys.argv[1])

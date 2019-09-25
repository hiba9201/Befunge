import Utils as u
import random


class Interpreter:
    STACK = []
    DIRECTIONS = {"^": (0, -1),
                  ">": (1, 0),
                  "<": (-1, 0),
                  "v": (0, 1)}
    TEXT_MODE = False

    def start(self, code_file):
        random.seed()
        program = u.Utils.lines_to_table(u.Utils.read_file(code_file))
        if not program:
            print("File is empty or doesn't exist")

        self.execute_program(program)

    def execute_program(self, program):
        current_direction = self.DIRECTIONS[">"]
        pos = (0, 0)
        while True:
            symb = program[pos[1]][pos[0]]

            if symb in self.DIRECTIONS.keys():
                current_direction = self.DIRECTIONS[symb]
            elif symb.isdigit():
                self.STACK.append(symb)
            elif symb == '"':
                self.TEXT_MODE = not self.TEXT_MODE
            elif self.TEXT_MODE:
                self.STACK.append(symb)
            elif symb == ",":
                print(str(self.STACK.pop()), end="")
            elif symb == ".":
                print(int(self.STACK.pop()), end="")
            elif symb == "?":
                current_direction = random.choice(list(self.DIRECTIONS.values()))
            elif symb == "|":
                direction = "v" if int(self.STACK.pop()) == 0 else "^"
                current_direction = self.DIRECTIONS[direction]
            elif symb == "@":
                print()
                break
            pos = (pos[0] + current_direction[0], pos[1] + current_direction[1])

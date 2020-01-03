import sys

import logic.utils as u
import logic.commands as cmds


class Interpreter:

    def __init__(self, inp=sys.stdin, out=sys.stdout):
        self.inp = inp
        self.out = out
        self.program = []
        self.stack_stack = [[]]
        self.stack = self.stack_stack[0]
        self.directions = {"^": (0, -1),
                           ">": (1, 0),
                           "v": (0, 1),
                           "<": (-1, 0)}
        self.text_mode = False
        self.nothing_mode = False
        self.input_mode = False
        self.ip = (0, 0)
        self.storage_offset = (0, 0)
        self.delta = self.directions[">"]
        self.finished = False
        self.iter_count = 1
        self.files = []
        self.imported_fps = []

    def init_interpreter(self, code_file):
        self.program = u.Utils.lines_to_table(u.Utils.read_file(code_file))

        if not self.program:
            return 1

        return 0

    def run(self):
        if not self.program:
            return 1
        while not self.finished:
            self.execute_one_step()

        return 0

    def execute_one_step(self):
        symb = self.program[self.ip[1]][self.ip[0]]

        if self.iter_count == 0:
            self.iter_count = 1
        elif symb == '"':
            self._change_text_mode()
        elif self.text_mode:
            self._push_char(symb)
        elif symb == ";":
            self._change_action_mode()
        elif self.nothing_mode:
            pass
        elif symb in self.directions.keys():
            self.delta = self.directions[symb]
        elif symb.isdigit() or (ord('a') <= ord(symb) <= ord('f')):
            self._push_digit(symb)
        else:
            for _ in range(self.iter_count):
                cmds.execute_command(self, symb)
            if symb != "k":
                self.iter_count = 1
        if self.input_mode:
            return

        self._go_1_step()

    def _change_text_mode(self):
        self.text_mode = not self.text_mode

    def _push_char(self, char):
        self.stack.append(ord(char))

    def _push_digit(self, digit):
        self.stack.append(int(digit, 16))

    def _change_action_mode(self):
        self.nothing_mode = not self.nothing_mode

    def _go_1_step(self):
        y = (self.ip[1] + self.delta[1]) % (len(self.program))
        self.ip = ((self.ip[0] + self.delta[0]) % (len(self.program[y])), y)

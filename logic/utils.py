import functools


class Utils:
    @staticmethod
    def read_file(path):
        try:
            with open(path) as file:
                return file.readlines()
        except OSError:
            return None

    @staticmethod
    def lines_to_table(lines):
        res = []
        if lines is None:
            return []

        max_len = Utils.get_max_len(lines)
        prepared_lines = map(lambda line: line.ljust(max_len), lines)
        for line in prepared_lines:
            prep_line = filter(lambda c: c != "\n", line)
            res.append(list(prep_line))

        return res

    @staticmethod
    def get_max_len(table):
        return max(map(len, table))

    @staticmethod
    def multiply_delta(inter, number):
        return inter.delta[0] * number, inter.delta[1] * number

    @staticmethod
    def pop_with_zero(inter):
        return 0 if len(inter.stack) == 0 else inter.stack.pop()

    @staticmethod
    def arithmetic(inter, action):
        b = Utils.pop_with_zero(inter)
        a = Utils.pop_with_zero(inter)
        action(b, a)

    @staticmethod
    def go_delta(inter, delta):
        y = (inter.ip[1] + delta[1]) % len(inter.program)
        inter.ip = ((inter.ip[0] + delta[0]) % len(inter.program[y]), y)

    @staticmethod
    def collect_string_from_stack(inter):
        res = ''
        current_symb = Utils.pop_with_zero(inter)
        while current_symb != 0:
            res += chr(current_symb)
            current_symb = Utils.pop_with_zero(inter)

        return res

    @staticmethod
    def write_string_to_stack(inter, string):
        inter.stack.append(0)
        for sym in string[::-1]:
            inter.stack.append(ord(sym))

    @staticmethod
    def write_file_to_program(inter, file, x, y):
        new_x = x
        for line in file:
            Utils.write_line_to_space(inter, line, x, y)
            new_x = len(line) if len(line) > new_x else new_x
            y += 1

        return new_x, y

    @staticmethod
    def get_line_from_space(inter, x, y, line_len):
        while len(inter.program) < y + 1:
            inter.program.append([' '] * len(inter.program[0]))

        return ''.join(inter.program[y][x:x + line_len]) + "\n"

    @staticmethod
    def write_line_to_space(inter, line, x, y, strip=True):
        while len(inter.program) < y + 1:
            inter.program.append([' '] * len(inter.program[0]))
        if len(inter.program[y]) < x:
            inter.program[y].extend([' '] *
                                    (x - len(inter.program[y]) + 1))

        if strip:
            line = line.rstrip('\n')
        inter.program[y][x:x + len(line)] = list(line)


class Registry:
    def __init__(self):
        self.commands = {}

    def command_decorator(self, cmd):
        def decorator(command_func):
            @functools.wraps(command_func)
            def wrapper(inter):
                return command_func(inter)

            self.commands[cmd] = wrapper

        return decorator

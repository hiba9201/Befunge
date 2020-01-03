import functools


def read_file(path):
    try:
        with open(path, encoding='utf-8') as file:
            return file.readlines()
    except OSError:
        return None


def lines_to_table(lines):
    res = []
    if lines is None:
        return res

    max_len = get_max_len(lines)
    prepared_lines = map(lambda line: line.ljust(max_len), lines)
    for line in prepared_lines:
        prep_line = filter(lambda c: c != "\n", line)
        res.append(list(prep_line))

    return res


def get_max_len(table):
    return max(map(len, table))


def multiply_delta(inter, number):
    return inter.delta[0] * number, inter.delta[1] * number


def pop_with_zero(inter):
    return 0 if len(inter.stack) == 0 else inter.stack.pop()


def arithmetic(inter, action):
    b = pop_with_zero(inter)
    a = pop_with_zero(inter)
    action(b, a)


def go_delta(inter, delta):
    y = (inter.ip[1] + delta[1]) % len(inter.program)
    inter.ip = ((inter.ip[0] + delta[0]) % len(inter.program[y]), y)


def collect_string_from_stack(inter):
    res = ''
    current_symb = pop_with_zero(inter)
    while current_symb != 0:
        res += chr(current_symb)
        current_symb = pop_with_zero(inter)

    return res


def write_string_to_stack(inter, string):
    inter.stack.append(0)
    for sym in string[::-1]:
        inter.stack.append(ord(sym))


def write_file_to_program(inter, file, x, y):
    new_x = x
    for line in file:
        write_line_to_space(inter, line, x, y)
        new_x = len(line) if len(line) > new_x else new_x
        y += 1

    return new_x, y


def get_line_from_space(inter, x, y, line_len):
    while len(inter.program) < y + 1:
        inter.program.append([' '] * len(inter.program[0]))

    return ''.join(inter.program[y][x:x + line_len]) + "\n"


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


class CustomIO:
    def __init__(self, inp, out):
        self.inp = inp
        self.out = out

    def get(self):
        return self.inp.read(1)

    def write(self, text):
        self.out.write(text)

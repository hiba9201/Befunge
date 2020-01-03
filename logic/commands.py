import os
import random
import sys
import importlib as il
import datetime as dt

import logic.utils as u

commands = u.Registry()


def execute_command(inter, command):
    if command not in commands.commands:
        if command != " ":
            commands.commands["r"](inter)
    else:
        commands.commands[command](inter)


random.seed()


# fingerprints import
@commands.command_decorator("(")
def load_fp(inter):
    count = u.pop_with_zero(inter)
    semantics_arr = []
    for i in range(count):
        semantics_arr.append(chr(u.pop_with_zero(inter)))

    semantics = ''.join(semantics_arr)

    project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               os.path.pardir)

    try:
        fp = il.import_module(f'fingerprints.{semantics}', project_dir)
        for letter in reversed(semantics):
            inter.stack.append(ord(letter))
        inter.stack.append(len(semantics))
    except ModuleNotFoundError:
        execute_command(inter, 'r')
        return

    commands.commands.update(fp.commands.commands)
    inter.imported_fps.append({'semantics': semantics,
                               'commands': list(fp.commands.commands.keys())})


@commands.command_decorator(")")
def unload_fp(inter):
    count = u.pop_with_zero(inter)
    semantics = ""
    for i in range(count):
        semantics += chr(u.pop_with_zero(inter))

    fp_to_unload = list(filter(lambda fp: fp['semantics'] == semantics,
                               inter.imported_fps))

    if not fp_to_unload:
        return

    unload_commands = fp_to_unload[0]['commands']
    del inter.imported_fps[inter.imported_fps.index(fp_to_unload[0])]

    for command in unload_commands:
        del commands.commands[command]

    if len(inter.imported_fps) > 0:
        last_semantics = inter.imported_fps[-1]['semantics']
        fprint = il.import_module(f'fingerprints.{last_semantics}',
                                  os.getcwd())
        commands.commands.update(fprint.commands.commands)


# turns
@commands.command_decorator("]")
def turn_right(inter):
    inter.delta = (inter.delta[0] * 0 + inter.delta[1] * (-1),
                   inter.delta[0] * 1 + inter.delta[1] * 0)


@commands.command_decorator("[")
def turn_left(inter):
    inter.delta = (inter.delta[0] * 0 + inter.delta[1] * 1,
                   inter.delta[0] * (-1) + inter.delta[1] * 0)


@commands.command_decorator("y")
def sys_info(inter):
    now = dt.datetime.now()
    current_date = (((now.year - 1900) * 256 * 256) + (now.month * 256) +
                    now.day)
    current_time = ((now.hour * 256 * 256) + (now.minute * 256) +
                    now.second)
    size_stack_stack = [len(stack) for stack in inter.stack_stack]
    sys_data = [len(inter.stack_stack), current_time, current_date,
                len(inter.program[-1]), len(inter.program),
                inter.storage_offset, inter.storage_offset,
                inter.delta[0], inter.delta[1], inter.ip[0],
                inter.ip[1], 0, 0, 2, ord(os.sep), 3, 1, 0,
                int((len(f'{sys.maxsize:b}') + 1) / 8), int('01110', 2)]
    environ = [f'{key}={value}' for (key, value) in os.environ.items()]

    num = u.pop_with_zero(inter)
    count = (len(size_stack_stack) + len(sys_data) + len(environ) +
             len(sys.argv[1:]))
    for var in environ:
        u.write_string_to_stack(inter, var)

    for arg in sys.argv[:1]:
        u.write_string_to_stack(inter, arg)

    for size in size_stack_stack:
        inter.stack.append(size)

    for data in sys_data:
        inter.stack.append(data)

    if num > 0:
        chosen_cell = inter.stack[-num]
        for i in range(count):
            u.pop_with_zero(inter)
        inter.stack.append(chosen_cell)


@commands.command_decorator("w")
def compare_dir(inter):
    b = u.pop_with_zero(inter)
    a = u.pop_with_zero(inter)
    if a < b:
        execute_command(inter, "[")
    elif a > b:
        execute_command(inter, "]")


@commands.command_decorator("'")
def push_next_char(inter):
    execute_command(inter, "#")
    inter.stack.append(ord(inter.program[inter.ip[1]][inter.ip[0]]))


@commands.command_decorator("$")
def pop(inter):
    u.pop_with_zero(inter)


@commands.command_decorator("x")
def absolute_vector(inter):
    dy = u.pop_with_zero(inter)
    dx = u.pop_with_zero(inter)
    inter.ip = (dx, dy)


@commands.command_decorator("#")
def go_1_step(inter):
    u.go_delta(inter, inter.delta)


@commands.command_decorator(",")
def print_char(inter):
    inter.io.write(chr(u.pop_with_zero(inter)))


@commands.command_decorator(".")
def print_digit(inter):
    inter.io.write(str(u.pop_with_zero(inter)))


@commands.command_decorator("=")
def execute(inter):
    inter.stack.append(os.system(u.collect_string_from_stack(inter)))


@commands.command_decorator("?")
def change_direction_random(inter):
    inter.delta = random.choice(list(inter.directions.values()))


@commands.command_decorator("|")
def vertical_direction_change(inter):
    direction = "v" if u.pop_with_zero(inter) == 0 else "^"
    inter.delta = inter.directions[direction]


@commands.command_decorator("_")
def horizontal_direction_change(inter):
    direction = ">" if u.pop_with_zero(inter) == 0 else "<"
    inter.delta = inter.directions[direction]


@commands.command_decorator(":")
def double_stack_value(inter):
    a = u.pop_with_zero(inter)
    inter.stack.append(a)
    inter.stack.append(a)


@commands.command_decorator("\\")
def switch_stack_values(inter):
    b = u.pop_with_zero(inter)
    a = u.pop_with_zero(inter)
    inter.stack.append(b)
    inter.stack.append(a)


@commands.command_decorator("%")
def mod(inter):
    u.arithmetic(inter, lambda b, a: inter.stack.append(0) if b == 0 else
                 inter.stack.append(a % b))


@commands.command_decorator("/")
def divide(inter):
    u.arithmetic(inter, lambda b, a: inter.stack.append(0) if b == 0 else
                 inter.stack.append(a / b))


@commands.command_decorator("!")
def negotiate(inter):
    a = 1 if u.pop_with_zero(inter) == 0 else 0
    inter.stack.append(a)


@commands.command_decorator("&")
def read_digit(inter):
    if not inter.input_mode:
        inter.input_mode = True
        return
    res = ''
    read = inter.io.get()
    while read and not read.isdigit():
        read = inter.io.get()
    while read and read.isdigit():
        res += read
        read = inter.io.get()

    if not res:
        return

    inter.stack.append(int(res))
    inter.input_mode = False


@commands.command_decorator("~")
def read_symb(inter):
    if not inter.input_mode:
        inter.input_mode = True
        return
    inter.input_mode = False
    symb = inter.io.get()
    if symb:
        inter.stack.append(ord(symb))
    else:
        inter.stack.append(-1)


# arithmetic
@commands.command_decorator("*")
def multiply(inter):
    u.arithmetic(inter, lambda s, f: inter.stack.append(s * f))


@commands.command_decorator("+")
def sum_cmd(inter):
    u.arithmetic(inter, lambda s, f: inter.stack.append(s + f))


@commands.command_decorator("-")
def subtract(inter):
    u.arithmetic(inter, lambda s, f: inter.stack.append(f - s))


@commands.command_decorator("`")
def compare(inter):
    u.arithmetic(inter, lambda s, f:
                 inter.stack.append(1 if f > s else 0))


# funge space operations
@commands.command_decorator("g")
def get(inter):
    try:
        y = u.pop_with_zero(inter)
        x = u.pop_with_zero(inter)
        get_c = ord(inter.program[y][x])
    except IndexError:
        get_c = 0
    inter.stack.append(get_c)


@commands.command_decorator("p")
def put(inter):
    y = u.pop_with_zero(inter)
    x = u.pop_with_zero(inter)
    n = u.pop_with_zero(inter)
    while len(inter.program) < y + 1:
        inter.program.append([" "] * len(inter.program[0]))
    if len(inter.program[y]) < x + 1:
        inter.program[y][len(inter.program[y]):x + 1] = ([" "] *
                                                         (x + 1 -
                                                          len(inter.program[y])
                                                          ))
    inter.program[y][x] = chr(n)


@commands.command_decorator("s")
def store(inter):
    n = u.pop_with_zero(inter)
    execute_command(inter, "#")
    inter.program[inter.ip[1]][inter.ip[0]] = chr(n)


@commands.command_decorator("n")
def clear(inter):
    while len(inter.stack):
        inter.stack.pop()


@commands.command_decorator("r")
def reflect(inter):
    inter.delta = u.multiply_delta(inter, -1)


# file input/output
@commands.command_decorator("i")
def input_file(inter):
    filename = u.collect_string_from_stack(inter)
    y = u.pop_with_zero(inter)
    x = u.pop_with_zero(inter)
    try:
        with open(filename, "r") as f:
            last_x, last_y = u.write_file_to_program(inter, f, x, y)
            inter.stack.append(last_x)
            inter.stack.append(last_y)

    except OSError:
        execute_command(inter, "r")


@commands.command_decorator("o")
def output_file(inter):
    filename = u.collect_string_from_stack(inter)
    f_y = u.pop_with_zero(inter)
    f_x = u.pop_with_zero(inter)

    s_y = u.pop_with_zero(inter)
    s_x = u.pop_with_zero(inter)

    lines_len = s_x - f_x

    try:
        with open(filename, "w") as f:
            for y in range(f_y, s_y + 1):
                f.write(u.get_line_from_space(inter, f_x, y,
                                              lines_len))
    except OSError:
        execute_command(inter, "r")


@commands.command_decorator("j")
def jump(inter):
    a = u.pop_with_zero(inter)
    u.go_delta(inter, u.multiply_delta(inter, a))


# program terminating
@commands.command_decorator("q")
def quit_program(inter):
    execute_command(inter, ".")
    inter.finished = True


@commands.command_decorator("@")
def finish(inter):
    inter.finished = True


@commands.command_decorator("k")
def iterate(inter):
    inter.iter_count = u.pop_with_zero(inter)


# stack stack operations
@commands.command_decorator("{")
def start_block(inter):
    n = int(u.pop_with_zero(inter))
    if n <= 0:
        inter.stack_stack.append([] * (-n))
    else:
        new_stack = [0] * (n - len(inter.stack) + 1)
        new_stack[-1:] = inter.stack[-min(n, len(inter.stack)):]
        inter.stack_stack.append(new_stack)
    inter.stack.append(inter.storage_offset[0])
    inter.stack.append(inter.storage_offset[1])

    inter.stack = inter.stack_stack[-1]
    inter.storage_offset = (
        (inter.ip[0] + inter.delta[0]) % len(inter.program[0]),
        (inter.ip[1] + inter.delta[1]) % len(inter.program))


@commands.command_decorator("}")
def end_block(inter):
    if len(inter.stack_stack) == 1:
        execute_command(inter, "r")
        return
    n = int(u.pop_with_zero(inter))
    toss = inter.stack_stack.pop()

    inter.stack = inter.stack_stack[-1]

    y = u.pop_with_zero(inter)
    x = u.pop_with_zero(inter)

    inter.storage_offset = (x, y)

    if n <= 0:
        for _ in range(min(-n, len(inter.stack))):
            inter.stack.pop()
    else:
        new_stack = [0] * (n - len(toss) + 1)
        new_stack[-1:] = toss[-min(n, len(toss)):]
        inter.stack[len(inter.stack):] = new_stack

    inter.stack = inter.stack_stack[-1]


@commands.command_decorator("u")
def stack_under_stack(inter):
    if len(inter.stack_stack) == 1:
        execute_command(inter, "r")
        return

    count = u.pop_with_zero(inter)
    if count > 0:
        for _ in range(count):
            item = 0 if len(inter.stack_stack[-2]
                            ) == 0 else inter.stack_stack[-2].pop()
            inter.stack.append(item)
    else:
        for _ in range(-count):
            item = u.pop_with_zero(inter)
            inter.stack_stack[-2].append(item)

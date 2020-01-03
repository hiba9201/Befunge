import logic.utils as u


commands = u.Registry()


@commands.command_decorator("A")
def append(inter):
    a = u.collect_string_from_stack(inter)
    b = u.collect_string_from_stack(inter)
    u.write_string_to_stack(inter, b + a)


@commands.command_decorator("C")
def compare(inter):
    a = u.collect_string_from_stack(inter)
    b = u.collect_string_from_stack(inter)
    inter.stack.append(int(a == b))


@commands.command_decorator("D")
def display(inter):
    a = u.collect_string_from_stack(inter)
    inter.io.write(a)


@commands.command_decorator("P")
def put_to_pos(inter):
    y = u.pop_with_zero(inter)
    x = u.pop_with_zero(inter)
    string = u.collect_string_from_stack(inter)

    while len(inter.program) <= y:
        inter.program.append([' '] * u.get_max_len(inter.program))

    for letter in string:
        inter.program[y][x] = letter
        x += 1
    inter.program[y][x] = '0'


@commands.command_decorator("G")
def get_from_pos(inter):
    y = u.pop_with_zero(inter)
    x = u.pop_with_zero(inter)
    res = []
    cur_char = ''
    while cur_char != '0':
        res.append(cur_char)
        cur_char = inter.program[y][x]
        x += 1
    u.write_string_to_stack(inter, ''.join(res))


@commands.command_decorator("I")
def input_str(inter):
    if not inter.input_mode:
        inter.input_mode = True
        return
    inter.input_mode = False
    res = []
    cur_char = inter.io.get()
    while cur_char and cur_char != '\n':
        res.append(cur_char)
        cur_char = inter.io.get()
    u.write_string_to_stack(inter, ''.join(res))


@commands.command_decorator("L")
def left(inter):
    count = u.pop_with_zero(inter)
    string = u.collect_string_from_stack(inter)

    u.write_string_to_stack(inter, string[:count])


@commands.command_decorator("R")
def right(inter):
    count = u.pop_with_zero(inter)
    string = u.collect_string_from_stack(inter)

    u.write_string_to_stack(inter, string[-count:])


@commands.command_decorator("M")
def substr(inter):
    count = u.pop_with_zero(inter)
    start = u.pop_with_zero(inter)
    string = u.collect_string_from_stack(inter)

    u.write_string_to_stack(inter, string[start:start + count])


@commands.command_decorator("N")
def length(inter):
    string = u.collect_string_from_stack(inter)
    u.write_string_to_stack(inter, string)
    inter.stack.append(len(string))


@commands.command_decorator("S")
def num_to_str(inter):
    num = u.pop_with_zero(inter)
    u.write_string_to_stack(inter, str(num))


@commands.command_decorator("V")
def num_to_str(inter):
    string = u.collect_string_from_stack(inter)
    inter.stack.append(int(string))

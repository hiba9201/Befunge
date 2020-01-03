import enum
import os

import logic.utils as u


open_file_mode = ['r', 'w', 'a', '+', 'w+', 'r+']

commands = u.Registry()


@commands.command_decorator("D")
def delete_file(inter):
    filename = u.collect_string_from_stack(inter)
    try:
        os.remove(filename)
    except OSError:
        inter.delta = u.multiply_delta(inter, -1)


@commands.command_decorator("O")
def open_file(inter):
    filename = u.collect_string_from_stack(inter)
    m = u.pop_with_zero(inter)
    y = u.pop_with_zero(inter)
    x = u.pop_with_zero(inter)

    try:
        mode = open_file_mode[m]
    except IndexError:
        inter.delta = u.multiply_delta(inter, -1)
        return

    try:
        opened_file = open(filename, mode, encoding='utf-8')
        inter.files.append({'file': opened_file,
                            'buffer_start': [x, y],
                            'buffer_end': x})
        inter.stack.append(len(inter.files) - 1)
    except OSError:
        inter.delta = u.multiply_delta(inter, -1)


@commands.command_decorator("C")
def close_file(inter):
    file_num = u.pop_with_zero(inter)
    if not (len(inter.files) > file_num >= 0):
        inter.delta = u.multiply_delta(inter, -1)
        return

    file = inter.files.pop(file_num)
    file['file'].close()


@commands.command_decorator("S")
def seek_file(inter):
    pos = u.pop_with_zero(inter)
    m = u.pop_with_zero(inter)
    file_num = u.pop_with_zero(inter)

    try:
        inter.files[file_num]['file'].seek(pos, m)
        inter.stack.append(file_num)
    except Exception:
        inter.delta = u.multiply_delta(inter, -1)


@commands.command_decorator("L")
def get_location(inter):
    file_num = u.pop_with_zero(inter)

    try:
        pos = inter.files[file_num]['file'].tell()
        inter.stack.append(file_num)
        inter.stack.append(pos)
    except Exception:
        inter.delta = u.multiply_delta(inter, -1)


@commands.command_decorator("G")
def read_line(inter):
    file_num = u.pop_with_zero(inter)

    try:
        line = inter.files[file_num]['file'].readline()
        inter.stack.append(file_num)
        u.write_string_to_stack(inter, line)
    except Exception:
        inter.delta = u.multiply_delta(inter, -1)


@commands.command_decorator("P")
def print_line(inter):
    file_num = u.pop_with_zero(inter)
    line = u.collect_string_from_stack(inter)

    try:
        inter.files[file_num]['file'].write(f'{line}\n')
        inter.stack.append(file_num)
    except Exception:
        inter.delta = u.multiply_delta(inter, -1)


@commands.command_decorator("R")
def read_file(inter):
    count = u.pop_with_zero(inter)
    file_num = u.pop_with_zero(inter)

    try:
        string = inter.files[file_num]['file'].read(count)
        _, y = inter.files[file_num]['buffer_start']
        x = inter.files[file_num]['buffer_end']
        u.write_line_to_space(inter, string, x, y, strip=False)
        inter.files[file_num]['buffer_end'] = len(string)
        inter.stack.append(file_num)
        for line in inter.program:
            print(''.join(line))
    except Exception:
        inter.delta = u.multiply_delta(inter, -1)


@commands.command_decorator("W")
def write_file(inter):
    count = u.pop_with_zero(inter)
    file_num = u.pop_with_zero(inter)

    if file_num >= len(inter.files) or file_num < 0:
        inter.delta = u.multiply_delta(inter, -1)
        return

    x, y = inter.files[file_num]['buffer_start']
    line_len = max(count, inter.files[file_num]['buffer_end'] - x)

    string = u.get_line_from_space(inter, x, y, line_len)
    try:
        inter.files[file_num]['file'].write(string)
        inter.files[file_num]['buffer_start'][0] = x + line_len
    except Exception:
        u.write_line_to_space(inter, string, x, y)
        inter.delta = u.multiply_delta(inter, -1)

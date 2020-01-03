import string

import logic.utils as u

commands = u.Registry()


@commands.command_decorator("H")
def to_hex(inter):
    inter.io.write('{0:x}'.format(u.pop_with_zero(inter)))


@commands.command_decorator("B")
def to_bin(inter):
    inter.io.write('{0:b}'.format(u.pop_with_zero(inter)))


@commands.command_decorator("O")
def to_octal(inter):
    inter.io.write('{0:o}'.format(u.pop_with_zero(inter)))


@commands.command_decorator("N")
def to_base(inter):
    num = u.pop_with_zero(inter)
    base = u.pop_with_zero(inter)
    inter.io.write(to_base_n(num, base))


@commands.command_decorator("I")
def from_base(inter):
    if not inter.input_mode:
        inter.input_mode = True
        return
    inter.input_mode = False
    base = u.pop_with_zero(inter)

    num = ''
    read = inter.io.get()
    while not read.isdigit():
        read = inter.io.get()
    while read.isdigit():
        num += read
        read = inter.io.get()

    res = int(to_base_n(int(num), base))
    inter.stack.append(res)


numerals = string.digits + string.ascii_lowercase


def to_base_n(num, b):
    return ((num == 0) and numerals[0]) or (
                to_base_n(num // b, b).lstrip(numerals[0]) +
                numerals[num % b])

import string

import logic.utils as u

commands = u.Registry()


@commands.command_decorator("H")
def to_hex(inter):
    inter.out.write('{0:x}'.format(u.Utils.pop_with_zero(inter)))
    inter.out.flush()


@commands.command_decorator("B")
def to_bin(inter):
    inter.out.write('{0:b}'.format(u.Utils.pop_with_zero(inter)))
    inter.out.flush()


@commands.command_decorator("O")
def to_octal(inter):
    inter.out.write('{0:o}'.format(u.Utils.pop_with_zero(inter)))
    inter.out.flush()


@commands.command_decorator("N")
def to_base(inter):
    num = u.Utils.pop_with_zero(inter)
    base = u.Utils.pop_with_zero(inter)
    inter.out.write(to_base_n(num, base))
    inter.out.flush()


@commands.command_decorator("I")
def from_base(inter):
    if not inter.input_mode:
        inter.input_mode = True
        return
    inter.input_mode = False
    base = u.Utils.pop_with_zero(inter)

    num = ''
    read = inter.inp.read(1)
    while not read.isdigit():
        read = inter.inp.read(1)
    while read.isdigit():
        num += read
        read = inter.inp.read(1)

    res = int(to_base_n(int(num), base))
    inter.stack.append(res)


numerals = string.digits + string.ascii_lowercase


def to_base_n(num, b):
    return ((num == 0) and numerals[0]) or (
                to_base_n(num // b, b).lstrip(numerals[0]) +
                numerals[num % b])

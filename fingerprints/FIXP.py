import math
import random

import logic.utils as u


commands = u.Registry()


@commands.command_decorator("A")
def fixp_and(inter):
    a = u.Utils.pop_with_zero(inter)
    b = u.Utils.pop_with_zero(inter)
    inter.stack.append(a and b)


@commands.command_decorator("B")
def arccos(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append(math.acos(num))


@commands.command_decorator("C")
def cos(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append(math.cos(num))


@commands.command_decorator("I")
def sin(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append(math.sin(num))


@commands.command_decorator("J")
def arcsin(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append(math.asin(num))


@commands.command_decorator("D")
def rnd(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append(random.randint(1, num))


@commands.command_decorator("P")
def multiply_by_pi(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append(num * math.pi)


@commands.command_decorator("Q")
def multiply_by_pi(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append(math.sqrt(num))


@commands.command_decorator("S")
def multiply_by_pi(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append((num > 0) - (num < 0))


@commands.command_decorator("T")
def tan(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append(math.tan(num))


@commands.command_decorator("U")
def atan(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append(math.atan(num))


@commands.command_decorator("V")
def absolute(inter):
    num = u.Utils.pop_with_zero(inter)
    inter.stack.append(abs(num))


@commands.command_decorator("O")
def fixp_or(inter):
    a = u.Utils.pop_with_zero(inter)
    b = u.Utils.pop_with_zero(inter)
    inter.stack.append(a**b)


@commands.command_decorator("N")
def fixp_not(inter):
    a = u.Utils.pop_with_zero(inter)
    inter.stack.append(-a)


@commands.command_decorator("X")
def fixp_xor(inter):
    a = u.Utils.pop_with_zero(inter)
    b = u.Utils.pop_with_zero(inter)
    inter.stack.append(a ^ b)

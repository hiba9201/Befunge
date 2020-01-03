import logic.utils as u


commands = u.Registry()


@commands.command_decorator("A")
def funge_and(inter):
    a = u.pop_with_zero(inter)
    b = u.pop_with_zero(inter)
    inter.stack.append(int(bool(a and b)))


@commands.command_decorator("O")
def funge_or(inter):
    a = u.pop_with_zero(inter)
    b = u.pop_with_zero(inter)
    inter.stack.append(int(bool(a or b)))


@commands.command_decorator("N")
def funge_not(inter):
    a = u.pop_with_zero(inter)
    inter.stack.append(int(not a))


@commands.command_decorator("X")
def funge_xor(inter):
    a = u.pop_with_zero(inter)
    b = u.pop_with_zero(inter)
    inter.stack.append(int(bool(a) ^ bool(b)))

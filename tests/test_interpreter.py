import os
import sys
import unittest
import io

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import logic.interpreter as intr
import logic.commands as cmds
import logic.utils as u


class CommandsTests(unittest.TestCase):
    # creating interpreter for each test
    def setUp(self):
        self.inp = io.StringIO()
        self.out = io.StringIO()
        self.inter = intr.Interpreter(u.CustomIO(self.inp, self.out))
        self.inter.init_interpreter("./tests/test_code.f98")

    # testing Interpreter class commands
    def test_text_mode_switch(self):
        self.inter._change_text_mode()
        self.assertTrue(self.inter.text_mode)
        self.inter._change_text_mode()
        self.assertFalse(self.inter.text_mode)

    def test_nothing_mode_switch(self):
        self.inter._change_action_mode()
        self.assertTrue(self.inter.nothing_mode)
        self.inter._change_action_mode()
        self.assertFalse(self.inter.text_mode)

    def test_push_char(self):
        self.inter._push_char("0")
        self.assertEqual([ord("0")], self.inter.stack)

    def test_push_decimal_digit(self):
        self.inter._push_digit("2")
        self.assertEqual([2], self.inter.stack)

    def test_push_hex_digit(self):
        self.inter._push_digit("f")
        self.assertEqual([15], self.inter.stack)

    def test_one_step(self):
        self.inter._go_1_step()
        self.assertEqual((1, 0), self.inter.ip)

    def test_one_step_down(self):
        self.inter.delta = self.inter.directions["v"]
        self.inter._go_1_step()
        self.assertEqual((0, 1), self.inter.ip)

    def test_go_out_of_space(self):
        self.inter.delta = self.inter.directions["<"]
        self.inter._go_1_step()
        self.assertEqual((8, 0), self.inter.ip)

    def test_program_execution(self):
        self.inter.run()
        self.assertEqual(self.inter.stack, [ord("h"), ord("e"), ord("y")])

    def test_start_on_non_existing_file(self):
        # wrong file so not using set up interpreter
        inter = intr.Interpreter()

        self.assertRaises(FileNotFoundError,
                          inter.init_interpreter, "tests/not_test_code.f98")

    # testing Commands class commands
    def test_turn(self):
        cmds.execute_command(self.inter, "]")
        self.assertEqual(self.inter.directions["v"], self.inter.delta)
        cmds.execute_command(self.inter, "[")
        self.assertEqual(self.inter.directions[">"], self.inter.delta)

    def test_compare_left(self):
        self.inter._push_digit("2")
        self.inter._push_digit("3")
        cmds.execute_command(self.inter, "w")
        self.assertEqual(self.inter.directions["^"], self.inter.delta)

    def test_compare_right(self):
        self.inter._push_digit("4")
        self.inter._push_digit("3")
        cmds.execute_command(self.inter, "w")
        self.assertEqual(self.inter.directions["v"], self.inter.delta)

    def test_compare_equal(self):
        self.inter._push_digit("2")
        self.inter._push_digit("2")
        cmds.execute_command(self.inter, "w")
        self.assertEqual(self.inter.directions[">"], self.inter.delta)

    def test_one_char_push(self):
        cmds.execute_command(self.inter, "'")
        self.assertEqual(ord("h"), self.inter.stack.pop())

    def test_pop(self):
        self.inter._push_digit("3")
        self.assertEqual(3, u.pop_with_zero(self.inter))
        self.inter._push_digit("3")
        cmds.execute_command(self.inter, "$")
        self.assertEqual(0, len(self.inter.stack))

    def test_pop_empty_stack(self):
        self.assertEqual(0, u.pop_with_zero(self.inter))

    def test_absolute_vector(self):
        self.inter._push_digit("2")
        self.inter._push_digit("2")
        cmds.execute_command(self.inter, "x")
        self.assertEqual((2, 2), self.inter.ip)

    def test_skip_cell(self):
        cmds.execute_command(self.inter, "#")
        self.assertEqual((1, 0), self.inter.ip)

    def test_print_char(self):
        self.inter._push_char("c")
        cmds.execute_command(self.inter, ",")
        self.assertEqual("c", self.out.getvalue())

    def test_print_digit(self):
        self.inter._push_digit("2")
        cmds.execute_command(self.inter, ".")
        self.assertEqual("2", self.out.getvalue())

    def test_execute(self):
        u.write_string_to_stack(self.inter, 'echo "hi"')
        cmds.execute_command(self.inter, "=")
        self.assertEqual(0, self.inter.stack.pop())

    def test_execute_failure(self):
        u.write_string_to_stack(self.inter, 'eco')
        cmds.execute_command(self.inter, "=")
        self.assertNotEqual(0, u.pop_with_zero(self.inter))

    def test_vertical_dir_change(self):
        cmds.execute_command(self.inter, "|")
        self.assertEqual(self.inter.directions["v"], self.inter.delta)
        self.inter._push_digit("1")
        cmds.execute_command(self.inter, "|")
        self.assertEqual(self.inter.directions["^"], self.inter.delta)

    def test_horizontal_dir_change(self):
        cmds.execute_command(self.inter, "_")
        self.assertEqual(self.inter.directions[">"], self.inter.delta)
        self.inter._push_digit("1")
        cmds.execute_command(self.inter, "_")
        self.assertEqual(self.inter.directions["<"], self.inter.delta)

    def test_double_stack_value(self):
        self.inter._push_digit("2")
        cmds.execute_command(self.inter, ":")
        self.assertEqual(2, len(self.inter.stack))
        self.assertEqual(2, self.inter.stack[-1])
        self.assertEqual(self.inter.stack[-1], self.inter.stack[-2])

    def test_swap_stack(self):
        self.inter._push_digit("2")
        self.inter._push_digit("3")
        cmds.execute_command(self.inter, "\\")
        self.assertEqual(2, self.inter.stack.pop())
        self.assertEqual(3, self.inter.stack.pop())

    def test_arithmetic_mod(self):
        self.inter._push_digit("2")
        self.inter._push_digit("3")
        cmds.execute_command(self.inter, "%")
        self.assertEqual(2, self.inter.stack.pop())

    def test_arithmetic_mod_by_zero(self):
        self.inter._push_digit("2")
        self.inter._push_digit("0")
        cmds.execute_command(self.inter, "%")
        self.assertEqual(0, self.inter.stack.pop())

    def test_arithmetic_div(self):
        self.inter._push_digit("2")
        self.inter._push_digit("3")
        cmds.execute_command(self.inter, "/")
        self.assertEqual(2 / 3, self.inter.stack.pop())

    def test_arithmetic_div_by_zero(self):
        self.inter._push_digit("2")
        self.inter._push_digit("0")
        cmds.execute_command(self.inter, "/")
        self.assertEqual(0, self.inter.stack.pop())

    def test_arithmetic_sum(self):
        self.inter._push_digit("2")
        self.inter._push_digit("3")
        cmds.execute_command(self.inter, "+")
        self.assertEqual(5, self.inter.stack.pop())

    def test_arithmetic_multiply(self):
        self.inter._push_digit("2")
        self.inter._push_digit("3")
        cmds.execute_command(self.inter, "*")
        self.assertEqual(6, self.inter.stack.pop())

    def test_arithmetic_subtract(self):
        self.inter._push_digit("2")
        self.inter._push_digit("3")
        cmds.execute_command(self.inter, "-")
        self.assertEqual(-1, self.inter.stack.pop())

    def test_negotiation(self):
        cmds.execute_command(self.inter, "!")
        self.assertEqual(1, self.inter.stack[-1])
        cmds.execute_command(self.inter, "!")
        self.assertEqual(0, self.inter.stack[-1])

    def test_read_digit(self):
        self.inp.write("lkasmd11212llll")
        self.inp.seek(0)
        cmds.execute_command(self.inter, "&")
        cmds.execute_command(self.inter, "&")
        self.assertEqual(11212, self.inter.stack.pop())

    def test_read_symb(self):
        self.inp.write("k")
        self.inp.seek(0)
        cmds.execute_command(self.inter, "~")
        cmds.execute_command(self.inter, "~")
        self.assertEqual(ord('k'), u.pop_with_zero(self.inter))

    def test_load_unload_fp(self):
        u.write_string_to_stack(self.inter, 'STRN')
        self.inter.stack.append(4)
        cmds.execute_command(self.inter, '(')
        self.assertEqual('STRN', self.inter.imported_fps[0]['semantics'])
        self.assertIn('A', cmds.commands.commands)
        self.assertIn('C', cmds.commands.commands)
        self.assertIn('D', cmds.commands.commands)
        self.assertIn('P', cmds.commands.commands)
        cmds.execute_command(self.inter, ')')
        self.assertEqual(len(self.inter.imported_fps), 0)
        self.assertNotIn('A', cmds.commands.commands)
        self.assertNotIn('C', cmds.commands.commands)
        self.assertNotIn('D', cmds.commands.commands)
        self.assertNotIn('P', cmds.commands.commands)

    def test_get(self):
        self.inter.stack.append(1)
        self.inter.stack.append(0)
        cmds.execute_command(self.inter, 'g')
        self.assertEqual(u.pop_with_zero(self.inter), ord('h'))

    def test_put(self):
        self.inter.stack.append(ord('a'))
        self.inter.stack.append(1)
        self.inter.stack.append(0)
        cmds.execute_command(self.inter, 'p')
        self.assertEqual(self.inter.program[0][1], 'a')

    def test_put_out_of_range(self):
        self.inter.stack.append(ord('a'))
        self.inter.stack.append(0)
        self.inter.stack.append(1)
        cmds.execute_command(self.inter, 'p')
        self.assertEqual(self.inter.program[1][0], 'a')

    def test_store(self):
        self.inter.stack.append(ord('a'))
        cmds.execute_command(self.inter, 's')
        self.assertEqual(self.inter.program[0][1], 'a')

    def test_clear_stack(self):
        self.inter.stack.append(ord('a'))
        self.inter.stack.append(0)
        self.inter.stack.append(1)
        self.assertEqual(len(self.inter.stack), 3)
        cmds.execute_command(self.inter, 'n')
        self.assertEqual(len(self.inter.stack), 0)

    def test_reflect_horizontal(self):
        self.assertEqual(self.inter.delta, (1, 0))
        cmds.execute_command(self.inter, 'r')
        self.assertEqual(self.inter.delta, (-1, 0))

    def test_reflect_vertical(self):
        self.inter.delta = (0, 1)
        cmds.execute_command(self.inter, 'r')
        self.assertEqual(self.inter.delta, (0, -1))

    def test_jump(self):
        self.inter.stack.append(3)
        cmds.execute_command(self.inter, 'j')
        self.assertEqual(self.inter.ip, (3, 0))

    def test_iterate(self):
        self.inter.stack.append(0)
        self.inter.stack.append(1)
        cmds.execute_command(self.inter, 'x')
        self.inter.run()
        self.assertEqual('hhh', self.out.getvalue())

    def test_block_start(self):
        self.inter.stack.append(2)
        self.inter.stack.append(1)
        self.assertEqual(len(self.inter.stack_stack), 1)
        cmds.execute_command(self.inter, '{')
        self.assertEqual(len(self.inter.stack_stack), 2)
        self.assertEqual(len(self.inter.stack), 1)

    def test_block_end(self):
        self.inter.stack.append(2)
        self.inter.stack.append(1)
        cmds.execute_command(self.inter, '{')
        self.inter.stack.append(1)
        cmds.execute_command(self.inter, '}')
        self.assertEqual(len(self.inter.stack_stack), 1)
        self.assertEqual(len(self.inter.stack), 2)

    def test_under_stack(self):
        self.inter.stack.append(2)
        self.inter.stack.append(1)
        cmds.execute_command(self.inter, '{')
        self.inter.stack.append(1)
        cmds.execute_command(self.inter, 'u')
        self.assertEqual(self.inter.stack, [2, 0])


class UtilsTests(unittest.TestCase):
    def test_lines_to_table(self):
        table = u.lines_to_table(['hey', 'hi'])
        self.assertEqual([['h', 'e', 'y'], ['h', 'i', ' ']], table)

    def test_get_line_from_space(self):
        self.inter = intr.Interpreter()
        self.inter.init_interpreter("./tests/test_code.f98")
        x = 0
        y = 2
        line_len = 6
        string = u.get_line_from_space(self.inter, x, y, line_len)
        self.assertEqual('string\n', string)


if __name__ == '__main__':
    unittest.main()

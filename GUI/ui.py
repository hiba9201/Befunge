import io

import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui
import PyQt5.QtCore as core

from logic import interpreter
from logic import utils


class Window(widgets.QWidget):
    def __init__(self, args):
        super().__init__()

        self._args = args
        self._running = False
        self._start_ui()

    def _start_ui(self):
        self._running = False
        commands_layout = widgets.QHBoxLayout()

        self._run_btn = Window.create_cmd_button('Запуск')
        run = widgets.QAction(self)
        run.setShortcut('F5')
        run.triggered.connect(self.run_program)
        self._run_btn.addAction(run)
        self._run_btn.clicked.connect(self.run_program)

        self._step_btn = Window.create_cmd_button('Шаг')
        step = widgets.QAction(self)
        step.setShortcut('Space')
        step.triggered.connect(self.make_step)
        self._step_btn.addAction(step)
        self._step_btn.clicked.connect(self.make_step)

        self._restart_btn = Window.create_cmd_button('Перезапустить')
        restart = widgets.QAction(self)
        restart.setShortcut('F9')
        restart.triggered.connect(self._create_interpreter)
        self._restart_btn.addAction(restart)
        self._restart_btn.clicked.connect(self._create_interpreter)

        commands_layout.addWidget(self._run_btn)
        commands_layout.addWidget(self._step_btn)
        commands_layout.addWidget(self._restart_btn)
        commands_layout.setAlignment(core.Qt.AlignLeft)

        commands_group = widgets.QGroupBox()
        commands_group.setLayout(commands_layout)
        commands_group.setMaximumHeight(40)
        commands_layout.setSpacing(20)
        commands_layout.setContentsMargins(0, 0, 0, 0)

        inp_label = widgets.QLabel('Поле ввода:')
        inp_label.setFont(gui.QFont('Mono', 20))

        inp_label.show()

        self._inp = widgets.QPlainTextEdit('', self)
        self._inp.setAutoFillBackground(True)
        self._inp.setMinimumHeight(90)
        self._inp.setFont(gui.QFont('Courier', 14))

        self._inp.show()

        self._input_button = widgets.QPushButton('Ввести')
        self._input_button.setFont(gui.QFont('Mono', 16))
        self._input_button.setStyleSheet('''background-color: #fff; 
                                            margin-top: 10px;''')
        self._input_button.clicked.connect(self.input_cmd)

        self._input_button.setFixedHeight(40)
        self._input_button.setFixedWidth(150)

        self._input_button.show()

        input_group = widgets.QGroupBox()

        input_layout = widgets.QVBoxLayout()
        input_layout.addWidget(inp_label)
        input_layout.addWidget(self._inp)
        input_layout.addWidget(self._input_button)
        input_layout.setAlignment(self._input_button, core.Qt.AlignRight)

        input_layout.setSpacing(5)
        input_layout.setContentsMargins(0, 0, 0, 0)

        input_group.setMaximumHeight(250)
        input_group.setMaximumWidth(400)
        input_group.setLayout(input_layout)

        out_label = widgets.QLabel('Поле вывода:')
        out_label.setFont(gui.QFont('Mono', 20))

        out_label.show()

        self._out = widgets.QPlainTextEdit('', self)
        self._out.setReadOnly(True)
        self._out.setMinimumHeight(100)
        self._out.setFont(gui.QFont('Courier', 14))
        self._out.setStyleSheet('background-color: #fff; border: none;')

        self._out.show()

        output_group = widgets.QGroupBox()

        output_layout = widgets.QVBoxLayout()
        output_layout.addWidget(out_label)
        output_layout.addWidget(self._out)
        output_layout.setSpacing(5)
        output_layout.setContentsMargins(0, 0, 0, 0)

        output_group.setMaximumHeight(250)
        output_group.setLayout(output_layout)

        self.setWindowTitle('Befunge Interpreter')
        self.setWindowIcon(gui.QIcon('media/icon.png'))
        self.setMinimumSize(800, 500)
        self.resize(1000, 600)
        self.center()

        self._space = Space(self)

        window_layout = widgets.QGridLayout()
        window_layout.setHorizontalSpacing(5)
        window_layout.setVerticalSpacing(10)
        window_layout.addWidget(commands_group, 0, 0, 1, 2)
        window_layout.addWidget(self._space, 1, 0, 4, 2)
        window_layout.addWidget(input_group, 5, 0)
        window_layout.addWidget(output_group, 5, 1)
        window_layout.setContentsMargins(10, 10, 10, 10)

        self._output_stream = io.StringIO()
        self._input_stream = io.StringIO()
        self._create_interpreter()

        self.setLayout(window_layout)
        self.setStyleSheet('background-color: #FFC20B;')
        self.show()

    def _create_interpreter(self):
        self._output_stream.truncate(0)
        self._input_stream.truncate(0)

        self._inter = interpreter.Interpreter(self._input_stream,
                                              self._output_stream)
        if self._inter.init_interpreter(self._args.program) == 1:
            self._out.appendPlainText("File is empty or doesn't exist")

        self._space.write_table_to_space(self._inter, False)

        self._inp.clear()
        self._out.clear()

        self.disable_input()

    def center(self):
        qr = self.frameGeometry()
        cp = widgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @staticmethod
    def create_cmd_button(text):
        button = widgets.QPushButton(text)

        button.setFixedWidth(100)
        button.setStyleSheet('background-color: #fff;')

        return button

    def make_step(self):
        if self._inter.finished:
            return

        if self._inter.input_mode:
            if len(self._input_stream.getvalue()) == 0:
                self.enable_input()
                return

        self._inter.execute_one_step()

        if self._inter.input_mode:
            self._inp.clear()
            self.enable_input()
        self._space.write_table_to_space(self._inter)
        self._out.setPlainText(self._output_stream.getvalue())

    def run_program(self):
        self._running = True

        while not self._inter.finished:
            if self._inter.input_mode:
                if len(self._inp.toPlainText()) == 0:
                    self.enable_input()
                    return

            self._inter.execute_one_step()

            if self._inter.input_mode:
                self._inp.clear()
                self.enable_input()
                self._out.setPlainText(self._output_stream.getvalue())

        self._running = False
        self._space.write_table_to_space(self._inter)
        self._out.setPlainText(self._output_stream.getvalue())

    def input_cmd(self):
        prev = self._input_stream.tell()
        self._input_stream.write(self._inp.toPlainText())
        self._input_stream.seek(prev)

        self.disable_input()

        if self._running:
            self.run_program()

    def disable_input(self):
        self._inp.setReadOnly(True)
        self._inp.setStyleSheet(
            'background-color: #DADADA; border: none;')
        self._input_button.setDisabled(True)

    def enable_input(self):
        self._inp.setReadOnly(False)
        self._inp.setStyleSheet(
            'background-color: #fff; border: none;')
        self._input_button.setDisabled(False)


class Space(widgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color: #fff;')
        self.setEditTriggers(widgets.QAbstractItemView.NoEditTriggers)

        self.show()

    def write_table_to_space(self, inter, show_cursor=True):
        active_color = gui.QColor()
        active_color.setRgb(255, 127, 248)
        active_brush = gui.QBrush(active_color)

        common_color = gui.QColor()
        common_color.setRgb(255, 255, 255)
        common_brush = gui.QBrush(common_color)

        ui_cursor = Space.get_cursor(inter,
                                     utils.Utils.multiply_delta(inter, -1))
        self.clear()
        for i in range(len(inter.program)):
            if i >= self.rowCount():
                self.insertRow(i)
            self.setRowHeight(i, 20)
            for j in range(len(inter.program[i])):
                if j >= self.columnCount():
                    self.insertColumn(j)
                self.setColumnWidth(j, 20)
                item = widgets.QTableWidgetItem()
                if not self.item(i, j):
                    self.setItem(i, j, item)
                self.item(i, j).setText(inter.program[i][j])
                self.item(i, j).setFlags(core.Qt.NoItemFlags)
                self.item(i, j).setFlags(core.Qt.ItemIsEnabled)
                if ui_cursor == (j, i) and show_cursor:
                    self.item(i, j).setBackground(active_brush)
                else:
                    self.item(i, j).setBackground(common_brush)

    @staticmethod
    def get_cursor(inter, delta):
        y = (inter.ip[1] + delta[1]) % len(inter.program)
        return (inter.ip[0] + delta[0]) % len(inter.program[y]), y

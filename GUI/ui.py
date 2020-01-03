import io
import time

from PyQt5 import QtGui, QtWidgets, QtCore

from logic import interpreter
from logic import utils


class Window(QtWidgets.QWidget):
    def __init__(self, args):
        super().__init__()

        self._args = args
        self.running = False
        self.step_running = False
        self._thread_pool = QtCore.QThreadPool()
        self._start_ui()

    def _start_ui(self):
        commands_layout = QtWidgets.QHBoxLayout()

        self._exit_dialog = ExitDialog(self)
        self._exit_dialog.setStyleSheet('background-color: #fff;')
        self._exit_dialog.setModal(True)
        self._exit_dialog.accepted.connect(
            QtCore.QCoreApplication.instance().quit)
        self._exit_dialog.rejected.connect(
            QtCore.QCoreApplication.instance().quit)

        self._run_btn = Window.create_cmd_button('Запуск')
        run = QtWidgets.QAction(self)
        run.setShortcut('F5')
        run.triggered.connect(self.run_program)
        self._run_btn.addAction(run)
        self._run_btn.clicked.connect(self.run_program)

        self._step_run_btn = Window.create_cmd_button('Запуск пошаговый')
        run = QtWidgets.QAction(self)
        run.setShortcut('F6')
        run.triggered.connect(self.step_run_program)
        self._step_run_btn.addAction(run)
        self._step_run_btn.clicked.connect(self.step_run_program)

        self._step_btn = Window.create_cmd_button('Шаг')
        step = QtWidgets.QAction(self)
        step.setShortcut('Space')
        step.triggered.connect(self.make_step)
        self._step_btn.addAction(step)
        self._step_btn.clicked.connect(self.make_step)

        self._restart_btn = Window.create_cmd_button('Перезапустить')
        restart = QtWidgets.QAction(self)
        restart.setShortcut('F9')
        restart.triggered.connect(self._create_interpreter)
        self._restart_btn.addAction(restart)
        self._restart_btn.clicked.connect(self._create_interpreter)

        commands_layout.addWidget(self._run_btn)
        commands_layout.addWidget(self._step_run_btn)
        commands_layout.addWidget(self._step_btn)
        commands_layout.addWidget(self._restart_btn)
        commands_layout.setAlignment(QtCore.Qt.AlignLeft)

        commands_group = QtWidgets.QGroupBox()
        commands_group.setLayout(commands_layout)
        commands_group.setMaximumHeight(40)
        commands_layout.setSpacing(20)
        commands_layout.setContentsMargins(0, 0, 0, 0)

        inp_label = QtWidgets.QLabel('Поле ввода:')
        inp_label.setFont(QtGui.QFont('Mono', 20))

        inp_label.show()

        self.inp = QtWidgets.QPlainTextEdit('', self)
        self.inp.setAutoFillBackground(True)
        self.inp.setMinimumHeight(90)
        self.inp.setFont(QtGui.QFont('Courier', 14))

        self.inp.show()

        self.input_button = QtWidgets.QPushButton('Ввести')
        self.input_button.setFont(QtGui.QFont('Mono', 16))
        self.input_button.setStyleSheet('''background-color: #fff; 
                                            margin-top: 10px;''')
        self.input_button.clicked.connect(self.input_cmd)

        self.input_button.setFixedHeight(40)
        self.input_button.setFixedWidth(150)

        self.input_button.show()

        input_group = QtWidgets.QGroupBox()

        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(inp_label)
        input_layout.addWidget(self.inp)
        input_layout.addWidget(self.input_button)
        input_layout.setAlignment(self.input_button, QtCore.Qt.AlignRight)

        input_layout.setSpacing(5)
        input_layout.setContentsMargins(0, 0, 0, 0)

        input_group.setMaximumHeight(250)
        input_group.setMaximumWidth(400)
        input_group.setLayout(input_layout)

        out_label = QtWidgets.QLabel('Поле вывода:')
        out_label.setFont(QtGui.QFont('Mono', 20))

        out_label.show()

        self.out = QtWidgets.QPlainTextEdit('', self)
        self.out.setReadOnly(True)
        self.out.setMinimumHeight(100)
        self.out.setFont(QtGui.QFont('Courier', 14))
        self.out.setStyleSheet('background-color: #fff; border: none;')

        self.out.show()

        output_group = QtWidgets.QGroupBox()

        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(out_label)
        output_layout.addWidget(self.out)
        output_layout.setSpacing(5)
        output_layout.setContentsMargins(0, 0, 0, 0)

        output_group.setMaximumHeight(250)
        output_group.setLayout(output_layout)

        self.setWindowTitle('Befunge Interpreter')
        self.setWindowIcon(QtGui.QIcon('media/icon.png'))
        self.setMinimumSize(800, 500)
        self.resize(1000, 600)
        self.center()

        self.space = Space(self)

        window_layout = QtWidgets.QGridLayout()
        window_layout.setHorizontalSpacing(5)
        window_layout.setVerticalSpacing(10)
        window_layout.addWidget(commands_group, 0, 0, 1, 2)
        window_layout.addWidget(self.space, 1, 0, 4, 2)
        window_layout.addWidget(input_group, 5, 0)
        window_layout.addWidget(output_group, 5, 1)
        window_layout.setContentsMargins(10, 10, 10, 10)

        self.output_stream = io.StringIO()
        self.input_stream = io.StringIO()

        self.setLayout(window_layout)
        self.setStyleSheet('background-color: #FFC20B;')
        self.show()
        self._create_interpreter()

    def _create_interpreter(self):
        self.output_stream.truncate(0)
        self.input_stream.truncate(0)
        io = utils.CustomIO(self.input_stream, self.output_stream)

        self.inter = interpreter.Interpreter(io)
        try:
            self.inter.init_interpreter(self._args.program)
        except FileNotFoundError as file_name:
            self._exit_dialog.set_text(f'Файл "{file_name}" не найден!')
            self._exit_dialog.open()
            return

        self.space.write_table_to_space(self.inter, False)

        self.inp.clear()
        self.out.clear()

        self.disable_input()
        self.running = False
        self.step_running = False

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @staticmethod
    def create_cmd_button(text):
        button = QtWidgets.QPushButton(text)

        button.setFixedWidth(100)
        button.setStyleSheet('background-color: #fff;')

        return button

    def make_step(self):
        if self.inter.finished:
            return

        if self.inter.input_mode:
            if len(self.input_stream.getvalue()) == 0:
                self.enable_input()
                return

        self.inter.execute_one_step()

        if self.inter.input_mode:
            self.inp.clear()
            self.enable_input()
        self.space.write_table_to_space(self.inter)
        self.out.setPlainText(self.output_stream.getvalue())

    def step_run_program(self):
        worker = ProgramWorker(self)
        worker.signals.update_ui.connect(self._update_ui)
        worker.signals.clear_input.connect(self.inp.clear)
        worker.signals.enable_input.connect(self.enable_input)

        self._thread_pool.start(worker)

    def run_program(self):
        self.running = True

        while not self.inter.finished and self.running:
            if self.inter.input_mode:
                if len(self.inp.toPlainText()) == 0:
                    self.enable_input()
                    return

            self.inter.execute_one_step()

            if self.inter.input_mode:
                self.inp.clear()
                self.enable_input()
                self._update_ui()

        self._update_ui()

        self.running = False

    def _update_ui(self):
        self.space.write_table_to_space(self.inter)
        self.out.setPlainText(self.output_stream.getvalue())

    def input_cmd(self):
        prev = self.input_stream.tell()
        self.input_stream.write(self.inp.toPlainText())
        self.input_stream.seek(prev)

        self.disable_input()

        if self.running:
            self.run_program()

        if self.step_running:
            self.step_run_program()

    def disable_input(self):
        self.inp.setReadOnly(True)
        self.inp.setStyleSheet(
            'background-color: #DADADA; border: none;')
        self.input_button.setDisabled(True)

    def enable_input(self):
        self.inp.setReadOnly(False)
        self.inp.setStyleSheet(
            'background-color: #fff; border: none;')
        self.input_button.setDisabled(False)


class ProgramWorkerSignals(QtCore.QObject):
    update_ui = QtCore.pyqtSignal()
    enable_input = QtCore.pyqtSignal()
    clear_input = QtCore.pyqtSignal()


class ProgramWorker(QtCore.QRunnable):
    def __init__(self, window):
        super(ProgramWorker, self).__init__()
        self.window = window
        self.signals = ProgramWorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        self.window.step_running = True

        while not self.window.inter.finished and self.window.step_running:
            if self.window.inter.input_mode:
                if len(self.window.inp.toPlainText()) == 0:
                    self.window.enable_input()
                    return

            self.window.inter.execute_one_step()

            if self.window.inter.input_mode:
                self.signals.clear_input.emit()
                self.signals.enable_input.emit()
                self.signals.update_ui.emit()

            self.signals.update_ui.emit()
            time.sleep(0.04)

        self.window.step_running = False


class ExitDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._label = QtWidgets.QLabel()

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._label)
        layout.addWidget(buttons)

        layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.setLayout(layout)

    def set_text(self, text):
        self._label.setText(text)


class Space(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color: #fff;')
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.show()

    def write_table_to_space(self, inter, show_cursor=True):
        active_color = QtGui.QColor()
        active_color.setRgb(255, 127, 248)
        active_brush = QtGui.QBrush(active_color)

        common_color = QtGui.QColor()
        common_color.setRgb(255, 255, 255)
        common_brush = QtGui.QBrush(common_color)

        ui_cursor = Space.get_cursor(inter,
                                     utils.multiply_delta(inter, -1))
        self.clear()
        for i in range(len(inter.program)):
            if i >= self.rowCount():
                self.insertRow(i)
            self.setRowHeight(i, 20)
            for j in range(len(inter.program[i])):
                if j >= self.columnCount():
                    self.insertColumn(j)
                self.setColumnWidth(j, 20)
                item = QtWidgets.QTableWidgetItem()
                if not self.item(i, j):
                    self.setItem(i, j, item)
                self.item(i, j).setText(inter.program[i][j])
                self.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                self.item(i, j).setFlags(QtCore.Qt.ItemIsEnabled)
                if ui_cursor == (j, i) and show_cursor:
                    self.item(i, j).setBackground(active_brush)
                else:
                    self.item(i, j).setBackground(common_brush)

    @staticmethod
    def get_cursor(inter, delta):
        y = (inter.ip[1] + delta[1]) % len(inter.program)
        return (inter.ip[0] + delta[0]) % len(inter.program[y]), y

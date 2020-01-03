#! /usr/local/bin/python3

import sys
import argparse
import PyQt5.QtWidgets as widgets

import GUI.ui as ui


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Python3.7 implementation Befunge-98 interpretator')
        self.parser.add_argument('program', type=str, help='program file')


if __name__ == '__main__':
    args = Parser().parser.parse_args()
    app = widgets.QApplication(sys.argv)

    window = ui.Window(args)

    sys.exit(app.exec_())


#!/usr/bin/python -u
# -*- coding: utf-8 -*-


#+=================================================================+
#|                      Sudoku Solver - 1.x                        |
#+=================================================================+
#|                                                                 |
#|       +-------------------------------------------------+       |
#|       |     Author   : पुष्पक दगड़े  (Pushpak Dagade)        |       |
#|       |     Email    : guanidene@gmail.com              |       |
#|       +-------------------------------------------------+       |
#|                                                                 |
#+=================================================================+

"""
A small graphical application for solving any Sudoku puzzle, almost
instantaneously.
"""

# avoid QString class altogether
import sip
sip.setapi("QString", 2)
from PyQt4 import QtGui
from mainwindow import MainWindow

__author__ = "पुष्पक दगड़े (Pushpak Dagade)"
__version__ = '1.x'


if __name__ == "__main__":
    app = QtGui.QApplication(['pySudokuSolver'])
    app.setOrganizationName('pySudokuSolver')
    app.setApplicationName('pySudokuSolver')
    widget = MainWindow()
    widget.show()
    exit(app.exec_())

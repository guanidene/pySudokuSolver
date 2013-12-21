#!/usr/bin/python -u
# -*- coding: utf-8 -*-
#
# date: 'Thu Dec 19 01:46:57 2013'

#+=================================================================+
#|                      Sudoku Solver - 1.x                        |
#+=================================================================+
#|                                                                 |
#|       +-------------------------------------------------+       |
#|       |     Author   : पुष्पक दगड़े  (Pushpak Dagade)        |       |
#|       |     Date     : XXXXXXXXXXXX                     |       |
#|       |     Email    : guanidene@gmail.com              |       |
#|       |     Blog     : http://guanidene.blogspot.com    |       |
#|       +-------------------------------------------------+       |
#|                                                                 |
#+=================================================================+

"""A small graphical application for solving any Sudoku puzzle,
almost instantaneously."""

from PyQt4 import QtCore, QtGui
from ui_sudoku_solver import Ui_MainWindow


# XXX. Next steps:
# 1. Try to modify MaainWindow using QtDesigner such that all the code in
#    sudokuframe.py caan be brought into the class MainWindow!

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        # Setup the GUI created using QtDesigner
        super(MainWindow, self).__init__(None)
        self.setupUi(self)

        self.window_maximized = False

        self.actionFullscreen.triggered.connect(self.menuFullscreen)
        
        # XXX
        # TODOS:
        #sys.stdout = self.frame.sidepanel.solutionbox
        #LoadPuzzle(self.frame)               # Load an existing Sudoku puzzle.

    def menuFullscreen(self):
        if self.windowState() & QtCore.Qt.WindowFullScreen:
            print 'self.window_maximized', self.window_maximized
            if self.window_maximized:
                self.showMaximized()
            else:
                self.showNormal()
        else:
            print 'ismaximized', self.isMaximized()
            if self.isMaximized():
                self.window_maximized = True
            self.showFullScreen()

#class SudokuSolverApp():    
#    def OnInit(self):
#        """Create a SudokuFrame instance and set it as the top window.
#        Also redirect the standard output stream to the SolutionBox."""
#        from sudokuframe import SudokuFrame   # Can't keep this import above.
#        self.frame = SudokuFrame(None)
#        sys.stdout = self.frame.sidepanel.solutionbox
#        #sys.stderr = self.frame.sidepanel.solutionbox
#        LoadPuzzle(self.frame)               # Load an existing Sudoku puzzle.
#        self.SetTopWindow(self.frame)
#        self.frame.Show()
#        return True

def LoadPuzzle(frame):
    """Load a puzzle."""
    cells = frame.sudokupanel.sudokucells
    setlabel = frame.sudokupanel.SetSudokuCellLabel
    from sudokucell import SudokuCell
    label = SudokuCell.Labels  # this is useful if you change the labels
                               # from 0-9 to something else, say A-I
    
    # This is a really tough puzzle, requiring upto 3
    # levels of assumptions to solve it completely.
    setlabel(cells[0][2], label[5])
    setlabel(cells[0][3], label[3])
    setlabel(cells[1][0], label[8])
    setlabel(cells[1][7], label[2])
    setlabel(cells[2][1], label[7])
    setlabel(cells[2][4], label[1])
    setlabel(cells[2][6], label[5])
    setlabel(cells[3][0], label[4])
    setlabel(cells[3][5], label[5])
    setlabel(cells[3][6], label[3])
    setlabel(cells[4][1], label[1])
    setlabel(cells[4][4], label[7])
    setlabel(cells[4][8], label[6])
    setlabel(cells[5][2], label[3])
    setlabel(cells[5][3], label[2])
    setlabel(cells[5][7], label[8])
    setlabel(cells[6][1], label[6])
    setlabel(cells[6][3], label[5])
    setlabel(cells[6][8], label[9])
    setlabel(cells[7][2], label[4])
    setlabel(cells[7][7], label[3])
    setlabel(cells[8][5], label[9])
    setlabel(cells[8][6], label[7])

if __name__ == "__main__":
    app = QtGui.QApplication(['pySudokuSolver'])
    app.setOrganizationName('pySudokuSolver')
    app.setApplicationName('pySudokuSolver')
    widget = MainWindow()
    widget.show()
    exit(app.exec_())

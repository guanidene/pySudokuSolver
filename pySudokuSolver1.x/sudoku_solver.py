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

"""A small graphical application for solving any Sudoku puzzle,
almost instantaneously."""

from PyQt4 import QtGui
from ui_sudoku_solver import Ui_MainWindow, _fromUtf8

__author__ = "Pushpak Dagade (पुष्पक दगड़े)"
__version__ = '1.x'


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        ## GUI related code
        # Setup the GUI created using QtDesigner
        super(MainWindow, self).__init__(None)
        self.setupUi(self)

        # add icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pics/Sudoku Solver.ico")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.actionShowSolution.triggered.connect(self.showSolution)
        self.actionFullscreen.triggered.connect(self.viewFullscreen)
        self.actionAbout.triggered.connect(self.helpAbout)
        self.actionHowToUse.triggered.connect(self.helpHowToUse)

        ## non GUI related code
        self.maximized_flag = self.isMaximized()
        # XXX. call initaliaze method on all the instances of class SudokuCell

        # XXX
        # TODOS:
        #sys.stdout = self.frame.sidepanel.solutionbox
        #LoadPuzzle(self.frame)               # Load an existing Sudoku puzzle.

    def showSolution(self):
        if self.actionShowSolution.isChecked():
            print 'Solution ON  [slow]'
        else:
            print 'Solution OFF [fast]'


    def viewFullscreen(self):
        """
        Toggle fullscreen mode
        """
        if self.isFullScreen():
            self.showNormal()
            if self.maximized_flag:
                self.showMaximized()
        else:
            self.maximized_flag = self.isMaximized()
            self.showFullScreen()
        self.actionFullscreen.setChecked(self.isFullScreen())

    def helpAbout(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.setText("<b>Sudoku Solver %s</b>\n" % __version__)
        msgBox.setInformativeText(
            u"A small graphical application for solving any Sudoku puzzle, "
            u"almost instantaneously.\n\n"
            u"Created by पुष्पक दगड़े (Pushpak Dagade) \n"
            u"(Update: December 2013)")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.exec_()

    def helpHowToUse(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.setText("<b>Sudoku Solver %s</b>\n" % __version__)
        msgBox.setInformativeText(
        "Entering numbers in the grid - \n"\
        "==================================\n"\
        "Scroll over cells to rotate through their permissible numbers.\n"\
        "\n"\
        "Buttons -\n"\
        "============\n"\
        "Save - Saves the current puzzle.\n"\
        "Clear - Clears the grid and the Solution Box.\n"\
        "Revert - Loads a saved puzzle.\n"\
        "Solve - Solves the Sudoku puzzle in the grid.\n"\
        "\n"\
        "Solution Box -\n"\
        "============\n"\
        "It is more or less like a log box.\n" \
        "1. When a puzzle is solved (on clicking the Solve button),\n"\
        "it logs the puzzle solution.\n"\
        "2. Additionally, it also logs actions of the\n"\
        "buttons Save, Revert and Clear.\n")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.exec_()


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
    setlabel = frame.sudokupanel.setSudokuCellLabel
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

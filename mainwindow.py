#!/usr/bin/python -u
# -*- coding: utf-8 -*-

__author__ = "पुष्पक दगड़े (Pushpak Dagade)"

"""
Sudoku Solver main window
"""

import sys
from time import time
from textwrap import dedent
from PyQt4 import QtGui
from logic import SolveSudokuPuzzle
from ui_sudoku_solver import Ui_MainWindow, _fromUtf8

__author__ = "पुष्पक दगड़े (Pushpak Dagade)"
__version__ = '1.x'


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        ## GUI related code
        # Setup the GUI created using QtDesigner
        super(MainWindow, self).__init__(None)
        self.setupUi(self)

        # set window icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(_fromUtf8("pics/Sudoku Solver.ico")),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)

        # connect singal to slots
        self.actionShowSolution.triggered.connect(self.showSolution)
        self.actionFullscreen.triggered.connect(self.viewFullscreen)
        self.actionAbout.triggered.connect(self.helpAbout)
        self.actionHowToUse.triggered.connect(self.helpHowToUse)
        self.btnClear.clicked.connect(self.onClear)
        self.btnRevert.clicked.connect(self.onRevert)
        self.btnSave.clicked.connect(self.onSave)
        self.btnSolve.clicked.connect(self.onSolve)

        ## non GUI related code
        self.savedPuzzle = None
        self.maximized_flag = self.isMaximized()
        self.sudokugrid.popululateSudokucells()
        self.LoadPuzzle()

        # redirect all stdout and stderr to txtbrwSolutionbox
        self.txtbrwSolutionbox.write = self.txtbrwSolutionbox.append
        sys.stdout = self.txtbrwSolutionbox
        sys.stderr = self.txtbrwSolutionbox

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
            u"Created by %s \n"
            u"(Update: December 2013)" % __author__)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.exec_()

    def helpHowToUse(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.setText("<b>Sudoku Solver %s</b>\n" % __version__)
        msgBox.setInformativeText(
            "Entering numbers in the grid - \n"
            "==================================\n"
            "Scroll over cells to rotate through their permissible numbers.\n"
            "\n"
            "Buttons -\n"
            "============\n"
            "Save - Saves the current puzzle.\n"
            "Clear - Clears the grid and the Solution Box.\n"
            "Revert - Loads a saved puzzle.\n"
            "Solve - Solves the Sudoku puzzle in the grid.\n"
            "\n"
            "Solution Box -\n"
            "============\n"
            "It is more or less like a log box.\n"
            "1. When a puzzle is solved (on clicking the Solve button),\n"
            "it logs the puzzle solution.\n"
            "2. Additionally, it also logs actions of the\n"
            "buttons Save, Revert and Clear.\n")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.exec_()

    def onSave(self):
        """
        Save the current state of the Sudoku puzzle.
        Overwrite, if any, previously saved puzzle.
        """
        self.savedPuzzle = self.sudokugrid.getPuzzle()
        print '[Sudoku puzzle Saved]'

    def onRevert(self):
        """
        Clear the grid and load a perviously saved puzzle, if any.
        If there is no previously saved puzzle, just clear off the grid.
        """
        if self.savedPuzzle:
            self.sudokugrid.setPuzzle(self.savedPuzzle)
            print '[Saved puzzle restored]'
        else:
            print '[No puzzle saved yet]'

    def onClear(self):
        """
        Clear off the grid for a fresh start.
        """
        self.sudokugrid.clearPuzzle()
        self.txtbrwSolutionbox.clear()

    def onSolve(self):
        """
        Try to solve the Sudoku puzzle. Print the solution as per user
        requirements. Also print the time taken in this process.
        """
        # Check if the grid is not empty before proceeding.
        if self.sudokugrid.isGridEmpty():
            print '[Nothing to solve]'
            return

        # I will print the solution if the users wants it. Note, even if user
        # wants the solution in solutionbox, I will first save it in a file
        # and then load it to the solution box in one stroke, because this is
        # faster than printing directly to the solutionbox from logic.

        # Redirect the stdout to a text file 'Solution.txt'
        temp = sys.stdout
        sys.stdout = open('Solution.txt', 'w')

        # Record the start time
        t0 = time()

        # Convert the puzzle in the grid into a string - str_question_puzzle
        str_question_puzzle = ""
        for sudokucell in self.sudokugrid:
            label = sudokucell.text()
            if label != "":
                str_question_puzzle += "%s " % label
            else:
                str_question_puzzle += ". "

        # Get solution puzzle for str_question_puzzle
        str_solution_puzzle = SolveSudokuPuzzle(str_question_puzzle)

        # Read str_solution_puzzle and fill the grid accordingly.
        numbers = str_solution_puzzle.split()
        for i, sudokucell in enumerate(self.sudokugrid):
            if numbers[i] != '.':
                self.sudokugrid.setSudokuCellLabel(sudokucell, numbers[i])
            else:
                self.sudokugrid.setSudokuCellLabel(sudokucell, '')

        # Restore the stdout to its previous value
        sys.stdout = temp

        # Load the solution from the solution file if user wants.
        if self.actionShowSolution.isChecked():
            self.txtbrwSolutionbox.setPlainText(open('Solution.txt').read())

        # Record the complete time
        t1 = time()

        print "[%.2f sec.]\n\n" \
              "[Solution saved in 'Solutions.txt']" \
              % (t1 - t0)     # print a timestamp in solution box.

        # Miscellaneous checking...
        if not self.sudokugrid.isPuzzleCorrect():
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Critical)
            msgBox.setText(
                "<b>Incorrect puzzle provided</b>."
                "\n\n"
                "The given puzzle cannot be solved. Please recheck.")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.exec_()
        elif not self.sudokugrid.isPuzzleComplete():
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setText(
                "<b>Inadequate entries provided.</b>\n"
                "\n\n"
                "The puzzle could not be solved within the level of "
                "assumptions set. Most probably, the puzzle has insufficient "
                "number of entries for it to have a unique solution."
                "\n\n"
                "Please add more entries.")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.exec_()

    def LoadPuzzle(self):
        """
        Load a puzzle at startup.
        This method is just for quickly loading the grid with a puzzle for
        testing. Can delete this lateron.
        """
        cells = self.sudokugrid.sudokucells
        setlabel = self.sudokugrid.setSudokuCellLabel
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

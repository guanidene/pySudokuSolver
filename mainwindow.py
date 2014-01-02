# -*- coding: utf-8 -*-

"""
pySudokuSolver main window of GUI
"""

import sys
from tempfile import NamedTemporaryFile
from time import time
from os.path import dirname, join
from PyQt4 import QtCore, QtGui
from logic import SolveSudokuPuzzle
from ui_sudoku_solver import Ui_MainWindow, _fromUtf8

__author__ = u"पुष्पक दगड़े (Pushpak Dagade)"
__version__ = '1.3'


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        ## GUI related code
        # Setup the GUI created using QtDesigner
        super(MainWindow, self).__init__(None)
        self.setupUi(self)
        self.setMinimumSize(600, 400)

        # set window icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(
            _fromUtf8(join(dirname(__file__), "icon/ss-256x256.png"))),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)

        # connect singals to slots
        self.actionFullscreen.triggered.connect(self.viewFullscreen)
        self.actionAbout.triggered.connect(self.helpAbout)
        self.actionHowToUse.triggered.connect(self.helpHowToUse)
        self.btnClear.clicked.connect(self.onClear)
        self.btnRevert.clicked.connect(self.onRevert)
        self.btnSave.clicked.connect(self.onSave)
        self.btnSolve.clicked.connect(self.onSolve)
        self.restoreSettings()

        ## non GUI related code
        self.savedPuzzle = None
        self.maximized_flag = self.isMaximized()
        self.sudokugrid.popululateSudokucells()
        self.LoadPuzzle()

        ## Save some fixed dimensions for quicker computation in the
        ## resizeEvent method
        # 1. self.centralwidget's layoutRightMargin + layoutSpacing +
        #                         layoutLeftMargin,
        self.margin_horizontal = 9 + 6 + 9
        # 2. self.centrakwidget's layoutTopMargin + layoutBottomMargin
        self.margin_vertical = 9 + 9
        # 3. gridLayoutSidePanel's fixed width
        self.width_sidepanel = self.gridLayoutSidePanel.minimumSize().width()

        # redirect all stdout and stderr to txtbrwSolutionbox
#        self.txtbrwSolutionbox.write = self.txtbrwSolutionbox.append
#        sys.stdout = self.txtbrwSolutionbox
#        sys.stderr = self.txtbrwSolutionbox

    def resizeEvent(self, event):
        """
        Keep mainwindow.sudokugrid centered as a square (with maximum size)
        within self.widget
        """
        # Keep in mind a practical problem - When the app starts, "self.widget"
        # is still small in size as it has not expanded yet to fill the space
        # within MainWindow. So cannot use "self.widget"'s height/width for
        # computation directly. Instead, I need to compute its dimensions by
        # subtracting gridLayoutSidePanel's dimensions from MainWindow's
        # dimensions.
        # So, some maths, albeit simple, is required here.

        widget_width = self.centralwidget.width() - self.width_sidepanel - \
            self.margin_horizontal
        widget_height = self.centralwidget.height() - self.margin_vertical
        newlength_sudokugrid = min(widget_width, widget_height)
        topleft_x = (widget_width - newlength_sudokugrid) / 2
        topleft_y = (widget_height - newlength_sudokugrid) / 2
        self.sudokugrid.setGeometry(QtCore.QRect(topleft_x, topleft_y,
                                                 newlength_sudokugrid,
                                                 newlength_sudokugrid))

    def closeEvent(self, event):
        self.saveSettings()
        event.accept()

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
        settings.setValue('windowgeometry', self.saveGeometry())
        settings.setValue('windowstate', self.saveState())

    def restoreSettings(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        settings = QtCore.QSettings()
        pos = settings.value('pos', QtCore.QPoint(screen.width() / 8.0,
                             screen.height() / 8.0))
        size = settings.value('size', QtCore.QSize(0.75 * screen.width(),
                              0.75 * screen.height()))
        self.move(pos)
        self.resize(size)
        if settings.contains('windowgeometry'):
            self.restoreGeometry(settings.value('windowgeometry'))
        if settings.contains('windowstate'):
            self.restoreState(settings.value('windowstate'))

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
        msgBox.setIconPixmap(self.icon.pixmap(128, 128))
        msgBox.setText("<b>Sudoku Solver %s</b>\n" % __version__)
        msgBox.setInformativeText(
            u"A small graphical application for solving any Sudoku puzzle, "
            u"almost instantaneously.\n\n"
            u"Created by %s \n"
            u"Updated Release: December 2013 \n"
            u"First Release: July 2011"
            % __author__)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.exec_()

    def helpHowToUse(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setIconPixmap(self.icon.pixmap(128, 128))
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
        self.txtbrwSolutionbox.append('[Sudoku puzzle Saved]')

    def onRevert(self):
        """
        Clear the grid and load a perviously saved puzzle, if any.
        If there is no previously saved puzzle, just clear off the grid.
        """
        if self.savedPuzzle:
            self.sudokugrid.setPuzzle(self.savedPuzzle)
            self.txtbrwSolutionbox.append('[Saved puzzle restored]')
        else:
            self.txtbrwSolutionbox.append('[No puzzle saved to restore]')

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
            self.txtbrwSolutionbox.append('[Nothing to solve]')
            return

        # Redirecting the stdout to a temp. file, to temporarily save
        # solutions in it.
        temp_file_solutions = NamedTemporaryFile(mode='w')
        temp = sys.stdout
        sys.stdout = temp_file_solutions

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
        # (This is the time consuming operation)
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
        temp_file_solutions.flush()
        if self.actionShowSolution.isChecked():
            self.txtbrwSolutionbox.append(
                open(temp_file_solutions.name).read())
        temp_file_solutions.close()   # closing deletes the temp. file

        # Record the complete time
        t1 = time()

        self.txtbrwSolutionbox.append(
            "[%.2f sec.]\n\n"
            % (t1 - t0))     # print a timestamp in solution box.

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

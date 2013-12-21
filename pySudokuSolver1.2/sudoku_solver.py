#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# sudoku_solver.py    [Sudoku Solver 1.2]

#+=================================================================+
#|                      Sudoku Solver - 1.2                        |
#+=================================================================+
#|                                                                 |
#|       +-------------------------------------------------+       |
#|       |     Author   : Pushpak Dagade                   |       |
#|       |     Date     : 20 July 2011                     |       |
#|       |     Email    : guanidene@gmail.com              |       |
#|       |     Blog     : http://guanidene.blogspot.com    |       |
#|       +-------------------------------------------------+       |
#|                                                                 |
#+=================================================================+

"""A small graphical application for solving any Sudoku puzzle,
almost instantaneously."""

__author__ = "Pushpak Dagade (पुष्पक दगड़े)"
__date__   = "$May 18, 2011 9:22:08 PM$"

import sys
import wx

class SudokuSolverApp(wx.App):    
    def OnInit(self):
        """Create a SudokuFrame instance and set it as the top window.
        Also redirect the standard output stream to the SolutionBox."""
        from sudokuframe import SudokuFrame   # Can't keep this import above.
        self.frame = SudokuFrame(None)
        sys.stdout = self.frame.sidepanel.solutionbox
        #sys.stderr = self.frame.sidepanel.solutionbox
        LoadPuzzle(self.frame)               # Load an existing Sudoku puzzle.
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

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
    app = SudokuSolverApp(False)
    app.MainLoop()

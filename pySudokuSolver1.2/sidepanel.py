# sidepanel.py    [Sudoku Solver 1.2]
# -*- coding: UTF-8 -*-

__author__ = "Pushpak Dagade (पुष्पक दगड़े)"
__date__   = "$May 22, 2011 5:15:52 PM$"

import sys
import time
import wx
from logic import SolveSudokuPuzzle
from solutionbox import SolutionBox

class SidePanel(wx.Panel):
    """Creates a Panel widget which contains a solutionbox.SolutionBox
    widget and 4 buttons widgets - Save, Revert, Clear and Solve."""
    
    def __init__(self, parent, sudokupanel):
        super(self.__class__, self).__init__(parent, -1,
          style = wx.NO_BORDER|wx.TAB_TRAVERSAL)

        # Attributes.
        self.sudokupanel = sudokupanel
        self.SavedPuzzle = None

        # Create children widgets.
        self.solutionbox = SolutionBox(self)
        self.buttonSave = wx.Button(self, -1, 'Save')
        self.buttonRevert = wx.Button(self, -1, 'Revert')
        self.buttonClear = wx.Button(self, -1, 'Clear')
        self.buttonSolve = wx.Button(self, -1, 'Solve')
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.GridSizer(2,2)
        sizer.Add(self.solutionbox, proportion=1,
          flag=wx.EXPAND|wx.ALL, border=3)
        sizer.Add(sizer2, flag=wx.EXPAND, proportion=0)
        sizer2.Add(self.buttonSave,
          flag=wx.EXPAND|wx.TOP|wx.RIGHT|wx.BOTTOM, border=2.5)
        sizer2.Add(self.buttonRevert,
          flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM, border=2.5)
        sizer2.Add(self.buttonClear,
          flag=wx.EXPAND|wx.RIGHT|wx.TOP, border=2.5)
        sizer2.Add(self.buttonSolve,
          flag=wx.EXPAND|wx.LEFT|wx.TOP, border=2.5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        
        # Bind events.
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.buttonSave)
        self.Bind(wx.EVT_BUTTON, self.OnRevert, self.buttonRevert)
        self.Bind(wx.EVT_BUTTON, self.OnClear, self.buttonClear)
        self.Bind(wx.EVT_BUTTON, self.OnSolve, self.buttonSolve)

    def OnSave(self, *args):
        """Save the current state of the Sudoku puzzle.
        Overwrite, if any, previously saved puzzle."""
        self.SavedPuzzle = self.sudokupanel.GetPuzzle()
        print '[Sudoku puzzle Saved]'

    def OnRevert(self, *args):
        """Clear the grid and load a perviously saved puzzle, if any.
        If there is no previously saved puzzle, just clear off the grid."""
        self.sudokupanel.SetPuzzle(self.SavedPuzzle)
        print '[Saved puzzle restored]'

    def OnClear(self, *args):
        """Clear off the grid for a fresh start."""
        self.sudokupanel.ClearPuzzle()
        self.solutionbox.Clear()

    def OnSolve(self, *args):
        """Try to solve the Sudoku puzzle. Print the solution as per user
        requirements. Also print the time taken in this process."""
        # Check if the grid is not empty before proceeding.
        if self.sudokupanel.IsGridEmpty():
            print '[Nothing to solve]'
            return

        # I will print the solution if the users wants it. Note, even if user
        # wants the solution in solutionbox, I will first save it in a file
        # and then load it to the solution box in one stroke, because this is
        # (for some reason I don't know) faster than printing directly to
        # the solutionbox from logic.

        # Redirect the stdout to a text file 'Solution.txt'
        temp = sys.stdout
        sys.stdout = open('Solution.txt', 'w')

        # Record the start time
        t0 = time.time()

        # Convert the puzzle in the grid into a string - str_question_puzzle
        str_question_puzzle = ""
        for sudokucell in self.sudokupanel:
            label = sudokucell.GetLabel()
            if label != "":
                str_question_puzzle += "%s " %label
            else:
                str_question_puzzle += ". "

        # Get solution puzzle for str_question_puzzle
        str_solution_puzzle = SolveSudokuPuzzle(str_question_puzzle)

        # Read str_solution_puzzle and fill the grid accordingly.
        numbers = str_solution_puzzle.split()
        for i,sudokucell in enumerate(self.sudokupanel):
            if numbers[i] != '.':
                self.sudokupanel.SetSudokuCellLabel(sudokucell, numbers[i])
            else:
                self.sudokupanel.SetSudokuCellLabel(sudokucell, '')

        # Restore the stdout to its previous value
        sys.stdout = temp

        # Load the solution from the solution file if user wants.
        menubar = self.GetParent().GetMenuBar()
        if menubar.IsChecked(10):              # 10 is the ID of the menu -
            f = open('Solution.txt','r')       # "Show solution in solutionbox"
            for line in f: print line,
            f.close()

        # Record the complete time
        t1 = time.time()

        print "[%.2f sec.]\n\n" \
              "[Solution saved in 'Solutions.txt']" \
              %(t1-t0)     # print a timestamp in solution box.

        # Miscellaneous checking...
        if not self.sudokupanel.IsPuzzleCorrect():
            messagebox = wx.MessageDialog(self, "The puzzle provided was"
              " incorrect and hence could not be solved." ,
              caption='Incorrect puzzle provided',
              style=wx.OK|wx.ICON_ERROR)
            messagebox.ShowModal()
            messagebox.Destroy()
        elif not self.sudokupanel.IsPuzzleComplete():
            messagebox = wx.MessageDialog(self, "The puzzle could not be solved"
              " as it had insufficient entries.",
              caption='Inadequate entries provided',
              style=wx.OK|wx.ICON_EXCLAMATION)
            messagebox.ShowModal()
            messagebox.Destroy()

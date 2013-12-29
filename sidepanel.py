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
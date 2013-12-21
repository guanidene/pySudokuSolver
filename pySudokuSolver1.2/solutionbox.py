# solutionbox.py    [Sudoku Solver 1.2]
# -*- coding: UTF-8 -*-

__author__ = "Pushpak Dagade (पुष्पक दगड़े)"
__date__   = "$May 24, 2011 10:49:50 PM$"

import wx

class SolutionBox(wx.TextCtrl):
    """Creates a TextCtrl widget for logging the steps taken in solving
    the Sudoku puzzle. Text can selected and/or copied from the widget,
    but not edited. Font used is a fixed width font."""

    def __init__(self, parent):
        super(self.__class__,self).__init__(parent, -1, size = (220,100),
          style=wx.TE_MULTILINE|wx.TE_READONLY|wx.VSCROLL)
        self.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))

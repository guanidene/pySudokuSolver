# sudokuframe.py    [Sudoku Solver 1.2]
# -*- coding: UTF-8 -*-

__author__ = "Pushpak Dagade (पुष्पक दगड़े)"
__date__   = "$May 21, 2011 7:40:09 PM$"

import os.path
import wx
from sudokupanel import SudokuPanel
from sidepanel import SidePanel

class SudokuFrame(wx.Frame):
    """Instance of this class will act as container for
    instances of classes SudokuPanel and SidePanel. It 
    also will be the top window."""
    
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent, -1, 'Sudoku Solver 1.2')

        # Create children widgets.
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        
        menufile = wx.Menu()
        menufile.Append(0, 'E&xit\tCtrl+W')
        menubar.Append(menufile, '&File')
        
        menusolution = wx.Menu()
        menusolution.AppendCheckItem(10, "Show solution in solutionbox\tCtrl+S")
        menubar.Append(menusolution, '&Solution')
        
        menuview = wx.Menu()
        menuview.AppendCheckItem(20,'&Full Screen\tF11')
        menubar.Append(menuview, '&View')
        
        menuhelp = wx.Menu()
        menuhelp.Append(30,'&How To Use?')
        menuhelp.Append(31,'&About')
        menubar.Append(menuhelp, '&Help')

        self.sudokupanel = SudokuPanel(self)
        self.sidepanel = SidePanel(self, self.sudokupanel)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.sudokupanel, proportion=1, border=10,
          flag=wx.SHAPED|wx.ALIGN_CENTER_HORIZONTAL|\
          wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        sizer.Add(self.sidepanel, flag=wx.EXPAND|wx.ALL,
          proportion=0, border=10)
        self.SetSizer(sizer)

        # Set size of frame according to screen size.
        displayrect = wx.Display().GetClientArea()
        sizey = (displayrect[3]-displayrect[0])*4/5
        sizex = sizey + self.sidepanel.GetClientSize()[0]
        size = (sizex, sizey)
        self.SetSize(size)

        # Set an icon (should work on both Windows and Linux platforms).
        path = os.path.join(os.path.dirname(__file__), "pics",
          "Sudoku Solver.ico")
        icon = wx.Icon(path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Bind events.
        self.Bind(wx.EVT_MENU, self.OnExit, id=0)
        self.Bind(wx.EVT_MENU, self.OnShowSolution, id=10)
        self.Bind(wx.EVT_MENU, self.OnFullscreen, id=20)
        self.Bind(wx.EVT_MENU, self.OnHowToUse, id=30)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=31)

        # Initialization
        menubar.Check(10,1)

    def OnExit(self, *args):
        """Safely exit the app."""
        self.Close(True)            # this triggers the window close event.

    def OnShowSolution(self, *args):
        if args[0].IsChecked():
            print 'Solution ON  [slow]'
        else:
            print 'Solution OFF [fast]'

    def OnFullscreen(self, *args):
        """Span the entire screen, hiding even taskbars."""
        self.ShowFullScreen(args[0].IsChecked(), style=wx.FULLSCREEN_ALL)

    def OnHowToUse(self, *args):
        """Show the How To Use dialog box."""
        strhowtouse = \
        "How to enter numbers in the grid?\n"\
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
        "buttons Save, Revert and Clear.\n"
        howtousebox = wx.MessageDialog(self, strhowtouse,
          caption='How To Use?', style=wx.OK)
        howtousebox.ShowModal()
        howtousebox.Destroy()

    def OnAbout(self, *args):
        """Show the About dialog box."""
        strabout = "Sudoku Solver 1.2\n" \
                   "(Update: July 2011)\n\n" \
                   "Made by Pushpak Dagade\n(May-June 2011)\n" \
                   "\nhttp://guanidene.blogspot.com"
        aboutbox = wx.MessageDialog(self, strabout,
          caption='About', style=wx.OK)
        aboutbox.ShowModal()
        aboutbox.Destroy()

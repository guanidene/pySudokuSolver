# sudokucell.py    [Sudoku Solver 1.2]
# -*- coding: UTF-8 -*-

"""This is a very important module contributing to both gui and logic.
The attribute LabelsRestrictionCount of the class SudkouCell is a very
important attribute in the working of this app."""

__author__ = "Pushpak Dagade (पुष्पक दगड़े)"
__date__   = "$May 21, 2011 7:33:59 PM$"

import wx
import wx.lib.stattext as stattext

class SudokuCell(stattext.GenStaticText):
    """Instances of this class will act as (graphical) containers for
    labels. Scrolling on an instance will rotate through its permissible
    labels"""
    
    # Define constants common to all the instances of the class here.
    
    Labels = ('','1','2','3','4','5','6','7','8','9')
    # You can modify the tuple 'Labels' in such a way that -
    # 1. Its consists of exactly 10 elements.
    # 2. Its first element is necessarily a '' (an empty string).
    # 3. All other 9 elements are also strings.
    # Ex. Labels = ('','A','B','C','D','E','F','G','H','I') will work.

    font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
    SizeDefault = (5,5)
    # XXX. When resizing the main window (sudokuframe) at runtime,
    # if the size of a Sudokucell instance decreases below 'SizeDefault',
    # it loses its boundary (I don't know why), hence keeping 'SizeDefault'
    # to be small.

    def __init__(self, parent, posx, posy):
        """
        """
        """The attribute LabelsRestrictionsCount is a very important attribute
        of this class. It is a dictionary object whose keys (string) are the
        items of the tuple SudokuCell.Labels and their values (int) represent
        the number of restrictions on them. These values are initialized to 0.
        This attribute helps the method SetSudokuCellLabel of the class
        SudokuPanel to decide whether or not a Label can be set to a
        sudokucell depending on the value corresponding to the key-Label
        (in the dict LabelsRestrictionsCount). If this value is greater than
        0, then it means that there is a restriction on setting the Label to
        the sudokucell (because some other sudokucell in its row, col or box
        has the same label and setting the same label more than once in
        a row,col or box is not permissible according to the rules of the game)
        and so the method SetSudokuCellLabel will not allow setting this
        label on the sudokucell.
        The first key of this dict '' (an empty string) is a special key,
        whose corresponding value needs to be kept 0 always. This is because
        there can be any number of 'empty' sudokucells in a row, col or box
        ie there is no restriction on keeping a sudokucell empty.

        Thus, this attribute (of every sudokucell) in conjunction with
        SetSudokuCellLabel method help in following the game rules tightly.

        Note: The values of the dict LabelRestrictionsCount attribute
        does not always represent the 'exact' no of restrictions, many a
        times it represents more than the actual number of restrictions (but
        never less), but this does not affect the working!
        (The reason for this is documentated in the SetSudokuCellLabel method
        of the class SudokuPanel.)

        """
        super(self.__class__, self).__init__(parent, -1, '',
          size = SudokuCell.SizeDefault,
          style = wx.ALIGN_CENTER|wx.SIMPLE_BORDER|wx.ST_NO_AUTORESIZE)
        # XXX. This declaration does not work for
        # Windows7 for some reason. It works only when wx.SIMPLE_BORDER
        # is removed. And even if it removed, the app doesn't look as it
        # looks on Ubuntu(Linux)

        # Attributes
        self.posx = posx
        self.posy = posy
        self.previous_font_sizex = 0
        self.LabelRestrictionsCount = dict(zip(SudokuCell.Labels,
                                      [0]*len(SudokuCell.Labels)))
        # The above statement is equivalent to - 
        # self.LabelRestrictionsCount = {'':0,'1':0,'2':0,'3':0,'4':0,
        #                               '5':0,'6':0,'7':0,'8':0,'9':0}
        # Although the former has lesser clarity, you won't have to change
        # it even if you change  SudokuCell.Labels which you will have to
        # change in the later case.

        # XXX. How to center the text vertically?

        # Bind events.
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseScroll)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

    def IsEmpty(self):
        """Return 1 if label is '' (empty string) else return 0."""
        return self.GetLabel() == ''

    def IsFilled(self):
        """Return not self.IsEmpty()."""
        return not self.GetLabel() == ''

    def IsLabelPermissible(self, label):
        """Return 1 if value of the key 'label' in the dict
        LabelsRestrictionsCount is 0 else return 0. If 'label'
        is not a key in the dict LabelRestrictionsCount then
        return 0."""
        label = str(label).strip()
        try:
            return self.LabelRestrictionsCount[label] == 0
        except Exception:
            # will get an exception if label not in self.LabelRestrictionsCount
            print '[Got label "%s" which is not in SudokuCell.Labels]' \
                  %label, sys.stderr
            return 0
        
    def LabelsPermissible(self):
        """Return a tuple of labels whose corresponding
        values in the dict LabelRestrictionsCount is 0."""
        # Note: This will always return '' (empty string)
        # as its 1st permissible label.
        return tuple([label for label in self.LabelRestrictionsCount
          if self.LabelRestrictionsCount[label] == 0])

    def OnResize(self, *args):
        """Scale the font according to the (new) size of the widget."""
        # XXX. When the parent frame is resized, the resize event gets
        # called 4 times. This unnecessarily slows up the resizing and
        # thus the startup of the program.
        # Solution: Inorder to tackle this, am checking while resizing
        # if the size has changed and am resizing only if the size has
        # really changed.
        # Note: size of cell font is cell_size*4/3 (= integer). So, for
        # example, if cell size initially was 58 and now it is 59,
        # the font size in both the case will be same (58/4*3 = 42 =
        # 59*4/3). Hence, if the size of the cell changes, the font
        # size should be changed only if cell_size/4*3 is different
        # initially and finally.

        new_font_sizex = int(args[0].GetSize()[0])/4*3
        if not new_font_sizex == self.previous_font_sizex:
            sizex = new_font_sizex         # Rem. sizex still will be an int
            SudokuCell.font.SetPixelSize((sizex, sizex))
            self.SetFont(SudokuCell.font)
            self.previous_font_sizex = new_font_sizex

    def OnMouseScroll(self, *args):
        """Set labels to the sudokucell through the list
        of its permissible labels in a rotating fashion.

        If the scroll event is a scroll up event, then set the next label
        from the list of permissible labels else set the previous label
        in the list if the scroll event is a scroll down event.

        """
        labels = list(SudokuCell.Labels)
        index = labels.index(self.GetLabel())
        labels = labels[index+1:] + labels[:index]

        # If wheelup, try increment, else if wheeldown, try decrement
        if args[0].GetWheelRotation() < 0: labels.reverse()
        for key in labels:
            if self.LabelRestrictionsCount[key] == 0:
                self.GetParent().SetSudokuCellLabel(self, key)
                break

    def OnEnterWindow(self, *args):
        """Magnify the font (size) of the sudokucell when mouse enters."""
        size = self.GetSize()
        font = self.GetFont()
        font.SetPixelSize(size)
        self.SetFont(font)
        
    def OnLeaveWindow(self, *args):
        """Restore the font size of the sudokucell when mouse leaves."""
        self.SetFont(SudokuCell.font)

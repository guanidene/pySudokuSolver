# sudokupanel.py    [Sudoku Solver 1.2]
# -*- coding: UTF-8 -*-

"""This is a very important module contributing to both gui and logic.
The method SetSudokuCellLabel of the class SudkouPanel is the most
important (and the most difficult to understand) method of this module."""

__author__ = "Pushpak Dagade (पुष्पक दगड़े)"
__date__   = "$May 21, 2011 7:34:23 PM$"

import wx
from sudokucell import SudokuCell

class SudokuPanel(wx.Panel):
    """Instance of this class which act as container for
    all instances of the class SudokuCell."""

    def __init__(self, parent):
        super(self.__class__, self).__init__(parent, -1)

        # Create children widgets.
        self.sudokucells = tuple([ [SudokuCell(self, cellx, celly)
          for celly in xrange(9)] for cellx in xrange(9) ])

        sizer = wx.GridSizer(9,9)
        for sudokucell in self: sizer.Add(sudokucell, flag=wx.SHAPED)
        self.SetSizer(sizer)
        sizer.Fit(self)

        # Set appearance.
        self.SetAppearance()

    def __iter__(self):
        return (sudokucell for cellrow in self.sudokucells
                           for sudokucell in cellrow)

    def SetAppearance(self, appearance='maze green'):
        """Set appearance of sudokucells.

        Giving a definite pattern of background colours to the sudokucells
        helps in easily identifying the 9 '3x3 grids' of sudokucells.

        Keyword arguments:
        appearance -- string, can take either of these values -->
                              'maze green' (default), 'maze blue'

        """
        appearance = appearance.strip()

        if appearance == 'maze green':
            bgcolour1 = '#E5EBDD'       # light greenish
            bgcolour2 = 'White'
        elif appearance == 'maze blue':
            bgcolour1 = '#E8FFFF'       # light bluish
            bgcolour2 = 'White'
        # More appearances can be added. Don't forget to add
        # these appearances in the above docstring.

        for sudokucell in self:
            if sudokucell.posx in (0,1,2) and sudokucell.posy in (0,1,2) or\
               sudokucell.posx in (0,1,2) and sudokucell.posy in (6,7,8) or\
               sudokucell.posx in (3,4,5) and sudokucell.posy in (3,4,5) or\
               sudokucell.posx in (6,7,8) and sudokucell.posy in (0,1,2) or\
               sudokucell.posx in (6,7,8) and sudokucell.posy in (6,7,8) :
                sudokucell.SetBackgroundColour(bgcolour1)
            else:
                sudokucell.SetBackgroundColour(bgcolour2)

    def IsGridEmpty(self):
        """Return 1 if grid is empty else return 0."""
        for sudokucell in self:
            if not sudokucell.IsEmpty(): return 0
        return 1

    def IsPuzzleComplete(self):
        """Return 1 if puzzle is complete and 0 if not complete.

        Note: If puzzle is complete then it cannot be incorrect,
        it will definately be correct (thanks to the mechanism
        employed in the SetSudokuCellLabel method of this class).
        
        """
        for sudokucell in self:
            if sudokucell.IsEmpty(): return 0
        return 1

    def IsPuzzleCorrect(self):
        """Return 0 if puzzle is (definately) incorrect else return 1.

        Note: The name of this method is a bit disguised.
        If it returns 1 it does not necessarily mean that puzzle is
        correct, only it means that it seems to be correct. It is quite 
        possible that as it is solved further, you will find that it is an
        incorrect puzzle. 
        But if it returns 0 then the puzzle is definately incorrect!

        So, this method is useful only if it returns 0.

        """
        # The puzzle can be incorrect only when there is atleast one
        # child sudokucell which has no permissible label other than
        # a '' (blank) (in this case the value of
        # len(sudokucell.LabelsPermissible()) is 1.
        for sudokucell in self:
            if sudokucell.IsEmpty() and \
              len(sudokucell.LabelsPermissible()) == 1:
                return 0
        return 1

    def ClearPuzzle(self):
        """Set every child SudokuCells' label to '' (empty string)"""
        for sudokucell in self: self.SetSudokuCellLabel(sudokucell, '')

    def GetPuzzle(self):
        """Return a tuple of labels of all child sudokucells"""
        return tuple([sudokucell.GetLabel() for sudokucell in self])

    def SetPuzzle(self, SavedData=None):
        """Set a puzzle according to the data in 'SavedData'.
        If there is no data in SavedData, just clear the grid."""        

        # You cannot directly set the labels because the mechanism of
        # SetSudokuCellLabel method prevents same labels in a row, col or
        # box of the Sudoku grid (which can occur if the grid is already
        # partially/completely filled and you are trying to set the labels
        # according to SavedData without). Hence, we have to clear the
        # puzzle first.
        self.ClearPuzzle()

        try:
            i = 0
            for sudokucell in self:
                self.SetSudokuCellLabel(sudokucell, SavedData[i])
                i += 1
        except Exception:
            # will get an exception if there is no data in SavedData.
            pass

    def GetSudokuCellsInRow(self, sudokucell):
        """Return a tuple of all child sudokucells
        in the same row as that of 'sudokucell'

        Length of tuple will be 8 (not 9, as 'sudokucell'
        will not be returned).

        """
        sudokucells = [self.sudokucells[sudokucell.posx][i] for i in xrange(9)]
        sudokucells.remove(sudokucell)
        return tuple(sudokucells)

    def GetSudokuCellsInCol(self, sudokucell):
        """Return a tuple of all child sudokucells
        in the same box as that of 'sudokucell'

        Length of tuple will be 8 (not 9, as 'sudokucell'
        will not be returned).

        """
        posy = sudokucell.posy
        sudokucells = [self.sudokucells[i][posy] for i in xrange(9)]
        sudokucells.remove(sudokucell)
        return tuple(sudokucells)

    def GetSudokuCellsInBox(self, sudokucell):
        """Return a tuple of all child sudokucells
        in the same box as that of 'sudokucell'

        Length of tuple will be 8 (not 9, as 'sudokucell'
        will not be returned).

        """
        # This is a bit abstract but concise way of getting
        # indices of required sudokucells.
        posx = sudokucell.posx
        posy = sudokucell.posy
        row_list = [posx/3*3+0, posx/3*3+1, posx/3*3+2]   # posx/3 is integer
        col_list = [posy/3*3+0, posy/3*3+1, posy/3*3+2]   # posy/3 is integer
        sudokucells = []
        for row in row_list:
            for col in col_list:
                sudokucells.append(self.sudokucells[row][col])
        sudokucells.remove(sudokucell)
        
        return tuple(sudokucells)

    def SetSudokuCellLabel(self, sudokucell, label):
        """Set 'label' to 'sudokucell', if possible.

        ===================
        Keyword arguments:
        ===================
        sudokucell -- SudokuCell, on which 'label' is to be set
        label -- string, which is to be assigned to 'sudokucell'

        ==============
        Return value:
        ==============
        0 -- failed to set 'label', either because already some other
             sudokucell in its row, col or box has it or because
             it is not in the SudokuCell.Labels
        1 -- successfully set 'label' to 'sudokucell'.
        """
        """
        Note: The values of the dict LabelRestrictionsCount attribute
        of sudokucells does not
        always represent the "exact" no of restrictions, many a times it
        represents more than the actual number of restrictions (but
        never less), but this does not affect the working!
        (How and Where this happens is explained further along with
        the code below)
        [To see the purpose of the 'LabelRestrictionsCount' attribute of
        sudokucells, refer to the class SudokuCell for its description.]

        Procedure: If 'label' is same as sudokucell's current label then
        ignore. Else, if 'label' is permissible to be set in 'sudokucell'-->
        1.If sudkoucell's current label is not '' (empty string), then
          decrease the count corresponding to sudokucell's current label
          by 1 from all sudokucells in its row, col and box (except from
          itself).
          [This is the step when sudokucells common in sudokucell's
          row, col & box will get their count corresponding to sudokucell's
          current label decreased by "more than 1". However, this is not a
          matter of concern as this effect is compensated by the next
          step. Hence, LabelRestrictionsCount does not represent the
          "exact" no of restrictions.]
        2.If label is not '' (empty string) then 
          increase the count corresponding to 'label' by 1 from all cells
          in its row, col and box (except for itself).
          [Again, this is the step when sudokucells common in sudokucell's
          row, col & box will get their count corresponding to
          'label' increased by "more than 1". However, this is not a
          matter of concern as this effect is compensated by the 1st
          step. Hence, LabelRestrictionsCount does not represent the
          "exact" no of restrictions.]
        3. Finally, set 'label' to 'sudokucell'

        In points 1. and 2. above checks have been made  if either 'label' or
        sudokucell's current label is '' (empty string) because its mandatory
        to keep the value of the key ''(empty string) of the dict
        SudokuCell.LabelRestrictionsCount to 0 always.
        (Reason for this is given in the class SudokuCell)
        
        If 'label' is not permissible to be set in 'sudokucells',
        print it as an error.
        
        """
        
        current_label = sudokucell.GetLabel()
        label = str(label).strip()
        if label == current_label: return 1

        if label in sudokucell.LabelRestrictionsCount and \
          sudokucell.LabelRestrictionsCount[label] == 0:

            sudokucells_list = self.GetSudokuCellsInRow(sudokucell) + \
                               self.GetSudokuCellsInCol(sudokucell) + \
                               self.GetSudokuCellsInBox(sudokucell)

            # Decrease the current_label count by 1 from all the cells
            # in its row,col and box (except if label is '')
            if current_label != '':
                for _sudokucell in sudokucells_list:
                    _sudokucell.LabelRestrictionsCount[current_label] -= 1

            # Increase the label count by 1 from all the cells
            # in its row,col and box (except for '')
            if label != '':
                for _sudokucell in sudokucells_list:
                    _sudokucell.LabelRestrictionsCount[label] += 1

            sudokucell.SetLabel(label)
            return 1                # success
        
        else:
            # Don't raise an exception, just print the error.
            print '[Trouble] Failed setting label-\n %s in cell (%d,%d)' \
              %(label, sudokucell.posx+1, sudokucell.posy+1)
            return 0                # failure

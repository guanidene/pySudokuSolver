# -*- coding: UTF-8 -*-

"""
This is a very important module contributing to both gui and logic.
The method setSudokuCellLabel of the class SudokuGrid is the most
important (and the most difficult to understand) method of this module.
"""

__author__ = u"पुष्पक दगड़े (Pushpak Dagade)"

from PyQt4 import QtGui
from sudokucell import SudokuCell


class SudokuGrid(QtGui.QFrame):
    """Instance of this class which act as container for
    all instances of the class SudokuCell."""

    def popululateSudokucells(self):
        # Let every sudokucell know its position w.r.t. the entire grid
        for sudokucell in self.findChildren(SudokuCell):
            sudokucell.savePosition()

        # need to arrange sudokucells in a 2d tuple, such that their indexes
        # match their (posx, posy) tuple
        all_sudokucells = sorted(self.findChildren(SudokuCell),
            key=lambda sudokucell: (sudokucell.posx, sudokucell.posy))
        self.sudokucells = tuple([all_sudokucells[x:x + 9]
                                 for x in xrange(0, len(all_sudokucells), 9)])

    # fixed
    def __iter__(self):
        return (sudokucell for cellrow in self.sudokucells
                for sudokucell in cellrow)

    def isGridEmpty(self):
        """Return 1 if grid is empty else return 0."""
        for sudokucell in self:
            if not sudokucell.isEmpty():
                return 0
        return 1

    def isPuzzleComplete(self):
        """Return 1 if puzzle is complete and 0 if not complete.

        Note: If puzzle is complete then it cannot be incorrect,
        it will definately be correct (thanks to the mechanism
        employed in the setSudokuCellLabel method of this class).

        """
        for sudokucell in self:
            if sudokucell.isEmpty():
                return 0
        return 1

    def isPuzzleCorrect(self):
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
            if sudokucell.isEmpty() and \
              len(sudokucell.labelsPermissible()) == 1:
                return 0
        return 1

    def clearPuzzle(self):
        """Set every child SudokuCells' label to '' (empty string)"""
        for sudokucell in self:
            self.setSudokuCellLabel(sudokucell, '')

    def getPuzzle(self):
        """Return a tuple of labels of all child sudokucells"""
        return tuple([sudokucell.text() for sudokucell in self])

    def setPuzzle(self, SavedData=None):
        """Set a puzzle according to the data in 'SavedData'.
        If there is no data in SavedData, just clear the grid."""

        # You cannot directly set the labels because the mechanism of
        # setSudokuCellLabel method prevents same labels in a row, col or
        # box of the Sudoku grid (which can occur if the grid is already
        # partially/completely filled and you are trying to set the labels
        # according to SavedData without). Hence, we have to clear the
        # puzzle first.
        self.clearPuzzle()

        try:
            i = 0
            for sudokucell in self:
                self.setSudokuCellLabel(sudokucell, SavedData[i])
                i += 1
        except Exception:
            # will get an exception if there is no data in SavedData.
            pass

    def getSudokuCellsInRow(self, sudokucell):
        """Return a tuple of all child sudokucells
        in the same row as that of 'sudokucell'

        Length of tuple will be 8 (not 9, as 'sudokucell'
        will not be returned).

        """
        sudokucells = [self.sudokucells[sudokucell.posx][i] for i in xrange(9)]
        sudokucells.remove(sudokucell)
        return tuple(sudokucells)

    def getSudokuCellsInCol(self, sudokucell):
        """Return a tuple of all child sudokucells
        in the same box as that of 'sudokucell'

        Length of tuple will be 8 (not 9, as 'sudokucell'
        will not be returned).

        """
        posy = sudokucell.posy
        sudokucells = [self.sudokucells[i][posy] for i in xrange(9)]
        sudokucells.remove(sudokucell)
        return tuple(sudokucells)

    def getSudokuCellsInBox(self, sudokucell):
        """Return a tuple of all child sudokucells
        in the same box as that of 'sudokucell'

        Length of tuple will be 8 (not 9, as 'sudokucell'
        will not be returned).

        """
        # This is a bit abstract but concise way of getting
        # indices of required sudokucells.
        posx = sudokucell.posx
        posy = sudokucell.posy
        row_list = [posx / 3 * 3 + 0, posx / 3 * 3 + 1, posx / 3 * 3 + 2]
        col_list = [posy / 3 * 3 + 0, posy / 3 * 3 + 1, posy / 3 * 3 + 2]
        sudokucells = []
        for row in row_list:
            for col in col_list:
                sudokucells.append(self.sudokucells[row][col])
        sudokucells.remove(sudokucell)

        return tuple(sudokucells)

    def setSudokuCellLabel(self, sudokucell, label):
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

        current_label = sudokucell.text()
        label = str(label).strip()
        if label == current_label:
            return 1

        if label in sudokucell.LabelRestrictionsCount and \
          sudokucell.LabelRestrictionsCount[label] == 0:

            sudokucells_list = self.getSudokuCellsInRow(sudokucell) + \
                self.getSudokuCellsInCol(sudokucell) + \
                self.getSudokuCellsInBox(sudokucell)

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

            sudokucell.setText(label)
            return 1                # success

        else:
            # Don't raise an exception, just print the error.
            print '[Trouble] Failed setting label-\n %s in cell (%d,%d)' \
                  % (label, sudokucell.posx + 1, sudokucell.posy + 1)
            return 0                # failure

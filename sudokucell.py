# -*- coding: UTF-8 -*-

"""This is a very important module contributing to both gui and logic.
The attribute LabelsRestrictionCount of the class SudkouCell is a very
important attribute in the working of this app."""

__author__ = u"पुष्पक दगड़े (Pushpak Dagade)"

import sys
from PyQt4 import QtGui


class SudokuCell(QtGui.QLabel):
    """Instances of this class will act as (graphical) containers for
    labels. Scrolling on an instance will rotate through its permissible
    labels"""

    # Define constants common to all the instances of the class here.

    Labels = ('', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    # You can modify the tuple 'Labels' in such a way that -
    # 1. Its consists of exactly 10 elements.
    # 2. Its first element is necessarily a '' (an empty string).
    # 3. All other 9 elements are also strings.
    # Ex. Labels = ('','A','B','C','D','E','F','G','H','I') will work.

    # Font size, relative to cell size, when mouse pointer
    # enters & leaves the cell respectively
    FONT_SIZE_FACTOR_MOUSE_OVER = 1.0
    FONT_SIZE_FACTOR_NORMAL = 0.8

    def __init__(self, *args, **kwargs):
        """
        """
        """The attribute LabelsRestrictionsCount is a very important attribute
        of this class. It is a dictionary object whose keys (string) are the
        items of the tuple SudokuCell.Labels and their values (int) represent
        the number of restrictions on them. These values are initialized to 0.
        This attribute helps the method setSudokuCellLabel of the class
        SudokuPanel to decide whether or not a Label can be set to a
        sudokucell depending on the value corresponding to the key-Label
        (in the dict LabelsRestrictionsCount). If this value is greater than
        0, then it means that there is a restriction on setting the Label to
        the sudokucell (because some other sudokucell in its row, col or box
        has the same label and setting the same label more than once in
        a row,col or box is not permissible according to the rules of the game)
        and so the method setSudokuCellLabel will not allow setting this
        label on the sudokucell.
        The first key of this dict '' (an empty string) is a special key,
        whose corresponding value needs to be kept 0 always. This is because
        there can be any number of 'empty' sudokucells in a row, col or box
        ie there is no restriction on keeping a sudokucell empty.

        Thus, this attribute (of every sudokucell) in conjunction with
        setSudokuCellLabel method help in following the game rules tightly.

        Note: The values of the dict LabelRestrictionsCount attribute
        does not always represent the 'exact' no of restrictions, many a
        times it represents more than the actual number of restrictions (but
        never less), but this does not affect the working!
        (The reason for this is documentated in the setSudokuCellLabel method
        of the class SudokuPanel.)

        """
        super(self.__class__, self).__init__(*args, **kwargs)

        self.LabelRestrictionsCount = dict(zip(SudokuCell.Labels,
                                               [0] * len(SudokuCell.Labels)))
        # The above statement is equivalent to -
        # self.LabelRestrictionsCount = {'':0,'1':0,'2':0,'3':0,'4':0,
        #                               '5':0,'6':0,'7':0,'8':0,'9':0}
        # Although the former has lesser clarity, you won't have to change
        # it even if you change  SudokuCell.Labels which you will have to
        # change in the later case.

    def savePosition(self):
        """Get the x and y positions of the cell w.r.t the entire grid"""
        # Created a separate method for this task, since objectName is not
        # availabe during initialization of the QLabel

        # assuming name of SudokuCell class instances is of format label_x_y
        # where, x=row index of SudokuCell &
        #        y=col index of SudokuCell
        self.posx = int(self.objectName()[-3])
        self.posy = int(self.objectName()[-1])

        # Note:
        # The following could be a more better way to do the above task:
        # One can get the position of a wiget in its parent layout; this can be
        # used to directly get the x and y positions; This will help avoid
        # setting objectNames for every label individually.

    def isEmpty(self):
        """Return 1 if label is '' (empty string) else return 0."""
        return self.text() == ''

    def isFilled(self):
        """Return not self.isEmpty()."""
        return not self.text() == ''

    def isLabelPermissible(self, label):
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
                  % label, sys.stderr
            return 0

    def labelsPermissible(self):
        """Return a tuple of labels whose corresponding
        values in the dict LabelRestrictionsCount is 0."""
        # Note: This will always return '' (empty string)
        # as its 1st permissible label.
        return tuple([label for label in self.LabelRestrictionsCount
                     if self.LabelRestrictionsCount[label] == 0])

    def resizeEvent(self, evt):
        """Scale the font according to the (new) size of the widget."""
        font = self.font()
        font.setPixelSize(SudokuCell.FONT_SIZE_FACTOR_NORMAL *
                          min(self.height(), self.width()))
        self.setFont(font)

    def wheelEvent(self, event):
        """
        Set labels to the sudokucell through the list
        of its permissible labels in a rotating fashion.

        If the scroll event is a scroll up event, then set the next label
        from the list of permissible labels else set the previous label
        in the list if the scroll event is a scroll down event.
        """
        labels = list(SudokuCell.Labels)
        index = labels.index(self.text())
        labels = labels[index + 1:] + labels[:index]

        # If wheelup, try increment, else if wheeldown, try decrement
        if event.delta() < 0:
            labels.reverse()
        for key in labels:
            if self.LabelRestrictionsCount[key] == 0:
                self.parent().setSudokuCellLabel(self, key)
                break

    def enterEvent(self, event):
        """Increase the font size of the sudokucell & make it bold when
           mouse enters."""
        font = self.font()
        font.setPixelSize(SudokuCell.FONT_SIZE_FACTOR_MOUSE_OVER *
                          min(self.height(), self.width()))
        font.setBold(True)
        self.setFont(font)

    def leaveEvent(self, event):
        """Restore the font size of the sudokucell when mouse leaves."""
        font = self.font()
        font.setPixelSize(SudokuCell.FONT_SIZE_FACTOR_NORMAL *
                          min(self.height(), self.width()))
        font.setBold(False)
        self.setFont(font)

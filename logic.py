# -*- coding: UTF-8 -*-

"""This module is the powerhouse of this app! The functions in this module
determine the performance of this app. These functions are not easy to
understand in one single reading.

Solving a Sudoku puzzle requires two approaches -
    1. Solving it exactly, with no assumptions.
       In this approach, we try to fill the puzzle 'exactly' as far as
       possible. This is the simplest approach and the puzzle won't be
       significantly solved in most cases.
    2. Solving it using assumptions.
       When unable to solve any further using the 1st approach, we resort
       to this approach. In this, we make an assumption. Then try to solve
       it further using the 1st approach.
       Sometimes, we have to take assumptions over assumptions which makes
       things more complicated.

    To see the steps taken in solving, refer to documentations of the
        functions Step1 and Stepk

Note: This module is completely independent , ie it does not depends on any
function/attribute defined in any other modules
(unlike in its previous version --> Sudoku Solver 1.0)

"""

__author__ = u"पुष्पक दगड़े (Pushpak Dagade)"
__date__ = "Jul 17, 2011 9:49:42 PM"

# SOLUTION by Sudoku Solver -
# Providing a good solution is an important aspect of Sudoku Solver.
# The solution should be good on visibility as well as easy to understand.
# As a part of visibility, keep the maximum character width per line
# to be 25 (which is per line character width of a puzzle printed by the
# function PrintPuzzle()).


# TODOS:
# 1. printing directly to stdout is not be the best way. Need to make it
#    flexible, ie. should allow printing to stdout or a file or txtbrwSolutions
#    but, without, compromising on the speed (use "timeit" to characterise).

from copy import deepcopy

SudokuPuzzle = [[''] * 9 for i in xrange(9)]                # an empty puzzle
LabelRestrictionsCount = [[[0] * 10 for i in xrange(9)] for j in xrange(9)]
Labels = ('', '1', '2', '3', '4', '5', '6', '7', '8', '9')


def ReadPuzzleFromString(str_puzzle):
    """
    Read the puzzle from the string str_puzzle, and store it as
    a 2D array of characters in the variable SudokuPuzzle.

    (Note. str_puzzle will have empty cells represented as '.').
    However, store '.' in str_puzzle as '' (empty character)
    in the array SudokuPuzzle (why to waste space unnecessarily?)
    """
    for i, ch in enumerate(str_puzzle.split()):
        row = i / 9
        col = i % 9
        if ch == '.':
            setSudokuCellLabel(row, col, '')
        else:
            setSudokuCellLabel(row, col, ch)


def WritePuzzleToString():
    """
    Write the puzzle in the 2D array SudokuPuzzle to the string str_puzzle
    converting empty cells (ie cells containing '') to '.' in the string.
    """
    str_solution_puzzle = ""
    for row in xrange(9):
        for col in xrange(9):
            if (SudokuPuzzle[row][col] == ''):
                str_solution_puzzle += '.'
            else:
                str_solution_puzzle += SudokuPuzzle[row][col]
            str_solution_puzzle += ' '

    return str_solution_puzzle


def PrintPuzzle():
    """
    Print the puzzle stored in the variable SudokuPuzzle in nice
    readable format.
    """
    # (Performance of this funtion is crucial to the performance of this app.)
    # (Try improving it.)
    sep = "+-------+-------+-------+"
    print "\n%s" % sep
    for row in xrange(9):
        print "|",
        for col in xrange(9):
            if (SudokuPuzzle[row][col] == ''):
                print ".",                           # print empty cells as '.'
            else:
                print "%s" % SudokuPuzzle[row][col],
            if (col == 2 or col == 5):
                print "|",
        print "|"
        if (row == 2 or row == 5):
            print sep
    print "%s\n" % sep


def GetLabelIndex(label):
    """
    Search for label in the global constant Labels and return its
    corresponding index. If not found, return -1.
    """
    try:
        return Labels.index(label)
    except ValueError:
        print "![Trouble] label: '%s' not in global const Labels!" % label
        return -1


def isPuzzleComplete():
    """
    Return 1 if puzzle is complete and 0 if not complete.

    Note: If puzzle is complete then it cannot be incorrect,
    it will definately be correct (thanks to the mechanism
    employed in the setSudokuCellLabel method of this class).
    """
    for row in xrange(9):
        for col in xrange(9):
            if SudokuPuzzle[row][col] == '':
                return 0
    return 1


def IsCellEmpty(row, col):
    """Return 1 if label is '' (empty string) else return 0."""
    return SudokuPuzzle[row][col] == ''


def IsLabelPermissible(row, col, label):
    """Return 1 if value of the key 'label' in the dict
    LabelsRestrictionsCount is 0 else return 0.

    Note: If 'label' is not in global constant 'Labels' then this
    won't produce any error, as GetLabelIndex would simply return
    -1. However, GetLabelIndex will give an error for this.

    """
    return LabelRestrictionsCount[row][col][GetLabelIndex(label)] == 0


def lenLabelsPermissible(row, col):
    """Return the number of permissible labels for the cell in (row,col)

    Note: '' (empty string) will always be a permissible label for any cell
    so minimum value returned by this function will be 1.

    """
    count = 0
    for i in xrange(10):    # 10 is the length of the constant 'Labels'
        if LabelRestrictionsCount[row][col][i] == 0:
            count += 1
    return count


def isPuzzleCorrect():
    """Return 0 if puzzle is (definately) incorrect else return 1.

    Note: The name of this method is a bit disguised.
    If it returns 1 it does not necessarily mean that puzzle is
    correct, only it means that it seems to be correct. It is quite
    possible that as it is solved further, you will find that it is an
    incorrect puzzle.
    But if it returns 0 then the puzzle is definately incorrect!

    So, this method is useful only if it returns 0.

    """
    for row in xrange(9):
        for col in xrange(9):
            if IsCellEmpty(row, col) and (lenLabelsPermissible(row, col) == 1):
                return 0
    return 1


def GetPermissibleLabels(row, col, n):
    """
    Return at the most n permissible labels. Will NOT return '' (empty str)
    as it will always be permissible for any cell.
    """
    count = 0
    labels = []
    for i in xrange(1, 10):     # Start i from 1 so as to skip ''
        if count >= n:
            break
        if IsLabelPermissible(row, col, Labels[i]):
            labels += Labels[i]
            count += 1
    return labels


def setSudokuCellLabel(row, col, label):
    """See the docstring for sudokupanel.SudokuPanel.setSudokuCellLabel"""
    global SudokuPuzzle
    global LabelRestrictionsCount

    current_label = SudokuPuzzle[row][col]
    if label == current_label:
        return 1

    if LabelRestrictionsCount[row][col][GetLabelIndex(label)] == 0:
        # for cells in same row (except for itself) -
        for row_ in xrange(9):
            if row_ != row:
                if current_label != '':
                    LabelRestrictionsCount[row_][col] \
                        [GetLabelIndex(current_label)] -= 1

                if label != '':
                    LabelRestrictionsCount[row_][col] \
                        [GetLabelIndex(label)] += 1

        # for cells in same col (except for itself) -
        for col_ in xrange(9):
            if col_ != col:
                if current_label != '':
                    LabelRestrictionsCount[row][col_] \
                        [GetLabelIndex(current_label)] -= 1

                if label != '':
                    LabelRestrictionsCount[row][col_] \
                        [GetLabelIndex(label)] += 1

        # for cells in same box (except for itself) -
        for row_ in (row / 3 * 3, row / 3 * 3 + 1, row / 3 * 3 + 2):
            for col_ in (col / 3 * 3, col / 3 * 3 + 1, col / 3 * 3 + 2):
                if not ((row_ == row) and (col_ == col)):
                    if current_label != '':
                        LabelRestrictionsCount[row_][col_] \
                            [GetLabelIndex(current_label)] -= 1

                    if label != '':
                        LabelRestrictionsCount[row_][col_] \
                            [GetLabelIndex(label)] += 1

        SudokuPuzzle[row][col] = label
        return 1
    else:
        print "[Trouble] Failed setting label-\n %s in cell (%d,%d)\n" \
              % (label, row + 1, col + 1)
        return 0


def SavePuzzle():
    """Return a deepcopy of SudokuPuzzle and LabelRestrictionsCount"""
    return deepcopy(SudokuPuzzle), deepcopy(LabelRestrictionsCount)


def LoadPuzzle(_sudokupuzzle, _labelrestrictionscount): # XXX. improve names
    global SudokuPuzzle
    global LabelRestrictionsCount

    SudokuPuzzle = deepcopy(_sudokupuzzle)
    LabelRestrictionsCount = deepcopy(_labelrestrictionscount)

#------------------------------------------------------------------------------


def printlong(character):
    print character * 25


def SolveSudokuPuzzle(str_input_puzzle, MaxAssumptionLevel=4):
    """
    Solve the puzzle in the string str_input_puzzle with MaxAssumptionLevel
    and return the solution puzzle (as a string).

    MaxAssumptionLevel = 3 can solve almost all sudoku puzzles which have a
    solution. But, just to be on a safe side, keep the MaxAssumptionLevel = 4
    (I have not found any puzzle requiring 4 or more levels of assumption
    to solve it.)
    """
    ReadPuzzleFromString(str_input_puzzle)
    PrintPuzzle()

    printlong('=')
    print "[Max Assumptions: %d]\n" % MaxAssumptionLevel
    SolveUptoSteps(MaxAssumptionLevel + 1)
    printlong('=')

    str_puzzle_solution = WritePuzzleToString()

    # (XXX. Find a better 'pythonic' way to tackle the below problem)
    # Restore the global variables while exiting from this module,
    # else, if you try to solve another puzzle, the values from the previous
    # puzzle will already be in these variables, and will create problems.
    global SudokuPuzzle
    global LabelRestrictionsCount
    SudokuPuzzle = [[''] * 9 for i in xrange(9)]              # an empty puzzle
    LabelRestrictionsCount = [[[0] * 10 for i in xrange(9)] for j in xrange(9)]

    return str_puzzle_solution


def SolveUptoSteps(MaxSteps, tree=[]):
    """Solve from steps 1 to MaxAssumptionLevel (including both)"""
    if MaxSteps == 1:
        Step1()
    else:
        Step1()

        for k in xrange(2, MaxSteps + 1):
            solved = Stepk(k, tree)
            if solved == 1:
                break


def Step1():
    """Try to solve the puzzle "exactly" (as far as possible).

    This is very first step in solving the puzzle and hence the name- 'Step1'.
    It uses 2 algorithms to solve the puzzle exactly.
    -----------------
    1st algorithm -
    -----------------
    Fill all the empty sudokucells which have only 1 permissible label
    other than '' (empty string) (ie a total of 2 permissible
    labels) with the non empty permissible label.

    -----------------
    2nd alogrithm -
    -----------------
    If a particular label (in SudokuCell.Labels) is possible in
    only one sudokucell in a row then that label is can be
    confidently set to that sudokucell. (Note: row, col and box approaches
    are all symmetric, so you can apply this rule by replacing row by
    column (or box) and you will get the same result. But there is no need
    to apply it for both row and column (and/or box) because it will
    unnecssarily waste cpu time. Just one check (either row or column
    or box) is enough (this can be proved.)) This check must be made for every
    possible label in SudokuCell.Labels (except for '' (empty string))
    in every row (or column or box, which ever you used before.)
    Once you get a sure hit, break from this algorithm immediately
    and go for the 1st algorithm (as this one is much more time
    complex.)

    The variable data_changed will let know if the puzzle has been solved
    any further in any of the two algorithms. If data_changed is 1 then loop
    will continue to cycle through algorithms 1 and 2, else it will break.

    """
    if isPuzzleComplete():
        return

    print "Solving exactly..."
    data_changed = 1

    while data_changed != 0:
        data_changed = 0

        # 1st algorithm -
        for row in xrange(9):
            for col in xrange(9):
                if IsCellEmpty(row, col) and \
                  lenLabelsPermissible(row, col) == 2:
                  # == 2 becoz 1st element is ''

                    # This part is to avoid the use of GetPermissibleLabels
                    # as it makes the solving process slightly slower.
                    for i in xrange(1, 10):       # skip the first label --> ''
                        if IsLabelPermissible(row, col, Labels[i]):
                            setSudokuCellLabel(row, col, Labels[i])
                            print "(%d,%d) --> %s" \
                                % (row + 1, col + 1, Labels[i])
                            data_changed = 1
                            break

        # This might help in improving the time complexity as the
        # 2nd alogrithm is more time complex.
        if (data_changed == 1):
            continue

        # 2nd algorithm -
        for row in xrange(9):
            for i in xrange(1, 10):  # start from i=1 to skip 1st label --> ''
                count = 0
                for col in xrange(9):
                    if IsCellEmpty(row, col) and \
                      IsLabelPermissible(row, col, Labels[i]):
                        count += 1
                        if count > 1:
                            break
                        temp_row = row
                        temp_col = col

                if count == 1:
                    setSudokuCellLabel(temp_row, temp_col, Labels[i])
                    print "(%d,%d) --> %s" \
                        % (temp_row + 1, temp_col + 1, Labels[i])
                    data_changed = 1

        # XXX. 2nd algorithm can be made more efficient by removing from
        # the variable 'labels' those labels which are already filled
        # everywhere.

    PrintPuzzle()


def Stepk(k, basetree=[]):    # XXX. make sure basetree is passed as expected.
    """Try to solve the puzzle using assumptions.

    k --> The step number. (1st step is solving exactly,
          2nd step is solving using 1 assumption,
          3rd step is solving using 2 assumptions and so on.)
    Note: The assumption level of this step will be k-1.

    basetree --> list of parent assumption levels.
                 It helps in getting the tree structure of (nested)
                 assumptions.
    Example- basetree = [3,2] --> This means that this Stepk function has been
    called (recursively) from another Stepk function (with k = 3) which was
    itself called from another Stepk function (with k = 4).

    ==============
    Return value:
    ==============
    1 - puzzle was solved in this step.
    0 - puzzle was not solved in this step.

    """
    # Note: If the puzzle being solved does not have a unique solution and
    # the parameter k is large (say 5 or more) then this function will give
    # one of the many possible solutions.
    # But whichever solution it gives, it will be definately correct!

    print "Puzzle complete?"
    if isPuzzleComplete():
        print "> Complete!"
        return 1
    else:
        print "> Not yet!"
        assumptionleveltree = basetree + [k - 1]
        print "\n(New Assumption Level.\nAssumption Tree: %s\n" \
              "Saving puzzle...)\n" % assumptionleveltree
        initialpuzzle, initiallabelrestrictionscount = SavePuzzle()

        for row in xrange(9):
            for col in xrange(9):

                # substitute for sudokucellswithonly2possibilities
                if (not (IsCellEmpty(row, col) and
                  (lenLabelsPermissible(row, col) == 3))):
                    continue # ==3 becoz 1st is a ''

                _labels = GetPermissibleLabels(row, col, 2)
                for i in (0, 1): # iterate through the permissible labels.

                    # XXX. improve this
                    if i == 0:
                        otherlabel = _labels[1]
                    else:
                        otherlabel = _labels[0]

                    print "Assuming %s in cell (%d,%d)\n[Other can be %s]\n" \
                      % (_labels[i], row + 1, col + 1, otherlabel)
                    setSudokuCellLabel(row, col, _labels[i])

                    if k != 2:
                        print "(Entering into nested\nassumption...)\n"
                    SolveUptoSteps(k - 1, assumptionleveltree)
                    if k != 2:
                        print "(Exiting from nested\nassumption...)\n"

                    print "Puzzle complete?"
                    if isPuzzleComplete():
                        # This means that the assumption taken above was
                        # correct and the puzzle got solved. Hence, return 1.
                        print "> Complete!" \
                               # add this later.. (Assumption Level Tree: %s)
                        return 1
                    else:
                        print "> Not yet!\n\nAssumption correct?"
                        if isPuzzleCorrect():
                            # This means that the puzzle is incompletely filled
                            # and it cannot be decided from this point whether
                            # the assumption taken above is correct or
                            # incorrect.
                            print "Maybe. Can't say anything\nas of now."\
                                  " Assumption was\n%s in (%d,%d)\n" \
                                  % (_labels[i], row + 1, col + 1)

                            # caching
                            if i == 0:
                                # This is caching, for speeding up the solve
                                # process. If 'label' is the 1st of the 2
                                # permissible labels then save the solution, it
                                # might be possible that the 2nd of the 2
                                # permissible options is definitely incorrect,
                                # (and consequently this assumption is correct)
                                # so we will need this solution!
                                # (better to save it, rather than finding it
                                # again later.)
                                print "Saving the above puzzle.\n" \
                                      "Will be useful if other\n" \
                                      "assumption (on same cell)\n"\
                                      "is definitely incorrect.\n"
                                temppuzzle, templabelrestrictionscount = \
                                    SavePuzzle()

                            # As it cannot be decided standing at this point
                            # whether the above assumption is correct or
                            # incorrect, revert to initial conditions and try
                            # the other options!
                            print "Reverting to this puzzle\n"\
                                  "(saved at the beginning \n"\
                                  "of this assumption) -"
                            LoadPuzzle(initialpuzzle,
                                       initiallabelrestrictionscount)
                            PrintPuzzle()
                        else:
                            # This means that puzzle is incorrectly filled, so
                            # it is sure that the above asumption is definately
                            # incorrect, so the other among the 2 permissible
                            # labels is definately correct.
                            print "Definately incorrect!\n" \
                                  "[%s in cell (%d,%d)]\n" \
                                  % (_labels[i], row + 1, col + 1)

                            # decide whether label is the 1st of the permissible
                            # the 1st labels or the 2nd one.
                            if i == 1:
                                # This means that the assumption we took
                                # (2nd of the 2 permissible labels) is
                                # incorrect, & as this assumption is incorrect,
                                # the 1st of the 2 assumptions is definately
                                # correct. Moreover, the puzzle solution to
                                # the 1st permissible label is already saved in
                                # temppuzzle, so just load it.
                                print "Hence previous assumption\n" \
                                      "was correct - \n" \
                                      "[%s in cell (%d,%d)]\n" \
                                      "Revert to the its\n" \
                                      "solution puzzle. \n" \
                                      "(Good, I had saved it!\n" \
                                      "Saved my time!)" \
                                      % (otherlabel, row + 1, col + 1)
                                PrintPuzzle()
                                LoadPuzzle(temppuzzle,
                                           templabelrestrictionscount)
                            else:
                                print "Hence, defintely correct-\n" \
                                      "[%s in cell (%d,%d)]\n" \
                                      % (otherlabel, row + 1, col + 1)
                                # This means that 2nd of the 2 permissible
                                # labels is correct, so revert to the puzzle
                                # that was at the beginning of the outermost
                                # for loop and then set the 2nd of the
                                # 2 permissible labels.
                                LoadPuzzle(initialpuzzle,
                                           initiallabelrestrictionscount)
                                setSudokuCellLabel(row, col, _labels[1])

                            # Delete all the variables defined at this point,
                            # as this function will be going into a recursive
                            # loop from here on, and this data, unnecessarily,
                            # will form a stack.
                            del initialpuzzle
                            del initiallabelrestrictionscount
                            del row
                            del col
                            del _labels
                            del i
                            del otherlabel

                            # Now, the puzzle solution has moved one step
                            # ahead, so try to solve it further using the
                            # "less complex", "previous" steps.
                            if k != 2:
                                print "(Entering into nested\nassumption...)\n"
                            SolveUptoSteps(k - 1, assumptionleveltree)
                            if k != 2:
                                print "(Exiting from nested\nassumption...)\n"

                            # Finally, repeat this step again to solve the
                            # puzzle further. (it is quite possile that in the
                            # previous step itself, the puzzle might have got
                            # solved. If so, it will just enter this function
                            # (in recursion) and return from the very
                            # 1st check)
                            return(Stepk(k, basetree))

    # If this part is getting executed means this function did not help
    # in solving the puzzle any further.
    print "Didn't get anything from\nthis Assumption Level.\n" \
          "Assumption Tree: %s\n" % assumptionleveltree
    return 0

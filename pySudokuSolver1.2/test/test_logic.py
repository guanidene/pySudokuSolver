#! /usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Pushpak Dagade (पुष्पक दगड़े)"
__date__   = "$18 Jul, 2011 11:14:55 PM$"

from os import devnull as devnull
import sys
import unittest
from pySudokuSolver.logic import SolveSudokuPuzzle

class LogicTest(unittest.TestCase):
    def setUp(self):
        self.str_question_puzzle = '. . 5 3 . . . . . '\
                                   '8 . . . . . . 2 . '\
                                   '. 7 . . 1 . 5 . . '\
                                   '4 . . . . 5 3 . . '\
                                   '. 1 . . 7 . . . 6 '\
                                   '. . 3 2 . . . 8 . '\
                                   '. 6 . 5 . . . . 9 '\
                                   '. . 4 . . . . 3 . '\
                                   '. . . . . 9 7 . . '
        self.str_solution_puzzle = '1 4 5 3 2 7 6 9 8 '\
                                   '8 3 9 6 5 4 1 2 7 '\
                                   '6 7 2 9 1 8 5 4 3 '\
                                   '4 9 6 1 8 5 3 7 2 '\
                                   '2 1 8 4 7 3 9 5 6 '\
                                   '7 5 3 2 9 6 4 8 1 '\
                                   '3 6 7 5 4 2 8 1 9 '\
                                   '9 8 4 7 6 1 2 3 5 '\
                                   '5 2 1 8 3 9 7 6 4 '

    def tearDown(self):
        self.str_question_puzzle = None
        self.str_solution_puzzle = None

    def test_SolveSudokuPuzzle(self):
        self.assertEquals(self.str_solution_puzzle,
                          SolveSudokuPuzzle(self.str_question_puzzle, 4),
                         "Could not solve the toughest puzzle. :(")

if __name__ == '__main__':
    temp = sys.stdout
    sys.stdout = open(devnull, 'w')
    unittest.main()
    sys.stdout = temp


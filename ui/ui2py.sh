#!/bin/bash

# Convert .ui file to .py class and place in appropriate folder

pyuic4 ui_sudoku_solver.ui > ../ui_sudoku_solver.py

if [ $? -eq 0 ]; then
	notify-send 'pyuic4 (Sudoku Solver)' 'Conversion Successsful' -i info
else
	notify-send 'pyuic4 (Sudoku Solver)' 'Conversion Failed' -i error -u critical
fi

#!/bin/bash

# Convert svg to pngs of various sizes using Inkscape cli

inkscape --export-height=256 --export-width=256 --export-png=ss-256x256.png --export-area-drawing sudoku-solver.svg 
inkscape --export-height=128 --export-width=128 --export-png=ss-128x128.png --export-area-drawing sudoku-solver.svg 
inkscape --export-height=64 --export-width=64 --export-png=ss-64x64.png --export-area-drawing sudoku-solver.svg 
inkscape --export-height=32 --export-width=32 --export-png=ss-32x32.png --export-area-drawing sudoku-solver.svg 
inkscape --export-height=16 --export-width=16 --export-png=ss-16x16.png --export-area-drawing sudoku-solver.svg 

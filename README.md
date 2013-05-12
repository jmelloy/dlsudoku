Solves any Sudoku puzzle using brute force and Donald Knuth's [Dancing Links](http://www-cs-faculty.stanford.edu/~uno/papers/dancing-color.ps.gz)

Usage:

   sudoku.py [-ma] [-p puzzle] [-f filename] [-g]

	Options:
  		-h, --help            show this help message and exit
  		-f FILE, --file=FILE  Read puzzles from file
  		-p PUZZLE, --puzzle=PUZZLE
                        Solve single puzzle
  		-g, --generate        
  		-a, --all             Find all solutions
  		-m MAX, --max=MAX     Find first N solutions
  		-w WRITE_PNG, --write-png=WRITE_PNG
                        Write out PNG of board

Writing out a PNG requires the PIL library to be installed.

board.py can also be used for N-queens.

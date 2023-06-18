from sudoku import SudokuSolver, SudokuGenerator
import sys
if len(sys.argv) == 2:
    solver = SudokuSolver()
    solver.solve_sudoku(sys.argv[1])
else:
    difficulty = input("Enter number of empty cells (1, 80): ")
    if difficulty == "":
        generator = SudokuGenerator()
    else:
        try:
            difficulty = int(difficulty)
        except ValueError:
            print("Not valid difficulty")
            exit()
    if difficulty < 1 or difficulty > 80:
        print("Not valid difficulty")
        exit()
    generator = SudokuGenerator(difficulty)
    generator.generate()
    board = generator.get_board()
    solver = SudokuSolver()
    solver.solve_sudoku(None, board)

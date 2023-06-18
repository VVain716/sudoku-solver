# sudoku-solver
Solves sudokus given a input, can also generate sudokus and solve them.

# Setup

Execute 
```bash
pip install Pillow
``` 
if not installed already


<br><br>
# Run 

Execute
```bash
python run.py [filename]
```

[filename] is optional and if provided will parse a 9x9 text file into a sudoku

Otherwise, sudoku will be auto-generated based on number of empty squares that user inputs


# Output

After program runs, it will output a PIL file in the grids directory. If the directory grids is not found, it will make it for you. 
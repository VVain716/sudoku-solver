from PIL import Image, ImageDraw, ImageFont
import os
import random
#Imports libraries
class SudokuSolver:
    def __init__(self):
        self.n = 9
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]

    def increment_counter(self):
        try:
            with open('counter.txt', 'r+') as file:
                counter = int(file.read())
                counter += 1
                file.seek(0)
                file.write(str(counter))
        except FileNotFoundError:
            with open('counter.txt', 'w') as file:
                file.write('1')

    def get_counter(self):
        try:
            with open('counter.txt', 'r') as file:
                counter = int(file.read())
                return counter
        except FileNotFoundError:
            return 0

    def parse(self, filename):
        try:
            with open(filename) as file:
                lines = file.readlines()
                for i in range(9):
                    line = lines[i].strip()
                    if len(line) != 9:
                        raise ValueError("Invalid input: Each line should contain exactly 9 characters.")
                    for j in range(9):
                        try:
                            self.board[i][j] = int(line[j])
                        except ValueError:
                            raise ValueError("Invalid input: Each character should be a digit (0-9).")
        except FileNotFoundError:
            print("Not a valid filename")
            exit(1)

    def isValid(self, row, col, number):
        for i in range(self.n):
            if self.board[row][i] == number or self.board[i][col] == number:
                return False
        row_index = row - row % 3
        col_index = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.board[i + row_index][j + col_index] == number:
                    return False
        return True

    def draw_bold_line(self, image, xy, color, width):
        draw = ImageDraw.Draw(image)
        x1, y1, x2, y2 = xy

        for _ in range(width):
            draw.line([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)], fill=color)
            x1 += 1
            y1 += 1
            x2 -= 1
            y2 -= 1

    def draw_sudoku_grid(self, grid, directory, initial=False):
        image_width = 400
        image_height = 400
        line_color = (0, 0, 0)  # Black
        bold_line_width = 3
        font_size = 32

        # Create a new image
        image = Image.new("RGB", (image_width, image_height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", font_size)

        # Draw the Sudoku grid lines
        cell_width = image_width // 9
        cell_height = image_height // 9
        for x in range(10):
            line_width = bold_line_width if x % 3 == 0 else 1
            draw.line([(x * cell_width, 0), (x * cell_width, image_height)], fill=line_color, width=line_width)
            draw.line([(0, x * cell_height), (image_width, x * cell_height)], fill=line_color, width=line_width)

        # Draw bold lines around the boxes
        box_width = cell_width * 3
        box_height = cell_height * 3
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                self.draw_bold_line(image,
                                    (x * cell_width, y * cell_height, (x + 3) * cell_width, (y + 3) * cell_height),
                                    line_color, bold_line_width)

        # Draw the numbers in the Sudoku grid
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    number = str(grid[i][j])
                    text_width, text_height = draw.textsize(number, font=font)
                    x = (cell_width - text_width) // 2 + j * cell_width
                    y = (cell_height - text_height) // 2 + i * cell_height
                    draw.text((x, y), number, font=font, fill=line_color)
        if initial:
            image.save(f"{directory}/initial.png")
        else:
            image.save(f"{directory}/solved.png")

    def solve(self, row=0, col=0):
        if row == self.n - 1 and col == self.n:
            return True

        if col == self.n:
            row += 1
            col = 0
        if self.board[row][col] != 0:
            return self.solve(row, col + 1)
        for number in range(1, self.n + 1):
            if self.isValid(row, col, number):
                self.board[row][col] = number
                if self.solve(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def solve_sudoku(self, filename, board=None):
        parent = "grids"
        if not os.path.exists(parent):
            os.makedirs(parent)
        directory = f"grids/{self.get_counter()}"
        if not os.path.exists(f"{directory}"):
            os.makedirs(directory)
        if not board:
            self.parse(filename)
        else:
            self.board = board
        self.draw_sudoku_grid(self.board, directory, initial=True)
        if self.solve():
            self.draw_sudoku_grid(self.board, directory)
            self.increment_counter()
            exit()
        print("No solution")

class SudokuGenerator():
    def __init__(self, empty_cells=55):
        self.board = [[0] * 9 for _ in range(9)]
        self.empty_cells=empty_cells
    def generate(self):
        self.fill_diagonal()
        self.fill_remaining(0, 3)
        self.remove_cells()

    def fill_diagonal(self):
        for i in range(0, 9, 3):
            self.fill_square(i, i)

    def fill_square(self, row, col):
        numbers = random.sample(range(1, 10), 9)
        index = 0
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = numbers[index]
                index += 1

    def is_safe(self, row, col, num):
        return (
            self.is_row_safe(row, num)
            and self.is_col_safe(col, num)
            and self.is_box_safe(row - row % 3, col - col % 3, num)
        )

    def is_row_safe(self, row, num):
        for col in range(9):
            if self.board[row][col] == num:
                return False
        return True

    def is_col_safe(self, col, num):
        for row in range(9):
            if self.board[row][col] == num:
                return False
        return True

    def is_box_safe(self, start_row, start_col, num):
        for row in range(3):
            for col in range(3):
                if self.board[start_row + row][start_col + col] == num:
                    return False
        return True

    def fill_remaining(self, row, col):
        if col >= 9 and row < 8:
            row += 1
            col = 0

        if row >= 9 and col >= 9:
            return True

        if row < 3:
            if col < 3:
                col = 3

        elif row < 6:
            if col == int(row / 3) * 3:
                col += 3

        else:
            if col == 6:
                row += 1
                col = 0
                if row >= 9:
                    return True

        for num in range(1, 10):
            if self.__is_safe(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0

        return False

    def remove_cells(self):
        empty_cells = self.empty_cells  # Adjust this value to control difficulty level

        while empty_cells > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if self.board[row][col] != 0:
                self.board[row][col] = 0
                empty_cells -= 1
    def get_board(self):
        return self.board

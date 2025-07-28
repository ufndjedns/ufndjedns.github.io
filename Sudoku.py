import tkinter as tk
from tkinter import messagebox
import random
import copy

class Sudoku:
    def __init__(self, difficulty='easy'):
        self.board = [[0]*9 for _ in range(9)]
        self.generate_full_board()
        self.solution = copy.deepcopy(self.board)
        self.remove_numbers(difficulty)

    def generate_full_board(self):
        self._fill_board()

    def _fill_board(self):
        nums = list(range(1, 10))

        def is_valid(num, row, col):
            for i in range(9):
                if self.board[row][i] == num or self.board[i][col] == num:
                    return False
            box_row, box_col = row - row % 3, col - col % 3
            for i in range(3):
                for j in range(3):
                    if self.board[box_row + i][box_col + j] == num:
                        return False
            return True

        def solve():
            for row in range(9):
                for col in range(9):
                    if self.board[row][col] == 0:
                        random.shuffle(nums)
                        for num in nums:
                            if is_valid(num, row, col):
                                self.board[row][col] = num
                                if solve():
                                    return True
                                self.board[row][col] = 0
                        return False
            return True

        solve()

    def remove_numbers(self, difficulty):
        levels = {'easy': 35, 'medium': 45, 'hard': 55}
        cells_to_remove = levels.get(difficulty, 45)
        count = 0
        while count < cells_to_remove:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count += 1

    def get_board(self):
        return self.board


class SudokuGUI:
    def __init__(self, root, difficulty='easy'):
        self.root = root
        self.root.title("Sudoku Game")
        self.sudoku = Sudoku(difficulty)
        self.board = self.sudoku.get_board()
        self.entries = [[None]*9 for _ in range(9)]
        self.cell_size = 50
        self.margin = 20
        self.canvas_size = self.cell_size * 9 + self.margin * 2

        # Timer
        self.start_time = 0
        self.time_elapsed = 0
        self.timer_label = tk.Label(self.root, text="Time: 00:00", font=("Arial", 14))
        self.timer_label.pack(pady=(10, 0))
        self.update_timer()

        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.create_grid()
        self.create_entries()

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Solve", width=10, command=self.solve).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Check", width=10, command=self.check_solution).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Clear", width=10, command=self.clear_board).grid(row=0, column=2, padx=5)

    def create_grid(self):
        for i in range(10):
            x = self.margin + i * self.cell_size
            y = self.margin + i * self.cell_size
            line_color = "black" if i % 3 == 0 else "gray"
            line_width = 3 if i % 3 == 0 else 1
            self.canvas.create_line(x, self.margin, x, self.canvas_size - self.margin, fill=line_color, width=line_width)
            self.canvas.create_line(self.margin, y, self.canvas_size - self.margin, y, fill=line_color, width=line_width)

    def create_entries(self):
        for i in range(9):
            for j in range(9):
                x = self.margin + j * self.cell_size
                y = self.margin + i * self.cell_size
                entry = tk.Entry(self.root, width=2, font=("Arial", 20), justify="center", bd=0)
                self.canvas.create_window(x + self.cell_size / 2, y + self.cell_size / 2,
                                          window=entry, width=self.cell_size - 4, height=self.cell_size - 4)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(state="readonly", disabledforeground="black")
                self.entries[i][j] = entry

    def update_timer(self):
        self.time_elapsed += 1
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)

    def solve(self):
        self.sudoku.generate_full_board()
        self.board = self.sudoku.get_board()
        self.time_elapsed = 0  # Reset timer
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(state="readonly", disabledforeground="black")

    def check_solution(self):
        user_board = [[0]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                value = entry.get()
                if value != "":
                    try:
                        user_board[i][j] = int(value)
                    except ValueError:
                        messagebox.showerror("Invalid input", "Only numbers 1-9 are allowed.")
                        return
        if user_board == self.sudoku.solution:
            messagebox.showinfo("Correct!", "Congratulations! You solved the puzzle!")
        else:
            messagebox.showerror("Incorrect", "Some values are incorrect. Try again!")

    def clear_board(self):
        self.time_elapsed = 0  # Reset timer
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(state="readonly", disabledforeground="black")


if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGUI(root, difficulty='medium')  # Choose: 'easy', 'medium', 'hard'
    root.mainloop()

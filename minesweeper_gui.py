import tkinter as tk
from tkinter import messagebox
import random


class Minesweeper:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = create_board(rows, cols, num_mines)
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.game_win = False

    def reveal_cell(self, row, col):
        if not self.revealed[row][col] and not self.flags[row][col]:
            if self.board[row][col] == '*':
                self.game_over = True
            else:
                mines_nearby = self.count_adjacent_mines(row, col)
                self.revealed[row][col] = True

                if mines_nearby == 0:
                    self.reveal_empty_squares(row, col)

                if self.check_win():
                    self.game_win = True

    def count_adjacent_mines(self, row, col):
        count = 0
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.board[i][j] == '*':
                    count += 1
        return count

    def reveal_empty_squares(self, row, col):
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if not self.revealed[i][j]:
                    self.reveal_cell(i, j)

    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.revealed[row][col] and self.board[row][col] != '*':
                    return False
        return True

def create_board(rows, cols, num_mines):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    mine_positions = random.sample(range(rows * cols), num_mines)

    for position in mine_positions:
        row = position // cols
        col = position % cols
        board[row][col] = '*'

    return board

class MinesweeperGUI:
    def __init__(self, master, rows, cols, num_mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = create_board(rows, cols, num_mines)
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]
        self.unprobed_color = "#EBEBEB"
        self.first_click = True

        self.create_widgets()


    def create_widgets(self):
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.master, text='', width=4, height=2, font=('Arial', 10),
                                   command=lambda r=row, c=col: self.click_square(r, c))

                button.configure(bg=self.unprobed_color)

                button.grid(row=row, column=col, padx=2, pady=2)
                button.bind('<Button-3>', lambda event, r=row, c=col: self.right_click_square(r, c))
                self.buttons[row][col] = button


    def click_square(self, row, col):
        if self.first_click:
            while self.board[row][col] == '*':
                self.board = create_board(self.rows, self.cols, self.num_mines)

            self.first_click = False

        if not self.revealed[row][col] and not self.flags[row][col]:
            if self.board[row][col] == '*':
                self.game_over()
            else:
                mines_nearby = self.count_adjacent_mines(row, col)
                self.revealed[row][col] = True
                self.buttons[row][col].config(text=str(mines_nearby))

                # Set the background color for probed cells
                color = self.get_cell_color(mines_nearby)
                self.buttons[row][col].config(state='disabled', bg=color)

                if mines_nearby == 0:
                    self.reveal_empty_squares(row, col)

                if self.check_win():
                    self.game_win()


    def right_click_square(self, row, col):
        if not self.revealed[row][col]:
            self.flags[row][col] = not self.flags[row][col]
            self.update_button_text(row, col)


    def count_adjacent_mines(self, row, col):
        count = 0
        rows, cols = self.rows, self.cols

        for i in range(max(0, row - 1), min(rows, row + 2)):
            for j in range(max(0, col - 1), min(cols, col + 2)):
                if self.board[i][j] == '*':
                    count += 1

        return count


    def reveal_empty_squares(self, row, col):
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if not self.revealed[i][j]:
                    self.click_square(i, j)


    def update_button_text(self, row, col):
        if self.flags[row][col]:
            self.buttons[row][col].config(text='🚩', bg='#33CD45')
        else:
            self.buttons[row][col].config(text='', bg=self.unprobed_color)


    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.revealed[row][col] and self.board[row][col] != '*':
                    return False
        return True
    
    
    def get_cell_color(self, value):
        low_intensity_color = "#FFE0D6"  # Color for low intensity
        high_intensity_color = "#946DED"  # Color for high intensity

        value_range = 8
        factor = value / value_range

        r_low, g_low, b_low = tuple(int(low_intensity_color[i:i+2], 16) for i in (1, 3, 5))
        r_high, g_high, b_high = tuple(int(high_intensity_color[i:i+2], 16) for i in (1, 3, 5))
        
        r = int(r_low + factor * (r_high - r_low))
        g = int(g_low + factor * (g_high - g_low))
        b = int(b_low + factor * (b_high - b_low))

        color = "#{:02x}{:02x}{:02x}".format(r, g, b)

        return color


    def game_over(self):
        self.show_mines()
        messagebox.showinfo("Game Over", "You hit a mine!")


    def show_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == '*':
                    self.buttons[row][col].config(text='💣', state='disabled', bg='#A62639')


    def game_win(self):
        self.show_mines()
        messagebox.showinfo("You Win!", "Congratulations! You've probed every non-mine containing cell.")
        self.master.destroy()


def play_game_gui():
    root = tk.Tk()
    root.title("Minesweeper")

    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))
    num_mines = int(input("Enter the number of mines: "))

    game = MinesweeperGUI(root, rows, cols, num_mines)

    root.mainloop()


if __name__ == "__main__":
    play_game_gui()

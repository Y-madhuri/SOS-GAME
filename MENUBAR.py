import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import numpy as np

class SOSGame:
    def __init__(self, master):
        self.master = master
        self.master.title("SOS Game")
        self.n = 0
        self.board = None
        self.player1 = None
        self.player2 = None
        self.current_player = None
        self.player1_symbol = None
        self.player2_symbol = None
        self.player1_score = 0
        self.player2_score = 0
        self.player1_score_label = None
        self.player2_score_label = None
        self.turn_label = None
        self.moves = []
        self.lines = []
        self.player1_color = None  # Added
        self.player2_color = None  # Added
        self.backtrack_count = 2  # Initial backtrack count
        self.create_size_selection()

    def create_size_selection(self):
        size_frame = tk.Frame(self.master)
        size_frame.pack(pady=20)

        self.label_n = tk.Label(size_frame, text="Enter size of the board (n x n):", font=('Elephant', 12))
        self.label_n.grid(row=0, column=0, padx=5, pady=5)
        self.entry_n = tk.Entry(size_frame)
        self.entry_n.grid(row=0, column=1, padx=5, pady=5)

        self.size_button = tk.Button(size_frame, text="Start Game", command=self.start_game, bg="Orange", fg="white")
        self.size_button.grid(row=1, columnspan=2, pady=10)

    def start_game(self):
        try:
            self.n = int(self.entry_n.get())
            if self.n < 2:
                raise ValueError
            self.create_widgets()
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter an integer value greater than 1 for size.")

    def create_widgets(self):
        self.label_n.grid_forget()
        self.entry_n.grid_forget()
        self.size_button.grid_forget()

        # Create label above the board to display current player's turn
        self.turn_label = tk.Label(self.master, text="", font=('Arial', 14))
        self.turn_label.pack(pady=10)

        self.board = np.full((self.n, self.n), ' ')

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(padx=20, pady=20)

        # Create a Canvas widget for drawing lines
        self.canvas = tk.Canvas(self.board_frame, width=self.n * 50, height=self.n * 50)
        self.canvas.pack()

        self.buttons = []
        for i in range(self.n):
            row_buttons = []
            for j in range(self.n):
                btn = tk.Button(self.canvas, text='', width=2, height=1, font=('Arial', 16),
                                command=lambda row=i, col=j: self.place_symbol(row, col))
                self.canvas.create_window(j * 50 + 25, i * 50 + 25, window=btn)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        self.player1 = tk.StringVar()
        self.player2 = tk.StringVar()
        self.create_player_options()

        self.player1_score_label = tk.Label(self.master, text="Player 1 Score: 0", font=('Arial', 12))
        self.player1_score_label.pack(pady=5)

        self.player2_score_label = tk.Label(self.master, text="Player 2 Score: 0", font=('Arial', 12))
        self.player2_score_label.pack(pady=5)

        self.current_player = 1
        
        self.update_turn_label()

    def create_player_options(self):
        player_frame = tk.Frame(self.master)
        player_frame.pack(pady=10)

        label_player1 = tk.Label(player_frame, text="Player 1 Symbol:", font=('Arial', 12))
        label_player1.grid(row=0, column=0, padx=5)

        dropdown_player1 = ttk.Combobox(player_frame, textvariable=self.player1, values=['S', 'O'], state='readonly')
        dropdown_player1.set('S')
        dropdown_player1.grid(row=0, column=1, padx=5)

        color_button1 = tk.Button(player_frame, text="Choose Color", command=self.choose_color1)
        color_button1.grid(row=0, column=2, padx=5)

        label_player2 = tk.Label(player_frame, text="Player 2 Symbol:", font=('Arial', 12))
        label_player2.grid(row=1, column=0, padx=5)

        dropdown_player2 = ttk.Combobox(player_frame, textvariable=self.player2, values=['S', 'O'], state='readonly')
        dropdown_player2.set('S')
        dropdown_player2.grid(row=1, column=1, padx=5)

        color_button2 = tk.Button(player_frame, text="Choose Color", command=self.choose_color2)
        color_button2.grid(row=1, column=2, padx=5)

    def choose_color1(self):
        color = colorchooser.askcolor(title="Choose Color for Player 1")[1]
        if color:
            self.player1_color = color

    def choose_color2(self):
        color = colorchooser.askcolor(title="Choose Color for Player 2")[1]
        if color:
            self.player2_color = color

    def place_symbol(self, row, col):
        if self.board[row][col] == ' ':
            symbol = self.player1.get() if self.current_player == 1 else self.player2.get()
            
            # Determine the text color based on the symbol and player
            text_color = self.player1_color if symbol == 'S' and self.current_player == 1 else self.player2_color
            
            self.board[row][col] = symbol
            self.buttons[row][col]['text'] = symbol
            color = self.player1_color if self.current_player == 1 else self.player2_color
            self.buttons[row][col]['fg'] = color
            self.moves.append((row, col, symbol))
            sos_detected, sos_positions = self.find_sos(row, col, symbol)
            if sos_detected:
                color = 'red' if self.current_player == 1 else 'blue'  # Highlight color for player and AI
                self.highlight_sos(sos_positions, color)
                self.update_score(len(sos_positions) // 3)  # Increment score based on number of SOS formations
            else:
                self.current_player = 2 if self.current_player == 1 else 1
                self.update_turn_label()
            self.check_game_over()

    def update_score(self, sos_count):
        if self.current_player == 1:
            self.player1_score += sos_count
            print(f"Player 1 Score: {self.player1_score}")
            self.player1_score_label.config(text=f"Player 1 Score: {self.player1_score}")
        else:
            self.player2_score += sos_count
            print(f"Player 2 Score: {self.player2_score}")
            self.player2_score_label.config(text=f"Player 2 Score: {self.player2_score}")

    def find_sos(self, row, col, symbol):
        sos_positions = []

        # Check Horizontal SOS
        if col >= 2 and self.board[row][col-2] == 'S' and self.board[row][col-1] == 'O' and self.board[row][col] == 'S':
            sos_positions.extend([(row, col-2), (row, col-1), (row, col)])
        if col >= 1 and col < self.n-1 and self.board[row][col-1] == 'S' and self.board[row][col] == 'O' and self.board[row][col+1] == 'S':
            sos_positions.extend([(row, col-1), (row, col), (row, col+1)])
        if col < self.n-2 and self.board[row][col] == 'S' and self.board[row][col+1] == 'O' and self.board[row][col+2] == 'S':
            sos_positions.extend([(row, col), (row, col+1), (row, col+2)])

        # Check Vertical SOS
        if row >= 2 and self.board[row-2][col] == 'S' and self.board[row-1][col] == 'O' and self.board[row][col] == 'S':
            sos_positions.extend([(row-2, col), (row-1, col), (row, col)])
        if row >= 1 and row < self.n-1 and self.board[row-1][col] == 'S' and self.board[row][col] == 'O' and self.board[row+1][col] == 'S':
            sos_positions.extend([(row-1, col), (row, col), (row+1, col)])
        if row < self.n-2 and self.board[row][col] == 'S' and self.board[row+1][col] == 'O' and self.board[row+2][col] == 'S':
            sos_positions.extend([(row, col), (row+1, col), (row+2, col)])
            # Check Diagonal SOS (top-left to bottom-right)
        if row >= 2 and col >= 2 and self.board[row-2][col-2] == 'S' and self.board[row-1][col-1] == 'O' and self.board[row][col] == 'S':
            sos_positions.extend([(row-2, col-2), (row-1, col-1), (row, col)])
        if row >= 1 and row < self.n-1 and col >= 1 and col < self.n-1 and self.board[row-1][col-1] == 'S' and self.board[row][col] == 'O' and self.board[row+1][col+1] == 'S':
            sos_positions.extend([(row-1, col-1), (row, col), (row+1, col+1)])
        if row < self.n-2 and col < self.n-2 and self.board[row][col] == 'S' and self.board[row+1][col+1] == 'O' and self.board[row+2][col+2] == 'S':
            sos_positions.extend([(row, col), (row+1, col+1), (row+2, col+2)])

        # Check Diagonal SOS (bottom-left to top-right)
        if row < self.n-2 and col >= 2 and self.board[row+2][col-2] == 'S' and self.board[row+1][col-1] == 'O' and self.board[row][col] == 'S':
            sos_positions.extend([(row, col), (row+1, col-1), (row+2, col-2)])
        if row >= 1 and row < self.n-1 and col < self.n-1 and col >= 1 and self.board[row-1][col+1] == 'S' and self.board[row][col] == 'O' and self.board[row+1][col-1] == 'S':
            sos_positions.extend([(row-1, col+1), (row, col), (row+1, col-1)])
        if row >= 2 and col < self.n-2 and self.board[row-2][col+2] == 'S' and self.board[row-1][col+1] == 'O' and self.board[row][col] == 'S':
            sos_positions.extend([(row-2, col+2), (row-1, col+1), (row, col)])

        return len(sos_positions) > 0, sos_positions

    def check_game_over(self):
        if ' ' not in self.board:
            if self.player1_score == 0 and self.player2_score == 0:
                self.backtrack()
                self.backtrack_count += 2  # Increment backtrack count
            else:
                if self.player1_score > self.player2_score:
                    winner = "Player 1"
                elif self.player1_score < self.player2_score:
                    winner = "Player 2"
                else:
                    winner = "It's a tie!"

                messagebox.showinfo("Game Over", f"{winner} wins with a score of {max(self.player1_score, self.player2_score)}!")
                self.restart_game()

    def count_sos(self, symbol):
        count = 0
        for row in range(self.n):
            for col in range(self.n):
                sos_detected, _ = self.find_sos(row, col, symbol)
                if sos_detected:
                    count += 1
        return count

    def update_turn_label(self):
        player_name = "Player 1" if self.current_player == 1 else "Player 2"
        if self.turn_label:
            self.turn_label.config(text=f"{player_name}'s Turn")

    def highlight_sos(self, positions, color):
        for i in range(0, len(positions) - 2, 3):
            row1, col1 = positions[i]
            row2, col2 = positions[i + 1]
            row3, col3 = positions[i + 2]
            if col1 < self.n and col2 < self.n:
                line1 = self.canvas.create_line(
                    col1 * 50 + 25, row1 * 50 + 25,
                    col2 * 50 + 25, row2 * 50 + 25,
                    fill=color, width=3)
                self.lines.append(line1)
            if col2 < self.n and col3 < self.n:
                line2 = self.canvas.create_line(
                    col2 * 50 + 25, row2 * 50 + 25,
                    col3 * 50 + 25, row3 * 50 + 25,
                    fill=color, width=3)
                self.lines.append(line2)

    def backtrack(self):
        print("Backtracking moves:")
        for _ in range(self.backtrack_count):
            if self.moves:
                row, col, symbol = self.moves.pop()
                print(f"Backtracked move: Row={row}, Column={col}, Symbol={symbol}")
                self.board[row][col] = ' '
                self.buttons[row][col]['text'] = ''
                self.buttons[row][col]['state'] = 'normal'
                sos_detected, sos_positions = self.find_sos(row, col, symbol)
                if sos_detected:
                    if self.current_player == 1:
                        self.player1_score -= 1
                        self.player1_score_label.config(text=f"Player 1 Score: {self.player1_score}")
                    else:
                        self.player2_score -= 1
                        self.player2_score_label.config(text=f"Player 2 Score: {self.player2_score}")
        self.current_player = 1 if self.current_player == 2 else 2
        self.update_turn_label()

    def restart_game(self):
        self.master.destroy()
        main()

def main():
    root = tk.Tk()
    game = SOSGame(root)

    restart_button = tk.Button(root, text="Restart", command=game.restart_game ,bg="Cyan", fg="white")
    restart_button.pack(side='left', padx=10, pady=10)

    quit_button = tk.Button(root, text="Quit", command=root.destroy, bg="Magenta", fg="white")
    quit_button.pack(side='right', padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

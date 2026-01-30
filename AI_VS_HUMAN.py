import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import numpy as np
import random

class SOSGame:
    def __init__(self, master):
        self.master = master
        self.master.title("SOS Game")
        self.n = 0
        self.board = None
        self.player1 = None
        self.current_player = None
        self.player1_score = 0
        self.ai_score = 0
        self.player1_score_label = None
        self.ai_score_label = None
        self.moves = []
        self.difficulty_label = None
        self.difficulty_dropdown = None
        self.create_size_selection()

    def create_size_selection(self):
        size_frame = tk.Frame(self.master)
        size_frame.pack(pady=20)

        self.label_n = tk.Label(size_frame, text="Enter size of the board (n x n):", font=('Arial', 12))
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

        self.board = np.full((self.n, self.n), ' ', dtype=np.object_)

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(padx=20, pady=20, anchor="n")  # Pack the board frame at the top of the window

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

        self.create_dropdowns()

        self.player1_score_label = tk.Label(self.master, text="Player Score: 0", font=('Arial', 12))
        self.player1_score_label.pack(pady=5)

        self.ai_score_label = tk.Label(self.master, text="AI Score: 0", font=('Arial', 12))
        self.ai_score_label.pack(pady=5)

        self.difficulty_label = tk.Label(self.master, text="Select AI Difficulty:", font=('Arial', 12))
        self.difficulty_label.pack(pady=5)

        self.difficulty_dropdown = ttk.Combobox(self.master, values=['Easy', 'Normal', 'Hard'], state='readonly')
        self.difficulty_dropdown.current(0)
        self.difficulty_dropdown.pack(pady=5)

        self.current_player = 1
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        restart_button = tk.Button(button_frame, text="Restart", command=self.restart_game, bg="green", fg="white")
        restart_button.pack(side='left', padx=10)

        quit_button = tk.Button(button_frame, text="Quit", command=self.quit_game, bg="red", fg="white")
        quit_button.pack(side='right', padx=10)


    def create_dropdowns(self):
        dropdown_frame = tk.Frame(self.master)
        dropdown_frame.pack(pady=10)

        label_player1 = tk.Label(dropdown_frame, text="Player symbol:", font=('Arial', 12))
        label_player1.pack(side='left', padx=5)
        self.player1 = 'S'
        dropdown_player1 = ttk.Combobox(dropdown_frame, values=['S', 'O'], state='readonly')
        dropdown_player1.set(self.player1)
        dropdown_player1.pack(side='left', padx=5)

    def place_symbol(self, row, col):
        if self.board[row][col] == ' ':
            symbol = self.player1 if self.current_player == 1 else 'O'
            if self.current_player == 1:
                selected_symbol = self.player1 if self.player1 == 'S' else 'O'
                response = messagebox.askyesno("Select Symbol", f"Do you want to place '{selected_symbol}'?")
                if response:
                    symbol = selected_symbol
                else:
                    symbol = 'O' if selected_symbol == 'S' else 'S'
            else:
                symbol = random.choice(['S', 'O'])

            self.board[row][col] = symbol
            self.buttons[row][col]['text'] = symbol

            bg_color = 'Magenta' if symbol == 'S' else 'Magenta'
            self.buttons[row][col].config(bg=bg_color)

            self.buttons[row][col]['state'] = 'disabled'

            self.moves.append((row, col, symbol))

            print(f"Player {'SOS' if symbol == 'S' else 'O'} move: ({row}, {col})") if self.current_player == 1 else print(f"AI {'SOS' if symbol == 'S' else 'O'} move: ({row}, {col})")

            sos_detected, sos_positions = self.find_sos(row, col, symbol)
            sos_count = len(sos_positions) // 3
            if self.current_player == 1:
                self.update_score(symbol, sos_detected, sos_count)
            else:
                self.update_score(symbol, sos_detected, sos_count, is_ai=True)

            if sos_detected:
                self.highlight_sos(sos_positions, True)

            self.check_game_over()
            if not sos_detected:
                self.current_player = 2 if self.current_player == 1 else 1
                if self.current_player == 2:
                    self.ai_move()

    def ai_move(self):
        difficulty = self.difficulty_dropdown.get()
        if difficulty == 'Easy':
            self.ai_move_easy()
        elif difficulty == 'Normal':
            self.ai_move_normal()
        else:
            self.ai_move_hard()

    def ai_move_easy(self):
        empty_positions = [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == ' ']
        row, col = random.choice(empty_positions)
        ai_symbol = random.choice(['S', 'O'])
        self.board[row][col] = ai_symbol
        print(f"AI {'SOS' if ai_symbol == 'S' else 'O'} move: ({row}, {col})")
        self.buttons[row][col]['text'] = ai_symbol
        self.buttons[row][col]['state'] = 'disabled'
        self.current_player = 1
        self.check_game_over()

    def ai_move_normal(self):
        ai_symbol = ''  # Define ai_symbol variable with a default value

        # Check if there are any empty positions left on the board
        if ' ' not in self.board:
            self.check_game_over()  # Check if the game is over
            return  # Game over, no more moves

        # Find all empty positions on the board
        empty_positions = [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == ' ']

        # Keep track of whether the AI has successfully placed a symbol and created an SOS
        made_sos = False

        # Introduce a probability factor to determine the likelihood of making a random move
        random_move_probability = 0.3  # Adjust this value to change the probability

        # First, check if the AI can make an SOS or block the player's SOS
        for row, col in empty_positions:
            for symbol in ['S', 'O']:
                # Check if placing the AI symbol creates an SOS
                self.board[row][col] = symbol
                sos_detected, sos_positions = self.find_sos(row, col, symbol)
                if sos_detected and random.random() > random_move_probability:
                    # Highlight the SOS formation
                    self.highlight_sos(sos_positions, False)
                    # Increment the AI's score based on SOS count only if it's a new SOS formation
                    new_sos = self.count_sos(symbol)
                    if new_sos:
                        self.update_score(symbol, sos_detected, new_sos, is_ai=True)
                        made_sos = True
                        ai_symbol = symbol  # Update ai_symbol with the symbol placed
                    # Disable the button
                    self.buttons[row][col]['text'] = symbol
                    self.buttons[row][col]['state'] = 'disabled'
                    print(f"AI {'SOS' if symbol == 'S' else 'O'} move: ({row}, {col})")  # Print AI's move
                    break
                # Reset the board for the next iteration
                self.board[row][col] = ' '
            if made_sos:
                break

        # If AI didn't make an SOS or block the player's SOS, make a random move
        if not made_sos or random.random() <= random_move_probability:
            # Make a random move
            row, col = random.choice(empty_positions)
            ai_symbol = random.choice(['S', 'O'])
            self.board[row][col] = ai_symbol
            print(f"AI {'SOS' if ai_symbol == 'S' else 'O'} move: ({row}, {col})")  # Print AI's move
            self.buttons[row][col]['text'] = ai_symbol
            self.buttons[row][col]['state'] = 'disabled'

        # Check if AI made an SOS and give it another turn
        if made_sos:
            self.ai_move()
        else:
            self.current_player = 1  # Switch to player's turn

        # Check if the game is over after AI's move
        self.check_game_over()

    def ai_move_hard(self):
        ai_symbol = ''  # Define ai_symbol variable with a default value

        # Check if there are any empty positions left on the board
        if ' ' not in self.board:
            self.check_game_over()  # Check if the game is over
            return  # Game over, no more moves

        # Find all empty positions on the board
        empty_positions = [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == ' ']

        # Keep track of whether the AI has successfully placed a symbol and created an SOS
        made_sos = False

        # First, check if the AI can make an SOS or block the player's SOS
        for row, col in empty_positions:
            for symbol in ['S', 'O']:
                # Check if placing the AI symbol creates an SOS
                self.board[row][col] = symbol
                sos_detected, sos_positions = self.find_sos(row, col, symbol)
                if sos_detected:
                    # Highlight the SOS formation
                    self.highlight_sos(sos_positions, False)
                    # Increment the AI's score based on SOS count only if it's a new SOS formation
                    new_sos = self.count_sos(symbol)
                    if new_sos:
                        self.update_score(symbol, sos_detected, new_sos, is_ai=True)
                        made_sos = True
                        ai_symbol = symbol  # Update ai_symbol with the symbol placed
                    # Disable the button
                    self.buttons[row][col]['text'] = symbol
                    self.buttons[row][col]['state'] = 'disabled'
                    print(f"AI {'SOS' if symbol == 'S' else 'O'} move: ({row}, {col})")  # Print AI's move
                    break
                # Reset the board for the next iteration
                self.board[row][col] = ' '
            if made_sos:
                break

        # If AI didn't make an SOS or block the player's SOS, make a random move
        if not made_sos:
            # Make a random move
            print("Invoking best_move function")
            # Call the best_move method to find the best move using minimax
            #row, col = self.best_move(self.board)
            row, col = random.choice(empty_positions)
            ai_symbol = random.choice(['S', 'O'])
            self.board[row][col] = ai_symbol
            print(f"AI {'SOS' if ai_symbol == 'S' else 'O'} move: ({row}, {col})")  # Print AI's move
            self.buttons[row][col]['text'] = ai_symbol
            self.buttons[row][col]['state'] = 'disabled'

        # Check if AI made an SOS and give it another turn
        if made_sos:
            self.ai_move()
        else:
            self.current_player = 1  # Switch to player's turn

        # Check if the game is over after AI's move
        self.check_game_over()



    def update_score(self, symbol, sos_detected, sos_count, is_ai=False):
        if sos_detected and sos_count > 0:
            if is_ai:
                self.ai_score += 1
                print(f"AI Score: {self.ai_score}")
                self.ai_score_label.config(text=f"AI Score: {self.ai_score}")
            else:
                self.player1_score += 1
                print(f"Player 1 Score: {self.player1_score}")
                self.player1_score_label.config(text=f"Player 1 Score: {self.player1_score}")

    def find_sos(self, row, col, symbol):
        sos_positions = []

        if col >= 2 and self.board[row][col-2] == 'S' and self.board[row][col-1] == 'O' and self.board[row][col] == 'S':
            sos_positions.extend([(row, col-2), (row, col-1), (row, col)])
        if col >= 1 and col < self.n-1 and self.board[row][col-1] == 'S' and self.board[row][col] == 'O' and self.board[row][col+1] == 'S':
            sos_positions.extend([(row, col-1), (row, col), (row, col+1)])
        if col < self.n-2 and self.board[row][col] == 'S' and self.board[row][col+1] == 'O' and self.board[row][col+2] == 'S':
            sos_positions.extend([(row, col), (row, col+1), (row, col+2)])

        if row >= 2 and self.board[row-2][col] == 'S' and self.board[row-1][col] == 'O' and self.board[row][col] == 'S':
            sos_positions.extend([(row-2, col), (row-1, col), (row, col)])
        if row >= 1 and row < self.n-1 and self.board[row-1][col] == 'S' and self.board[row][col] == 'O' and self.board[row+1][col] == 'S':
            sos_positions.extend([(row-1, col), (row, col), (row+1, col)])
        if row < self.n-2 and self.board[row][col] == 'S' and self.board[row+1][col] == 'O' and self.board[row+2][col] == 'S':
            sos_positions.extend([(row, col), (row+1, col), (row+2, col)])

        if row >= 2 and col >= 2 and self.board[row-2][col-2] == 'S' and self.board[row-1][col-1] == 'O' and self.board[row][col] == 'S':
            sos_positions.extend([(row-2, col-2), (row-1, col-1), (row, col)])
        if row >= 1 and row < self.n-1 and col >= 1 and col < self.n-1 and self.board[row-1][col-1] == 'S' and self.board[row][col] == 'O' and self.board[row+1][col+1] == 'S':
            sos_positions.extend([(row-1, col-1), (row, col), (row+1, col+1)])
        if row < self.n-2 and col < self.n-2 and self.board[row][col] == 'S' and self.board[row+1][col+1] == 'O' and self.board[row+2][col+2] == 'S':
            sos_positions.extend([(row, col), (row+1, col+1), (row+2, col+2)])

        if row < self.n-2 and col >= 2 and self.board[row+2][col-2] == 'S' and self.board[row+1][col-1] == 'O' and self.board[row][col] == 'S':
            sos_positions.extend([(row, col), (row+1, col-1), (row+2, col-2)])
        if row >= 1 and row < self.n-1 and col < self.n-1 and col >= 1 and self.board[row-1][col+1] == 'S' and self.board[row][col] == 'O' and self.board[row+1][col-1] == 'S':
            sos_positions.extend([(row-1, col+1), (row, col), (row+1, col-1)])
        if row >= 2 and col < self.n-2 and self.board[row-2][col+2] == 'S' and self.board[row-1][col+1] == 'O' and self.board[row][col] == 'S':
            sos_positions.extend([(row-2, col+2), (row-1, col+1), (row, col)])

        sos_detected = len(sos_positions) > 0

        return sos_detected, sos_positions

    def check_game_over(self):
        if ' ' not in self.board:
            print("Game over, determining winner...")
            if self.player1_score > self.ai_score:
                winner = "Player"
            elif self.player1_score < self.ai_score:
                winner = "AI"
            else:
                winner = "It's a tie!"

            messagebox.showinfo("Game Over", f"{winner} wins with a score of {max(self.player1_score, self.ai_score)}!")


    def restart_game(self):
        self.master.destroy()
        main()

    def quit_game(self):
        self.master.destroy()

    def highlight_sos(self, positions, is_player):
        color = 'red' if is_player else 'blue'
        for i in range(0, len(positions) - 2, 3):
            row1, col1 = positions[i]
            row2, col2 = positions[i + 1]
            row3, col3 = positions[i + 2]
            if col1 < self.n and col2 < self.n:
                line1 = self.canvas.create_line(
                    col1 * 50 + 25, row1 * 50 + 25,
                    col2 * 50 + 25, row2 * 50 + 25,
                    fill=color, width=3)
            if col2 < self.n and col3 < self.n:
                line2 = self.canvas.create_line(
                    col2 * 50 + 25, row2 * 50 + 25,
                    col3 * 50 + 25, row3 * 50 + 25,
                    fill=color, width=3)


    def count_sos(self, symbol):
        count = 0
        for row in range(self.n):
            for col in range(self.n):
                if self.board[row][col] == symbol:
                    sos_detected, _ = self.find_sos(row, col, symbol)
                    if sos_detected:
                        count += 1
        return count

    def best_move(self, board):
        print("best move")
        best_score = -np.inf
        best_move = None
        for i in range(self.n):
            for j in range(self.n):
                if board[i][j] == ' ':
                    board[i][j] =  random.choice(['S', 'O'])
                    score = self.minimax(board, False, 0, -np.inf, np.inf)
                    board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def minimax(self, board, is_maximizing, depth, alpha, beta):
        if ' ' not in board or depth == 3:
            return self.evaluate(board)

        if is_maximizing:
            max_eval = -np.inf
            for i in range(self.n):
                for j in range(self.n):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        eval = self.minimax(board, False, depth+1, alpha, beta)
                        board[i][j] = ' '
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = np.inf
            for i in range(self.n):
                for j in range(self.n):
                    if board[i][j] == ' ':
                        board[i][j] = 'S'
                        eval = self.minimax(board, True, depth+1, alpha, beta)
                        board[i][j] = ' '
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def evaluate(self, board):
        player_score = self.count_sos('S')
        ai_score = self.count_sos('O')
        return ai_score - player_score

def main():
    root = tk.Tk()
    app = SOSGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

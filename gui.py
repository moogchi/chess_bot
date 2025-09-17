import tkinter as tk
import chess
import engine # Your engine file

# Settings
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8
LIGHT_COLOR = "#F0D9B5"
DARK_COLOR = "#B58863"
HIGHLIGHT_COLOR = "#FFFF99"
FONT_SIZE = 52

class ChessGui(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Chess Engine")
        self.pack(fill="both", expand=True)

        # Game state
        self.board = chess.Board()
        self.selected_square = None
        self.player_is_white = True # Change to False if you want to play as Black

        # Widgets
        self.canvas = tk.Canvas(self, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack()
        self.status_label = tk.Label(self, text="White's Turn", font=("Arial", 16))
        self.status_label.pack(pady=10)

        # Bindings
        self.canvas.bind("<Button-1>", self.on_square_click)

        # Initial Draw 
        self.piece_images = {}
        self.draw_board()
        self.draw_pieces()
        
        # Start game if AI is White
        if not self.player_is_white:
            self.parent.after(500, self.make_ai_move)

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                x1, y1 = col * SQUARE_SIZE, row * SQUARE_SIZE
                x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def draw_pieces(self):
        self.canvas.delete("pieces") # Clear old pieces
        
        piece_map = {
            'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
            'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
        }
        
        for i in range(64):
            piece = self.board.piece_at(i)
            if piece:
                symbol = piece.symbol()
                color = "black" if piece.color == chess.BLACK else "white"
                
                # Flip board if player is black
                row, col = (7 - (i // 8), i % 8) if self.player_is_white else (i // 8, 7 - (i % 8))

                x = col * SQUARE_SIZE + SQUARE_SIZE / 2
                y = row * SQUARE_SIZE + SQUARE_SIZE / 2
                self.canvas.create_text(x, y, text=piece_map[symbol], 
                                        font=("Arial", FONT_SIZE), fill=color, tags="pieces")

    def on_square_click(self, event):
        if self.board.is_game_over():
            return
            
        # Don't allow clicks during AI's turn
        if self.board.turn != (chess.WHITE if self.player_is_white else chess.BLACK):
            return

        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        
        # Flip coordinates if player is black
        if not self.player_is_white:
            row = 7 - row
            col = 7 - col

        clicked_square = chess.square(col, 7 - row)

        if self.selected_square is None:
            # --- First click (select a piece) ---
            piece = self.board.piece_at(clicked_square)
            if piece and piece.color == self.board.turn:
                self.selected_square = clicked_square
                self.highlight_square(clicked_square)
        else:
            # --- Second click (move the piece) ---
            move = chess.Move(self.selected_square, clicked_square)
            
            # Handle promotions (auto-promotes to Queen)
            if self.board.piece_type_at(self.selected_square) == chess.PAWN:
                if (chess.square_rank(clicked_square) == 7 and self.board.turn == chess.WHITE) or \
                   (chess.square_rank(clicked_square) == 0 and self.board.turn == chess.BLACK):
                    move.promotion = chess.QUEEN

            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.draw_board()
                self.draw_pieces()
                self.check_game_over()
                
                # Trigger AI move after a short delay
                if not self.board.is_game_over():
                    self.parent.after(200, self.make_ai_move)
            else:
                self.selected_square = None
                self.draw_board() # Remove highlight
                self.draw_pieces()

    def make_ai_move(self):
        self.status_label.config(text="Bot is thinking...")
        self.update() # Force GUI update

        # --- Call your engine here ---
        ai_move = engine.find_best_move(self.board, depth=3) # Adjust depth as needed

        if ai_move:
            self.board.push(ai_move)
            self.draw_board()
            self.draw_pieces()
            self.check_game_over()

    def highlight_square(self, square):
        self.draw_board() # Redraw board to clear previous highlights
        row, col = 7 - chess.square_rank(square), chess.square_file(square)
        
        # Flip for black player
        if not self.player_is_white:
            row, col = 7-row, 7-col
            
        x1, y1 = col * SQUARE_SIZE, row * SQUARE_SIZE
        x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=HIGHLIGHT_COLOR, outline="", stipple="gray50")
        self.draw_pieces()

    def check_game_over(self):
        if self.board.is_game_over():
            result = self.board.result()
            if self.board.is_checkmate():
                status = f"Checkmate! Winner is {'Black' if self.board.turn == chess.WHITE else 'White'}."
            elif self.board.is_stalemate():
                status = "Stalemate! It's a draw."
            elif self.board.is_insufficient_material():
                status = "Draw by insufficient material."
            else:
                status = f"Game Over. Result: {result}"
            self.status_label.config(text=status)
        else:
            turn = "White" if self.board.turn == chess.WHITE else "Black"
            self.status_label.config(text=f"{turn}'s Turn")

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGui(root)
    root.mainloop()
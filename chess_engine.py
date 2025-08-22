import chess
import random as rnd

piece_value_dict = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate_board(board):
    total = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_value_dict[piece.piece_type]

            # Positive value is better for white
            if piece.color == chess.WHITE:
                total += value
            else:
                total -= value
    return total

#Recursively check
def minimax(board,depth,maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizing_player: #if white's turn
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            #explore 1 less depth and change turn
            eval = minimax(board,depth-1, False)

            #undo the move
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for move in board.legal_moves:
            board.push(move)
            #explore 1 less depth and change turn
            eval = minimax(board,depth-1, True)
            #undo the move
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval


def find_best_move(board, depth):
    best_move = None
    max_eval = -float('inf')

    for move in board.legal_moves:
        board.push(move)

        eval = minimax(board, depth - 1 ,False)
        board.pop()

        if eval > max_eval:
            max_eval = eval
            best_move = move
    return best_move


def play_move():
    board = chess.Board()
    print("name")
    print(board)

    while not board.is_game_over():
        move = find_best_move(board, 3)
        board.push(move)

        print()
        print("Next Move")
        print(board)

    print("\n Game Over")
    print(f"Result: {board.result()}")

play_move()
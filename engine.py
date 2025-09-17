import chess
from pst import piece_value, pawn_pst, knight_pst, bishop_pst, rook_pst, queen_pst, king_mg_pst, king_eg_pst

transposition_table = {}
EXACT, LOWER_BOUND, UPPER_BOUND = 0, 1, 2

def evaluate_board(board):
    total_eval = 0
    is_endgame = len(board.piece_map()) < 10

    # Create the full PST dictionary for this evaluation
    pst = {
        chess.PAWN: pawn_pst, chess.KNIGHT: knight_pst, chess.BISHOP: bishop_pst,
        chess.ROOK: rook_pst, chess.QUEEN: queen_pst, 
        chess.KING: king_eg_pst if is_endgame else king_mg_pst
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue
        
        score = piece_value[piece.piece_type] + pst[piece.piece_type][
            chess.square_mirror(square) if piece.color == chess.BLACK else square
        ]
        total_eval += score if piece.color == chess.WHITE else -score
        
    return total_eval

def quiescence(board, alpha, beta):
    stand_pat = evaluate_board(board) * (1 if board.turn == chess.WHITE else -1)
    if stand_pat >= beta:
        return beta
    alpha = max(alpha, stand_pat)

    for move in [m for m in board.legal_moves if board.is_capture(m)]:
        board.push(move)
        score = -quiescence(board, -beta, -alpha)
        board.pop()
        if score >= beta:
            return beta
        alpha = max(alpha, score)
    return alpha

def negamax(board, depth, alpha, beta):
    original_alpha = alpha
    zobrist_hash = board._board_state().zobrist_hash()

    if zobrist_hash in transposition_table and transposition_table[zobrist_hash]['depth'] >= depth:
        entry = transposition_table[zobrist_hash]
        if entry['flag'] == EXACT: return entry['score']
        elif entry['flag'] == LOWER_BOUND: alpha = max(alpha, entry['score'])
        elif entry['flag'] == UPPER_BOUND: beta = min(beta, entry['score'])
        if alpha >= beta: return entry['score']

    if depth == 0 or board.is_game_over():
        return quiescence(board, alpha, beta)

    max_eval = -float('inf')
    for move in board.legal_moves:
        board.push(move)
        eval = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()
        max_eval = max(max_eval, eval)
        alpha = max(alpha, eval)
        if alpha >= beta:
            break
            
    flag = EXACT if max_eval > original_alpha and max_eval < beta else (
           LOWER_BOUND if max_eval >= beta else UPPER_BOUND)
    transposition_table[zobrist_hash] = {'score': max_eval, 'depth': depth, 'flag': flag}
    
    return max_eval
    
def find_best_move(board, depth):
    best_move = None
    max_eval = -float('inf')
    alpha, beta = -float('inf'), float('inf')

    for move in board.legal_moves:
        board.push(move)
        eval = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move
    return best_move

def play_game():
    board = chess.Board()
    print(board)
    while not board.is_game_over():
        move = find_best_move(board, depth=3)
        board.push(move)
        print("\nEngine plays:", move.uci())
        print(board)
    print("\nGame Over:", board.result())

if __name__ == "__main__":
    play_game()
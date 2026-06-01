"""
Terminal Tic-Tac-Toe Game with Strategic AI Opponent
2-player or vs AI mode; AI blocks winning moves; detects win/draw; tracks scores.
"""

import random

EMPTY = ' '
X = 'X'
O = 'O'

WINNING_COMBOS = [
    (0,1,2),(3,4,5),(6,7,8),  # rows
    (0,3,6),(1,4,7),(2,5,8),  # cols
    (0,4,8),(2,4,6),           # diagonals
]


def new_board():
    return [EMPTY] * 9


def print_board(board, scores=None):
    print()
    for row in range(3):
        cells = []
        for col in range(3):
            idx = row * 3 + col
            c = board[idx]
            display = c if c != EMPTY else str(idx + 1)
            cells.append(f" {display} ")
        print("  " + "│".join(cells))
        if row < 2:
            print("  " + "─" * 11)
    print()
    if scores:
        print(f"  Score — X: {scores['X']}  O: {scores['O']}  Draws: {scores['D']}")
    print()


def check_winner(board):
    for a, b, c in WINNING_COMBOS:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)
    return None, None


def is_draw(board):
    return EMPTY not in board


def available_moves(board):
    return [i for i, c in enumerate(board) if c == EMPTY]


def minimax(board, is_maximizing, ai_mark, human_mark, depth=0, max_depth=9):
    winner, _ = check_winner(board)
    if winner == ai_mark:
        return 10 - depth
    if winner == human_mark:
        return depth - 10
    if is_draw(board):
        return 0

    moves = available_moves(board)

    if is_maximizing:
        best = -100
        for move in moves:
            board[move] = ai_mark
            score = minimax(board, False, ai_mark, human_mark, depth + 1, max_depth)
            board[move] = EMPTY
            best = max(best, score)
        return best
    else:
        best = 100
        for move in moves:
            board[move] = human_mark
            score = minimax(board, True, ai_mark, human_mark, depth + 1, max_depth)
            board[move] = EMPTY
            best = min(best, score)
        return best


def ai_move_hard(board, ai_mark, human_mark):
    """Best move using minimax."""
    best_score = -100
    best_move = None
    for move in available_moves(board):
        board[move] = ai_mark
        score = minimax(board, False, ai_mark, human_mark)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def ai_move_medium(board, ai_mark, human_mark):
    """Block winning moves + take wins; otherwise random."""
    moves = available_moves(board)

    # Try to win
    for move in moves:
        board[move] = ai_mark
        if check_winner(board)[0] == ai_mark:
            board[move] = EMPTY
            return move
        board[move] = EMPTY

    # Block human from winning
    for move in moves:
        board[move] = human_mark
        if check_winner(board)[0] == human_mark:
            board[move] = EMPTY
            return move
        board[move] = EMPTY

    # Take centre if free
    if 4 in moves:
        return 4

    # Take corner
    corners = [m for m in [0, 2, 6, 8] if m in moves]
    if corners:
        return random.choice(corners)

    return random.choice(moves)


def get_human_move(board, player):
    while True:
        try:
            move = int(input(f"  Player {player}, enter position (1-9): ")) - 1
            if move in available_moves(board):
                return move
            else:
                print("  ✗ That position is taken or invalid. Try again.")
        except ValueError:
            print("  ✗ Please enter a number 1-9.")


def play_game(player1_type='human', player2_type='ai', ai_difficulty='medium'):
    board = new_board()
    current_player = X
    player_marks = {X: player1_type, O: player2_type}

    print("\n  New Game! X goes first.")
    print("  Position guide:")
    print_board(new_board())

    while True:
        print_board(board)
        p_type = player_marks[current_player]

        if p_type == 'human':
            move = get_human_move(board, current_player)
        else:
            other = O if current_player == X else X
            if ai_difficulty == 'hard':
                move = ai_move_hard(board, current_player, other)
            else:
                move = ai_move_medium(board, current_player, other)
            print(f"  AI ({current_player}) plays position {move + 1}")

        board[move] = current_player
        winner, combo = check_winner(board)

        if winner:
            print_board(board)
            print(f"  🎉 Player {winner} wins!")
            return winner

        if is_draw(board):
            print_board(board)
            print("  🤝 It's a draw!")
            return 'D'

        current_player = O if current_player == X else X


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Terminal Tic-Tac-Toe v1.0             ║")
    print("╚══════════════════════════════════════════╝")

    scores = {X: 0, O: 0, 'D': 0}

    while True:
        print("\n  [1] Human vs AI (Medium)  [2] Human vs AI (Hard)")
        print("  [3] Human vs Human        [4] AI vs AI")
        print("  [5] Show Scores           [6] Quit")
        choice = input("  Choice: ").strip()

        if choice == '6':
            break
        elif choice == '1':
            result = play_game('human', 'ai', 'medium')
        elif choice == '2':
            result = play_game('human', 'ai', 'hard')
        elif choice == '3':
            result = play_game('human', 'human')
        elif choice == '4':
            result = play_game('ai', 'ai', 'hard')
        elif choice == '5':
            print(f"\n  Scores → X: {scores[X]}  O: {scores[O]}  Draws: {scores['D']}")
            continue
        else:
            print("  Invalid choice.")
            continue

        scores[result] += 1
        print(f"\n  Scores → X: {scores[X]}  O: {scores[O]}  Draws: {scores['D']}")

    print(f"\n  Final Scores:")
    print(f"  X wins : {scores[X]}")
    print(f"  O wins : {scores[O]}")
    print(f"  Draws  : {scores['D']}")
    print("  Thanks for playing!")


if __name__ == "__main__":
    main()

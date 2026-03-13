"""
Tic Tac Toe Player
"""


X = "X"
O = "O"  # noqa: E741
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count the number of X's and O's on the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # If X has made more moves, it's O's turn
    if x_count > o_count:
        return O

    # Otherwise, it's X's turn
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")

    i, j = action
    # Create a new board with the move applied
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != EMPTY:
            return board[0][j]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or len(actions(board)) == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    curr_player = player(board)

    if curr_player == X:
        # X wants to maximize utility
        _, move = max_value(board, float("-inf"), float("inf"))
        return move
    else:
        # O wants to minimize utility
        _, move = min_value(board, float("-inf"), float("inf"))
        return move


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    v = float("-inf")
    best_move = None
    for action in actions(board):
        v_next, _ = min_value(result(board, action), alpha, beta)
        if v_next > v:
            v = v_next
            best_move = action

        # Alpha-beta pruning: update alpha and check if we can prune
        alpha = max(alpha, v)
        if alpha >= beta:
            break

    return v, best_move


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    v = float("inf")
    best_move = None
    for action in actions(board):
        v_next, _ = max_value(result(board, action), alpha, beta)
        if v_next < v:
            v = v_next
            best_move = action

        # Alpha-beta pruning: update beta and check if we can prune
        beta = min(beta, v)
        if alpha >= beta:
            break

    return v, best_move

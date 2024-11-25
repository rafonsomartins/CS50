"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
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
    flattened_board = [cell for row in board for cell in row]
    x_count = flattened_board.count(X)
    o_count = flattened_board.count(O)
    if x_count == o_count:
        return X
    elif x_count > o_count:
        return O
    else:
        raise ValueError("Board has invalid state: O has more turns than X.")


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Board doesn't support an action.")
    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[2][0] != EMPTY:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    flattened_board = [cell for row in board for cell in row]
    count = flattened_board.count(EMPTY)
    return count == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == O:
        return -1
    return winner(board) == X


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -10
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = 10
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def player_max(board):
    possible_actions = actions(board)
    v = -10
    final_action = None
    for action in possible_actions:
        value = min_value(result(board, action))
        if value > v:
            v = value
            final_action = action
    return final_action


def player_min(board):
    possible_actions = actions(board)
    v = 10
    final_action = None
    for action in possible_actions:
        value = max_value(result(board, action))
        if value < v:
            v = value
            final_action = action
    return final_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        return player_max(board)
    return player_min(board)

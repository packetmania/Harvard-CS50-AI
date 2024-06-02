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
    countX = countO = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                countX += 1
            elif board[i][j] == O:
                countO += 1

    if countX > countO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    acts = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                acts.add((i, j))

    return acts


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    def deepcopy(lst):
        if isinstance(lst, list):
            return [deepcopy(item) for item in lst]
        else:
            return lst

    i, j = action
    if i not in range(3) or j not in range(3):
        raise IndexError
    if board[i][j] is not EMPTY:
        print(board)
        raise ValueError

    newBoard = deepcopy(board)
    nextPlayer = player(board)
    newBoard[i][j] = nextPlayer
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check winner in a row horizontally
    for row in board:
        if len(set(row)) == 1 and row[0] is not EMPTY:
            return row[0]

    # check winner in a row vertically
    for col in range(3):
        if (board[0][col] == board[1][col] == board[2][col]) and \
                board[0][col] is not EMPTY:
            return board[0][col]

    # check winner in a row diagonally
    if (board[0][0] == board[1][1] == board[2][2]) and \
            board[1][1] is not EMPTY:
        return board[1][1]
    if (board[0][2] == board[1][1] == board[2][0]) and \
            board[1][1] is not EMPTY:
        return board[1][1]

    return None  # no winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    who = winner(board)
    if who == X:
        ret = 1
    elif who == O:
        ret = -1
    else:
        ret = 0
    return ret


def minimax_original(board):
    """
    Returns the optimal action for the current player on the board.
    """
    actor = player(board)

    def MaxValue(b):
        if terminal(b):
            ut = utility(b)
            if actor == O:
                ut = -ut
            return ut, None

        valact_list = []
        for a in actions(b):
            v, a2 = MinValue(result(b, a))
            valact_list.append((v, a))

        print(f"maxval:{valact_list}")
        return max(valact_list)

    def MinValue(b):
        if terminal(b):
            ut = utility(b)
            if actor == O:
                ut = -ut
            return ut, None

        valact_list = []
        for a in actions(b):
            v, a2 = MaxValue(result(b, a))
            valact_list.append((v, a))

        print(f"minval:{valact_list}")
        return min(valact_list)

    val, act = MaxValue(board)
    # print(val, act)
    return act


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    This solution applies alpha-beta-search to minimax algorithm
    """
    actor = player(board)

    def MaxValue(b, alpha, beta):
        if terminal(b):
            ut = utility(b)
            if actor == O:
                ut = -ut
            return ut, None

        v = float('-inf')
        for a in actions(b):
            v2, a2 = MinValue(result(b, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def MinValue(b, alpha, beta):
        if terminal(b):
            ut = utility(b)
            if actor == O:
                ut = -ut
            return ut, None

        v = float('inf')
        for a in actions(b):
            v2, a2 = MaxValue(result(b, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move


    val, act = MaxValue(board, float('-inf'), float('inf'))
    # print(val, act)
    return act
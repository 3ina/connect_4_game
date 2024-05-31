import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    res = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return res


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (board[r][c] == piece and
                    board[r][c + 1] == piece and
                    board[r][c + 2] == piece and
                    board[r][c + 3] == piece):
                return True

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if (board[r][c] == piece and
                    board[r + 1][c] == piece and
                    board[r + 2][c] == piece and
                    board[r + 3][c] == piece):
                return True

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT-3):
            if (board[r][c] == piece and
                    board[r + 1][c+1] == piece and
                    board[r + 2][c+2] == piece and
                    board[r + 3][c+3] == piece):
                return True

    for r in range(3,ROW_COUNT):
        for c in range(COLUMN_COUNT-3):
            if (board[r][c] == piece and
                    board[r - 1][c+1] == piece and
                    board[r - 2][c+2] == piece and
                    board[r - 3][c+3] == piece):
                return True


def print_board(board):
    print(np.flip(board, 0))


board = create_board()
game_over = False
turn = 0

while not game_over:

    if turn == 0:
        col = int(input("player1 please inter number between 0-6"))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board,1):
                print("PLAYER 1 win")
                game_over = True

    else:
        col = int(input("player2 please inter number between 0-6"))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board,2):
                print("PLAYER 2 win")
                game_over = True

    turn += 1
    turn = turn % 2
    print_board(board)

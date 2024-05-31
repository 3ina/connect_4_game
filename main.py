import sys

import numpy as np
import pygame

SQUARESPACE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
ROW_COUNT = 6
COLUMN_COUNT = 7
RADIUS = int(SQUARESPACE/2 -5)


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
        for c in range(COLUMN_COUNT - 3):
            if (board[r][c] == piece and
                    board[r + 1][c + 1] == piece and
                    board[r + 2][c + 2] == piece and
                    board[r + 3][c + 3] == piece):
                return True

    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if (board[r][c] == piece and
                    board[r - 1][c + 1] == piece and
                    board[r - 2][c + 2] == piece and
                    board[r - 3][c + 3] == piece):
                return True


def print_board(board):
    print(np.flip(board, 0))


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,BLUE,(c*SQUARESPACE,r*SQUARESPACE+SQUARESPACE,SQUARESPACE,SQUARESPACE))
            pygame.draw.circle(screen,BLACK,(c*SQUARESPACE+SQUARESPACE//2,r*SQUARESPACE+SQUARESPACE+SQUARESPACE//2),RADIUS)


width = COLUMN_COUNT * SQUARESPACE
height = (ROW_COUNT + 1) * SQUARESPACE
size = (width, height)
board = create_board()
game_over = False
turn = 0

pygame.init()
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:


            if turn == 0:
                col = int(input("player1 please inter number between 0-6"))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        print("PLAYER 1 win")
                        game_over = True

            else:
                col = int(input("player2 please inter number between 0-6"))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        print("PLAYER 2 win")
                        game_over = True

            turn += 1
            turn = turn % 2
            print_board(board)

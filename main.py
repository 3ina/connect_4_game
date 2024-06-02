import math
import sys

import numpy as np
import pygame

SQUARESPACE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
ROW_COUNT = 6
COLUMN_COUNT = 7
RADIUS = int(SQUARESPACE/2 -5)

pygame.font.init()
font = pygame.font.Font(None,100)


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

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]==1:
                pygame.draw.circle(screen, RED, (c * SQUARESPACE + SQUARESPACE // 2,height- (r * SQUARESPACE + SQUARESPACE // 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c * SQUARESPACE + SQUARESPACE // 2,height-( r * SQUARESPACE + SQUARESPACE // 2)), RADIUS)

    pygame.display.update()

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

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESPACE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen,RED,(posx,SQUARESPACE//2),RADIUS)
            else:
                pygame.draw.circle(screen,YELLOW,(posx,SQUARESPACE//2),RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESPACE))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESPACE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = font.render("Player 1 wins!!",1,RED)
                        screen.blit(label,(40,10))
                        game_over = True

            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESPACE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = font.render("Player 2 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

            turn += 1
            turn = turn % 2
            print_board(board)
            draw_board(board)

    if game_over:
        pygame.time.wait(5000)

import math
import random
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
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4

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

def evaluate_window(window,piece):
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80

    return score

def score_position(board,piece):
    score = 0
    center_array = [int(i) for i in list(board[:,COLUMN_COUNT//2])]
    score += center_array.count(piece) * 6

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window,piece)

    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)


    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window,piece)

    return score



def is_terminal_node(board):
    return winning_move(board,PLAYER_PIECE) or winning_move(board,AI_PIECE) or len(get_valid_location(board)) == 0

def minimax(board,depth,alpha,beta,maximizingPLayer):
    valid_location = get_valid_location(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board,AI_PIECE):
                return None,math.inf
            elif winning_move(board,PLAYER_PIECE):
                return None,-math.inf
            else:
                return None,0
        else:
            return None,score_position(board,AI_PIECE)
    if maximizingPLayer:
        value = -math.inf
        column = random.choice(valid_location)
        for col in valid_location:
            row = get_next_open_row(board,col)
            b_copy = board.copy()
            drop_piece(b_copy,row,col,AI_PIECE)
            new_score = minimax(b_copy,depth-1,alpha,beta,False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column,value
    else:
        value = math.inf
        column = random.choice(valid_location)
        for col in valid_location:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1,alpha,beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta,value)
            if beta <= alpha:
                break
        return column,value




def get_valid_location(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board,col):
            valid_locations.append(col)
    return valid_locations
def pick_best_move(board,piece):
    valid_locations = get_valid_location(board)
    best_score = 0
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board,col)
        temp_board = board.copy()
        drop_piece(temp_board,row,col,piece)
        score = score_position(temp_board,piece)
        if score > best_score:
            best_col = col
            best_score = score

    return best_col


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
            if board[r][c]==PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (c * SQUARESPACE + SQUARESPACE // 2,height- (r * SQUARESPACE + SQUARESPACE // 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
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
            if turn == PLAYER:
                pygame.draw.circle(screen,RED,(posx,SQUARESPACE//2),RADIUS)


        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESPACE))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESPACE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, 1):
                        label = font.render("Player 1 wins!!",1,RED)
                        screen.blit(label,(40,10))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)

    if turn == AI and not game_over:
        col,score = minimax(board,4,-math.inf,math.inf,True)

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

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

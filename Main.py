import numpy as np
import random
import pygame
import keyboard
import time
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (450, 100)

board = np.array([[0] * 9 for i in range(9)])
copy_board = np.array([[0] * 9 for i in range(9)])
complete_board = np.array([[0] * 9 for i in range(9)])
pygame.init()
# K = int(input("Enter K numbers remove: "))
# SPEED = float(input("Enter speed solving: "))
SPEED = 0.001
# Easy => 20 - 35, Medium => 35 - 45, Hard => 45 - 65
K = 40
SIZE = 660
LINE = SIZE // 11
selected_square = {'x': LINE * 9, 'y': LINE * 9}
colors = {'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0), 'green': (0, 128, 0), 'yellow': (255, 255, 0)}
screen = pygame.display.set_mode((SIZE, SIZE))
screen.fill(colors['white'])
pygame.display.flip()
pygame.display.set_caption('Sudoku')


def print_message(msg, pos=(0, 0), font_size=18, background_color=colors['white'], font_color=colors['red']):
    font = pygame.font.Font('freesansbold.ttf', font_size)                             # defined the font of text
    text = font.render(msg, True, font_color, background_color)                                   # create the text object
    screen.blit(text, pos)                                                # print the text in screen


def copy_boards():
    for i in range(9):
        for j in range(9):
            complete_board[i][j] = board[i][j]


def check_row(num, row):
    return num in board[row]


def check_cell(num, col):
    return num in np.array([row[col] for row in board])


def check_square(num, row, col):
    r, c = row, col
    for i in range(r // 3 * 3, r // 3 * 3 + 3):
        for j in range(c // 3 * 3, c // 3 * 3 + 3):
            if num == board[i][j]:
                return True
    return False


def fill_diagonal():
    for i in range(3):
        fill_box(i * 3, i * 3)


def fill_box(row, col):
    for i in range(row, row + 3):
        for j in range(col, col + 3):
            num = random.randint(1, 9)
            while check_square(num, i, j):
                num = random.randint(1, 9)
            board[i][j] = num


def fill_remaining(row, col):
    # end of row
    if col == 9 and row < 8:
        row = row + 1
        col = 0

    # end of board
    if row == 9 and col == 9:
        return True

    if row < 3:                         # top left diagonal
        if col < 3:
            col = 3
    elif 2 < row < 6:                   # middle diagonal
        if 2 < col < 6:
            col = 6
    elif row >= 6:                      # lower right diagonal
        if 6 <= col < 9:
            row = row + 1
            col = 0
            if row == 9:
                return True

    for num in range(1, 10):
        if not check_square(num, row, col) and not check_row(num, row) and not check_cell(num, col):
            board[row][col] = num
            if fill_remaining(row, col + 1):
                return True
            board[row][col] = 0
    return False


def remove_k_digits():
    count = K
    while count:
        random_square = random.randint(0, 80)
        i = random_square // 9
        j = random_square % 9
        if board[i][j] != 0:
            count -= 1
            board[i][j] = 0
        else:
            continue


def check_more_than_one(num, arr):
    digit_count = 0
    for k in arr:
        if k == num:
            digit_count += 1
    return digit_count > 1


def print_board():
    pygame.draw.rect(screen, colors['black'], [LINE, LINE, SIZE - 2 * LINE, SIZE - 2 * LINE], 1)
    pygame.draw.rect(screen, colors['black'], [LINE, LINE * 4, LINE * 9, 0], 5)
    pygame.draw.rect(screen, colors['black'], [LINE, LINE * 7, LINE * 9, 0], 5)
    pygame.draw.rect(screen, colors['black'], [LINE * 4, LINE, 0, LINE * 9], 5)
    pygame.draw.rect(screen, colors['black'], [LINE * 7, LINE, 0, LINE * 9], 5)
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(screen, colors['black'], [LINE + (LINE * j), LINE + (LINE * i), LINE, LINE], 1)
            if board[i][j] != 0:
                print_message(str(board[i][j]), (LINE + LINE * j + LINE // 3, LINE + LINE * i + LINE // 3), 24)
            elif copy_board[i][j] != 0:
                print_message(str(copy_board[i][j]), (LINE + LINE * j + LINE // 3, LINE + LINE * i + LINE // 3), 24)

    print(copy_board)
    # check every digit in digits row  if some digits is filled
    for num in range(1, 10):
        flag = True
        num_count = 0
        for i in range(9):
            for j in range(9):
                if copy_board[i][j] == num:
                    num_count += 1
                    row = copy_board[i]
                    if check_more_than_one(num, row):
                        flag = False
                    col = np.array([row[j] for row in board])
                    if check_more_than_one(num, col):
                        flag = False
                    square = []
                    r, c = i, j
                    for x in range(r // 3 * 3, r // 3 * 3 + 3):
                        for y in range(c // 3 * 3, c // 3 * 3 + 3):
                            square.append(copy_board[x][y])
                    if check_more_than_one(num, square):
                        flag = False

        if 0 < num_count < 9 or num_count > 9:
            print_message(str(num), (num * LINE + 20, SIZE - LINE + 20), font_size=24)
        elif not flag:
            print_message(str(num), (num * LINE + 20, SIZE - LINE + 20), font_size=24)
    pygame.display.flip()


def init_board():
    fill_diagonal()
    # print(board, '\n')
    fill_remaining(0, 3)
    # print(board)
    copy_boards()
    # print(complete_board)


def move_selected_square(key='up'):
    if key == 'up' and selected_square['y'] // LINE > 1:
        selected_square['y'] -= LINE
    elif key == 'down' and selected_square['y'] // LINE < 9:
        selected_square['y'] += LINE
    elif key == 'left' and selected_square['x'] // LINE > 1:
        selected_square['x'] -= LINE
    elif key == 'right' and selected_square['x'] // LINE < 9:
        selected_square['x'] += LINE
    pygame.draw.rect(screen, colors['yellow'], [LINE, selected_square['y'], LINE * 9, LINE], 3)
    pygame.draw.rect(screen, colors['yellow'], [selected_square['x'], LINE, LINE, LINE * 9], 3)
    pygame.draw.rect(screen, colors['red'], [selected_square['x'], selected_square['y'], LINE, LINE], 5)


def refresh_screen():
    screen.fill(colors['white'])
    print_board()


def is_safe(num, i, j):
    pygame.draw.rect(screen, colors['yellow'], [LINE, i * LINE + LINE, LINE * 9, LINE], 3)
    pygame.draw.rect(screen, colors['yellow'], [j * LINE + LINE, LINE, LINE, LINE * 9], 3)
    pygame.draw.rect(screen, colors['red'], [j * LINE + LINE, i * LINE + LINE, LINE, LINE], 5)
    print_message(str(num), (j * LINE + LINE + 20, i * LINE + LINE + 20), font_size=24, font_color=colors['black'])
    pygame.display.flip()
    time.sleep(SPEED)
    if not check_square(num, i, j) and not check_row(num, i) and not check_cell(num, j):
        return True
    return False


def find_empty_location(l):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False


def solve():
    # 'l' is a list variable that keeps the record of row and col in find_empty_location Function
    l = [0, 0]

    # If there is no unassigned location, we are done
    if not find_empty_location(l):
        return True

    # Assigning list values to row and col that we got from the above Function
    row = l[0]
    col = l[1]

    # consider digits 1 to 9
    for num in range(1, 10):

        # if looks promising
        if is_safe(num, row, col):
            # make tentative assignment
            board[row][col] = num
            refresh_screen()
            pygame.display.flip()

            # return, if success, ya ! if(solve()):
            if solve():
                return True

        # failure, unmake & try again
        board[row][col] = 0

    # this triggers backtracking
    return False


def check_game_over():
    for i in range(9):
        for j in range(9):
            if copy_board[i][j] == 0:
                return False
    flag = True
    for i in range(9):
        for j in range(9):
            if copy_board[i][j] != complete_board[i][j]:
                flag = False
                break
    if flag:
        return True
    for i in range(9):
        for j in range(9):
            row = copy_board[i]
            if len(np.unique(row)) != len(row):
                return False
            col = np.array([row[j] for row in board])
            if len(np.unique(col)) != len(col):
                return False
            square = []
            r, c = i, j
            for x in range(r // 3 * 3, r // 3 * 3 + 3):
                for y in range(c // 3 * 3, c // 3 * 3 + 3):
                    square.append(copy_board[x][y])
            if any([square.count(e > 1 for e in square)]):
                return False
    return True


def start_game():
    init_board()
    remove_k_digits()
    for i in range(9):
        for j in range(9):
            copy_board[i][j] = board[i][j]
    print_board()
    print(board)
    print(complete_board)
    # solve()
    running = True
    while running:
        pygame.display.flip()
        if check_game_over():
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # when clicked the exit button
                running = False
            elif keyboard.is_pressed('s'):
                solve()
                print(board)
                time.sleep(1)
                running = False
            elif keyboard.is_pressed('up'):
                refresh_screen()
                move_selected_square('up')
            elif keyboard.is_pressed('down'):
                refresh_screen()
                move_selected_square('down')
            elif keyboard.is_pressed('left'):
                refresh_screen()
                move_selected_square('left')
            elif keyboard.is_pressed('right'):
                refresh_screen()
                move_selected_square('right')
            elif event.type == pygame.KEYDOWN:
                for num in range(1, 10):
                    if keyboard.is_pressed(str(num)):
                        print(num)
                        if board[selected_square['y'] // LINE - 1][selected_square['x'] // LINE - 1] == 0:
                            copy_board[selected_square['y'] // LINE - 1][selected_square['x'] // LINE - 1] = num
                        refresh_screen()


start_game()

from GUI import *
from globals import *

BOARD_SIZE = get_BOARD_SIZE()

def pos_to_index(x, y):

    FIELD_HEIGHT = get_FIELD_HEIGHT()
    FIELD_WIDTH = get_FIELD_WIDTH()

    i = 0
    x -= FIELD_WIDTH
    while x > X_BOARD_START:
        i += 1
        x += -(FIELD_WIDTH + BOARDER_WIDTH)

    j = 0
    y -= FIELD_HEIGHT
    while y > Y_BOARD_START:
        j += 1
        y += -(FIELD_HEIGHT + BOARDER_WIDTH)

    return i, j

def index_to_pos(r, center = True, diag = True):
    # Transform from x as a row, to x as a coordinate

    FIELD_HEIGHT = get_FIELD_HEIGHT()
    FIELD_WIDTH = get_FIELD_WIDTH()

    x1 = X_BOARD_START + r[1]*(FIELD_WIDTH + BOARDER_WIDTH)
    y1 = Y_BOARD_START + r[0]*(FIELD_HEIGHT + BOARDER_WIDTH)
    x2 = X_BOARD_START + r[3]*(FIELD_WIDTH + BOARDER_WIDTH)
    y2 = Y_BOARD_START + r[2]*(FIELD_HEIGHT + BOARDER_WIDTH)

    if center:
        x1 += FIELD_WIDTH//2
        x2 += FIELD_WIDTH//2
        y1 += FIELD_HEIGHT//2
        y2 += FIELD_HEIGHT//2
    elif diag:
        x2 += FIELD_WIDTH
        y2 += FIELD_HEIGHT - BOARDER_WIDTH

    return x1, y1, x2, y2

def check_win(num, x, y, board):
    BOARD_SIZE = get_BOARD_SIZE()
    CONNECTED_TO_WIN = get_CONNECTED_TO_WIN()

    beg_x = beg_y = mbeg_x = mbeg_y = mend_x = mend_y = 0
    # Check row x
    in_row = max_in_row = 0
    for i in range(BOARD_SIZE):
        if board[x][i] == num:
            if in_row == 0:
                beg_x, beg_y = x, i
            in_row += 1
        else:
            if in_row >= max_in_row:
                mbeg_x, mbeg_y, mend_x, mend_y = beg_x, beg_y, x, i - 1
                max_in_row = in_row
            in_row = 0

    if in_row >= max_in_row:
        mbeg_x, mbeg_y, mend_x, mend_y = beg_x, beg_y, beg_x, BOARD_SIZE - 1
        max_in_row = in_row
    if max_in_row >= CONNECTED_TO_WIN:
        return mbeg_x, mbeg_y, mend_x, mend_y

    beg_x = beg_y = mbeg_x = mbeg_y = mend_x = mend_y = 0
    # Check col y
    in_col = max_in_col = 0
    for i in range(BOARD_SIZE):
        if board[i][y] == num:
            if in_col == 0:
                beg_x, beg_y = i, y
            in_col += 1
        else:
            if in_col >= max_in_col:
                mbeg_x, mbeg_y, mend_x, mend_y = beg_x, beg_y, i - 1, y
                max_in_col = in_col
            in_col = 0

    if in_col >= max_in_col:
        mbeg_x, mbeg_y, mend_x, mend_y = beg_x, beg_y, i, y
        max_in_col = in_col
    if max_in_col >= CONNECTED_TO_WIN:
        return mbeg_x, mbeg_y, mend_x, mend_y

    beg_x = beg_y = mbeg_x = mbeg_y = mend_x = mend_y = 0
    # Check left diagonal
    l_diag = max_l_diag = 0
    diag_x = x - y
    if diag_x >= 0:
        diag_y = 0
    else:
        diag_y = diag_x * (-1)
        diag_x = 0

    while diag_x < BOARD_SIZE and diag_y < BOARD_SIZE:
        if board[diag_x][diag_y] == num:
            if l_diag == 0:
                beg_x, beg_y = diag_x, diag_y
            l_diag += 1
        else:
            if l_diag >= max_l_diag:
                max_l_diag = l_diag
                mbeg_x, mbeg_y, mend_x, mend_y = beg_x, beg_y, diag_x - 1, diag_y - 1
            l_diag = 0

        diag_x += 1
        diag_y += 1

    if l_diag >= max_l_diag:
        mbeg_x, mbeg_y, mend_x, mend_y = beg_x, beg_y, diag_x - 1, diag_y - 1
        max_l_diag = l_diag
    if max_l_diag >= CONNECTED_TO_WIN:
        return mbeg_x, mbeg_y, mend_x, mend_y

    beg_x = beg_y = mbeg_x = mbeg_y = mend_x = mend_y = 0
    # Check right diagonal
    r_diag = max_r_diag = 0
    diag_x = x + y
    if diag_x < BOARD_SIZE:
        diag_y = 0
    else:
        diag_y = diag_x - BOARD_SIZE + 1
        diag_x = BOARD_SIZE - 1

    while diag_x >= 0 and diag_y < BOARD_SIZE:
        if board[diag_x][diag_y] == num:
            if r_diag == 0:
                beg_x, beg_y = diag_x, diag_y
            r_diag += 1
        else:
            if r_diag >= max_r_diag:
                mbeg_x, mbeg_y, mend_x, mend_y = beg_x, beg_y, diag_x + 1, diag_y - 1
                max_r_diag = r_diag
            r_diag = 0

        diag_x -= 1
        diag_y += 1

    if r_diag >= max_r_diag:
        mbeg_x, mbeg_y, mend_x, mend_y = beg_x, beg_y, diag_x + 1, diag_y - 1
        max_r_diag = r_diag
    if max_r_diag >= CONNECTED_TO_WIN:
        return mbeg_x, mbeg_y, mend_x, mend_y

    return False

def is_board_full(board):
    BOARD_SIZE = get_BOARD_SIZE()

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j]==0:
                return False
    return True

def valid_move(x, y, board):
    BOARD_SIZE = get_BOARD_SIZE()

    if x >= BOARD_SIZE or y >= BOARD_SIZE:
        return False
    if board[x][y] == 0:
        return True

    return False

def player_turn(board, player, sp = False):
    from main import clock, handle_events, main, is_menu_button_pressed, player_name

    good_move = False
    while not good_move:
        clock.tick(FPS)
        handle_events()
        if is_menu_button_pressed(MENU_BUTTON):
            main()
        else:
            if sp == False:
                draw_window(board, player)
            else:
                draw_window(board, 3, sp=True)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                c, r = pos_to_index(pos[0], pos[1])
                if valid_move(r, c, board):
                    board[r][c] = player
                    good_move = True
    win = check_win(player, r, c, board)
    if win:
        if sp:
            draw_winner(board, player_name(3) + " Wins!", player, sp)
        else:
            draw_winner(board, player_name(player) + " Wins!", player, sp)
        pos_winning_line = index_to_pos(win)
        draw_winning_line(pos_winning_line, player)
        pygame.time.delay(2000)
        main()
    elif is_board_full(board):
        draw_winner(board, "Draw!", 0)
        pygame.time.delay(1000)
        run = False
        main()

def pvp():
    BOARD_SIZE = get_BOARD_SIZE()

    from main import clock
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    run = True
    draw_window(board, 1)

    while run:
        clock.tick(FPS)

        draw_window(board, 1)
        player_turn(board, 1)
        pygame.time.delay(10)
        draw_window(board, 2)
        player_turn(board, 2)
        pygame.time.delay(10)

def in_board(a):
    BOARD_SIZE = get_BOARD_SIZE()
    return a>=0 and a < BOARD_SIZE

def neighbours(board, x, y):
    dirs=((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    result = [0, 0, 0]
    for dir in dirs:
        a, b = x + dir[0], y + dir[1]
        if in_board(a) and in_board(b):
            result[board[a][b]] += 1
    return result

def increase_in_neighbors_line(x, y, board, calc, val):
    dirs=((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for dir in dirs:
        a, b = x + dir[0], y + dir[1]
        if in_board(a) and in_board(b) and board[a][b] == board[x][y]:
            c, d = a + dir[0], b + dir[1]
            if in_board(c) and in_board(d) and board[c][d] == 0:
                calc[c][d] += val

def how_much_in_row_possibble(x, y, board, num):
    dirs = ((-1, -1), (-1, 0), (-1, 1), (0, -1))
    MaxDir = (-1, -1)
    MaxRes = 0
    results = [0, 0, 0, 0]
    i = 0
    for dir in dirs:
        a, b = x + dir[0], y+ dir[1]
        c, d = x - dir[0], y - dir[1]
        while in_board(a) and in_board(b) and board[a][b] == num :
            results[i] += 1
            a += dir[0]
            b += dir[1]
        while in_board(c) and in_board(d) and board[c][d] == num:
            results[i] += 1
            c -= dir[0]
            d -= dir[1]

        if results[i] > MaxRes:
            MaxRes = results[i]
            MaxDir = dir
        i += 1


    return MaxRes, MaxDir

def possible_to_win(x, y, board): # how many possible wins form this tile (to avoid taking pointless tiles)
    dirs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    result = 0
    for dir in dirs:
        pos_moves_in_line = 1
        a, b = x + dir[0], y + dir[1]
        while in_board(a) and in_board(b):
            if board[a][b] == 0:
                pos_moves_in_line += 1
            elif pos_moves_in_line >= CONNECTED_TO_WIN:
                result += 1
                break
            else:
                break
            if pos_moves_in_line >= CONNECTED_TO_WIN:
                result += 1
                break
            a += dir[0]
            b += dir[1]

    return result

def ai_move(board):
    BOARD_SIZE = get_BOARD_SIZE()

    calculated_moves = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    Max_row = Max_col = Max_val = -1
    mod_board = board
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            if board[row][col] != 0:
                calculated_moves[row][col] = -1
                increase_in_neighbors_line(row, col, board, calculated_moves, 60)
            else:
                mod_board[row][col] = 2
                if check_win(2, row, col, board):
                    calculated_moves[row][col] += 3000
                mod_board[row][col] = 1
                if check_win(1, row, col, board):
                    calculated_moves[row][col] += 1000
                mod_board[row][col] = 0
                neares_tiles = neighbours(board, row, col)

                calculated_moves[row][col] += 7 * neares_tiles[0]
                calculated_moves[row][col] += 3 * neares_tiles[1]
                calculated_moves[row][col] += 10 * neares_tiles[2]

                calculated_moves[row][col] += 20 * possible_to_win(row, col, board)
                calculated_moves[row][col] += 8 * how_much_in_row_possibble(row, col, board, 2)[0]
                calculated_moves[row][col] += 10 * how_much_in_row_possibble(row, col, board, 1)[0] # how much opponent may have next turn

                mod_board[row][col] = 1
                increase_in_neighbors_line(row, col, mod_board, calculated_moves, 10)
                mod_board[row][col] = 2
                increase_in_neighbors_line(row, col, mod_board, calculated_moves, 10)
                mod_board[row][col] = 0

                if how_much_in_row_possibble(row, col, board, 1) == CONNECTED_TO_WIN - 1:
                    calculated_moves[row, col] += 550

                if calculated_moves[row][col] > Max_val:
                    Max_val = calculated_moves[row][col]
                    Max_row = row
                    Max_col = col

    # print(calculated_moves)

    return Max_row, Max_col

def ai_turn(board):
    from main import main
    x, y = ai_move(board)
    board[x][y] = 2
    win = check_win(2, x, y, board)
    if win:
        draw_winner(board, "GAME OVER!", 2)
        pos_winning_line = index_to_pos(win)
        draw_winning_line(pos_winning_line, 2)
        pygame.time.delay(1000)
        main()
    elif is_board_full(board):
        draw_winner(board, "Draw!", 0)
        pygame.time.delay(1000)
        run = False
        main()

def sp():
    from main import clock

    BOARD_SIZE = get_BOARD_SIZE()

    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    run = True

    while run:
        clock.tick(FPS)

        draw_window(board, 1, sp = True)
        player_turn(board, 1, sp = True)
        pygame.time.delay(100)

        draw_window(board, 2, sp = True)
        ai_turn(board)

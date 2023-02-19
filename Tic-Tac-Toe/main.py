import pygame

pygame.init()
pygame.display.init()
pygame.font.init()

#OPTIONS
BOARD_SIZE = 3 # check if >= CONNECTED_TO_WIN needed
CONNECTED_TO_WIN = 3
WIDTH, HEIGHT = 800, 600
IS_TURN_TEXT = True
TURN_TEXT_FONT = pygame.font.SysFont('Calibri', 60)
WINNER_TEXT_FONT = pygame.font.SysFont('comicsnas', 60)
MENU_FONT = pygame.font.SysFont('verdana', 75, bold = pygame.font.Font.bold)
MENU_OPTIONS_FONT = pygame.font.SysFont('verdana', 60)
TURN_BOARDER_WIDTH = 20
DIS_TEXT_TO_BOARDER = 5
BOARD_WIDTH, BOARD_HEIGHT = WIDTH - 2*TURN_BOARDER_WIDTH, HEIGHT - TURN_TEXT_FONT.get_height() - 3*TURN_BOARDER_WIDTH + DIS_TEXT_TO_BOARDER*2
X_BOARD_START, Y_BOARD_START = 20, TURN_TEXT_FONT.get_height() + 40
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BOARDER_WIDTH = 4

BOARDER_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (64, 64, 64)
FPS = 60
PLAYER_1_COLOR = (255, 255, 100)
PLAYER_2_COLOR = (0, 200, 100)
DRAW_COLOR = MENU_COLOR = (0, 200, 200)

P1_NAME = "Player 1"
P2_NAME = "Player 2"
CLICK = pygame.USEREVENT + 1

FIELD_HEIGHT, FIELD_WIDTH = (BOARD_HEIGHT - (BOARD_SIZE - 1) * BOARDER_WIDTH)//BOARD_SIZE, (BOARD_WIDTH - (BOARD_SIZE - 1) * BOARDER_WIDTH)//BOARD_SIZE
ICON_SIZE = min(FIELD_HEIGHT, FIELD_WIDTH)//2
# To-do:
# menu
# interactive menu (options get bold when cursor hovers)
# options
# check if text is not to long
# options
# test for bugs
# add single player

def draw_menu():
    pygame.Surface.fill(WIN, BACKGROUND_COLOR)
    header = MENU_FONT.render("MENU", True, MENU_COLOR)
    WIN.blit(header, (WIDTH//2 - header.get_width()//2, TURN_BOARDER_WIDTH))
    dec = pygame.Rect(TURN_BOARDER_WIDTH, TURN_BOARDER_WIDTH + header.get_height()//3, WIDTH//2 - header.get_width()//2 - 2*TURN_BOARDER_WIDTH, header.get_height()//3)
    pygame.draw.rect(WIN, MENU_COLOR, dec)
    pygame.draw.rect(WIN, MENU_COLOR, pygame.Rect.move(dec, header.get_width()//2 + WIDTH//2, 0))

    # Important: I can draw every option separatly, but I can also make list of options and then draw them, but it would be hard to bold them when hoverd by cursor
    text_sp = MENU_OPTIONS_FONT.render("Single Player", True, MENU_COLOR)
    #WIN.blit(text_sp, (WIDTH//2 - text_sp.get_width()//2))



    pygame.display.update()

def handle_events():
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()

def draw_window(board, player, is_turn_text = True):
    pygame.Surface.fill(WIN, BACKGROUND_COLOR)
    #draw boarders
    y = FIELD_HEIGHT + Y_BOARD_START
    for h in range(1, BOARD_SIZE):
        horizontal_boarder = pygame.Rect(X_BOARD_START, y, BOARD_WIDTH, BOARDER_WIDTH)
        y += FIELD_HEIGHT + BOARDER_WIDTH
        pygame.draw.rect(WIN, BOARDER_COLOR, horizontal_boarder)

    x = FIELD_WIDTH + X_BOARD_START
    for v in range(1, BOARD_SIZE):
        vertical_boarder = pygame.Rect(x, Y_BOARD_START , BOARDER_WIDTH, BOARD_HEIGHT)
        x += FIELD_WIDTH + BOARDER_WIDTH
        pygame.draw.rect(WIN, BOARDER_COLOR, vertical_boarder)

    #draw player moves
    row, col = 0, 0
    x, y = FIELD_WIDTH//2-ICON_SIZE//2 + X_BOARD_START, FIELD_HEIGHT//2 - ICON_SIZE//2 + Y_BOARD_START

    while row < BOARD_SIZE:
        while col < BOARD_SIZE:
            if board[row][col] == 1:
                pygame.draw.line(WIN, PLAYER_1_COLOR,  (x, y), (x + ICON_SIZE, y+ICON_SIZE), ICON_SIZE//4)
                pygame.draw.line(WIN, PLAYER_1_COLOR ,(x + ICON_SIZE, y), (x, y+ICON_SIZE), ICON_SIZE//4)
            elif board[row][col] == 2:
                tmp = pygame.Rect(x, y, ICON_SIZE, ICON_SIZE)
                pygame.draw.circle(WIN, PLAYER_2_COLOR, (x+ICON_SIZE//2, y+ICON_SIZE//2), round(ICON_SIZE/1.5), ICON_SIZE//4)

            col +=1
            x += FIELD_WIDTH + BOARDER_WIDTH
        x = FIELD_WIDTH//2 - ICON_SIZE//2 + X_BOARD_START
        y += FIELD_HEIGHT + BOARDER_WIDTH
        col = 0
        row += 1

    # Turn text
    if player == 1:
        text = P1_NAME + " turn"
        color = PLAYER_1_COLOR
    elif player == 2:
        text = P2_NAME + " turn"
        color = PLAYER_2_COLOR
    else:
        text = "???"
        color = DRAW_COLOR

    turn_text = TURN_TEXT_FONT.render(text, True, color)
    if is_turn_text:
        WIN.blit(turn_text, (WIDTH//2 - turn_text.get_width()//2, TURN_BOARDER_WIDTH))

    # Turn boarder
    turn_hor_boarder = pygame.Rect(0, 0, WIDTH, TURN_BOARDER_WIDTH)
    pygame.draw.rect(WIN, color, turn_hor_boarder)
    pygame.draw.rect(WIN, color, pygame.Rect.move(turn_hor_boarder, 0,turn_text.get_height() + 2*DIS_TEXT_TO_BOARDER))
    pygame.draw.rect(WIN, color, pygame.Rect.move(turn_hor_boarder, 0, HEIGHT - TURN_BOARDER_WIDTH))
    turn_ver_boarder = pygame.Rect(0, 0, TURN_BOARDER_WIDTH, HEIGHT)
    pygame.draw.rect(WIN, color, turn_ver_boarder)
    pygame.draw.rect(WIN, color, pygame.Rect.move(turn_ver_boarder, WIDTH - TURN_BOARDER_WIDTH, 0))

    pygame.display.update()

def draw_winner(board, winner_text, player):
    draw_window(board, player, False)
    if player == 0:
        color = DRAW_COLOR
    elif player == 1:
        color = PLAYER_1_COLOR
    else:
        color = PLAYER_2_COLOR

    text = WINNER_TEXT_FONT.render(winner_text, True, color)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, TURN_BOARDER_WIDTH + DIS_TEXT_TO_BOARDER))
    pygame.display.update()

def pos_to_index(x, y):
    i = 0
    x -= FIELD_WIDTH
    while x> X_BOARD_START:
        i += 1
        x += -(FIELD_WIDTH + BOARDER_WIDTH)
    
    j = 0 
    y -= FIELD_HEIGHT
    while y > Y_BOARD_START:
        j += 1 
        y += -(FIELD_HEIGHT + BOARDER_WIDTH)

    return i, j

def check_win(num, x, y, board):

    #Check row x
    in_row = max_in_row = 0
    for i in range(BOARD_SIZE):
        if board[x][i] == num:
            in_row += 1
        else:
            if in_row >= max_in_row:
                max_in_row = in_row
            in_row = 0

    if in_row >= max_in_row:
        max_in_row = in_row
    if max_in_row >= CONNECTED_TO_WIN:
        return True

    #Check col y
    in_col = max_in_col = 0
    for i in range(BOARD_SIZE):
        if board[i][y] == num:
            in_col += 1
        else:
            if in_col >= max_in_col:
                max_in_col = in_col
            in_col = 0

    if in_col >= max_in_col:
        max_in_col = in_col
    if max_in_col >= CONNECTED_TO_WIN:
        return True

    #Check left diagonal
    l_diag = max_l_diag = 0
    diag_x = x - y
    if diag_x >= 0:
        diag_y = 0
    else:
        diag_y = diag_x * (-1)
        diag_x = 0

    while diag_x < BOARD_SIZE and diag_y < BOARD_SIZE:
        if board[diag_x][diag_y] == num:
            l_diag += 1
        else:
            if l_diag >= max_l_diag:
                max_l_diag = l_diag
            l_diag = 0
        
        diag_x += 1
        diag_y += 1

    if l_diag >= max_l_diag:
        max_l_diag = l_diag
    if max_l_diag >= CONNECTED_TO_WIN:
        return True

    #Check right diagonal
    r_diag = max_r_diag = 0
    diag_x = x + y
    if diag_x < BOARD_SIZE:
        diag_y = 0
    else:
        diag_y = diag_x - BOARD_SIZE + 1
        diag_x = BOARD_SIZE - 1

    while diag_x >= 0 and diag_y < BOARD_SIZE:
        if board[diag_x][diag_y] == num:
            r_diag += 1
        else:
            if r_diag >= max_r_diag:
                max_r_diag = r_diag
            r_diag = 0
        
        diag_x -= 1
        diag_y += 1

    if r_diag >= max_r_diag:
        max_r_diag = r_diag
    if max_r_diag >= CONNECTED_TO_WIN:
        return True

    return False
    
def is_board_full(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j]==0:
                return False
    return True

def valid_move(x, y, board):
    if x >= BOARD_SIZE or y >= BOARD_SIZE:
        return False
    if board[x][y] == 0:
        return True

    return False

def pvp():
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    run = True
    draw_window(board, 1)

    while run:
        clock.tick(FPS)
        #player 1 turn 
        draw_window(board, 1)
        good_move = False
        while not good_move:
            clock.tick(FPS)
            handle_events()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()               
                c, r = pos_to_index(pos[0], pos[1])
                if valid_move(r, c, board):
                    board[r][c] = 1
                    good_move = True

        if check_win(1, r, c, board):
            print("Player 1 wins!")
            draw_winner(board, P1_NAME + " Wins!", 1)
            pygame.time.delay(3000)
            run = False
            break
        elif is_board_full(board):
            draw_winner(board, "Draw!", 0)
            pygame.time.delay(1000)
            run = False
            break

        draw_window(board, 2)
        pygame.time.delay(500)

        good_move = False
        while not good_move:
            clock.tick(FPS)
            handle_events()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                c, r = pos_to_index(pos[0], pos[1])
                if valid_move(r, c, board):
                    board[r][c] = 2
                    good_move = True

        

        if check_win(2, r, c, board):
            draw_winner(board, P2_NAME + " Wins!", 2)
            pygame.time.delay(3000)
            run = False
            break
        elif is_board_full(board):
            draw_window(board, 2)
            pygame.time.delay(1000)
            run = False
            break

        draw_window(board, 1)
        pygame.time.delay(500)
    
    exit()

def sp():
    pass

def main():
    draw_menu()
    #while True:
    #    handle_events()
    #pygame.time.delay(1000)
    #mode = int(input("Tryb gry \n 1) Single Player \n 2) Player vs Player \n"))
    mode = 2 #To usunac jak bedzie sp
    if mode == 1:
        sp()
    else:
        pvp()
  
if __name__ == "__main__":
    clock = pygame.time.Clock()
    main()

    exit()

import pygame
from threading import Thread


pygame.init()
pygame.display.init()
pygame.font.init()

#OPTIONS
BOARD_SIZE = 5 # max 9 (due to current moves loading), check if >= CONNECTED_TO_WIN needed
CONNECTED_TO_WIN = 3
WIDTH, HEIGHT = 800, 600
BOARD_WIDTH, BOARD_HEIGHT = WIDTH-300, HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BOARDER_WIDTH = 4

BOARDER_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (64, 64, 64)
FPS = 60
PLAYER_1_COLOR = (255, 255, 100)
PLAYER_2_COLOR = (150, 50, 255)
ROUND_TEXT_FONT = pygame.font.SysFont('comicsans', 60, bold=pygame.font.Font.bold)
TEXT_P1 = "PLAYER 1"
TEXT_P2 = "PLAYER 2"
CLICK = pygame.USEREVENT + 1

FIELD_HEIGHT, FIELD_WIDTH = (BOARD_HEIGHT - (BOARD_SIZE - 1) * BOARDER_WIDTH)//BOARD_SIZE, (BOARD_WIDTH - (BOARD_SIZE - 1) * BOARDER_WIDTH)//BOARD_SIZE
ICON_SIZE = min(FIELD_HEIGHT, FIELD_WIDTH)//2
# To-do:
# better icons
# turn text
# add single player

def handle_events():
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()

def draw_window(board):
    pygame.Surface.fill(WIN, BACKGROUND_COLOR)
    #draw boarders
    y = FIELD_HEIGHT
    for h in range(1, BOARD_SIZE):
        horizontal_boarder = pygame.Rect(0, y, WIDTH, BOARDER_WIDTH)
        y += FIELD_HEIGHT + BOARDER_WIDTH
        pygame.draw.rect(WIN, BOARDER_COLOR, horizontal_boarder)

    x = FIELD_WIDTH
    for v in range(1, BOARD_SIZE):
        vertical_boarder = pygame.Rect(x, 0 , BOARDER_WIDTH, HEIGHT)
        x += FIELD_WIDTH + BOARDER_WIDTH
        pygame.draw.rect(WIN, BOARDER_COLOR, vertical_boarder)

    #draw player moves
    row, col = 0, 0
    x, y = FIELD_WIDTH//2-ICON_SIZE//2, FIELD_HEIGHT//2 - ICON_SIZE//2

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
        x = FIELD_WIDTH//2 - ICON_SIZE//2
        y += FIELD_HEIGHT + BOARDER_WIDTH
        col = 0
        row += 1
        

    
    tmp = pygame.Rect(0, FIELD_HEIGHT , WIDTH, BOARDER_WIDTH)
    pygame.draw.rect(WIN, BOARDER_COLOR, tmp)

    pygame.display.update()

def pos_to_index(x, y):
    i = 0
    x -= FIELD_WIDTH
    while x>0:
        i += 1
        x += -(FIELD_WIDTH + BOARDER_WIDTH)
    
    j = 0 
    y -= FIELD_HEIGHT
    while y>0:
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
    
def valid_move(x, y, board):
    if board[x][y] == 0:
        return True

    return False

def pvp():
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    run = True

    while run:
        clock.tick(FPS)
        #player 1 turn 
        draw_window(board)
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
            run = False
            break

        draw_window(board)
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
            print("Player 2 wins!")
            run = False
            break

        draw_window(board)
        pygame.time.delay(500)
    
    exit()

def sp():
    pass

def main():
    #mode = int(input("Tryb gry \n 1) Single Player \n 2) Player vs Player \n"))
    mode = 2 #To usunac jak bedzie sp
    if mode == 1:
        sp()
    else:
        pvp()
  
if __name__ == "__main__":
    clock = pygame.time.Clock()
    #T_handling = Thread(target = handle_events)
    #T_main = Thread(target = main)
    #T_main.start()
    #T_handling.start()
    main()

    exit()

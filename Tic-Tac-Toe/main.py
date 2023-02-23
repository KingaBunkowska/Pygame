import pygame
import json

pygame.init()
pygame.display.init()
pygame.font.init()

#OPTIONS
BOARD_SIZE = 3
MAX_BOARD_SIZE = 25
CONNECTED_TO_WIN = 3
WIDTH, HEIGHT = 800, 600
IS_TURN_TEXT = True
TURN_TEXT_FONT = pygame.font.SysFont('Calibri', 60)
WINNER_TEXT_FONT = pygame.font.SysFont('Calibri', 60)
MENU_FONT = pygame.font.SysFont('verdana', 75, bold = pygame.font.Font.bold)
MENU_OPTIONS_FONT = pygame.font.SysFont('verdana', 60)
OPTIONS_OPTIONS_FONT = pygame.font.SysFont('verdana', 40)
HOVERED_MENU_OPTIONS_FONT = pygame.font.SysFont('verdana', 65, bold = pygame.font.Font.bold)
HOVERED_OPTIONS_OPTIONS_FONT = pygame.font.SysFont('verdana', 45, bold = pygame.font.Font.bold)
CONFIRMATION_FONT = pygame.font.SysFont('verdana', 45, bold = pygame.font.Font.bold)
TURN_BOARDER_WIDTH = 20
DIS_TEXT_TO_BOARDER = 5
BOARD_WIDTH, BOARD_HEIGHT = WIDTH - 2*TURN_BOARDER_WIDTH, HEIGHT - TURN_TEXT_FONT.get_height() - 3*TURN_BOARDER_WIDTH + DIS_TEXT_TO_BOARDER*2
X_BOARD_START, Y_BOARD_START = TURN_BOARDER_WIDTH, TURN_BOARDER_WIDTH + TURN_TEXT_FONT.get_height() + TURN_BOARDER_WIDTH
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BOARDER_WIDTH = 4
WINNING_LINE_WIDTH = 3*BOARDER_WIDTH
WINNING_LINE_COLOR = (210, 60, 60)

BOARDER_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (64, 64, 64)
FPS = 60
PLAYER_1_COLOR = (255, 255, 100)
PLAYER_2_COLOR = (0, 200, 100)
DRAW_COLOR = MENU_COLOR = (0, 200, 200)
HOVERED_MENU_COLOR = (0, 230, 230)
MENU_OPTIONS = ("Single Player", "Player vs Player", "Options", "Exit")
OPTIONS_OPTIONS = ("Player 1 name", "Player 2 name", "Board size", "Connected to win", "Defaults", "Back to menu")
LETTER_DISTANCE = 50
OK_COLOR = (30, 230, 30)
NO_OK_COLOR = (230, 30, 30)
BACKGROUND_CONFIRMATION_COLOR = (50, 50, 50)

P1_NAME = "Player 1"
P2_NAME = "Player 2"
Player1_name = ""
Player2_name = ""

FIELD_HEIGHT, FIELD_WIDTH = (BOARD_HEIGHT - (BOARD_SIZE - 1) * BOARDER_WIDTH)//BOARD_SIZE, (BOARD_WIDTH - (BOARD_SIZE - 1) * BOARDER_WIDTH)//BOARD_SIZE
ICON_SIZE = min(FIELD_HEIGHT, FIELD_WIDTH)//2

# To-do
# test for bugs
# add single player

def confirmation():
    WIN.fill(BACKGROUND_COLOR)
    pygame.draw.rect(WIN, BACKGROUND_CONFIRMATION_COLOR, (WIDTH//4, HEIGHT//4, WIDTH//2, HEIGHT//2))
    text = CONFIRMATION_FONT.render("Are you sure?", True, MENU_COLOR)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//4 + 10))

    ok_button = pygame.Rect(WIDTH//2 + 40, HEIGHT//2 + 30, WIDTH//6, HEIGHT//8)
    pygame.draw.rect(WIN, OK_COLOR, ok_button)
    ok_text = CONFIRMATION_FONT.render("YES", True, BACKGROUND_CONFIRMATION_COLOR)
    WIN.blit(ok_text, (ok_button.x + ok_button.width//2 - ok_text.get_width()//2, ok_button.y + ok_button.height//2 - ok_text.get_height()//2))

    no_button = pygame.Rect(WIDTH//2 - 40 - WIDTH//6, HEIGHT//2 + 30, WIDTH//6, HEIGHT//8)
    pygame.draw.rect(WIN, NO_OK_COLOR, no_button)
    no_text = CONFIRMATION_FONT.render("NO", True, BACKGROUND_CONFIRMATION_COLOR)
    WIN.blit(no_text, (no_button.x + no_button.width // 2 - no_text.get_width() // 2,
                       no_button.y + no_button.height // 2 - no_text.get_height() // 2))

    pygame.display.update()

    while True:
        clock.tick(FPS)
        handle_events()
        if pygame.mouse.get_pressed()[0]:
            if pygame.Rect.collidepoint(ok_button, pygame.mouse.get_pos()):
                while pygame.mouse.get_pressed()[0]:
                    handle_events()
                return True
            if pygame.Rect.collidepoint(no_button, pygame.mouse.get_pos()):
                while pygame.mouse.get_pressed()[0]:
                    handle_events()
                return False

def recalculate():
    global FIELD_HEIGHT, FIELD_WIDTH, ICON_SIZE, WINNING_LINE_WIDTH
    FIELD_HEIGHT, FIELD_WIDTH = (BOARD_HEIGHT - (BOARD_SIZE - 1) * BOARDER_WIDTH) // BOARD_SIZE, (
                BOARD_WIDTH - (BOARD_SIZE - 1) * BOARDER_WIDTH) // BOARD_SIZE
    ICON_SIZE = min(FIELD_HEIGHT, FIELD_WIDTH) // 2

    if BOARD_SIZE >= 10:
        WINNING_LINE_WIDTH = 2*BOARDER_WIDTH

def set_default_options():
    with open("options.json", "w") as options:
        with open("default_options.json", "r") as default:
            options.write(default.read())

def load_options():
    global Player1_name, Player2_name, BOARD_SIZE, CONNECTED_TO_WIN

    with open("options.json", "r") as file:
        dict_json = json.loads(file.read())
        if "Player 1 name" in dict_json:
            Player1_name = dict_json["Player 1 name"].upper()
        if "Player 2 name" in dict_json:
            Player2_name = dict_json["Player 2 name"].upper()
        if "Board size" in dict_json and "Connected to win" in dict_json:
            new_size = dict_json["Board size"]
            connection = dict_json["Connected to win"]
            if new_size >= connection:
                BOARD_SIZE = new_size
                CONNECTED_TO_WIN = connection
            else:
                print("Invalid Board size and Connected to win values")

def save_options():
    dict_json = None
    with open("options.json", "r") as file:
        dict_json = json.loads(file.read())
        dict_json["Player 1 name"] = Player1_name
        dict_json["Player 2 name"] = Player2_name
        dict_json["Board size"] = BOARD_SIZE
        dict_json["Connected to win"] = CONNECTED_TO_WIN
    with open("options.json", "w") as file:
        json.dump(dict_json, file)

def draw_letter(x, y, letter, size):
    letter_font = pygame.font.SysFont('Calibri', size)
    ready_letter = letter_font.render(letter, True, MENU_COLOR)
    WIN.blit(ready_letter, (x, y))

def valid_name(name):
    result = ""
    for letter in name:
        if letter != "_":
            result += letter
        elif letter == "_" and result != "":
            return result
    return result

def number_input(MIN, MAX, value):
    number = value
    Number_font = pygame.font.SysFont('Calibri', 80)


    while True:
        clock.tick(FPS)
        handle_events()

        WIN.fill(BACKGROUND_COLOR)
        ok_button = pygame.Rect(WIDTH // 2 - WIDTH // 12, HEIGHT // 2 + 50, WIDTH // 6, HEIGHT // 8)
        pygame.draw.rect(WIN, OK_COLOR, ok_button)
        ok_text = CONFIRMATION_FONT.render("SAVE", True, BACKGROUND_COLOR)
        WIN.blit(ok_text, (ok_button.x + ok_button.width // 2 - ok_text.get_width() // 2,
                           ok_button.y + ok_button.height // 2 - ok_text.get_height() // 2))
        WIN.blit(ok_text, (ok_button.x + ok_button.width // 2 - ok_text.get_width() // 2,
                           ok_button.y + ok_button.height // 2 - ok_text.get_height() // 2))

        if pygame.mouse.get_pressed()[0] and pygame.Rect.collidepoint(ok_button, pygame.mouse.get_pos()):
            while pygame.mouse.get_pressed()[0]:
                handle_events()
            return number
        text = Number_font.render(str(number), True, MENU_COLOR)
        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2 - 50))

        add_1_button = pygame.Rect(WIDTH//2 + text.get_width()//2 + 50, HEIGHT//2 - HEIGHT//16 - 50, WIDTH//8, HEIGHT//8)
        pygame.draw.rect(WIN, MENU_COLOR, add_1_button)
        add_1_text = CONFIRMATION_FONT.render("+1", True, BACKGROUND_COLOR)
        WIN.blit(add_1_text, (add_1_button.x + add_1_button.width//2 - add_1_text.get_width()//2, add_1_button.y + add_1_button.height//2 - add_1_text.get_height()//2))
        if pygame.mouse.get_pressed()[0] and pygame.Rect.collidepoint(add_1_button, pygame.mouse.get_pos()):
            if number < MAX:
                number += 1
            pygame.time.delay(130)

        add_10_button = pygame.Rect(add_1_button.x + add_1_button.width + 50, add_1_button.y, add_1_button.width, add_1_button.height)
        pygame.draw.rect(WIN, MENU_COLOR, add_10_button)
        add_10_text = CONFIRMATION_FONT.render("+10", True, BACKGROUND_COLOR)
        WIN.blit(add_10_text, (add_10_button.x + add_1_button.width//2 - add_10_text.get_width()//2, add_10_button.y + add_1_button.height//2 - add_10_text.get_height()//2))
        if pygame.mouse.get_pressed()[0] and pygame.Rect.collidepoint(add_10_button, pygame.mouse.get_pos()):
            number += 10
            if number > MAX:
                number = MAX
            pygame.time.delay(130)

        sub_1_button = pygame.Rect(WIDTH//2 - text.get_width()//2 - add_1_button.width - 50, add_1_button.y, add_1_button.width, add_1_button.height)
        pygame.draw.rect(WIN, MENU_COLOR, sub_1_button)
        sub_1_text = CONFIRMATION_FONT.render("-1", True, BACKGROUND_COLOR)
        WIN.blit(sub_1_text, (sub_1_button.x + add_1_button.width // 2 - sub_1_text.get_width() // 2,
                               sub_1_button.y + add_1_button.height // 2 - sub_1_text.get_height() // 2))
        if pygame.mouse.get_pressed()[0] and pygame.Rect.collidepoint(sub_1_button, pygame.mouse.get_pos()):
            number -= 1
            if number < MIN:
                number = MIN
            pygame.time.delay(130)

        sub_10_button = pygame.Rect(sub_1_button.x - add_1_button.width - 50, add_1_button.y,
                                   add_1_button.width, add_1_button.height)
        pygame.draw.rect(WIN, MENU_COLOR, sub_10_button)
        sub_10_text = CONFIRMATION_FONT.render("-10", True, BACKGROUND_COLOR)
        WIN.blit(sub_10_text, (sub_10_button.x + add_1_button.width // 2 - sub_10_text.get_width() // 2,
                               sub_10_button.y + add_1_button.height // 2 - sub_10_text.get_height() // 2))
        if pygame.mouse.get_pressed()[0] and pygame.Rect.collidepoint(sub_10_button, pygame.mouse.get_pos()):
            number -= 10
            if number < MIN:
                number = MIN
            pygame.time.delay(130)


        pygame.display.update()

def text_input(x = -1, y = -1, size = 60, no_of_letters = 8):
    x = WIDTH//2 - no_of_letters * (10+LETTER_DISTANCE) //2
    y = HEIGHT // 2 - size
    name = ["_" for _ in range(no_of_letters)]
    or_x = x
    while True:
        WIN.fill(BACKGROUND_COLOR)
        handle_events()
        x = or_x
        for i in range(no_of_letters):
            draw_letter(x, y, name[i], size)
            arrow_down = pygame.Rect(x+5, y + 65, 20, 10)
            arrow_up = pygame.Rect(x+5, y - 15, 20, 10)

            up = down = False
            if pygame.Rect.collidepoint(arrow_up, pygame.mouse.get_pos()):
                up = True
                down = False
            elif pygame.Rect.collidepoint(arrow_down, pygame.mouse.get_pos()):
                up = False
                down = True
            else:
                up = down = False

            if pygame.mouse.get_pressed()[0] and up:
                if name[i] == "_":
                    name[i] = "A"
                elif name[i] == "Z":
                    name[i] = "_"
                else:
                    name[i] = chr(ord(name[i]) + 1)
                pygame.time.delay(120)
            elif pygame.mouse.get_pressed()[0] and down:
                if name[i] == "_":
                    name[i] = "Z"
                elif name[i] == "A":
                    name[i] = "_"
                else:
                    name[i] = chr(ord(name[i]) - 1)
                pygame.time.delay(120)

            if up:
                pygame.draw.polygon(WIN, HOVERED_MENU_COLOR, ((arrow_up.x, arrow_up.y + arrow_up.height), (arrow_up.x + arrow_up.width, arrow_up.y + arrow_up.height), (arrow_up.x + arrow_up.width // 2, arrow_up.y)))
                pygame.draw.polygon(WIN, MENU_COLOR, ((arrow_down.x, arrow_down.y), (arrow_down.x + arrow_down.width, arrow_down.y),(arrow_down.x + arrow_down.width // 2, arrow_down.y + arrow_down.height)))
            elif down:
                pygame.draw.polygon(WIN, MENU_COLOR, ((arrow_up.x, arrow_up.y + arrow_up.height), (arrow_up.x + arrow_up.width, arrow_up.y + arrow_up.height),(arrow_up.x + arrow_up.width // 2, arrow_up.y)))
                pygame.draw.polygon(WIN, HOVERED_MENU_COLOR, ((arrow_down.x, arrow_down.y), (arrow_down.x + arrow_down.width, arrow_down.y), (arrow_down.x + arrow_down.width // 2, arrow_down.y + arrow_down.height)))
            else:
                pygame.draw.polygon(WIN, MENU_COLOR, ((arrow_up.x, arrow_up.y + arrow_up.height), (arrow_up.x + arrow_up.width, arrow_up.y + arrow_up.height), (arrow_up.x + arrow_up.width//2, arrow_up.y)))
                pygame.draw.polygon(WIN, MENU_COLOR, ((arrow_down.x, arrow_down.y), (arrow_down.x + arrow_down.width, arrow_down.y), (arrow_down.x + arrow_down.width//2, arrow_down.y + arrow_down.height)))

            x += LETTER_DISTANCE
            if i == no_of_letters - 1:
                ok = pygame.Rect(x, y, 20, 20)
                hoverd = False
                if pygame.Rect.collidepoint(ok, pygame.mouse.get_pos()):
                    hoverd = True
                curr_name = valid_name(name)
                if curr_name:
                    pygame.draw.rect(WIN, OK_COLOR, ok)
                else:
                    pygame.draw.rect(WIN, NO_OK_COLOR, ok)

                if hoverd and pygame.mouse.get_pressed()[0] and curr_name:
                    return curr_name

        pygame.display.update()

def options_option_action(no):
    global CONNECTED_TO_WIN
    if no == 0:
        global Player1_name
        Player1_name = text_input()
        save_options()
    elif no == 1:
        global Player2_name
        Player2_name = text_input()
        save_options()
    elif no == 2:
        global BOARD_SIZE
        BOARD_SIZE = number_input(CONNECTED_TO_WIN, MAX_BOARD_SIZE, BOARD_SIZE)
        save_options()
        recalculate()
    elif no == 3:
        CONNECTED_TO_WIN = number_input(1, BOARD_SIZE, CONNECTED_TO_WIN)
        save_options()
    elif no == 4:
        if confirmation():
            set_default_options()
            load_options()
            recalculate()
    elif no == 5:
        main()
def draw_options():
    pygame.Surface.fill(WIN, BACKGROUND_COLOR)
    header = MENU_FONT.render("OPTIONS", True, MENU_COLOR)
    WIN.blit(header, (WIDTH // 2 - header.get_width() // 2, TURN_BOARDER_WIDTH))
    dec = pygame.Rect(TURN_BOARDER_WIDTH, TURN_BOARDER_WIDTH + header.get_height() // 3, WIDTH // 2 - header.get_width() // 2 - 2 * TURN_BOARDER_WIDTH, header.get_height() // 3)
    pygame.draw.rect(WIN, MENU_COLOR, dec)
    pygame.draw.rect(WIN, MENU_COLOR, pygame.Rect.move(dec, header.get_width() // 2 + WIDTH // 2, 0))

    distance = (HEIGHT - 4 * TURN_BOARDER_WIDTH - MENU_FONT.get_height()) // len(OPTIONS_OPTIONS)
    options_positiones = []
    no_option = 0
    x = 3 * TURN_BOARDER_WIDTH + MENU_FONT.get_height()
    for option in OPTIONS_OPTIONS:
        text = OPTIONS_OPTIONS_FONT.render(option, True, MENU_COLOR)
        options_positiones.append(
            pygame.Rect(WIDTH // 2 - text.get_width() // 2, x, text.get_width(), text.get_height()))
        if pygame.Rect.collidepoint(options_positiones[no_option], pygame.mouse.get_pos()):
            text = HOVERED_OPTIONS_OPTIONS_FONT.render(option, True, HOVERED_MENU_COLOR)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, x))
        else:
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, x))
        x += distance

        if pygame.mouse.get_pressed()[0] and pygame.Rect.collidepoint(options_positiones[no_option], pygame.mouse.get_pos()):
            pygame.time.delay(300)
            while pygame.mouse.get_pressed()[0]:
                handle_events()
            options_option_action(no_option)

        no_option += 1

    pygame.display.update()
def options():
    while True:
        clock.tick(FPS)
        handle_events()
        draw_options()

        #text = text_input(100, 100, 60, 8)
def option_action(no):
    if no == 0: # Single Player
        print("Jeszcze nie zaimplementowany")
    elif no == 1:
        pvp()
    elif no == 2:
        options()
    elif no == 3:
        exit()

def draw_menu():
    pygame.Surface.fill(WIN, BACKGROUND_COLOR)
    header = MENU_FONT.render("MENU", True, MENU_COLOR)
    WIN.blit(header, (WIDTH//2 - header.get_width()//2, TURN_BOARDER_WIDTH))
    dec = pygame.Rect(TURN_BOARDER_WIDTH, TURN_BOARDER_WIDTH + header.get_height()//3, WIDTH//2 - header.get_width()//2 - 2*TURN_BOARDER_WIDTH, header.get_height()//3)
    pygame.draw.rect(WIN, MENU_COLOR, dec)
    pygame.draw.rect(WIN, MENU_COLOR, pygame.Rect.move(dec, header.get_width()//2 + WIDTH//2, 0))

    distance = (HEIGHT - 4*TURN_BOARDER_WIDTH - MENU_FONT.get_height())// len(MENU_OPTIONS)
    options_positiones = []
    no_option = 0
    x = 3*TURN_BOARDER_WIDTH + MENU_FONT.get_height()
    for option in MENU_OPTIONS:
        text = MENU_OPTIONS_FONT.render(option, True, MENU_COLOR)
        options_positiones.append(pygame.Rect(WIDTH//2 - text.get_width()//2, x, text.get_width(), text.get_height()))
        if pygame.Rect.collidepoint(options_positiones[no_option], pygame.mouse.get_pos()):
            text = HOVERED_MENU_OPTIONS_FONT.render(option, True, HOVERED_MENU_COLOR)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, x))
        else:
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, x))
        x += distance
        if pygame.mouse.get_pressed()[0] and pygame.Rect.collidepoint(options_positiones[no_option], pygame.mouse.get_pos()):
            pygame.time.delay(500)
            option_action(no_option)

        no_option += 1

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
        vertical_boarder = pygame.Rect(x, Y_BOARD_START, BOARDER_WIDTH, BOARD_HEIGHT)
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
        text = player_name(1) + " turn"
        color = PLAYER_1_COLOR
    elif player == 2:
        text = player_name(2) + " turn"
        color = PLAYER_2_COLOR
    else:
        text = "???"
        color = DRAW_COLOR

    turn_text = TURN_TEXT_FONT.render(text, True, color)
    if is_turn_text:
        WIN.blit(turn_text, (WIDTH//2 - turn_text.get_width()//2, TURN_BOARDER_WIDTH + DIS_TEXT_TO_BOARDER))

    # Turn boarder
    turn_hor_boarder = pygame.Rect(0, 0, WIDTH, TURN_BOARDER_WIDTH)
    pygame.draw.rect(WIN, color, turn_hor_boarder)
    pygame.draw.rect(WIN, color, pygame.Rect.move(turn_hor_boarder, 0,turn_text.get_height() + TURN_BOARDER_WIDTH + DIS_TEXT_TO_BOARDER)) # + 2*DIS_TEXT_TO_BOARDER
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

def player_to_color(player):
    if player==1:
        return PLAYER_1_COLOR
    elif player == 2:
        return PLAYER_2_COLOR
    else:
        return DRAW_COLOR

def player_name(player):
    if player == 1 and Player1_name != "":
        return Player1_name
    elif player == 1:
        return P1_NAME
    elif Player2_name != "":
        return Player2_name
    else:
        return P2_NAME

def draw_winning_line(r, player):
    pygame.draw.line(WIN, WINNING_LINE_COLOR, (r[0], r[1]), (r[2], r[3]), WINNING_LINE_WIDTH)
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

def index_to_pos(r, center = True, diag = True):
    # Transform from x as a row, to x as a coordinate
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
    beg_x = beg_y = mbeg_x = mbeg_y = mend_x = mend_y = 0
    #Check row x 
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
    #Check col y
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
            if r_diag == 0:
                beg_x, beg_y = diag_x, diag_y
            r_diag += 1
        else:
            if r_diag >= max_r_diag:
                mbeg_x, mbeg_y, mend_x, mend_y = beg_x, beg_y, diag_x - 1, diag_y - 1
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

def player_turn(board, player):
    good_move = False
    while not good_move:
        clock.tick(FPS)
        handle_events()
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            c, r = pos_to_index(pos[0], pos[1])
            if valid_move(r, c, board):
                board[r][c] = player
                good_move = True

    win = check_win(player, r, c, board)
    if win:
        draw_winner(board, player_name(player) + " Wins!", player)
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
    
    exit()

def sp():
    pass

def main():
    load_options()
    recalculate()
    while True:
        clock.tick(FPS)
        draw_menu()
        handle_events()
  
if __name__ == "__main__":
    clock = pygame.time.Clock()
    main()

    exit()

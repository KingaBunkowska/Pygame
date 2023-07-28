from game import *
import os

BOARD_SIZE = get_BOARD_SIZE()


FIELD_HEIGHT, FIELD_WIDTH = (BOARD_HEIGHT - (BOARD_SIZE - 1) * BOARDER_WIDTH)//BOARD_SIZE, (BOARD_WIDTH - (BOARD_SIZE - 1) * BOARDER_WIDTH)//BOARD_SIZE
ICON_SIZE = min(FIELD_HEIGHT, FIELD_WIDTH)//2

# To-do
# test for bugs

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
    sourceFileDir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(sourceFileDir, "options.json"), "w") as options:
        with open("default_options.json", "r") as default:
            options.write(default.read())

def load_options():
    global Player1_name, Player2_name, BOARD_SIZE, CONNECTED_TO_WIN
    
    sourceFileDir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(sourceFileDir, "options.json"), "r") as file:
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
    sourceFileDir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(sourceFileDir, "options.json"), "r") as file:
        dict_json = json.loads(file.read())
        dict_json["Player 1 name"] = Player1_name
        dict_json["Player 2 name"] = Player2_name
        dict_json["Board size"] = BOARD_SIZE
        dict_json["Connected to win"] = CONNECTED_TO_WIN
    with open(os.path.join(sourceFileDir, "options.json"), "w") as file:
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


def options_option_action(no):
    if no == 0:
        set_Player_name(1, text_input())
        save_options()
    elif no == 1:
        set_Player_name(2, text_input())
        save_options()
    elif no == 2:
        set_BOARD_SIZE(number_input(CONNECTED_TO_WIN, MAX_BOARD_SIZE, BOARD_SIZE))
        save_options()
        recalculate()
    elif no == 3:
        set_CONNECTED_TO_WIN(number_input(1, BOARD_SIZE, CONNECTED_TO_WIN))
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


    pygame.display.update()
def options():
    while True:
        clock.tick(FPS)
        handle_events()
        draw_options()


def option_action(no):
    if no == 0:  # Single Player
        sp()
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
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def player_to_color(player):
    if player == 1:
        return PLAYER_1_COLOR
    elif player == 2 or player == 3:
        return PLAYER_2_COLOR
    else:
        return DRAW_COLOR


def player_name(player):
    Player1_name = get_Player_Name(1)
    Player2_name = get_Player_Name(2)

    if player == 1 and Player1_name != "":
        return get_Player_Name(1)
    if player == 1:
        return P1_NAME
    if player == 2 and Player2_name != "":
        return get_Player_Name(2)
    if player == 2:
        return P2_NAME
    if player == 3 and Player1_name != "":
        return get_Player_Name(1)
    else:
        return SP_NAME


def is_menu_button_pressed(menu_button):
    if pygame.mouse.get_pressed()[0] and pygame.Rect.collidepoint(menu_button, pygame.mouse.get_pos()):
        if confirmation():
            return True
    return False


def main():
    global BOARD_SIZE
    load_options()
    BOARD_SIZE = get_BOARD_SIZE()
    recalculate()
    while pygame.mouse.get_pressed()[0]:
        handle_events()
    while True:
        clock.tick(FPS)
        draw_menu()
        handle_events()


if __name__ == "__main__":
    main()
    exit()
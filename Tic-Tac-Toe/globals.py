import pygame
import json

pygame.font.init()
pygame.init()

clock = pygame.time.Clock()

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


P1_NAME = "PLAYER 1"
P2_NAME = "PLAYER 2"
SP_NAME = "PLAYER"
Player1_name = ""
Player2_name = ""
MENU_BUTTON = None

# MENU_BUTTON init
MENU_BUTTON = pygame.Rect(TURN_BOARDER_WIDTH + 10, TURN_BOARDER_WIDTH + (TURN_TEXT_FONT.get_height() + DIS_TEXT_TO_BOARDER)//2 - HEIGHT//32, WIDTH//12,  HEIGHT//16)

FIELD_HEIGHT, FIELD_WIDTH = (BOARD_HEIGHT - (BOARD_SIZE - 1) * BOARDER_WIDTH)//BOARD_SIZE, (BOARD_WIDTH - (BOARD_SIZE - 1) * BOARDER_WIDTH)//BOARD_SIZE
ICON_SIZE = min(FIELD_HEIGHT, FIELD_WIDTH)//2

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

def set_BOARD_SIZE(new_size):
    global BOARD_SIZE
    BOARD_SIZE = new_size

def set_CONNECTED_TO_WIN(new_val):
    global CONNECTED_TO_WIN
    CONNECTED_TO_WIN = new_val

def set_Player_name(player, new_name):
    global Player1_name, Player2_name
    if player == 1:
        print("*", new_name, Player1_name)
        Player1_name = new_name
        print(new_name, Player1_name)
    else:
        Player2_name = new_name

def get_BOARD_SIZE():
    return BOARD_SIZE

def get_CONNECTED_TO_WIN():
    return CONNECTED_TO_WIN

def get_Player_Name(player):
    global Player1_name, Player2_name
    if player == 2:
        return Player2_name
    else:
        return Player1_name

def get_FIELD_HEIGHT():
    return FIELD_HEIGHT

def get_FIELD_WIDTH():
    return FIELD_WIDTH

def get_ICON_SIZE():
    return ICON_SIZE
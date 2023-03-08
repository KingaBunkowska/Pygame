from game import *

BOARD_SIZE = get_BOARD_SIZE()


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
from globals import *


def draw_letter(x, y, letter, size):
    letter_font = pygame.font.SysFont('Calibri', size)
    ready_letter = letter_font.render(letter, True, MENU_COLOR)
    WIN.blit(ready_letter, (x, y))

def number_input(MIN, MAX, value):
    from main import clock, handle_events

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
    from main import handle_events, valid_name

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

def draw_options():
    from main import handle_events, options_option_action

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

def draw_menu():
    from main import option_action

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

def draw_window(board, player, is_turn_text = True, sp = False):
    from main import player_name

    FIELD_WIDTH = get_FIELD_WIDTH()
    FIELD_HEIGHT = get_FIELD_HEIGHT()
    ICON_SIZE = get_ICON_SIZE()

    pygame.Surface.fill(WIN, BACKGROUND_COLOR)

    #draw boarders
    y = FIELD_HEIGHT + Y_BOARD_START
    for h in range(1, len(board)):
        horizontal_boarder = pygame.Rect(X_BOARD_START, y, BOARD_WIDTH, BOARDER_WIDTH)
        y += FIELD_HEIGHT + BOARDER_WIDTH
        pygame.draw.rect(WIN, BOARDER_COLOR, horizontal_boarder)

    x = FIELD_WIDTH + X_BOARD_START
    for v in range(1, len(board)):
        vertical_boarder = pygame.Rect(x, Y_BOARD_START, BOARDER_WIDTH, BOARD_HEIGHT)
        x += FIELD_WIDTH + BOARDER_WIDTH
        pygame.draw.rect(WIN, BOARDER_COLOR, vertical_boarder)

    #draw player moves
    row, col = 0, 0
    x, y = FIELD_WIDTH//2-ICON_SIZE//2 + X_BOARD_START, FIELD_HEIGHT//2 - ICON_SIZE//2 + Y_BOARD_START

    while row < len(board):
        while col < len(board):
            if board[row][col] == 1:
                pygame.draw.line(WIN, PLAYER_1_COLOR,  (x, y), (x + ICON_SIZE, y+ICON_SIZE), ICON_SIZE//4)
                pygame.draw.line(WIN, PLAYER_1_COLOR, (x + ICON_SIZE, y), (x, y+ICON_SIZE), ICON_SIZE//4)
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
    if player == 1 and sp == False:
        text = player_name(1) + " turn"
        color = PLAYER_1_COLOR
    elif player == 2:
        text = player_name(2) + " turn"
        color = PLAYER_2_COLOR
    elif sp:
        text = player_name(3) + " turn"
        color = PLAYER_1_COLOR
    else:
        text = "???"
        color = DRAW_COLOR

    turn_text = TURN_TEXT_FONT.render(text, True, color)
    if is_turn_text:
        WIN.blit(turn_text, (WIDTH//2 - turn_text.get_width()//2, TURN_BOARDER_WIDTH + DIS_TEXT_TO_BOARDER))

    # Turn boarder
    turn_hor_boarder = pygame.Rect(0, 0, WIDTH, TURN_BOARDER_WIDTH)
    pygame.draw.rect(WIN, color, turn_hor_boarder)
    pygame.draw.rect(WIN, color, pygame.Rect.move(turn_hor_boarder, 0,turn_text.get_height() + TURN_BOARDER_WIDTH + DIS_TEXT_TO_BOARDER))
    pygame.draw.rect(WIN, color, pygame.Rect.move(turn_hor_boarder, 0, HEIGHT - TURN_BOARDER_WIDTH))
    turn_ver_boarder = pygame.Rect(0, 0, TURN_BOARDER_WIDTH, HEIGHT)
    pygame.draw.rect(WIN, color, turn_ver_boarder)
    pygame.draw.rect(WIN, color, pygame.Rect.move(turn_ver_boarder, WIDTH - TURN_BOARDER_WIDTH, 0))

    global MENU_BUTTON
    menu_button = MENU_BUTTON = pygame.Rect(TURN_BOARDER_WIDTH + 10, TURN_BOARDER_WIDTH + (turn_text.get_height() + DIS_TEXT_TO_BOARDER)//2 - HEIGHT//32, WIDTH//12,  HEIGHT//16)
    pygame.draw.rect(WIN, MENU_COLOR, menu_button)

    # draw arrow on menu_button
    pygame.draw.polygon(WIN, BACKGROUND_COLOR, ((MENU_BUTTON.x + 5, MENU_BUTTON.y + MENU_BUTTON.height//2), (MENU_BUTTON.x + 25, MENU_BUTTON.y + 5), (MENU_BUTTON.x + 25, MENU_BUTTON.y + MENU_BUTTON.height - 5)))
    pygame.draw.rect(WIN, BACKGROUND_COLOR, (MENU_BUTTON.x + 25, MENU_BUTTON.y + MENU_BUTTON.height//2 - 5, 30, 10))

    pygame.display.update()

def draw_winner(board, winner_text, player, sp = False):
    draw_window(board, player, False, sp = sp)
    if player == 0:
        color = DRAW_COLOR
    elif player == 1 or player == 3:
        color = PLAYER_1_COLOR
    else:
        color = PLAYER_2_COLOR

    text = WINNER_TEXT_FONT.render(winner_text, True, color)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, TURN_BOARDER_WIDTH + DIS_TEXT_TO_BOARDER))
    pygame.display.update()

def draw_winning_line(r, player):
    pygame.draw.line(WIN, WINNING_LINE_COLOR, (r[0], r[1]), (r[2], r[3]), WINNING_LINE_WIDTH)
    pygame.display.update()

def confirmation():
    from main import clock, handle_events

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

import pygame
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()

# SETTINGS
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (120, 120, 220)
BORDER_WIDTH = 10
BORDER_COLOR = (80, 50, 255)
BORDER = pygame.Rect(WIDTH//2-BORDER_WIDTH//2, 0, BORDER_WIDTH, HEIGHT)
WIN=pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
VEL = 3
BULLET_VEL = 5
BULLET_WIDTH, BULLET_HEIGHT = 10, 6
MAX_BULLETS = 5
YELLOW_BULLET_COLOR = (255, 255, 70)
RED_BULLET_COLOR = (255, 50, 0)
START_HEALTH = 5

WINNER_FONT = pygame.font.SysFont('Calibri', 100, bold=pygame.font.Font.bold)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
HEALTH_COLOR = (255, 255, 255)

# Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# ASSETS
sourceFileDir = os.path.dirname(os.path.abspath(__file__))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(sourceFileDir, 'Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(sourceFileDir, 'Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join(sourceFileDir, 'Assets', 'space2.jpg')), (WIDTH, HEIGHT))
#Sound
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(sourceFileDir, 'Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(sourceFileDir, 'Assets', 'Gun+Silencer.mp3'))


def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BORDER_COLOR, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # draws on window, order is important
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), True, HEALTH_COLOR)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), True, HEALTH_COLOR)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_BULLET_COLOR, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED_BULLET_COLOR, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a]:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d]:
        yellow.x += VEL
    if keys_pressed[pygame.K_w]:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s]:
        yellow.y += VEL

    yellow.x, yellow.y = border_control(yellow.x, yellow.y, "yellow")

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT]:
        red.x += VEL
    if keys_pressed[pygame.K_UP]:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN]:
        red.y += VEL

    red.x, red.y = border_control(red.x, red.y, "red")

def border_control(x, y, type):
    if type =="yellow":
        if x<0:
            x=0
        if y<0:
            y=0
        if x>=BORDER.x-SPACESHIP_WIDTH:
            x = WIDTH/2-BORDER_WIDTH/2-SPACESHIP_WIDTH
        if y>=HEIGHT-SPACESHIP_HEIGHT:
            y = HEIGHT - SPACESHIP_HEIGHT
    else:
        if x < BORDER.x+BORDER_WIDTH:
            x = BORDER.x+BORDER_WIDTH
        if y < 0:
            y = 0
        if x >= WIDTH - SPACESHIP_WIDTH:
            x = WIDTH - SPACESHIP_WIDTH
        if y >= HEIGHT-SPACESHIP_HEIGHT:
            y = HEIGHT - SPACESHIP_HEIGHT
    return x, y

def shot(player, player_bullets):
    if player.x <= BORDER.x-SPACESHIP_WIDTH:
        bullet = pygame.Rect(player.x + SPACESHIP_WIDTH, player.y + SPACESHIP_HEIGHT//2 - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
        #print("Yellow: pew!")
    else:
        bullet = pygame.Rect(player.x, player.y + SPACESHIP_HEIGHT//2 - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
        #print("Red: pew!")

    player_bullets.append(bullet)

def handle_bullets(yellow_bullets, red_bullets, yellow, red):

    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        if bullet.x >= WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x <= 0:
            red_bullets.remove(bullet)

def draw_winner(text, color):
    pygame.display.update()
    winner_text = WINNER_FONT.render(text, True, color)

    WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
    main()

def main():
    clock = pygame.time.Clock()
    run = True
    red_health = yellow_health = START_HEALTH
    yellow_bullets = []
    red_bullets = []

    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN :

                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    shot(yellow, yellow_bullets)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RALT and len(red_bullets) < MAX_BULLETS:
                    shot(red, red_bullets)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()


        if red_health == yellow_health == 0:
            draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)
            draw_winner("Draw", (255, 255, 255))
        elif red_health <= 0:
            draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)
            draw_winner("Yellow Wins!", YELLOW_BULLET_COLOR)
        elif yellow_health <= 0:
            draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)
            draw_winner("Red Wins!", RED_BULLET_COLOR)


        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)

    pygame.quit()

if __name__=="__main__":
    main()
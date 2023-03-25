import pygame.event

import game
import GUI

FPS = 60

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

if __name__ == "__main__":
    game = game.Game()
    game.spawn_snake()
    gui = GUI.GUI(game, 0, 0)
    clock = pygame.time.Clock()
    while 1: #for testing purposes, that should be done by game class probably, but clock should be only one, so if more than one game is launch, it will be synchronous
        clock.tick(FPS)
        handle_events()
        gui.draw_board()
        gui.draw_snake()
        gui.draw_fruit()
        pygame.display.flip()

# TO-DO
# in game make methode on_tick which would handle moving snake, checking is fruit eaten, also it should take player keyboard presses
# probably game class need variable current_dir so snake is moved when any key presses are not detected
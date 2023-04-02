import pygame.event

import game
import GUI

FPS = 60

def handle_events(game = None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game!=None:
            game.handle_player_moves(event)


if __name__ == "__main__":
    game = game.Game()
    games =[game]
    gui = GUI.GUI(game, 0, 0)
    clock = pygame.time.Clock()
    ticks_in_game = 0

    while 1: #for testing purposes, that should be done by game class probably, but clock should be only one, so if more than one game is launch, it will be synchronous
        clock.tick(FPS)
        handle_events(game)

        gui.draw_board()
        gui.draw_snake()
        gui.draw_fruits()
        pygame.display.flip()
        ticks_in_game+=1
        if ticks_in_game%10 == 9:
            game.snake.move()
            game.turn_activity()
# TO-DO
# in game make methode on_tick which would handle moving snake, checking is fruit eaten, also it should take player keyboard presses
# probably game class need variable current_dir so snake is moved when any key presses are not detected
# when fruits are adjusted the second is left unpicked
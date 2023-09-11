import pygame.event

import Game

FPS = 60

def handle_events(game=None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game != None:
            game.handle_player_moves(event)


if __name__ == "__main__":
    
    clock = pygame.time.Clock()

    game = Game.Game(fruit_number=1)
    game.run(clock)


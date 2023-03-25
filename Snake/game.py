import random

import pygame

import snake

class Game:
    board_size = 15
    random_start = False
    snake = None
    fruit = (10, 7)

    def __init__(self, s=15):
        if s>=3 and s<=40:
            self.board_size = s
        else:
            self.board_size = 15
        self.random_start = False


    def set_random_start(self, bool):
        if bool == 0 or bool == 1:
            self.random_start = bool

    def spawn_snake(self, poz_x=board_size//2, poz_y=board_size//2):
        self.snake = snake.Snake(poz_x, poz_y)

    def spawn_fruit(self):
        x, y = random.randint(0,self.board_size), random.randint(0,self.board_size)
        while self.snake.is_field_occupied():
            x, y = random.randint(0, self.board_size), random.randint(0, self.board_size)

        self.fruits.append((x, y))

    def snake_eats_fruit(self):
        snake.eat()
        self.spawn_fruit()

    def get_dir_from_player(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.K_w:
                return (0, -1)
            if event.type == pygame.K_s:
                return (0, 1)
            if event.type == pygame.K_d:
                return (1, 0)
            if event.type == pygame.K_a:
                return (-1, 0)

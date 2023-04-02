import random
import pygame
import snake

class Game:
    board_size = 15
    random_start = False
    snake = None
    fruits = [(10, 7)]
    last_dir = (1, 0)
    turn_dir = (1, 0)

    def __init__(self, s=15, fruit_number=0):
        if s>=3 and s<=40:
            self.board_size = s
        else:
            self.board_size = 15
        self.random_start = False

        self.spawn_snake()

        for i in range(fruit_number):
            self.spawn_fruit()

    def set_random_start(self, bool):
        if bool == 0 or bool == 1:
            self.random_start = bool

    def spawn_snake(self, poz_x=board_size//2, poz_y=board_size//2):
        self.snake = snake.Snake(poz_x, poz_y)

    def is_field_occupied(self, x, y):
        if self.snake.is_field_occupied(x, y):
            for fruit in self.fruits:
                if fruit == (x, y):
                    return True
        return False

    def spawn_fruit(self):
        x, y = random.randint(0,self.board_size-1), random.randint(0,self.board_size-1)
        while self.is_field_occupied(x, y):
            x, y = random.randint(0, self.board_size), random.randint(0, self.board_size)

        self.fruits.append((x, y))

    def snake_eats_fruit(self):
        self.snake.eat()
        self.spawn_fruit()

    def turn_activity(self):
        for fruit_no in range(len(self.fruits)):
            if self.snake.head() == self.fruits[fruit_no]:
                self.snake_eats_fruit()
                self.fruits.pop(fruit_no)

        self.last_dir = self.turn_dir
    def handle_player_moves(self, event):
        dir = self.last_dir
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                dir = (0, -1)
            if event.key == pygame.K_d:
                dir = (1, 0)
            if event.key == pygame.K_s:
                dir = (0, 1)
            if event.key == pygame.K_a:
                dir = (-1, 0)

            if dir[0] == (-1)*self.last_dir[0] and dir[1] == (-1)*self.last_dir[1]:
                dir = self.turn_dir

            print(dir, self.snake.dir)
            self.turn_dir = dir
            self.snake.set_dir(dir)

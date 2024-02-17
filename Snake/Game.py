import random
import pygame
import snake
import GUI
import main
import time


class Game:
    board_size = 15
    snake = None
    fruits = [(10, 7)]
    last_dir = (1, 0)
    turn_dir = (1, 0)
    score = 0
    start_time = time.time()

    def __init__(self, s=15, fruit_number=0):
        if s >= 3 and s <= 40:
            self.board_size = s
        else:
            self.board_size = 15

        self.spawn_snake()

        for i in range(fruit_number - 1):
            self.spawn_fruit()

    def spawn_snake(self, poz_x=board_size // 2, poz_y=board_size // 2):
        self.snake = snake.Snake(poz_x, poz_y)

    def snake_is_facing_boarder(self):

        # left
        if self.snake.head()[0] == 0 and self.last_dir==(-1, 0):
            return True
        # right
        if self.snake.head()[0] == self.board_size-1 and self.last_dir==(1, 0):
            return True
        # up
        if self.snake.head()[1] == 0 and self.last_dir==(0, -1):
            return True
        # down
        if self.snake.head()[1] == self.board_size-1 and self.last_dir==(0, 1):
            return True
    
        return False

    def is_field_occupied(self, x, y):
        for fruit in self.fruits:
            if fruit[0] == x and fruit[1] == y:
                return True
        return False

    def spawn_fruit(self):
        # is board full
        if self.score + len(self.fruits) >= self.board_size**2:
            return

        x, y = random.randint(0, self.board_size - 1), random.randint(
            0, self.board_size - 1
        )
        while self.is_field_occupied(x, y) or self.snake.is_field_occupied(x, y):
            x, y = random.randint(0, self.board_size - 1), random.randint(
                0, self.board_size - 1
            )

        self.fruits.append((x, y))

    def snake_eats_fruit(self):
        self.snake.eat()
        self.spawn_fruit()
        self.score += 1

    def turn_activity(self):
        # check if snakes body touched a fruit
        for fruit_no in range(len(self.fruits)):
            if (
                fruit_no < len(self.fruits)
                and self.snake.head() == self.fruits[fruit_no]
            ):
                self.snake_eats_fruit()
                self.fruits.pop(fruit_no)

        # check if snake touched itself or move form board
        if self.snake.collide(self.board_size):
            print("GAME OVER! Score:", self.score)
            pygame.quit()
            exit()

        if self.score == self.board_size**2 - 1:
            print("You won! Score:", self.score)
            pygame.quit()
            exit()

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

            # check if desired move is valid
            if dir[0] == (-1) * self.last_dir[0] and dir[1] == (-1) * self.last_dir[1]:
                dir = self.turn_dir

            self.turn_dir = dir
            self.snake.set_dir(dir)

    def run(self, clock):
        gui = GUI.GUI(self, 5, 5)  
        ticks_in_game = 0
        while (1):
            clock.tick(main.FPS)
            main.handle_events(self)

            
            ticks_in_game += 1
            if ticks_in_game % 10 == 9:

                self.snake.move()
                self.turn_activity() 

                gui.draw_board()
                gui.draw_snake()
                gui.draw_fruits()
                gui.draw_border()
                gui.draw_score(self.score)
                gui.draw_time(time.time()-self.start_time)

                pygame.display.flip()


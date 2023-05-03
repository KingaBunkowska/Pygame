import pygame

pygame.init()

class GUI:

    EYE_COLOR = (0, 0, 0)
    EYE_WIDTH = 20
    EYE_SIZE = 5
    #TODO:  make eye_width precent value, so it depends on width of snake body
    def __init__(self, game, x_start, y_start, x_end=-1, y_end=-1):

        self.WIDTH, self.HEIGHT = 800, 600
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.FIELD_COLORS = ((100, 230, 150), (50, 230, 80))
        self.BACKGROUND_COLOR = (120, 190, 160)
        self.SNAKE_COLOR = (240, 240, 100)
        self.game = game
        self.FRUIT_COLOR = (240, 50, 50)

        if x_end == -1:
            x_end, y_end = self.WIDTH, self.HEIGHT
        self.LEFT = x_start
        self.TOP = y_start
        self.FIELD_SIZE = (y_end - y_start)//game.board_size

    def draw_board(self):
        pygame.Surface.fill(self.WIN, self.BACKGROUND_COLOR)

        FIELD = pygame.Rect(self.LEFT, self.TOP, self.FIELD_SIZE, self.FIELD_SIZE)

        i = 0
        for row in range(0, self.game.board_size):
            for col in range(0, self.game.board_size):
                pygame.draw.rect(self.WIN, self.FIELD_COLORS[i%2], FIELD)
                FIELD = FIELD.move(self.FIELD_SIZE, 0)
                i+=1
            FIELD.update(0,self.FIELD_SIZE*(row+1), self.FIELD_SIZE, self.FIELD_SIZE)


        #pygame.display.update()

        # draw square representing fields in different colours

        # check if values are actually square
        #draw_lines between fields
        #draw background
        #draw boarders around board(if there is a place for them)

    def pos_to_coordinates(self, coordinates): # return top left corner
        return (self.FIELD_SIZE*coordinates[0], self.FIELD_SIZE*coordinates[1])

    def draw_snake(self):

        head_coordinates = self.pos_to_coordinates(self.game.snake.head())
        head = pygame.Rect(head_coordinates[0], head_coordinates[1], self.FIELD_SIZE, self.FIELD_SIZE)
        pygame.draw.rect(self.WIN, self.SNAKE_COLOR, head)

        # draw eyes
        #TODO: make eyes turn when snake turns
        pygame.draw.circle(self.WIN, self.EYE_COLOR, (head.x+head.width/2, head.y+head.height/2+self.EYE_WIDTH/2), self.EYE_SIZE)
        pygame.draw.circle(self.WIN, self.EYE_COLOR, (head.x + head.width / 2, head.y + head.height / 2 - self.EYE_WIDTH / 2), self.EYE_SIZE)

        for i in range(1, len(self.game.snake.snake_body)):
            part_coordinates = self.pos_to_coordinates(self.game.snake.snake_body[i])
            body_part = pygame.Rect(part_coordinates[0], part_coordinates[1], self.FIELD_SIZE, self.FIELD_SIZE)
            pygame.draw.rect(self.WIN, self.SNAKE_COLOR, body_part)

        #pygame.display.update()

    def draw_fruits(self):
        for fruit in self.game.fruits:
            fruit_coordinates = self.pos_to_coordinates(fruit)
            pygame.draw.circle(self.WIN, self.FRUIT_COLOR, (fruit_coordinates[0]+self.FIELD_SIZE//2, fruit_coordinates[1]+self.FIELD_SIZE//2), self.FIELD_SIZE//2)

        #pygame.display.update()


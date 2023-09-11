import pygame

pygame.init()


class GUI:
    EYE_COLOR = (0, 0, 0)
    EYE_WIDTH = 20
    EYE_SIZE = 5
    TONGUE_COLOR = (235, 35, 35)
    TONGUE_LENGHT = 10
    TONGUE_WIDTH = 5

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
        self.FIELD_SIZE = (y_end - y_start) // game.board_size

        self.scale_percent = self.FIELD_SIZE / 40
        self.TONGUE_LENGHT *= self.scale_percent
        self.TONGUE_WIDTH *= self.scale_percent
        self.EYE_SIZE *= self.scale_percent
        self.EYE_WIDTH *= self.scale_percent

    def draw_board(self):
        pygame.Surface.fill(self.WIN, self.BACKGROUND_COLOR)

        FIELD = pygame.Rect(self.LEFT, self.TOP, self.FIELD_SIZE, self.FIELD_SIZE)

        i = 0
        for row in range(0, self.game.board_size):
            for col in range(0, self.game.board_size):
                pygame.draw.rect(self.WIN, self.FIELD_COLORS[i % 2], FIELD)
                FIELD = FIELD.move(self.FIELD_SIZE, 0)
                i += 1
            FIELD.update(
                self.LEFT,
                self.TOP + self.FIELD_SIZE * (row + 1),
                self.FIELD_SIZE,
                self.FIELD_SIZE,
            )

    def pos_to_coordinates(self, coordinates):  # return top left corner
        return (
            self.LEFT + self.FIELD_SIZE * coordinates[0],
            self.TOP + self.FIELD_SIZE * coordinates[1],
        )

    def draw_snake(self):
        head_coordinates = self.pos_to_coordinates(self.game.snake.head())
        head = pygame.Rect(
            head_coordinates[0], head_coordinates[1], self.FIELD_SIZE, self.FIELD_SIZE
        )
        pygame.draw.rect(self.WIN, self.SNAKE_COLOR, head)

        self.draw_eyes(head)
        if not self.game.snake_is_facing_boarder():
            self.draw_tongue(head)

        gradiented_snake_color = [self.SNAKE_COLOR[i] for i in range(3)]

        for i in range(1, len(self.game.snake.snake_body)):
            gradiented_snake_color[2] = min(200, gradiented_snake_color[2] + 2)
            part_coordinates = self.pos_to_coordinates(self.game.snake.snake_body[i])
            body_part = pygame.Rect(
                part_coordinates[0],
                part_coordinates[1],
                self.FIELD_SIZE,
                self.FIELD_SIZE,
            )
            pygame.draw.rect(self.WIN, gradiented_snake_color, body_part)

    def draw_eyes(self, head: pygame.Rect) -> None:
        if self.game.last_dir[0] != 0:
            pygame.draw.circle(
                self.WIN,
                self.EYE_COLOR,
                (
                    head.x + head.width / 2,
                    head.y + head.height / 2 + self.EYE_WIDTH / 2,
                ),
                self.EYE_SIZE,
            )
            pygame.draw.circle(
                self.WIN,
                self.EYE_COLOR,
                (
                    head.x + head.width / 2,
                    head.y + head.height / 2 - self.EYE_WIDTH / 2,
                ),
                self.EYE_SIZE,
            )
        else:
            pygame.draw.circle(
                self.WIN,
                self.EYE_COLOR,
                (
                    head.x + head.width / 2 + self.EYE_WIDTH / 2,
                    head.y + head.height / 2,
                ),
                self.EYE_SIZE,
            )
            pygame.draw.circle(
                self.WIN,
                self.EYE_COLOR,
                (
                    head.x + head.width / 2 - self.EYE_WIDTH / 2,
                    head.y + head.height / 2,
                ),
                self.EYE_SIZE,
            )

    def draw_tongue(self, head: pygame.Rect) -> None:
        # left
        if self.game.last_dir[0] == 1:
            tongue = pygame.Rect(
                head.x + head.width,
                head.y + head.height / 2 - self.TONGUE_WIDTH / 2,
                self.TONGUE_LENGHT,
                self.TONGUE_WIDTH,
            )
            pygame.draw.polygon(
                self.WIN,
                self.TONGUE_COLOR,
                [
                    (tongue.x + self.TONGUE_LENGHT, tongue.y),
                    (
                        tongue.x + self.TONGUE_WIDTH + self.TONGUE_LENGHT,
                        tongue.y - self.TONGUE_WIDTH,
                    ),
                    (tongue.x + self.TONGUE_WIDTH + self.TONGUE_LENGHT, tongue.y - 1),
                    (
                        tongue.x + self.TONGUE_WIDTH / 2 + self.TONGUE_LENGHT,
                        tongue.y + self.TONGUE_WIDTH / 2,
                    ),
                    (
                        tongue.x + self.TONGUE_WIDTH + self.TONGUE_LENGHT,
                        tongue.y + tongue.height,
                    ),
                    (
                        tongue.x + self.TONGUE_WIDTH + self.TONGUE_LENGHT,
                        tongue.y + 2 * self.TONGUE_WIDTH - 1,
                    ),
                    (tongue.x + self.TONGUE_LENGHT, tongue.y + tongue.height - 1),
                ],
            )
        # right
        elif self.game.last_dir[0] == -1:
            tongue = pygame.Rect(
                head.x - self.TONGUE_LENGHT,
                head.y + head.height / 2 - self.TONGUE_WIDTH / 2,
                self.TONGUE_LENGHT,
                self.TONGUE_WIDTH,
            )
            pygame.draw.polygon(
                self.WIN,
                self.TONGUE_COLOR,
                [
                    (tongue.x, tongue.y),
                    (tongue.x - self.TONGUE_WIDTH, tongue.y - self.TONGUE_WIDTH),
                    (tongue.x - self.TONGUE_WIDTH, tongue.y - 2),
                    (
                        tongue.x - self.TONGUE_WIDTH / 2 + 1,
                        tongue.y + self.TONGUE_WIDTH / 2,
                    ),
                    (tongue.x - self.TONGUE_WIDTH, tongue.y + tongue.height),
                    (
                        tongue.x - self.TONGUE_WIDTH,
                        tongue.y + 2 * self.TONGUE_WIDTH - 1,
                    ),
                    (tongue.x, tongue.y + tongue.height - 1),
                ],
            )
        # up
        elif self.game.last_dir[1] == -1:
            tongue = pygame.Rect(
                head.x + head.width / 2 - self.TONGUE_WIDTH / 2,
                head.y - self.TONGUE_LENGHT,
                self.TONGUE_WIDTH,
                self.TONGUE_LENGHT,
            )
            pygame.draw.polygon(
                self.WIN,
                self.TONGUE_COLOR,
                [
                    (tongue.x, tongue.y),
                    (tongue.x - self.TONGUE_WIDTH, tongue.y - self.TONGUE_WIDTH),
                    (tongue.x - 1, tongue.y - self.TONGUE_WIDTH),
                    (
                        tongue.x + self.TONGUE_WIDTH / 2,
                        tongue.y - self.TONGUE_WIDTH / 2 + 1,
                    ),
                    (tongue.x + self.TONGUE_WIDTH, tongue.y - self.TONGUE_WIDTH),
                    (
                        tongue.x + 2 * self.TONGUE_WIDTH - 1,
                        tongue.y - self.TONGUE_WIDTH,
                    ),
                    (tongue.x + self.TONGUE_WIDTH - 1, tongue.y),
                ],
            )
        # down
        else:
            tongue = pygame.Rect(
                head.x + head.width / 2 - self.TONGUE_WIDTH / 2,
                head.y + head.height,
                self.TONGUE_WIDTH,
                self.TONGUE_LENGHT,
            )
            pygame.draw.polygon(
                self.WIN,
                self.TONGUE_COLOR,
                [
                    (tongue.x, tongue.y + self.TONGUE_LENGHT),
                    (
                        tongue.x - self.TONGUE_WIDTH,
                        tongue.y + self.TONGUE_WIDTH + self.TONGUE_LENGHT,
                    ),
                    (tongue.x - 1, tongue.y + self.TONGUE_WIDTH + self.TONGUE_LENGHT),
                    (
                        tongue.x + self.TONGUE_WIDTH / 2,
                        tongue.y + self.TONGUE_WIDTH / 2 + self.TONGUE_LENGHT,
                    ),
                    (
                        tongue.x + self.TONGUE_WIDTH,
                        tongue.y + self.TONGUE_WIDTH + self.TONGUE_LENGHT,
                    ),
                    (
                        tongue.x + 2 * self.TONGUE_WIDTH - 1,
                        tongue.y + self.TONGUE_WIDTH + self.TONGUE_LENGHT,
                    ),
                    (tongue.x + self.TONGUE_WIDTH - 1, tongue.y + self.TONGUE_LENGHT),
                ],
            )

        pygame.draw.rect(self.WIN, self.TONGUE_COLOR, tongue)

    def draw_fruits(self):
        for fruit in self.game.fruits:
            fruit_coordinates = self.pos_to_coordinates(fruit)
            pygame.draw.circle(
                self.WIN,
                self.FRUIT_COLOR,
                (
                    fruit_coordinates[0] + self.FIELD_SIZE // 2,
                    fruit_coordinates[1] + self.FIELD_SIZE // 2,
                ),
                self.FIELD_SIZE // 2,
            )

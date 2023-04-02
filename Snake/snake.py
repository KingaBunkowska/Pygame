from collections import deque

class Snake:

    lenght = 1
    dir = [1, 0]

    def __init__(self, poz_x, poz_y):
        self.snake_body = deque()
        self.snake_body.append((poz_x, poz_y))

    def eat(self):
        x, y = self.tail()
        self.move()
        self.lenght += 1
        self.snake_body.append((x, y))

    def tail(self):
        tail = self.snake_body[len(self.snake_body)-1]
        return tail

    def head(self):
        head = self.snake_body[0]
        return head

    def set_dir(self, dir):
        self.dir = dir

    def move(self):
        self.snake_body.appendleft((self.head()[0]+self.dir[0], self.head()[1]+self.dir[1]))
        self.snake_body.pop()

    def is_field_occupied(self, x, y):
        for body_part in self.snake_body:
            if body_part == (x, y):
                return True
        return False
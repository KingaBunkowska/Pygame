from collections import deque

class Snake:

    dir = [1, 0]
    is_grow = 0

    def __init__(self, poz_x, poz_y):
        self.snake_body = deque()
        self.snake_body.append((poz_x, poz_y))

    def eat(self):
        x, y = self.tail()
        self.is_grow = (x, y)


    def grow(self):
        if self.is_grow!=0:
            self.snake_body.append((self.is_grow))

        self.is_grow=0

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
        self.grow()

    def is_field_occupied(self, x, y):
        for body_part in self.snake_body:
            if body_part == (x, y):
                return True
        return False

    def collide(self, board_size):
        head = self.head()
        for i in range(1, len(self.snake_body)):
            if self.snake_body[i] == head:
                return True

        if head[0]<0 or head[1]<0 or head[0]>=board_size or head[1]>=board_size:
            return True

        return False
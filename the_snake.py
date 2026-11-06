import sys
from random import choice, randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_POSITION = (320, 240)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

TURNS = {
    pg.K_UP: (UP, DOWN),
    pg.K_DOWN: (DOWN, UP),
    pg.K_LEFT: (LEFT, RIGHT),
    pg.K_RIGHT: (RIGHT, LEFT),
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BASE_COLOR = (0, 0, 0)

SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=START_POSITION, body_color=BASE_COLOR):
        """Инициализация переменных."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заглушка отрисовки."""
        class_name = self.__class__.__name__
        message = f'Метод не переопределен в дочернем классе {class_name}'
        raise NotImplementedError(message)

    def draw_square(self, position=None, body_color=None, border=True):
        """Отрисовывает квадрат."""
        position = position or self.position
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        body_color = body_color or self.body_color
        pg.draw.rect(screen, body_color, rect)
        if border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Отвечает за появление и отрисовку яблока."""

    def __init__(self, position=START_POSITION, body_color=APPLE_COLOR):
        """Инициализация переменных."""
        super().__init__(position, body_color)

    def randomize_position(self, using_squares):
        """Генерирует случайные координаты яблока."""
        while True:
            position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (position_x, position_y)
            if self.position not in using_squares:
                break

    def draw(self):
        """Отрисовывает яблоко."""
        self.draw_square()


class Snake(GameObject):
    """Отвечает за движение и отрисовку змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация переменных."""
        super().__init__(body_color=body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку в заданном направлении."""
        head_position_x, head_position_y = self.get_head_position()
        new_head_position_x = head_position_x + self.direction[0] * GRID_SIZE
        new_head_position_x = new_head_position_x % SCREEN_WIDTH
        new_head_position_y = head_position_y + self.direction[1] * GRID_SIZE
        new_head_position_y = new_head_position_y % SCREEN_HEIGHT
        new_head_position = (new_head_position_x, new_head_position_y)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает игру до изначального состояния."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self):
        """Отрисовывает змейку."""
        self.draw_square(self.get_head_position(), self.body_color)
        if self.last:
            self.draw_square(self.last, BOARD_BACKGROUND_COLOR, False)


def handle_keys(game_object):
    """Изменяет направление движения."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN and event.key in TURNS:
            new_direction, opposite = TURNS[event.key]
            if game_object.direction != opposite:
                game_object.next_direction = new_direction
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()


def main():
    """Основной игровой процесс."""
    pg.init()
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        head_position = snake.get_head_position()
        if apple.position == head_position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif head_position in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

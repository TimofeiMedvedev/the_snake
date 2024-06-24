from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет фона по умолчанию:
DEFAULT_OBG_COLOR = (100, 100, 100)

# Цвет змейки по умолчанию:
SNAKE_GREEN = (0, 255, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Создадим базовый класс c общими атрибутами."""

    def __init__(self, body_color=None, next_direction=None
                 ) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color
        self.next_direction = next_direction

    def draw(self):
        """создадим метод отрисовки для изменений в дочернем классе."""
        raise NotImplementedError('добавить этот метод в дочерние классы')

    def draw_rect(self, position_draw):
        """А это общий модуль для отрисовки фигур в дочерних классах"""
        rect = pg.Rect(position_draw, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Создадим класс объекта - Яблоко."""

    def __init__(self, body_color=None) -> None:
        super().__init__(body_color)
        self.body_color = APPLE_COLOR
        self.randomize_position([])

    def randomize_position(self, position_list):
        """Метод определения случайных координат в яблоке."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

        while self.position in position_list:
            # self.randomize_position(position_list)
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )   

    def draw(self):
        """Метод рисования яблока."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Создадим класс объекта - Змейка."""

    def __init__(self, body_color=None, next_direction=None) -> None:
        super().__init__(body_color, next_direction)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.body_color = SNAKE_GREEN
        self.last = 0

    def update_direction(self, next_direction):
        """Метод изменения направления змейки после нажатия на кнопку."""
        if next_direction:
            self.direction = next_direction
            next_direction = None

    def move(self):
        """Метод вычисления координат головы и тела змейки при
        движении, а также проверка на столкновение с телом змейки
        """
        (x_head, y_head) = self.get_head_position()
        x, y = self.direction
        self.update_direction(self.next_direction)
        x_new_head_snake = (x_head + x * GRID_SIZE) % SCREEN_WIDTH
        y_new_head_snake = (y_head + y * GRID_SIZE) % SCREEN_HEIGHT
        new_head_snake = (x_new_head_snake, y_new_head_snake)

        self.positions.insert(0, new_head_snake)

        self.last = self.positions.pop() if len(self.positions) > self.length\
            else self.last == 0

    def draw(self):
        """Метод отрисовки змейки и затирание последнего сегмента"""
        for position_snake in self.positions[:-1]:
            self.draw_rect(position_snake)

        # Рисование головы
        self.draw_rect(self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Делаем сброс настроек через _init_, чтобы не дублировать код"""
        self.__init__()

    def get_head_position(self):
        """Возвращение сегмента головы змейки"""
        return self.positions[0]


def handle_keys(game_object):
    """Функция управления объектом класса яблоко или змейки"""
    dir_key = {
        pg.K_UP: UP,
        pg.K_DOWN: DOWN,
        pg.K_LEFT: LEFT,
        pg.K_RIGHT: RIGHT}
    
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                pg.quit()
                raise SystemExit
            dir = dir_key.get(event.key, game_object.direction)
            if not (dir[0] + game_object.direction[0] == 0 and dir[1] + game_object.direction[1] == 0):
                game_object.next_direction = dir
               

def main():
    """Функция, где находится основной игровой цикл"""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            position_list = snake.positions
            apple.randomize_position(position_list)
        snake.move()
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

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

    def __init__(self, body_color=None, position=None, position_list=None) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color
        self.position_list = position_list
        
    

class Apple(GameObject):
    """Создадим класс объекта - Яблоко."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        
        self.randomize_position(self.position_list)
    
    def randomize_position(self, position_list):
        """Метод определения случайных координат в яблоке."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

        if position_list not in self.position:
            self.position = self.position

    
        
            

    def draw(self):
        """Метод рисования яблока."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Создадим класс объекта - Змейка."""

    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_GREEN
        self.last = 0

    def update_direction(self):
        """Метод изменения направления змейки после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод вычисления координат головы и тела змейки при
        движении, а также проверка на столкновение с телом змейки
        """
        x_head, y_head = self.get_head_position()
        x, y = self.direction
        self.update_direction()
        x_new_head_snake = (x_head + x * GRID_SIZE) % SCREEN_WIDTH
        y_new_head_snake = (y_head + y * GRID_SIZE) % SCREEN_HEIGHT
        new_head_snake = (x_new_head_snake, y_new_head_snake)

        self.positions.insert(0, new_head_snake)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод отрисовки змейки и затирание последнего сегмента"""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)   
    
    def get_head_position(self):
        """Возвращение сегмента головы змейки"""
            
        (x_0, y_0) = self.positions[0]
        return (x_0, y_0)
    
    def reset(self):
        """Метод сброса настроек змейки при столкновении"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = randint(UP, LEFT, RIGHT, DOWN)
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция управления объектом класса яблоко или змейки"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


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
        snake.move()
        snake.draw()
        apple.draw()
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            position_list = snake.positions[:-1]
            apple.randomize_position(position_list)
        

        pg.display.update()


if __name__ == '__main__':
    main()

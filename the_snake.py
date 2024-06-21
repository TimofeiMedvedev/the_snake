from random import randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Создадим базовый класс c общими атрибутами."""

    def __init__(self, body_color=None, position=None) -> None:
        self.position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.body_color = body_color
        self.positions = [self.position]
        self.randomize_position()

    def draw(self):
        """Метод отрисовки змейки и затирание последнего сегмента"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
    
    def randomize_position(self):
        """Метод определения случайных координат в яблоке."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

        if self.position in self.position:
            return False


class Apple(GameObject):
    """Создадим класс объекта - Яблоко."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод рисования яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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
        head_snake = self.get_head_position()
        x, y = self.direction
        self.update_direction()
        new_head_snake = (
            (head_snake[0] + x * GRID_SIZE) % SCREEN_WIDTH,
            (head_snake[1] + y * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_head_snake in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_snake)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def get_head_position(self):
        """Возвращение сегмента головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод сброса настроек змейки при столкновении"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = randint(UP, DOWN, LEFT, RIGHT)
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция управления объектом класса яблоко или змейки"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция, где находится основной игровой цикл"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()
        snake.draw()
        apple.draw()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        pygame.display.update()


if __name__ == '__main__':
    main()

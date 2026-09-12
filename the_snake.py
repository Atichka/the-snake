"""Игра «Змейка» на PyGame."""

import random

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

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self,
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        body_color=(255, 255, 255),
    ):
        """Инициализирует позицию и цвет объекта."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = (screen_width / 2, screen_height / 2)
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объекта. Переопределяется в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс яблока, которое съедает змейка."""

    def __init__(
        self,
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
    ):
        """Инициализирует яблоко в случайной позиции."""
        super().__init__(screen_width, screen_height, body_color=(255, 0, 0))
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        # Количество клеток по горизонтали и вертикали
        cols = self.screen_width // GRID_SIZE
        rows = self.screen_height // GRID_SIZE

        # Случайная клетка
        x = random.randint(0, cols - 1) * GRID_SIZE
        y = random.randint(0, rows - 1) * GRID_SIZE

        # Сохраняем координаты
        self.position = (x, y)

    # Метод draw класса Apple
    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, которой управляет игрок."""

    def __init__(
        self,
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
    ):
        """Инициализирует змейку в центре экрана."""
        super().__init__(screen_width, screen_height, body_color=(0, 255, 0))
        self.length = 1
        self.positions = [(screen_width // 2, screen_height // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    # Метод draw класса Snake
    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Двигает змейку в текущем направлении."""
        dx, dy = self.direction
        head = self.get_head_position()

        new_head = (
            (head[0] + dx * GRID_SIZE) % self.screen_width,
            (head[1] + dy * GRID_SIZE) % self.screen_height,
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновляет направление движения после нажатия клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(self.screen_width // 2, self.screen_height // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для изменения направления змейки."""
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
    """Запускает основной игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT)
    apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

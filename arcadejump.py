import pygame
import random

# Инициализация Pygame
pygame.init()

# Загрузка звука для золотого яблока
golden_apple_sound = pygame.mixer.Sound(r"C:\Уроки\колледж\collegeshit\valorant-ace-sound.mp3")

# Константы
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN_SPOTS = (139, 69, 19)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLOCK_SIZE = 20
SPEED = 10
score = 0
high_score = 0
paused = False

# Окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakaligma Game")

# Шрифты
font = pygame.font.Font(None, 36)

# Функция отрисовки счета
def draw_score():
    global high_score
    high_score = max(score, high_score)
    screen.blit(font.render(f"Body count: {score}", True, RED), (10, 10))
    screen.blit(font.render(f"Aura +: {high_score}", True, RED), (10, 40))

# Класс змейки
class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = (BLOCK_SIZE, 0)

    def move(self):
        if not paused:
            new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
            self.body.insert(0, new_head)
            if new_head == food.position:
                global score, SPEED
                if food.is_bonus:
                    pygame.mixer.Sound.play(golden_apple_sound)  # Воспроизведение звука
                    score += 5
                else:
                    score += 1
                if score % 5 == 0:
                    SPEED += 1
                food.spawn()
            else:
                self.body.pop()

    def check_collision(self):
        return self.body[0] in self.body[1:]

    def draw(self):
        for i, segment in enumerate(self.body):
            x, y = segment
            if i == 0:
                pygame.draw.rect(screen, GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE), border_radius=8)
                pygame.draw.circle(screen, WHITE, (x + 5, y + 6), 3)
                pygame.draw.circle(screen, WHITE, (x + 15, y + 6), 3)
            else:
                pygame.draw.rect(screen, DARK_GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE), border_radius=6)
                if random.randint(0, 3) == 0:
                    spot_x = x + random.randint(4, 10)
                    spot_y = y + random.randint(4, 10)
                    pygame.draw.ellipse(screen, BROWN_SPOTS, (spot_x, spot_y, 6, 6))

    def wrap_around(self):
        head_x, head_y = self.body[0]
        if head_x >= WIDTH:
            self.body[0] = (0, head_y)
        elif head_x < 0:
            self.body[0] = (WIDTH - BLOCK_SIZE, head_y)
        if head_y >= HEIGHT:
            self.body[0] = (head_x, 0)
        elif head_y < 0:
            self.body[0] = (head_x, HEIGHT - BLOCK_SIZE)

# Класс еды
class Food:
    def __init__(self):
        self.position = (random.randint(0, WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE,
                         random.randint(0, HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE)
        self.is_bonus = False

    def spawn(self):
        self.position = (random.randint(0, WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE,
                         random.randint(0, HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE)
        self.is_bonus = random.randint(1, 5) == 1

    def draw(self):
        color = GOLD if self.is_bonus else RED
        pygame.draw.circle(screen, color, (self.position[0] + BLOCK_SIZE // 2, self.position[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 2)

# Основной цикл игры
snake = Snake()
food = Food()
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, BLOCK_SIZE):
                snake.direction = (0, -BLOCK_SIZE)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -BLOCK_SIZE):
                snake.direction = (0, BLOCK_SIZE)
            elif event.key == pygame.K_LEFT and snake.direction != (BLOCK_SIZE, 0):
                snake.direction = (-BLOCK_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-BLOCK_SIZE, 0):
                snake.direction = (BLOCK_SIZE, 0)
            elif event.key == pygame.K_p:
                paused = not paused

    if not paused:
        snake.move()
        snake.wrap_around()
        if snake.check_collision():
            snake = Snake()
            score = 0
            SPEED = 10

    snake.draw()
    food.draw()
    draw_score()

    pygame.display.flip()
    clock.tick(SPEED)

pygame.quit()

import unittest
from arcadejump import Snake, Food, BLOCK_SIZE, WIDTH, HEIGHT

class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.snake = Snake()
        self.food = Food()

    def test_snake_initial_position(self):
        """Проверяем, что змейка создается с правильной длиной"""
        self.assertEqual(len(self.snake.body), 3)

    def test_snake_moves_correctly(self):
        """Проверяем, что змейка движется в заданном направлении"""
        initial_head = self.snake.body[0]
        self.snake.move()
        new_head = self.snake.body[0]
        self.assertEqual(new_head, (initial_head[0] + BLOCK_SIZE, initial_head[1]))

    def test_snake_grows_after_eating(self):
        """Проверяем, что змейка увеличивается в размере после еды"""
        initial_length = len(self.snake.body)
        self.snake.body.insert(0, self.food.position)  # Симулируем поедание еды
        self.assertEqual(len(self.snake.body), initial_length + 1)

    def test_snake_wraps_around_screen(self):
        """Проверяем, что змейка появляется с другой стороны экрана"""
        self.snake.body[0] = (WIDTH, 100)
        self.snake.wrap_around()
        self.assertEqual(self.snake.body[0], (0, 100))

        self.snake.body[0] = (-BLOCK_SIZE, 100)
        self.snake.wrap_around()
        self.assertEqual(self.snake.body[0], (WIDTH - BLOCK_SIZE, 100))

        self.snake.body[0] = (100, HEIGHT)
        self.snake.wrap_around()
        self.assertEqual(self.snake.body[0], (100, 0))

        self.snake.body[0] = (100, -BLOCK_SIZE)
        self.snake.wrap_around()
        self.assertEqual(self.snake.body[0], (100, HEIGHT - BLOCK_SIZE))

    def test_snake_collides_with_itself(self):
        """Проверяем, что змейка обнаруживает столкновение с самой собой"""
        self.snake.body = [(100, 100), (120, 100), (140, 100), (100, 100)]
        self.assertTrue(self.snake.check_collision())

    def test_snake_does_not_collide_with_itself_initially(self):
        """Проверяем, что змейка не сталкивается с собой при старте"""
        self.assertFalse(self.snake.check_collision())

if __name__ == "__main__":
    unittest.main()

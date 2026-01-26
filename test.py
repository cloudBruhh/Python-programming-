import random
import pygame


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}


class Tetromino:
    def __init__(self):
        self.type = random.choice(list(SHAPES.keys()))
        self.shape = [row[:] for row in SHAPES[self.type]]
        self.color = COLORS[self.type]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [[self.shape[j][i] for j in range(len(self.shape))]
                      for i in range(len(self.shape[0]) - 1, -1, -1)]


class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.board = [[None for _ in range(BOARD_WIDTH)]
                      for _ in range(BOARD_HEIGHT)]
        self.current_piece = Tetromino()
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def check_collision(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + offset_x
                    new_y = piece.y + y + offset_y
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                        return True
                    if new_y >= 0 and self.board[new_y][new_x] is not None:
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_y = self.current_piece.y + y
                    board_x = self.current_piece.x + x
                    if board_y >= 0:
                        self.board[board_y][board_x] = self.current_piece.color

    def clear_lines(self):
        lines_cleared = 0
        y = BOARD_HEIGHT - 1
        while y >= 0:
            if all(cell is not None for cell in self.board[y]):
                del self.board[y]
                self.board.insert(0, [None for _ in range(BOARD_WIDTH)])
                lines_cleared += 1
            else:
                y -= 1

        if lines_cleared > 0:
            points = [0, 100, 300, 500, 800][lines_cleared] * self.level
            self.score += points
            self.lines += lines_cleared
            self.level = self.lines // 10 + 1
            self.fall_speed = max(100, 500 - (self.level - 1) * 50)

    def new_piece(self):
        self.current_piece = Tetromino()
        if self.check_collision(self.current_piece):
            self.game_over = True

    def move(self, dx):
        if not self.check_collision(self.current_piece, dx, 0):
            self.current_piece.x += dx

    def rotate_piece(self):
        old_shape = [row[:] for row in self.current_piece.shape]
        self.current_piece.rotate()
        if self.check_collision(self.current_piece):
            self.current_piece.shape = old_shape

    def drop(self):
        if not self.check_collision(self.current_piece, 0, 1):
            self.current_piece.y += 1
            return False
        else:
            self.merge_piece()
            self.clear_lines()
            self.new_piece()
            return True

    def hard_drop(self):
        while not self.check_collision(self.current_piece, 0, 1):
            self.current_piece.y += 1
        self.drop()

    def draw_board(self):
        # Draw grid
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                rect = pygame.Rect(x * BLOCK_SIZE, y *
                                   BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)
                if self.board[y][x] is not None:
                    pygame.draw.rect(self.screen, self.board[y][x], rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 2)

    def draw_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (self.current_piece.x + x) * BLOCK_SIZE,
                        (self.current_piece.y + y) * BLOCK_SIZE,
                        BLOCK_SIZE, BLOCK_SIZE
                    )
                    pygame.draw.rect(
                        self.screen, self.current_piece.color, rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 2)

    def draw_ui(self):
        score_text = self.small_font.render(
            f'Score: {self.score}', True, WHITE)
        level_text = self.small_font.render(
            f'Level: {self.level}', True, WHITE)
        lines_text = self.small_font.render(
            f'Lines: {self.lines}', True, WHITE)

        self.screen.blit(score_text, (BOARD_WIDTH * BLOCK_SIZE + 10, 20))
        self.screen.blit(level_text, (BOARD_WIDTH * BLOCK_SIZE + 10, 50))
        self.screen.blit(lines_text, (BOARD_WIDTH * BLOCK_SIZE + 10, 80))

        controls = [
            'Controls:',
            '← → : Move',
            '↑ : Rotate',
            '↓ : Soft Drop',
            'Space: Hard Drop'
        ]
        for i, text in enumerate(controls):
            control_text = self.small_font.render(text, True, WHITE)
            self.screen.blit(control_text, (BOARD_WIDTH *
                             BLOCK_SIZE + 10, 150 + i * 25))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render('GAME OVER', True, RED)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        restart_text = self.small_font.render(
            'Press R to Restart', True, WHITE)

        self.screen.blit(game_over_text,
                         (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        self.screen.blit(score_text,
                         (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 260))
        self.screen.blit(restart_text,
                         (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 320))

    def reset(self):
        self.board = [[None for _ in range(BOARD_WIDTH)]
                      for _ in range(BOARD_HEIGHT)]
        self.current_piece = Tetromino()
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 500

    def run(self):
        running = True
        while running:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset()
                    else:
                        if event.key == pygame.K_LEFT:
                            self.move(-1)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1)
                        elif event.key == pygame.K_DOWN:
                            self.drop()
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            self.hard_drop()

            if not self.game_over and self.fall_time >= self.fall_speed:
                self.drop()
                self.fall_time = 0

            self.screen.fill(BLACK)
            self.draw_board()
            if not self.game_over:
                self.draw_piece()
            self.draw_ui()

            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    game = TetrisGame()
    game.run()

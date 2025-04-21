import pygame
import sys

WIDTH, HEIGHT = 540, 540
ROWS, COLS = 9, 9
GAP = WIDTH // COLS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

class Cell:
    def __init__(self, value, row, col, screen, width=540, height=540):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.selected = False
        self.screen = screen
        self.width = width
        self.height = height

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        gap = self.width // 9
        x = self.col * gap
        y = self.row * gap

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, gap, gap), 3)

        if self.sketched_value != 0 and self.value == 0:
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))

        elif self.value != 0:
            font = pygame.font.SysFont("comicsans", 40)
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + gap // 2, y + gap // 2))
            self.screen.blit(text, text_rect)

cells = [[Cell(0, row, col, screen) for col in range(COLS)] for row in range(ROWS)]
selected_cell = None

def draw_grid():
    screen.fill((255, 255, 255))  # White background

    for i in range(ROWS + 1):
        line_width = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * GAP), (WIDTH, i * GAP), line_width)
        pygame.draw.line(screen, (0, 0, 0), (i * GAP, 0), (i * GAP, HEIGHT), line_width)

    for row in cells:
        for cell in row:
            cell.draw()

    pygame.display.update()

def main():
    global selected_cell
    running = True

    while running:
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // GAP, pos[0] // GAP
                selected_cell = cells[row][col]
                for r in cells:
                    for c in r:
                        c.selected = False
                selected_cell.selected = True

            if event.type == pygame.KEYDOWN and selected_cell:
                if event.key in range(pygame.K_1, pygame.K_9 + 1):
                    value = event.key - pygame.K_0
                    selected_cell.set_sketched_value(value)
                if event.key == pygame.K_RETURN:
                    if selected_cell.sketched_value != 0:
                        selected_cell.set_cell_value(selected_cell.sketched_value)
                        selected_cell.set_sketched_value(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


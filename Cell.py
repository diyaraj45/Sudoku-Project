import pygame
import sys

#Dimentions (This are the common dimentions for Sudoku)
WIDTH, HEIGHT = 540, 540
ROWS = COLS = 9
CELL_SIZE = WIDTH // COLS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

class Cell:
    def __init__(self, val, row, col, scrn, width=540, height=540):
        self.value = val
        self.sketched = 0
        self.row = row
        self.col = col
        self.screen = scrn
        self.width = width
        self.height = height
        self.selected = False
#sketched is meant for when there is writing on the sudoku grid

    def set_cell_value(self, val):
        self.value = val

    def set_sketched_value(self, val):
        self.sketched = val
#This is meant for numbers that are only placed temporarily.

    def draw(self):
        square_size = self.width // 9
        x = self.col * square_size
        y = self.row * square_size

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, square_size, square_size), 3)

        if self.sketched != 0 and self.value == 0:
            font = pygame.font.SysFont("comicsans", 30)
            sketched_text = font.render(str(self.sketched), True, (128, 128, 128))
            self.screen.blit(sketched_text, (x + 5, y + 5))

        elif self.value != 0:
            font = pygame.font.SysFont("comicsans", 40)
            text = font.render(str(self.value), True, (0, 0, 0))
            rect = text.get_rect(center=(x + square_size // 2, y + square_size // 2))
            self.screen.blit(text, rect)

cells = [[Cell(0, r, c, screen) for c in range(COLS)] for r in range(ROWS)]
active_cell = None
# This keeps track of currently clicked cell

def draw_grid():
    screen.fill((255, 255, 255))

#Grid lines
    for i in range(10):
        line_thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_thickness)
        pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), line_thickness)

    for row in cells:
        for cell in row:
            cell.draw()

    pygame.display.update()

def main():
    global active_cell
    running = True

    while running:
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                r = mouse_pos[1] // CELL_SIZE
                c = mouse_pos[0] // CELL_SIZE
                active_cell = cells[r][c]
                for row in cells:
                    for cell in row:
                        cell.selected = False
                active_cell.selected = True

            elif event.type == pygame.KEYDOWN and active_cell:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    active_cell.set_sketched_value(num)

                elif event.key == pygame.K_RETURN:
                    if active_cell.sketched != 0:
                        active_cell.set_cell_value(active_cell.sketched)
                        active_cell.set_sketched_value(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

import pygame
import sys
from sudoku_generator import SudokuGenerator
from cell import Cell
from board import Board

# Constants
WIDTH, HEIGHT = 540, 620
WHITE = (255, 255, 255)
# Darker Pink
PINK = (216, 74, 143)
# lighter Rect. Pink
PINKY = (252, 224, 234)
# End button pink
SALMON = (255, 121, 148)
FPS = 60

# Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comfortaa", 40)

def draw_start_screen():
    # Background
    background = pygame.image.load("sbb.png")
    background_rect = background.get_rect()
    # Centers png
    background_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(background, background_rect.topleft)

    # Title
    title = pygame.font.SysFont("comfortaa", 60).render("Select Difficulty", True, PINK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

    # Game Mode
    buttons = {}
    labels = ["Easy", "Medium", "Hard"]
    for i, label in enumerate(labels):
        # Rectangle Area and Location
        # Center from the sides, height from top + height from each other, rectangle horizontal, rectangle vertical
        rect = pygame.Rect(WIDTH//2 - 75, 150 + i * 90, 150, 50)
        # Rectangle Background Color
        pygame.draw.rect(screen, PINKY, rect)
        # Rectangle Word Color
        text = font.render(label, True, PINK)
        screen.blit(text, (rect.x + 35, rect.y + 10))
        buttons[label.lower()] = rect

    pygame.display.update()
    return buttons

def draw_playing_screen(board):
    screen.fill("white")
    board.draw()

    # Pink background for labels(new buttons)
    pygame.draw.rect(screen, "pink", (0, 542, WIDTH, 60))

    # Button spacing and size
    button_width = 100
    button_height = 40
    spacing = 30
    total_width = 3 * button_width + 2 * spacing
    start_x = (WIDTH - total_width) // 2
    y = 550
    buttons = {}

    # Label set-up: include button spacing and size
    labels = ["Reset", "Restart", "Exit"]
    for i, label in enumerate(labels):
        rect = pygame.Rect(start_x + i * (button_width + spacing), y, button_width, button_height)
        # Makes the curves on the buttons by giving radius
        pygame.draw.rect(screen, WHITE, rect, border_radius=10)
        text = font.render(label, True, PINK)
        # Centers text in buttons(rect)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        buttons[label.lower()] = rect

    pygame.display.update()

    # Check if the board is complete and correct
    if board.is_full():
        if board.check_board():
            return "game_won"
        else:
            return "game_over"
    return "playing", buttons

def draw_game_over_screen():
    # Background
    screen.fill("white")
    background = pygame.image.load("sad.png")
    background_rect = background.get_rect()
    background_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(background, background_rect.topleft)

    # Title
    title = pygame.font.SysFont("comfortaa", 60).render("Game Over :(", True, SALMON)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 15))

    # Restart button
    restart_button = pygame.Rect(WIDTH // 2 - 75, 500, 150, 50)
    pygame.draw.rect(screen, SALMON, restart_button, border_radius=10)
    restart_text = font.render("Restart", True, "white")
    screen.blit(restart_text, (restart_button.x + 30, restart_button.y + 10))

    pygame.display.update()
    return restart_button

def draw_game_won_screen():
    # Background
    screen.fill("white")
    background = pygame.image.load("hp.png")
    background_rect = background.get_rect()
    background_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(background, background_rect.topleft)

    # Title
    title = pygame.font.SysFont("comfortaa", 60).render("Game Won!", True, "white")
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 15))

    exit_button = pygame.Rect(WIDTH//2 - 75, 150, 150, 50)
    pygame.draw.rect(screen, PINKY, exit_button, border_radius=10)
    exit_text = font.render("Exit", True, PINK)
    screen.blit(exit_text, (exit_button.x + 35, exit_button.y + 10))

    pygame.display.update()
    return exit_button

def main():
    running = True
    game_state = "start"
    board = None
    selected_difficulty = None

    while running:
        clock.tick(FPS)

        if game_state == "start":
            buttons = draw_start_screen()
        elif game_state == "game_over":
            restart_button = draw_game_over_screen()
        elif game_state == "game_won":
            exit_button = draw_game_won_screen()
        elif game_state == "playing" and board:
            result = draw_playing_screen(board)
            if isinstance(result, tuple):
                game_state, play_buttons = result
            else:
                if result == "game_won":
                    game_state = "game_won"
                else:
                    game_state = "game_over"



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if game_state == "start":
                    for label, rect in buttons.items():
                        if rect.collidepoint(pos):
                            # Connecting labels to that selected
                            selected_difficulty = label.capitalize()
                            # print(f"Selected difficulty: {selected_difficulty}")

                            board = Board(WIDTH, 540, screen, selected_difficulty)
                            game_state = "playing"

                elif game_state == "playing" and board:
                    x, y = pos
                    clicked = board.click(x, y)
                    if clicked:
                        row, col = clicked
                        board.select(row, col)

                    for label, rect in play_buttons.items():
                        if rect.collidepoint(pos):
                            if rect.collidepoint(pos):
                                if label.capitalize() == "Reset":
                                    board.reset_to_original()
                                elif label.capitalize() == "Restart":
                                    game_state = "start"
                                elif label.capitalize() == "Exit":
                                    running = False

                elif game_state == "game_won":
                    # Exits game when exit button is selected
                    if exit_button.collidepoint(pos):
                        running = False

                elif game_state == "game_over":
                    # Brings to start state when restart button is selected
                    if restart_button.collidepoint(pos):
                        game_state = "start"

            elif event.type == pygame.KEYDOWN:
                if game_state == "playing" and board.selected:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        board.sketch(event.key - pygame.K_0)
                    elif event.key == pygame.K_RETURN:
                        r, c = board.selected
                        cell = board.cells[r][c]
                        if cell.sketched != 0:
                            board.place_number(cell.sketched)
                    elif event.key == pygame.K_BACKSPACE:
                        board.clear()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
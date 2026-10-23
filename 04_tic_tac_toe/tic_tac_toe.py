import pygame
import sys

pygame.init()

# ---------- Settings ----------
WIDTH, HEIGHT = 400, 500       # 400x400 board + 100 for the status bar
BOARD_SIZE = 400
CELL = BOARD_SIZE // 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
BLUE = (50, 80, 220)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.SysFont(None, 40)

# ---------- Game state ----------
board = [[None] * 3 for _ in range(3)]   # None, "X" or "O"
current_player = "X"
winner = None
draw = False


def draw_grid():
    """Draw the 2 vertical and 2 horizontal lines."""
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (i * CELL, 0), (i * CELL, BOARD_SIZE), 4)
        pygame.draw.line(screen, BLACK, (0, i * CELL), (BOARD_SIZE, i * CELL), 4)


def draw_symbols():
    """Draw X and O in the cells that are filled."""
    for row in range(3):
        for col in range(3):
            x = col * CELL
            y = row * CELL
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (x + 25, y + 25), (x + CELL - 25, y + CELL - 25), 8)
                pygame.draw.line(screen, RED, (x + CELL - 25, y + 25), (x + 25, y + CELL - 25), 8)
            elif board[row][col] == "O":
                center = (x + CELL // 2, y + CELL // 2)
                pygame.draw.circle(screen, BLUE, center, CELL // 2 - 25, 8)


def check_winner():
    """Return 'X' or 'O' if someone has a line, else None."""
    # rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    # diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None


def is_board_full():
    return all(cell is not None for row in board for cell in row)


def draw_status():
    """Show whose turn it is, or the result, in the bar below the board."""
    pygame.draw.rect(screen, WHITE, (0, BOARD_SIZE, WIDTH, 100))
    if winner:
        message = f"Player {winner} wins!"
    elif draw:
        message = "It's a draw!"
    else:
        message = f"Player {current_player}'s turn"
    text = font.render(message, True, BLACK)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, BOARD_SIZE + 50)))


def reset_game():
    global board, current_player, winner, draw
    board = [[None] * 3 for _ in range(3)]
    current_player = "X"
    winner = None
    draw = False


def redraw():
    screen.fill(WHITE)
    draw_grid()
    draw_symbols()
    draw_status()
    pygame.display.update()


# ---------- Main loop ----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # only count clicks inside the board
            if mouse_y < BOARD_SIZE:
                col = mouse_x // CELL
                row = mouse_y // CELL

                if board[row][col] is None:
                    board[row][col] = current_player

                    winner = check_winner()
                    if winner is None and is_board_full():
                        draw = True

                    if winner is None and not draw:
                        current_player = "O" if current_player == "X" else "X"

                    redraw()

                    # Show the result for 2 seconds, then reset
                    if winner or draw:
                        pygame.time.wait(2000)
                        reset_game()

    redraw()
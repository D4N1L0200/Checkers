import pygame
from time import sleep

WIDTH = 8
HEIGHT = 8
CELL_SIZE = 90
PADDING = 1

board = [
    [" ", "x", " ", "x", " ", "x", " ", "x"],
    ["x", " ", "x", " ", "x", " ", "x", " "],
    [" ", "x", " ", "x", " ", "x", " ", "x"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["o", " ", "o", " ", "o", " ", "o", " "],
    [" ", "o", " ", "o", " ", "o", " ", "o"],
    ["o", " ", "o", " ", "o", " ", "o", " "],
]

pygame.init()
window = pygame.display.set_mode(
    (
        WIDTH * (CELL_SIZE + PADDING) + PADDING,
        HEIGHT * (CELL_SIZE + PADDING) + PADDING,
    )
)
clock = pygame.time.Clock()


def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    if ((x % (PADDING + CELL_SIZE)) - PADDING < 0) or (
        (y % (PADDING + CELL_SIZE)) - PADDING < 0
    ):
        return -1, -1
    row = y // (PADDING + CELL_SIZE)
    col = x // (PADDING + CELL_SIZE)
    return col, row


def move_piece(start, end, curr_turn, curr_board):
    sy, sx = start
    ey, ex = end
    absx = abs(sx - ex)
    absy = abs(sy - ey)
    if curr_board[sy][sx].lower() != curr_turn:
        print("Turno incorreto.")
        return False
    if absx != absy:
        print("Movimento não é diagonal.")
        return False
    if absx == 0:
        print("Não é movimento.")
        return False
    if curr_board[ey][ex] != " ":
        print("Espaço final ocupado.")
        return False
    if absx == 1:
        if (curr_board[sy][sx] == "x" and sy > ey) or (
            curr_board[sy][sx] == "o" and sy < ey
        ):
            print("Movimento para trás.")
            return False
    if absx == 1 and (
        (curr_board[sy][sx] == "x" and sy > ey)
        or (curr_board[sy][sx] == "o" and sy < ey)
    ):
        print("Movimento para trás.")
        return False
    if absx > 1:
        if sy > ey:
            cy = ey + 1
        else:
            cy = ey - 1
        if sx > ex:
            cx = ex + 1
        else:
            cx = ex - 1
        if curr_board[sy][sx] not in ["X", "O"]:
            if absx > 2 or curr_board[cy][cx] == " ":
                print("Movimento grande demais.")
                return False
        if curr_board[sy][sx] == curr_board[cy][cx]:
            print(f"Capturando mesmo time.")
            return False
        curr_board[cy][cx] = " "

    curr_board[ey][ex] = curr_board[sy][sx]
    curr_board[sy][sx] = " "

    if curr_board[ey][ex] == "o" and ey == 0:
        curr_board[ey][ex] = "O"
    elif curr_board[ey][ex] == "x" and ey == 7:
        curr_board[ey][ex] = "X"
    return curr_board


def player_turn(curr_board, curr_turn, play):
    play = [[b, a] for a, b in play]

    for i in range(len(play) - 1):
        updated_board = move_piece(play[i], play[i + 1], curr_turn, curr_board)
        if not updated_board:
            sleep(1)
            return curr_board, curr_turn
        else:
            curr_board = updated_board

    if curr_turn == "o":
        print("Turno de vermelho.")
        return curr_board, "x"
    elif curr_turn == "x":
        print("Turno de azul.")
        return curr_board, "o"


def finished(curr_board):
    if "o" not in [i.lower() for i in sum(curr_board, [])]:
        print("Parabéns!! O jogador vermelho ganhou o jogo!")
        return True
    if "x" not in [i.lower() for i in sum(curr_board, [])]:
        print("Parabéns!! O jogador azul ganhou o jogo!")
        return True


play = []
turn = "o"
print("Turno de azul.")

done = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            board = [[" " if i.lower() == turn else i for i in line] for line in board]
        if event.type == pygame.MOUSEBUTTONUP and not done:
            match event.button:
                case 1:
                    play.append(get_mouse_pos())
                case 2:
                    play = []
                case 3:
                    board, turn = player_turn(board, turn, play)
                    play = []

    if not done and finished(board):
        done = True

    window.fill(0)
    for iy, row in enumerate(board):
        for ix, cell in enumerate(row):
            color = (
                (50, 255, 50)
                if (ix, iy) in play
                else (255, 255, 255)
                if (ix % 2) ^ (iy % 2)
                else (120, 120, 120)
            )
            pygame.draw.rect(
                window,
                color,
                (
                    ix * (CELL_SIZE + PADDING) + PADDING,
                    iy * (CELL_SIZE + PADDING) + PADDING,
                    CELL_SIZE,
                    CELL_SIZE,
                ),
            )
            if cell != " ":
                pygame.draw.circle(
                    window,
                    (255, 0, 0) if cell in "xX" else (0, 0, 255),
                    (
                        ix * (CELL_SIZE + PADDING) + PADDING + CELL_SIZE / 2,
                        iy * (CELL_SIZE + PADDING) + PADDING + CELL_SIZE / 2,
                    ),
                    CELL_SIZE / (2.1 if cell in "XO" else 3.5),
                )
    pygame.display.flip()
    pygame.display.set_caption(f"Checkers - FPS: {round(clock.get_fps(), 2)}")
    clock.tick(240)

pygame.quit()
exit()

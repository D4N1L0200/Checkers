from os import system
from time import sleep


def display(curr_board, disp_type):
    if disp_type in [1, 2]:
        out = ""
    elif disp_type == 3:
        out = "   a b c d e f g h\n"
    for idx, line in enumerate(curr_board):
        if disp_type == 1:
            out += f"\n   {' '.join(line)}"
        elif disp_type == 2:
            out += f"\n{8-idx}  {' '.join(line)}"
        elif disp_type == 3:
            out += f"\n{8-idx}  {' '.join(line)}  {8-idx}"
    if disp_type == 1:
        out += "\n\n"
    elif disp_type in [2, 3]:
        out += "\n\n   a b c d e f g h\n"
    system("cls")
    print(out)


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


def player_turn(curr_board, curr_turn):
    inp = input(f"Turno de '{curr_turn}'\nSua Jogada: ")
    if inp == "-":
        curr_board = [
            [" " if i.lower() == curr_turn else i for i in line] for line in curr_board
        ]
    elif inp:
        try:
            play = [
                [8 - int(b), ["a", "b", "c", "d", "e", "f", "g", "h"].index(a)]
                for a, b in inp.split()
            ]
        except ValueError:
            print("Movimento inválido.")
            sleep(1)
            return curr_board, curr_turn

        for i in range(len(play) - 1):
            updated_board = move_piece(play[i], play[i + 1], curr_turn, curr_board)
            if not updated_board:
                sleep(1)
                return curr_board, curr_turn
            else:
                curr_board = updated_board

    if curr_turn == "o":
        return curr_board, "x"
    elif curr_turn == "x":
        return curr_board, "o"


def finished(curr_board):
    if "o" not in [i.lower() for i in sum(curr_board, [])]:
        print("Parabéns!! O jogador 'x' ganhou o jogo!")
        return True
    if "x" not in [i.lower() for i in sum(curr_board, [])]:
        print("Parabéns!! O jogador 'o' ganhou o jogo!")
        return True


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
turn = "o"

system("cls")
print(
    """
       Tipo 1                    Tipo 2                    Tipo 3        \n
                                                       a b c d e f g h   \n
     x   x   x   x        8    x   x   x   x        8    x   x   x   x  8
   x   x   x   x          7  x   x   x   x          7  x   x   x   x    7
     x   x   x   x        6    x   x   x   x        6    X   X   x   x  6
                          5                         5                   5
                          4                         4                   4
   o   o   o   o          3  o   o   o   o          3  o   o   O   O    3
     o   o   o   o        2    o   o   o   o        2    o   o   o   o  2
   o   o   o   o          1  o   o   o   o          1  o   o   o   o    1\n
                             a b c d e f g h           a b c d e f g h   
"""
)
display_type = input("Qual o tipo de tabuleiro? (1, 2, 3) ")
if display_type not in ["1", "2", "3"]:
    print("Tipo desconhecido.")
    exit()
else:
    display_type = int(display_type)

display(board, display_type)
while True:
    board, turn = player_turn(board, turn)
    display(board, display_type)
    if finished(board):
        break

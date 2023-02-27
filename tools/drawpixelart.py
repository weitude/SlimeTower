import time

import pygame

N = 64
P = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (40, 106, 181)
RED = (189, 65, 58)
GREEN = (92, 184, 66)

HEIGHT = (N + 2) * P
BH = (HEIGHT - 50) / 4

WIN = pygame.display.set_mode(((N + 1) * P + 50, (N + 2) * P))
WIN.fill(BLUE)

map = [[0 for i in range(N)] for j in range(N)]


def getcode(grid):
    for i in range(16):
        binary = ""
        for j in range(16):
            if grid[i][j] == 1:
                binary = "1" + binary
            else:
                binary = "0" + binary

        isNegative = False

        if binary[0] == "1":
            isNegative = True
            oneComplement = ""
            for k in range(16):
                if binary[k] == "1":
                    oneComplement = oneComplement + "0"
                else:
                    oneComplement = oneComplement + "1"

            binary = oneComplement

        value = 0
        for k in range(16):
            value = value * 2
            if binary[k] == "1":
                value = value + 1

        if isNegative:
            value = -((value + 1) % 32768)

        s = "do Memory.poke(memAddress+" + str(i * 32) + ", " + str(value) + ");"
        print(s)


def draw():
    WIN.fill(BLUE)
    pygame.draw.rect(WIN, WHITE, pygame.Rect((N + 1) * P + 10, 10, 30, BH))
    pygame.draw.rect(WIN, BLACK, pygame.Rect((N + 1) * P + 10, 20 + BH, 30, BH))
    pygame.draw.rect(WIN, GREEN, pygame.Rect((N + 1) * P + 10, 30 + 2 * BH, 30, BH))
    pygame.draw.rect(WIN, RED, pygame.Rect((N + 1) * P + 10, 40 + 3 * BH + (BH // 2), 30, BH / 4))
    for i in range(N):
        for j in range(N):
            if map[j][i] == 0:
                pygame.draw.rect(WIN, WHITE, pygame.Rect((i + 1) * P, (j + 1) * P, P, P))
            else:
                pygame.draw.rect(WIN, BLACK, pygame.Rect((i + 1) * P, (j + 1) * P, P, P))

    pygame.display.update()


cc = 1
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw()

    if not pygame.mouse.get_pressed()[0]:
        continue

    x, y = pygame.mouse.get_pos()

    if P <= x <= N * P and P <= y <= N * P:
        dx = [1, 1, 1, 0, 0, 0, -1, -1, -1]
        dy = [1, 0, -1, 1, 0, -1, 1, 0, -1]
        for i in range(9):
            xx = x // P - 1 + dx[i]
            yy = y // P - 1 + dy[i]
            if 0 <= xx < N and 0 <= yy < N:
                map[yy][xx] = cc

    if (N + 1) * P + 10 <= x <= (N + 1) * P + 40 and 10 <= y <= 10 + BH:
        cc = 0

    if (N + 1) * P + 10 <= x <= (N + 1) * P + 40 and 20 + BH <= y <= 20 + 2 * BH:
        cc = 1

    if (N + 1) * P + 10 <= x <= (N + 1) * P + 40 and 30 + 2 * BH <= y <= 30 + 3 * BH:
        time.sleep(0.2)
        if not N % 16 == 0:
            print("no code for you")
            continue

        g = [[0 for i in range(16)] for j in range(16)]

        for k in range(int(N / 16)):
            for l in range(int(N / 16)):

                for i in range(16):
                    for j in range(16):
                        ii = k * 16 + i
                        jj = l * 16 + j
                        g[i][j] = map[ii][jj]

                getcode(g)

                print(f"let memAddress = memAddress+1;")

            print(f"let memAddress = memAddress+512-{N // 16};")

    if (N + 1) * P + 10 <= x <= (N + 1) * P + 10 + 30 and 40 + 3 * BH + (BH // 2) <= y <= 40 + 3 * BH + (
            BH // 2) + BH / 4:
        # print(map)
        map = [[0 for i in range(N)] for j in range(N)]
        time.sleep(1)

pygame.quit()
print("finish!")

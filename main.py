from typing import List
from pygame import Color, display, draw, event, image, key, locals, Rect, Surface, mouse, time, transform
import pygame as p
from nqueen import Queen, BoardNode, rand_initial_state, a_star

# constans of the app, N is the board sze and FPS is the framearte for the engine
WIDTH = HEIGHT = 512
N = 10
SQUARE_SIZE = int(WIDTH / N)
FPS = 2000
QUEEN = transform.scale(image.load('blackQueen.png'),
                        (SQUARE_SIZE, SQUARE_SIZE))


state = rand_initial_state(N)
visited_states: List[BoardNode] = []
# queens = [Queen(0)] * N
# queens = [Queen(0), Queen(3), Queen(1), Queen(0)]


def main():
    p.init()
    display.set_caption('N-Queen')
    screen = display.set_mode((WIDTH, HEIGHT))
    screen.fill(Color('white'))
    clock = time.Clock()

    running = True
    while running:
        for e in event.get():
            if e.type == locals.QUIT:
                running = False

        global state
        global visited_states

        drawBoard(screen)
        drawQueens(screen,  state.queens)

        clock.tick(FPS)
        display.flip()

        if state.total_threats > 0:
            state = a_star(state, visited_states)


# draws the board
def drawBoard(screen: Surface):
    colors = [Color(220, 211, 234), Color(138, 120, 93)]
    for row in range(N):
        for col in range(N):
            color = colors[(row + col) % 2]
            draw.rect(screen, color, Rect(col * SQUARE_SIZE,
                                          row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# draw the queens
def drawQueens(screen: Surface, queens: List[Queen]):
    for col in range(N):
        screen.blit(QUEEN, Rect(col * SQUARE_SIZE,
                                queens[col].pos * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


if __name__ == '__main__':
    main()

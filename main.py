from typing import List
from pygame import Color, display, draw, event, image, key, locals, Rect, Surface, mouse, time, transform
import pygame as p
import pygame_gui as gui
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
search = True

# queens = [Queen(0)] * N
# queens = [Queen(0), Queen(3), Queen(1), Queen(0)]

p.init()
display.set_caption('N-Queen')

screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
clock.tick(FPS)
manager = gui.UIManager((WIDTH, HEIGHT))

btn_astar = gui.elements.UIButton(relative_rect=Rect((0, 0), (100, 50)),
                                  text='Start A*',
                                  manager=manager)
btn_genetic = gui.elements.UIButton(relative_rect=Rect((150, 0), (130, 50)),
                                    text='Start Genetinc',
                                    manager=manager)


def main():
    running = True
    while running:
        screen.fill(Color(41, 45, 62))

        for e in event.get():
            if e.type == locals.QUIT:
                running = False

            if e.type == locals.USEREVENT:
                if e.user_type == gui.UI_BUTTON_PRESSED:
                    if e.ui_element == btn_astar:
                        global state
                        state = rand_initial_state(N)
                        a_star_window()

            manager.process_events(e)

        manager.update(FPS)
        screen.blit(screen, (0, 0))
        manager.draw_ui(screen)
        display.flip()
    pass


def genetic_menu():
    pass


def genetic_window():
    pass


def a_star_menu():
    pass


def a_star_window():
    global search
    global state
    global visited_states
    search = True
    running = True
    while running:

        for e in event.get():
            if e.type == locals.QUIT:
                running = False

            if e.type == locals.KEYDOWN:
                if e.key == locals.K_ESCAPE:
                    running = False
                if e.key == locals.K_SPACE:
                    search = not search

        drawBoard(screen)
        drawQueens(screen,  state.queens)

        # clock.tick(FPS)

        display.flip()

        if (state.total_threats > 0) & (search):
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

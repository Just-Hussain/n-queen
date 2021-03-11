import time as t
from typing import List
from pygame import Color, display, draw, event, image, key, locals, Rect, Surface, mouse, time, transform, font
import pygame as p
import pygame_gui as gui
from pygame_gui.elements import text
from nqueen import Queen, BoardNode, rand_initial_state, a_star, genetic


# constans of the app, N is the board sze and FPS is the framearte for the engine
WIDTH = HEIGHT = 920
N = 10
SQUARE_SIZE = 40
FPS = 15
QUEEN = transform.scale(image.load('blackQueen.png'),
                        (SQUARE_SIZE, SQUARE_SIZE))


# Globals to help A*
state = rand_initial_state(N)
visited_states: List[BoardNode] = []
steps_count = 0
generation_count = 0
search = True


p.init()
display.set_caption('N-Queen')
_font = font.SysFont(None, 20)

screen = display.set_mode((WIDTH, HEIGHT), locals.RESIZABLE)
clock = time.Clock()
clock.tick(FPS)
manager = gui.UIManager((WIDTH, HEIGHT))


input_N = gui.elements.UITextEntryLine(
    relative_rect=Rect((10, 50), (100, 50)), manager=manager)
input_N.set_allowed_characters('numbers')


def main():
    btn_astar = gui.elements.UIButton(relative_rect=Rect((150, 35), (100, 50)),
                                      text='Start A*',
                                      manager=manager)
    btn_genetic = gui.elements.UIButton(relative_rect=Rect((300, 35), (130, 50)),
                                        text='Start Genetinc',
                                        manager=manager)

    lbl_size = gui.elements.UILabel(
        relative_rect=Rect((10, 100), (400, 50)), manager=manager, text='Poplation Size')
    in_size = gui.elements.UITextEntryLine(
        relative_rect=Rect((10, 150), (100, 100)), manager=manager)
    in_size.set_allowed_characters('numbers')

    lbl_gens = gui.elements.UILabel(
        relative_rect=Rect((10, 200), (400, 50)), manager=manager, text='Number of generations')
    in_gens = gui.elements.UITextEntryLine(
        relative_rect=Rect((10, 250), (100, 100)), manager=manager)
    in_gens.set_allowed_characters('numbers')

    lbl_cross = gui.elements.UILabel(
        relative_rect=Rect((10, 300), (400, 50)), manager=manager, text='Single or multipoint crossover')
    select_cross = gui.elements.UISelectionList(
        relative_rect=Rect((10, 350), (250, 50)), manager=manager,
        item_list=['single point', 'multipoint']
    )

    lbl_cross_rate = gui.elements.UILabel(
        relative_rect=Rect((10, 400), (400, 50)), manager=manager, text='Crossover Rate')
    in_cross_rate = gui.elements.UITextEntryLine(
        relative_rect=Rect((10, 450), (100, 100)), manager=manager)

    lbl_mutation_rate = gui.elements.UILabel(
        relative_rect=Rect((10, 500), (400, 50)), manager=manager, text='Mutation Rate')
    in_mutation_rate = gui.elements.UITextEntryLine(
        relative_rect=Rect((10, 550), (100, 100)), manager=manager)

    lbl_elite = gui.elements.UILabel(
        relative_rect=Rect((10, 600), (400, 50)), manager=manager, text='With/without elitism')
    select_elite = gui.elements.UISelectionList(
        relative_rect=Rect((10, 650), (250, 50)), manager=manager,
        item_list=['With elitism', 'Without elitism']
    )

    running = True
    while running:
        screen.fill(Color(41, 45, 62))

        for e in event.get():
            if e.type == locals.QUIT:
                running = False

            if e.type == locals.USEREVENT:
                if e.user_type == gui.UI_BUTTON_PRESSED:
                    global N
                    global generation_count
                    generation_count = [0]

                    if e.ui_element == btn_astar:
                        global state
                        input = input_N.get_text()
                        N = int(input) if input.isdigit() else 0
                        if N >= 4:
                            state = rand_initial_state(N)
                            a_star_window()

                    if e.ui_element == btn_genetic:
                        input = input_N.get_text()

                        N = int(input) if input.isdigit() else 0

                        size = int(in_size.get_text()
                                   ) if in_size.get_text().isdigit() else 100

                        generations = int(
                            in_gens.get_text()) if in_gens.get_text().isdigit() else 1000

                        # multipoint = False if select_cross.get_single_selection() == 'single point' else True
                        multipoint = False

                        crossover_rate = float(in_cross_rate.get_text(
                        )) if in_cross_rate.get_text().isnumeric() else 1.0

                        mutation_rate = float(in_mutation_rate.get_text(
                        )) if in_mutation_rate.get_text().isnumeric() else 0.1

                        elitism = False if select_elite.get_single_selection() == 'Without elitism' else True

                        if N >= 4:
                            genetic_window(genetic(N, size, generations, elitism,
                                                   mutation_rate, multipoint, crossover_rate, generation_count).queens)

            manager.process_events(e)

        manager.update(FPS)
        screen.blit(screen, (0, 0))
        manager.draw_ui(screen)

        draw_text(text='Enter N >= 4', x=10, y=30)
        display.flip()
    pass


def genetic_window(queens):

    running = True
    while running:

        for e in event.get():
            if e.type == locals.QUIT:
                running = False

            if e.type == locals.KEYDOWN:
                if e.key == locals.K_ESCAPE:
                    running = False

        drawBoard(screen)
        drawQueens(screen,  queens)

        draw_text(text=f'generation count: {generation_count[0]}', color=(
            0, 0, 0))
        display.flip()


def a_star_window():
    global search
    global state
    global visited_states
    global steps_count
    steps_count = [0]
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

        draw_text(text=f'steps count: {steps_count[0]}', color=(
            0, 0, 0))

        # clock.tick(FPS)

        display.flip()

        if (state.total_threats > 0) & (search):
            state = a_star(state, visited_states, steps_count)


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


def draw_text(text, font=_font, color=(255, 255, 255), surface=screen, x=0, y=0):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


if __name__ == '__main__':
    main()

from typing import List
import random


##################################


# GENERAL STUFF


class Queen():
    def __init__(self, pos: int, threats: int = -1):
        # the position of the queen on the board
        self.pos = pos
        # the number of threats on the queen
        self.threats = threats

    def __eq__(self, o: object) -> bool:
        return (self.pos == o.pos) & (self.threats == o.threats)

    def __str__(self) -> str:
        return f'Queen(pos: {self.pos}, threats: {self.threats})'


def calc_threats(queens: List[Queen]) -> List[int]:
    # check threats on same row, main diagonal and antidiagonal
    # the check for same row is obvious: [0, 2, 1, 2]
    # loop and check for duplicated of the number (position)

    # the check for the diagonal goes like this:
    # the diagonal is formed by pos, pos + 1, pos + 2, pos + 3, and so on....
    # the same for pos - 1, pos - 2, pos - 3 ....
    # for a conflict to occur on the diagonal, pos will be an increment of ouu current queen position,
    # also the increment increases by 1 when the position increse
    # example: [1, 3, 0, 2] has no conflict even though the last queen is an increment of the first queen position.
    # and that is because the increment is not constant and increses as we go further.
    # the same for why the second queen is not counted as a threat, it is not a single increment.
    # the increment changes to a decrement for other sides of the diagonal.

    length = len(queens)
    threats = [0] * length

    # check for same row threats
    col = 0
    while col < length:
        # check for +ve same row threats
        row = col + 1
        while row < length:
            if (queens[row].pos == queens[col].pos):
                threats[col] += 1
            row += 1

        # check for -ve same row threats
        row = col - 1
        while row > -1:
            if (queens[row].pos == queens[col].pos):
                threats[col] += 1
            row -= 1

        col += 1

    # check for main diagonal threats
    col = 0
    while col < length:
        # check for +ve main diagonal
        row = col + 1
        inc = 1
        while row < length:
            if queens[row].pos == queens[col].pos + inc:
                threats[col] += 1
            inc = inc + 1
            row = row + 1

        # check for -ve main diagonal
        row = col - 1
        dec = 1
        while row > -1:
            if queens[row].pos == queens[col].pos - dec:
                threats[col] += 1
            dec = dec + 1
            row = row - 1

        col += 1

    # check for antidiagonal threats
    col = 0
    while col < length:
        # check for +ve antidiagonal threats
        row = col + 1
        dec = 1
        while row < length:
            if queens[row].pos == queens[col].pos - dec:
                threats[col] += 1
            dec = dec + 1
            row = row + 1

        # check for -ve antidiagonal threats
        row = col - 1
        inc = 1
        while row > -1:
            if queens[row].pos == queens[col].pos + inc:
                threats[col] += 1
            inc = inc + 1
            row = row - 1

        col += 1

    return threats


def update_threats(queens: List[Queen], threats: List[int]) -> None:
    for i, queen in enumerate(queens):
        queen.threats = threats[i]


def copy_queens(queens: List[Queen]) -> List[Queen]:
    copy = []
    for queen in queens:
        copy.append(Queen(queen.pos, queen.threats))
    return copy


##################################


# A* STUFF


class BoardNode():
    # no. of steps default to 0 representing the initial (start) state
    def __init__(self, queens: List[Queen] = None, steps: int = 0):
        # the queens that defines the state of this board node
        # the index of the array itself represents what col we are at.
        # the value in the index represents what row we are at.
        # example: [2, 0, 1], represents:
        #   0 1 2   <- column
        # 0 - x -
        # 1 - - x
        # 2 x - -
        # ^ row
        self.queens = queens

        # total_threats "h": defines the total number of threats on the board
        total_threats = 0
        for queen in queens:
            total_threats += queen.threats
        self.total_threats = total_threats

        # steps "g": defines the number of steps taken by a queen to reach this state
        self.steps = steps
        # f = g + h
        self.cost = self.steps + self.total_threats

    def __eq__(self, o: object) -> bool:
        return self.queens == o.queens

    def __str__(self) -> str:
        str = '['
        for q in self.queens:
            str += f'{q.pos}, '
        str += ']'
        return f'BoardNode({self.cost} = {self.steps} + {self.total_threats}, queens: {str})'


def generate_states(queensList: List[Queen]) -> List[BoardNode]:
    # the goal of this function is to generate all possible moves
    # or (states), a state represents the board, hence the usage of BoardNode
    # a boardNode stores the cost of reaching (steps) it and the amount of threats in it
    # this is used to calculate its cost (cost [f] = steps [g] + h [total_threats])
    # a boardNode is generated by moving a queen, using the new positions and threats to create it.
    # after exploring all possible (vertical) moves, they all will be added to the possible_states.
    # the possible states will be used to pick the lowest cost, and then repeat.

    possible_states: List[BoardNode] = []

    # generate +ve moves
    col = 0
    while col < len(queensList):
        queens = copy_queens(queensList)

        steps = 0
        row = queens[col].pos
        while row < len(queens) - 1:
            queens[col].pos += 1
            steps += 1

            new_threats = calc_threats(queens)
            update_threats(queens, new_threats)

            qs = copy_queens(queens)
            possible_states.append(BoardNode(qs, steps))

            row += 1

        col += 1

    # generate -ve moves
    col = 0
    while col < len(queensList):
        queens = copy_queens(queensList)

        steps = 0
        row = queens[col].pos
        while row > 0:
            queens[col].pos -= 1
            steps += 1

            new_threats = calc_threats(queens)
            update_threats(queens, new_threats)
            qs = copy_queens(queens)
            possible_states.append(BoardNode(qs, steps))

            row -= 1

        col += 1

    def sortKey(e: BoardNode):
        return e.cost

    possible_states.sort(reverse=True, key=sortKey)

    return possible_states


def rand_initial_state(N: int) -> BoardNode:
    queens: List[Queen] = []
    for n in range(N):
        queens.append(Queen(random.randint(0, N - 1)))
    threats = calc_threats(queens)
    update_threats(queens, threats)
    return BoardNode(queens)


def a_star(state: BoardNode, visited_states: List[BoardNode], steps_count):
    # generate possible next moves/states
    states: List[BoardNode] = generate_states(state.queens)
    # get the move/state with lowest cost
    next_state: BoardNode = states.pop()

    # if the popped state and the one before it has equal cost (f),
    # check if the one before it has lower threats (h), if yes choose it.
    if next_state.cost == states[-1].cost:
        if states[-1].total_threats < next_state.total_threats:
            next_state = states.pop()

    # check if the goal state has been reached.
    # the goal states is defined by the threats (h) being 0
    if next_state.total_threats == 0:
        visited_states.clear()
        print('HOLAAA')
        print(f'final state: {next_state}')
        steps_count[0] += 1
        return next_state

    # check if the popped state has already been visited before
    # if yes, get the next possible state/move, and repeat.
    i = 0
    while i < len(visited_states):
        if next_state == visited_states[i]:
            if (len(states) > 0):
                next_state = states.pop()
                i = 0
                continue
        i += 1

    steps_count[0] += 1
    visited_states.append(next_state)
    return next_state


##################################


# GENETIC STUFF


MUTATE_RATE: float = 0.05
CROSSOVER_RATE: float = 1.0
MULTIPOINT: bool = False


class Solution():
    def __init__(self, queens: List[Queen]):
        # the queens define the solution/chromosome,
        # The position of each queen is a gene.
        # the queen object itself is just a wrapper class for the queen position and theeats on it.
        self.queens = queens

        # total_threats (fitness): the fitness of the solution, lower is better. 0 is solved.
        total_threats = 0
        for queen in queens:
            total_threats += queen.threats
        self.total_threats = total_threats

    def __str__(self) -> str:
        str = '['
        for q in self.queens:
            str += f'{q.pos}, '
        str += ']'
        return f'Solution(fitness: {self.total_threats}, queens: {str})'


# creates a random solution (random queen positions)
def create_solution(N) -> Solution:
    queens: List[Queen] = []
    for n in range(N):
        queens.append(Queen(random.randint(0, N - 1)))
    threats = calc_threats(queens)
    update_threats(queens, threats)
    return Solution(queens)


# returns a mutated gene (a new position for a queen)
def mutated_gene(N: int) -> int:
    return random.randint(0, N - 1)


# where the magic happens,
# depending on the passe paras it will crossover and mutate to produce a new solution out of the two passed solutions.
def mate(parent1: Solution, parent2: Solution, mutate_rate: float = MUTATE_RATE, multipoint: bool = MULTIPOINT, crossover_rate: float = CROSSOVER_RATE) -> Solution:

    child: Solution = None

    prob = random.random()

    if prob < crossover_rate:
        child = crossover(parent1, parent2, multipoint)
    else:
        child = parent1 if parent1.total_threats < parent2.total_threats else parent2

    for queen in child.queens:
        prob = random.random()
        if prob < mutate_rate:
            queen.pos = mutated_gene(len(child.queens))

    return child


# takes two solutions and crosses them over on a random point,
# this produces to children, the fittest is returned.
def crossover(parent1: Solution, parent2: Solution, multipoint: bool = False) -> Solution:
    if not multipoint:
        point: int = random.randint(0, len(parent1.queens) - 1)

        queens1: List[Queen] = copy_queens(
            parent1.queens[:point] + parent2.queens[point:])
        queens2: List[Queen] = copy_queens(
            parent2.queens[:point] + parent1.queens[point:])

        new_threats = calc_threats(queens1)
        update_threats(queens1, new_threats)
        new_threats = calc_threats(queens2)
        update_threats(queens2, new_threats)

        child1: Solution = Solution(queens1)
        child2: Solution = Solution(queens2)

        return child1 if child1.total_threats < child2.total_threats else child2


def genetic(N: int, population_size: int, generations: int, elitism: bool = True, mutate_rate: float = MUTATE_RATE, multipoint: bool = MULTIPOINT, crossover_rate: float = CROSSOVER_RATE, generation_count=[0]) -> Solution:
    generation: int = 1
    solved: bool = False
    population: List[Solution] = []

    for _ in range(population_size):
        population.append(create_solution(N))

    while (generation <= generations) & (not solved):

        # sort the population based on fitness (threats)
        population.sort(key=lambda solution: solution.total_threats)

        if population[0].total_threats == 0:
            solved = True
            print('Hola FOUND ITTTT')
            print(population[0])
            generation_count[0] = generation
            return population[0]

        new_generation: List[Solution] = []

        if elitism:
            # pass the top 10% solutions to the next generation
            top_ten = int((10 * population_size) / 100)
            new_generation.extend(population[:top_ten])

        # pick and mate parents for the next genration randomly from the top 50%
        top_fifty = int((50 * population_size) / 100)
        for _ in range(int((90 * population_size) / 100)):
            parent1 = random.choice(population[:top_fifty])
            parent2 = random.choice(population[:top_fifty])

            child = mate(parent1, parent2, mutate_rate,
                         multipoint, crossover_rate)
            new_generation.append(child)

        population = new_generation

        # print(f'gen: {generation}, {population[0]}')

        generation += 1

        generation_count[0] = generation

    population.sort(key=lambda solution: solution.total_threats)
    return population[0]


# print(genetic(8, 100, 100))

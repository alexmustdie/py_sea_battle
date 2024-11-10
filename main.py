import sys
import random

class Dot:

    STATES = {'O': 97, '■': 92, 'X': 91, 'T': 93, '-': 96}

    def __init__(self, x, y, state='O'):
        self.x = x
        self.y = y
        self.state = state

    def __eq__(self, item):
        return (self.x == item.x and self.y == item.y)

    def print_state(self, hid):
        state = (self.state if self.state in ('X', 'T') else '-') if hid else self.state
        print('\033[{}m{}\033[00m'.format(self.STATES[state], state), end=' | ')

class Ship:

    def __init__(self, dot, length, direction='h'):

        self.dots = [dot]
        self.health = length
        self.direction = direction

        for i in range(1, length):
            try:
                x = dot.x + (i if direction == 'h' else 0)
                if x < 1 or x > 6:
                    raise
                y = dot.y + (i if direction == 'v' else 0)
                if y < 1 or y > 6:
                    raise
            except:
                raise Exception('Out of bounds')
            self.dots += [Dot(x, y)]

class Board:

    def __init__(self, scale, name, hid=False):

        self.scale = scale
        self.name = name
        self.hid = hid
        self.dots = []
        self.ships = []

        for i in range(1, scale + 1):
            for j in range(1, scale + 1):
                self.dots += [Dot(i, j)]

    def check_ships_health(self):
        print(f'{self.name}\'s ship sunk')
        if not len([s for s in self.ships if s.health]):
            print(f'Game over! {self.name} lost.')
            sys.exit(0)

    def check_contour(self, dot):
        x, y = dot.x, dot.y
        contour = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        for ship in self.ships:
            for d in ship.dots:
                if (d.x, d.y) in contour:
                    return True
        return False

    def get_dot(self, dot):
        return [d for d in self.dots if d == dot][0]

    def choice_dot(self, states=['O']):
        return random.choice([d for d in self.dots if d.state in states])

    def add_ship(self, length=1):
        old_dots = self.dots
        while True:
            dots = old_dots
            ship = None
            try:
                ship = Ship(dot=self.choice_dot(), length=length, direction=random.choice(['v', 'h']))
                for dot in ship.dots:
                    if self.check_contour(dot):
                        raise Exception('Contour check failed')
                for i, dot in enumerate(dots):
                    for ship_dot in ship.dots:
                        if dot == ship_dot:
                            dots[i].state = '■'
            except Exception as e:
                # print(f'{e}\n')
                continue
            self.ships += [ship]
            self.dots = dots
            break

    def print(self):
        print(f'{self.name}\'s board:\n')
        print('  |', ' | '.join([str(x) for x in list(range(1, self.scale + 1))]), '|\n')
        print(1, end=' | ')
        i = 1
        k = 2
        for dot in self.dots:
            dot.print_state(self.hid)
            if i % self.scale == 0 and k < (self.scale + 1):
                print(f'\n\n{k}', end=' | ')
                k += 1
            i += 1
        print('\n')

class Player:

    def __init__(self, enemy_board):
        self.board = enemy_board

    def random_board(self):
        self.board.add_ship(length=3)
        [self.board.add_ship(length=2) for _ in range(2)]
        [self.board.add_ship() for _ in range(4)]

    def ask(self):
        pass

    def shot(self, dot):
        dot.state = 'T'
        for ship in self.board.ships:
            for ship_dot in ship.dots:
                if dot == ship_dot:
                    dot.state = 'X'
                    ship.health -= 1
                    if ship.health == 0:
                        self.board.check_ships_health()
                        return True
                    else:
                        print(f'{self.board.name}\'s ship damaged')
        return False

    def print_enemy_board(self):
        self.board.print()

class AI(Player):

    def ask(self):
        return self.board.choice_dot(['O', '■'])

class User(Player):

    def ask(self):
        while True:
            try:
                x, y = [int(x) for x in input('Type dot: ').split(' ')]
                if x < 1 or x > self.board.scale or y < 1 or y > self.board.scale:
                    raise Exception(f'Type two numbers from 1 to {self.board.scale}')
                dot = self.board.get_dot(Dot(x, y))
                if dot.state in ('T', 'X'):
                    raise Exception('Already shooted!')
                return dot
            except ValueError:
                print('Type 2 numbers separated by space\n')
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                print(f'{e}\n')

class Game:

    def __init__(self, scale, hid=True):
        self.ai = AI(enemy_board=Board(scale, 'User'))
        self.user = User(enemy_board=Board(scale, 'AI', hid))

    def print_header(self):
        print('*' * (3 + 4 * self.user.board.scale) + '\n')
        self.user.print_enemy_board()
        self.ai.print_enemy_board()

    def start(self):

        self.ai.random_board()
        self.user.random_board()

        ai_sunk_ship = False
        user_sunk_ship = False

        while True:
            self.print_header()
            if not ai_sunk_ship:
                user_sunk_ship = self.user.shot(self.user.ask())
            if not user_sunk_ship:
                ai_sunk_ship = self.ai.shot(self.ai.ask())

if __name__ == '__main__':

    try:
        scale = int(sys.argv[1])
    except:
        scale = 6

    try:
        hid = sys.argv[2] == 'h'
    except:
        hid = False

    Game(scale, hid).start()

import sys
import random

class Ship:
    def __init__(self, dots):
        self.dots = []
        for dot in dots:
            x, y = dot
            self.dots += [(x, y)]

class Desk:

    def __init__(self, name):
        self.name = name
        self.ships = []
        self.dots = []
        for i in range(1, 7):
            for j in range(1, 7):
                self.dots += [[i, j, 'O']]

    def print_state(self, state, code):
        print('\033[{}m{}\033[00m'.format(code, state), end=' | ')

    def print(self):
        print(f'\n{self.name}\'s desk:\n\n')
        print('  |', ' | '.join([str(x) for x in list(range(1, 7))]), '|\n')
        print(1, end=' | ')
        i = 1
        k = 2
        x_count = 0
        for dot in self.dots:
            if dot[2] == 'O':
                self.print_state(dot[2], 97)
            if dot[2] == '■':
                self.print_state(dot[2], 92 if self.name == 'Computer' else 94)
            if dot[2] == 'X':
                self.print_state(dot[2], 91)
                x_count += 1
            if dot[2] == 'T':
                self.print_state(dot[2], 93)
            if i % 6 == 0 and k < 7:
                print(f'\n\n{k}', end=' | ')
                k += 1
            i += 1
        print('\n')
        if x_count == 11:
            print(f'Game over! {self.name} lost.')
            sys.exit(0)

    def choice_dot(self, states=['O']):
        return tuple(random.choice([d for d in self.dots if d[2] in states])[:-1])

    def check_if_free(self, x, y):
        square = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        for ship in self.ships:
            for dot in ship.dots:
                if dot in square:
                    return False
        return True

    def set_dots_state(self, dots, state='■'):
        for i, dot in enumerate(self.dots):
            if tuple(dot[:-1]) in dots:
                self.dots[i][2] = state

    def choice_two_dots(self):
        while True:
            x_1, y_1 = self.choice_dot()
            if 1 < x_1 < 6 and 1 < y_1 < 6\
                and self.check_if_free(x_1, y_1):
                break
        while True:
            x_2 = x_1 + random.randint(-1, 1)
            y_2 = y_1 + (random.choice((-1, 1)) if x_1 == x_2 else 0)
            if self.check_if_free(x_2, y_2):
                break
        return [(x_1, y_1), (x_2, y_2)]

    def gen_ship_three_dots(self):
        dot_1, dot_2 = self.choice_two_dots()
        x_2, y_2 = dot_1
        x_1, y_1 = dot_2
        while True:
            x_3 = x_2 + (0 if x_1 == x_2 else (1 if x_1 < x_2 else -1))
            y_3 = y_2 + (0 if y_1 == y_2 else (1 if y_1 < y_2 else -1))
            if self.check_if_free(x_3, y_3):
                break
        dots = [dot_1, dot_2, (x_3, y_3)]
        self.set_dots_state(dots)
        self.ships.append(Ship(dots))

    def gen_ship_two_dots(self):
        dots = self.choice_two_dots()
        self.set_dots_state(dots)
        self.ships.append(Ship(dots))

    def gen_ship_one_dots(self):
        while True:
            dot = self.choice_dot()
            if self.check_if_free(*dot):
                break
        self.set_dots_state([dot])
        self.ships.append(Ship([dot]))

    def gen_ships(self):
        self.gen_ship_three_dots()
        [self.gen_ship_two_dots() for _ in range(2)]
        [self.gen_ship_one_dots() for _ in range(4)]

    def shoot(self, x, y):
        self.set_dots_state([(x, y)], 'T')
        for ship in self.ships:
            for dot in ship.dots:
                if dot == (x, y):
                    self.set_dots_state(ship.dots, 'X')
                    continue

if __name__ == '__main__':

    human_desk = Desk('Human')
    human_desk.gen_ships()
    shooted_dots = []

    comp_desk = Desk('Computer')
    comp_desk.gen_ships()

    while True:
        print('***************************')
        human_desk.print()
        comp_desk.print()
        ### Human's shot
        while True:
            try:
                print('Type dot:', end=' ')
                x, y = [int(x) for x in input().split(' ')]
                if x < 1 or x > 6 or y < 1 or y > 6:
                    raise Exception('Type 2 numbers from 1 to 6')
                if (x, y) not in shooted_dots:
                    comp_desk.shoot(x, y)
                    shooted_dots += [(x, y)]
                    break
                else:
                    print('Already shooted!\n')
                    continue
            except ValueError:
                print('Type 2 numbers separated by space\n')
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                print(f'{e}\n')
        ### Computer's shot
        dot = human_desk.choice_dot(['O', '■'])
        human_desk.shoot(*dot)
        print()

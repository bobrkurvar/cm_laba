import random
from collections import namedtuple

def gen_card_base(height: int, width: int, suit: str, cost: str) -> str:
    card_base = ''
    for i in range(height):
        if i == 0:
            card_base += '/' + '-' * width + '\\\n'
        elif i == 1:
            card_base += '|' + ' ' + cost + ' ' * (width - 2) + '|\n'
        elif i == 2:
            card_base += '|' + ' ' + suit + ' ' * (width - 2) + '|\n'
        elif i == height - 2:
            card_base += '|' + ' ' * (width - 2) + suit + ' ' + '|\n'
        elif i == height - 1:
            card_base += '|' + ' ' * (width - 2) + cost + ' ' + '|\n'
        else:
            card_base += '|' + ' ' * width + '|\n'
    else:
        card_base += '\\' + '-' * width + '/'
    return card_base

def gen_card_ace(height: int, width: int, suit: str, cost: str) -> str:
    card_base = gen_card_base(height, width, suit, cost)
    layers = card_base.split('\n')
    start_h = height // 3
    start_w = width // 4
    for j, i in enumerate(range(height - start_h, start_h - 1, -1)):
        if i == (len(range(height - start_h, start_h - 1, -1)) // 2) + start_h:
            layers[i] = layers[i][:start_w+j + 1] + (suit + ' ') * 4 + layers[i][start_w + j + 9: ]
        else:
            layers[i] = layers[i][:start_w + j] + suit + layers[i][start_w+j+1:]
            layers[i] = layers[i][: width-start_w - j: -1] + suit + layers[i][width-start_w-j-1: : -1]
    card_ace = '\n'.join(layers)
    return card_ace

def gen_card_queen(height: int, width: int, suit: str, cost: str) -> str:
    card_base = gen_card_base(height, width, suit, cost)
    layers = card_base.split('\n')
    start_h = height // 3
    start_w = width // 4
    for j, i in enumerate(range(height - start_h, start_h - 1, -1)):
        if j == 0:
            layers[i] = layers[i][:start_w] + suit * 3 + layers[i][start_w + 1:]
    card_queen = '\n'.join(layers)
    return card_queen



if __name__ == "__main__":
    # Card = namedtuple('Card', 'cost, suit')
    # # user = {}
    # # bot = {}
    # # while True:
    # #     user_pick = input('Взять карту (y/n): ')
    # #     if user_pick == 'y': pass
    # #     elif user_pick == 'n': pass
    # #     else:
    # #         print('Неправильный ввод')
    height, width = 11, 20
    c = gen_card_ace(height, width, '♠', 'A')
    a = gen_card_queen(height, width, '♠', 'Q')
    print(a)
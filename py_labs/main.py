import random
from typing import List

def gen_card_base(height: int, width: int, suit: str, cost: str) -> str:
    card_base = ''
    for i in range(height):
        if i == 0:
            card_base += '/' + '=' * width + '\\\n'
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
        card_base += '\\' + '=' * width + '/'
    return card_base

def split_to_rows_lst(string: str) -> List[List[str]]:
    layers: list = string.split('\n')
    for i in range(len(layers)):
        layers[i] = list(layers[i])
    return layers

def join_lst_to_str(lst: List[List[str]]):
    for i in range(len(lst)):
        lst[i] = ''.join(lst[i])
    card = '\n'.join(lst)
    return card

def gen_card_ace(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 4, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers =  split_to_rows_lst(card_base)
    for j, i in enumerate(range(height - start_h, start_h-1, -1)):
        if i == start_h:
            if start_w + j == width // 2:
                layers[i][start_w + j] = suit
            else:
                print(j)
                for a in range(width-(2 * j + 6)):
                    layers[i][start_w + j + a] = suit
        elif i == (height-start_h)//2 + start_h - 1:
            for q in range(0, 3*j + 1, 2):
                layers[i][start_w + j + q] = suit
        else:
            layers[i][start_w + j] = suit
            layers[i][width - start_w - j] = suit

    card = join_lst_to_str(layers)
    return card

def gen_card_queen(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 4, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers =  split_to_rows_lst(card_base)

    for j in range(2, width - 2 * start_w - 1, 2):
        layers[start_h][start_w + j] = suit
        layers[height - start_h][start_w + j] = suit

    for j in range(1, height - 2 * start_h ):
        layers[start_h + j][start_w] = suit
        layers[start_h + j][width - start_w] = suit

    layers[height - start_h][width - start_w + 1] = suit

    card = join_lst_to_str(layers)
    return card

def gen_card_king(suit: str, cost: str, height: int = 13, width: int = 18):
    start_h, start_w = 4, (width - 4) // 2
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)

    for i in range(start_h, height - start_h + 1):
        layers[i][start_w] = suit

    for j, i in enumerate(range(height - 2 * start_h + 1, height - start_h + 1), 1):
        layers[i][start_w + j] = suit
        layers[height - i][start_w + j] = suit

    card = join_lst_to_str(layers)
    return card

def gen_card_jack(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 4, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)

    for i in range(start_h, height - start_h):
        layers[i][width - 2 * start_w] = suit

    for i in range(start_w + 4, width - start_w, 2):
        layers[start_h][i] = suit

    layers[height-start_h][width - 2 * start_w - 1] = suit
    layers[height - start_h -1][width - 2 * start_w - 3] = suit

    card = join_lst_to_str(layers)
    return card

def gen_card_two(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 3, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)
    for i in range(2):
        layers[start_h + 4*i][width // 2 + 1] = suit
        layers[start_h + 1 + 4*i][width // 2 + 1] = suit
        layers[start_h + 2 + 4*i][width // 2 + 1] = suit
        layers[start_h + 1 + 4*i][width // 2 + 2] = suit
        layers[start_h + 1 + 4*i][width // 2] = suit
    card = join_lst_to_str(layers)
    return card

def gen_card_three(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 2, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)
    for i in range(3):
        layers[start_h + 4*i][width // 2 + 1] = suit
        layers[start_h + 1 + 4*i][width // 2 + 1] = suit
        layers[start_h + 2 + 4*i][width // 2 + 1] = suit
        layers[start_h + 1 + 4*i][width // 2 + 2] = suit
        layers[start_h + 1 + 4*i][width // 2] = suit
    card = join_lst_to_str(layers)
    return card

def gen_card_four(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 4, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)
    for i in range(2):
        layers[start_h + 4*i][start_w + 1] = suit
        layers[start_h + 1 + 4*i][start_w + 1] = suit
        layers[start_h + 2 + 4*i][start_w + 1] = suit
        layers[start_h + 1 + 4*i][start_w + 2] = suit
        layers[start_h + 1 + 4*i][start_w] = suit
    for i in range(2):
        layers[start_h + 4*i][width-start_w-1] = suit
        layers[start_h + 1 + 4*i][width-start_w-1] = suit
        layers[start_h + 2 + 4*i][width-start_w-1] = suit
        layers[start_h + 1 + 4*i][width-start_w-2] = suit
        layers[start_h + 1 + 4*i][width-start_w] = suit
    card = join_lst_to_str(layers)
    return card

def gen_card_five(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 4, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)
    layers[start_h][start_w] = suit
    layers[height - start_h][start_w] = suit
    layers[start_h][width - start_w] = suit
    layers[height - start_h][width - start_w] = suit
    layers[height - 2 * start_h + 1][width - 2 * start_w - 1] = suit
    card = join_lst_to_str(layers)
    return card

def gen_card_six(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 4, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)
    for i in range(0, 5, 2):
        layers[start_h + i][start_w] = suit

    for i in range(0, 5, 2):
        layers[start_h + i][width - start_w] = suit

    card = join_lst_to_str(layers)
    return card

def gen_card_seven(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 4, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)
    for i in range(0, 5, 2):
        layers[start_h + i][start_w] = suit

    layers[start_h + 1][width//2] = suit

    for i in range(0, 5, 2):
        layers[start_h + i][width - start_w] = suit

    card = join_lst_to_str(layers)
    return card

def gen_card_eight(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 4, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)
    for i in range(0, 5, 2):
        layers[start_h + i][start_w] = suit

    layers[start_h + 1][width//2] = suit
    layers[height - start_h - 2][width // 2] = suit

    for i in range(0, 5, 2):
        layers[start_h + i][width - start_w] = suit

    card = join_lst_to_str(layers)
    return card

def gen_card_nine(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 4, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)
    for i in range(0, 5, 2):
        layers[start_h + i - 1][start_w] = suit

    layers[start_h][width//2] = suit
    layers[height//2][width//2] = suit
    layers[height - start_h][width // 2] = suit

    for i in range(0, 5, 2):
        layers[start_h + i - 1][width - start_w] = suit

    card = join_lst_to_str(layers)
    return card

def gen_card_ten(suit: str, cost: str, height: int = 13, width: int = 18) -> str:
    start_h, start_w = 4, 4
    card_base = gen_card_base(height, width, suit, cost)
    layers = split_to_rows_lst(card_base)
    for i in range(0, 7, 2):
        layers[start_h + i - 1][start_w] = suit

    layers[start_h][width//2] = suit
    layers[height - start_h - 1][width // 2] = suit

    for i in range(0, 7, 2):
        layers[start_h + i - 1][width - start_w] = suit

    card = join_lst_to_str(layers)
    return card

def gen_card(suit: str, cost: str) -> str:
    options = {
        '2': gen_card_two, '3': gen_card_three, '4': gen_card_four,
        '5': gen_card_five, '6': gen_card_six, '7': gen_card_seven,
        '8': gen_card_eight, '9': gen_card_nine, '10': gen_card_ten,
        'J': gen_card_jack, 'Q': gen_card_queen, 'K': gen_card_king,
        'A': gen_card_ace
    }
    return options.get(cost)(suit, cost)

def from_str_cost_to_int(cost: str, card_sum: int) -> int:
    options = {}
    options = options.fromkeys(['J', 'Q', 'K'], 10)
    options['A'] = 11 if card_sum <= 10 else 1
    num = options.get(cost)
    if num is None: num = int(cost)
    return num

def print_cards(cards):
    cards_with_layers = [i.split('\n') for i in cards]
    height, width = 14, 18
    for i in range(height):
        for j in range(len(cards_with_layers)):
            print(cards_with_layers[j][i], end='\t')
        print()


if __name__ == "__main__":
    deck = []
    for i in tuple(range(2, 11)) + ('J', 'Q', 'K', 'A'):
        for j in ('♠', '♥', '♦', '♣'):
            deck.append(dict(suit=j, cost=str(i)))
    random.shuffle(deck)
    while input('Играем? (y/n): ').lower() == 'y':
        user = [deck[0], deck[1]]
        bot = [deck[2], deck[3]]
        user_sum = 0
        bot_sum = 0
        deck = deck[4:]
        print('user cards: ')
        for card in user: user_sum += from_str_cost_to_int(card['cost'], user_sum)
        print_cards(gen_card(card['suit'], card['cost']) for card in user)
        print(f'user sum: {user_sum}')
        print('bot cards: ')
        for card in bot: bot_sum += from_str_cost_to_int(card['cost'], bot_sum)
        print_cards(gen_card(card['suit'], card['cost']) for card in bot)
        print(f'bot sum: {bot_sum}')
        if user_sum == 21 and bot_sum == 21:
            print('DRAW')
            continue
        elif user_sum == 21:
            print('USER WIN')
            continue
        elif bot_sum == 21:
            print('BOT WIN')
            continue

        while True:
            user_lose = False
            bot_lose = False
            while input('Брать карту? (y/n): ').lower() == 'y':
                card = deck[0]
                user_sum += from_str_cost_to_int(card['cost'], user_sum)
                user.append(card)
                deck = deck[1:]
                print('user cards: ')
                print_cards(gen_card(card['suit'], card['cost']) for card in user)
                print(f'user sum: {user_sum}')
                if user_sum >= 21:
                    if user_sum > 21: user_lose = True
                    break
            if user_lose:
                print('BOT WIN')
                break
            while bot_sum < 21:
                card = deck[0]
                bot_sum += from_str_cost_to_int(card['cost'], bot_sum)
                bot.append(card)
                deck = deck[1:]
                print('bot cards: ')
                print_cards(gen_card(card['suit'], card['cost']) for card in bot)
                print(f'bot sum: {bot_sum}')
                if bot_sum > 21:
                    bot_lose = True
                    break
            if bot_lose:
                print('USER WIN')
                break

            if user_sum > bot_sum: print('USER WIN')
            elif bot_sum > user_sum: print('BOT WIN')
            else: print('DRAW')


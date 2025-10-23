from cards import SimpleCard
from random import shuffle, randint

class User:

    def __init__(self):
        self.deck = None


class Game:

    def __init__(self, users: list[User]):
        deck = [SimpleCard(color, value) for color in ("blue", "red") for value in range(5)]
        shuffle(deck)
        self.deck = deck
        self.users = users
        self.current_card = None
        self.turn = None

    def give_cards(self):
        for user in self.users:
            cnt = 3
            user.deck = self.deck[:cnt]
            self.deck = self.deck[cnt:]

    @staticmethod
    def match_cards(card1: SimpleCard, card2: SimpleCard):
        return card1.value == card2.value or card1.color == card2.color

    def toss_card(self, uno: list, card_index: int = 0, match: bool = True):
        if not match or self.match_cards(self.current_card, self.users[self.turn].deck[int(card_index)]):
            self.current_card = self.users[self.turn].deck.pop(card_index)
            self.deck.append(self.current_card)
            if len(self.users[self.turn].deck) == 1:
                say_uno = input("UNO: (y/n): ")
                if say_uno.lower() == 'y':
                    try:
                        uno.remove(self.users[self.turn])
                    except ValueError:
                        pass
                elif say_uno.lower() == 'n' and self.users[self.turn] not in uno:
                    uno.append(self.users[self.turn])

    def table_info(self):
        print("table deck length:", len(self.deck))
        print(f"turn User {self.turn}")
        for i, user in enumerate(self.users):
            print(f"User {i} deck length: {len(user.deck)}")

    def give_new_cards(self, user: User | None = None, num: int = 1):
        for i in range(num):
            new_card = self.deck.pop(0)
            print("взяли карту: ", new_card)
            if user:
                user.deck.append(new_card)
            else:
                self.users[self.turn].deck.append(new_card)

    def start(self):
        shuffle(self.users)
        self.give_cards()
        uno = []
        self.turn = randint(0, len(self.users) - 1)
        self.toss_card(match=False, uno=uno)
        game_flag = True
        self.turn = self.turn + 1 if self.turn + 1 < len(self.users) else 0
        while game_flag:
            print(f"User {self.turn} your turn\ncard on the table: {self.current_card}")
            print(f"your cards: {", ".join(str(card) for card in self.users[self.turn].deck)}")
            input_flag = True
            while input_flag and (info := input("выберете действие: 1 - бросить карту, 2 - взять новую карту, 3 - UNO 4 - tale_info: ")):
                if info == "1":
                    print(f"card on the table: {self.current_card}")
                    cards_for = [str(i) + " - ( " + str(card) + " )" for i, card in enumerate(self.users[self.turn].deck)]
                    card_index = input(f"выберите какую карту бросить: {", ".join(cards_for)}: ")
                    if self.match_cards(self.current_card, self.users[self.turn].deck[int(card_index)]):
                        self.toss_card(card_index = int(card_index), uno=uno)
                        input_flag = False
                    else:
                        print("Нельзя положить данную карту на текущую на столе")
                elif info == "2":
                    self.give_new_cards()
                    self.toss_card(card_index=len(self.users[self.turn].deck) - 1, uno=uno)
                    input_flag = False
                elif info == "3":
                    for user in self.users:
                        if len(user.deck) == 1:
                            if self.users[self.turn] is user:
                                print(f"UNO BY USER {self.turn}")
                                try:
                                    uno.remove(user)
                                except ValueError:
                                    pass
                                input_flag = False
                            elif user in uno:
                                print(f"2 новые карты пользователю")
                                self.give_new_cards(user, 2)
                elif info == "4":
                    self.table_info()
                else:
                    pass
            if not self.users[self.turn].deck:
                print(f"User {self.turn} победил")
                game_flag = False
            self.turn = self.turn + 1 if self.turn < len(self.users) - 1 else 0
            print()








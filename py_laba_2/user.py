from cards import SimpleCard
from random import shuffle, randint

class User:

    def __init__(self):
        self.deck = None


class Game:

    def __init__(self, users: list[User]):
        deck = [SimpleCard(color, value) for color in ("green", "yellow", "blue", "red") for value in range(10)]
        shuffle(deck)
        self.deck = deck
        self.users = users

    def give_cards(self):
        for user in self.users:
            user.deck = self.deck[:7]
            self.deck = self.deck[7:]

    @staticmethod
    def match_cards(card1: SimpleCard, card2: SimpleCard):
        return card1.value == card2.value or card1.color == card2.color

    def start(self):
        shuffle(self.users)
        self.give_cards()
        turn = randint(0, len(self.users) - 1)
        current_card = self.users[turn].deck.pop(0)
        flag = True
        i = turn + 1 if turn + 1 < len(self.users) else 0
        while flag:
            print(f"User {i} your turn\ncard on the table: {current_card}")
            print(f"your cards: {", ".join(str(card) for card in self.users[i].deck)}")
            input_flag = True
            while input_flag and (info := input("выберете действие: 1 - бросить карту, 2 - взять новую карту, 3 - UNO: ")):
                if info == "1":
                    print(f"card on the table: {current_card}")
                    cards_for = [str(i) + " - ( " + str(card) + " )" for i, card in enumerate(self.users[i].deck)]
                    card_index = input(f"выберите какую карту бросить: {", ".join(cards_for)}: ")
                    if self.match_cards(current_card, self.users[i].deck[int(card_index)]):
                        new_card = self.users[i].deck.pop(int(card_index))
                        self.deck.append(new_card)
                        current_card = new_card
                        input_flag = False
                    else:
                        print("Нельзя положить данную карту на текущую на столе")
                elif info == "2":
                    new_card = self.deck.pop(0)
                    print("взяли карту: ", new_card)
                    self.users[i].deck.append(new_card)
                    input_flag = False
                elif info == "UNO":
                    input_flag = False
                else:
                    pass
            if i < len(self.users) - 1:
                i += 1
            else:
                i = 0
            print()








class SimpleCard:

    def __init__(self, color: str, value: int):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"{self.color} : {self.value}"

    def __str__(self):
        return f"{self.color} : {self.value}"

    def special_action(self):
        pass


class SpecialCard(SimpleCard):

    def __init__(self, color: str, value: int):
        SimpleCard.__init__(self, color, value)

    def special_action(self):
        pass


class WildCard(SpecialCard):

    def __init__(self, color: str, value: int, plus: int):
        super().__init__(color, value)
        self.plus = plus

    def special_action(self):
        return {
            "plus": self.plus
        }



class WildCardPlusTwo(WildCard):
    def __init__(self, color: str, value: int):
        self.plus = 2
        super().__init__(color, value, self.plus)



class WildCardPlusFour(WildCard):
    def __init__(self, color: str, value: int):
        self.plus = 4
        super().__init__(color, value, self.plus)


class WildCardReverse(SpecialCard):

    def __init__(self, color: str, value: int, plus: int):
        super().__init__(color, value)
        self.plus = plus

    def special_action(self):
        return {
            "reverse": -1
        }


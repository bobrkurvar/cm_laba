
class SimpleCard:

    def __init__(self, color: str, value: int):
        self.color = color
        self.value = value

    def special_action(self):
        pass

    def __repr__(self):
        return f"{self.color} : {self.value}"

    def __str__(self):
        return f"{self.color} : {self.value}"

class SpecialCard(SimpleCard):

    def __init__(self, color, value, special):
        SimpleCard.__init__(self, color, value)
        self.special = special

    def special_action(self):
        pass


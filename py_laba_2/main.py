from user import User, Game

if __name__ == "__main__":
    n = input("Введите количество игроков: ")
    users = [User() for _ in range(int(n))]
    game = Game(users)
    game.start()
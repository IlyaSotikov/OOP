from abc import ABC, abstractmethod

class Entity(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

class Game(Entity):
    total_games = 0

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.currencies = {}
        Game.total_games += 1

    def add_currency(self, currency):
        self.currencies[currency.name] = currency

    def remove_currency(self, currency_name):
        if currency_name in self.currencies:
            del self.currencies[currency_name]

    def __str__(self):
        currency_names = list(self.currencies.keys())
        return f"Игра: {self.name}, Описание: {self.description}, Валюты: {currency_names}"

    def get_id(self):
        return self.name

    @staticmethod
    def get_total_games():
        return Game.total_games

class Currency(Entity):
    def __init__(self, name, price_per_unit):
        self.name = name
        self.price_per_unit = price_per_unit

    def __str__(self):
        return f"Валюта: {self.name}, Цена за единицу: {self.price_per_unit}"

    def get_id(self):
        return self.name

class User(Entity):
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.purchase_history = {}  # Используем словарь для хранения истории покупок

    def make_purchase(self, purchase):
        self.purchase_history[purchase.get_id()] = purchase

    def __str__(self):
        purchase_details = [str(purchase) for purchase in self.purchase_history.values()]
        return f"Пользователь: {self.username}, Email: {self.email}, История покупок: {purchase_details}"

    def get_id(self):
        return self.user_id

class Purchase(Entity):
    def __init__(self, user, game, currency, amount, payment_method):
        self.user = user
        self.game = game
        self.currency = currency
        self.amount = amount
        self.payment_method = payment_method
        self.status = "В ожидании"

    def confirm_purchase(self):
        self.status = "Подтверждено"
        self.user.make_purchase(self)

    def __str__(self):
        return (f"Покупка: Пользователь: {self.user.username}, Игра: {self.game.name}, "
                f"Валюта: {self.currency.name}, Количество: {self.amount}, "
                f"Способ оплаты: {self.payment_method.method_name}, Статус: {self.status}")

    def get_id(self):
        return f"{self.user.get_id()}_{self.game.get_id()}_{self.currency.get_id()}"

    def __eq__(self, other):
        if isinstance(other, Purchase):
            return self.get_id() == other.get_id()
        return False

    def __lt__(self, other):
        if isinstance(other, Purchase):
            return self.amount < other.amount
        return False

    def __hash__(self):
        return hash(self.get_id())

class PaymentMethod(Entity):
    def __init__(self, method_name, details):
        self.method_name = method_name
        self.details = details

    def __str__(self):
        return f"Способ оплаты: {self.method_name}, Детали: {self.details}"

    def get_id(self):
        return self.method_name

def main():
    games = {}
    users = {}
    payment_methods = {}

    while True:
        print("\nМеню:")
        print("1. Добавить игру")
        print("2. Добавить валюту в игру")
        print("3. Добавить пользователя")
        print("4. Добавить способ оплаты")
        print("5. Совершить покупку")
        print("6. Показать все данные")
        print("7. Выйти")

        choice = input("Введите ваш выбор: ")

        if choice == '1':
            name = input("Введите название игры: ")
            description = input("Введите описание игры: ")
            game = Game(name, description)
            games[name] = game
            print("Игра добавлена успешно!")

        elif choice == '2':
            game_name = input("Введите название игры для добавления валюты: ")
            try:
                game = games[game_name]
                currency_name = input("Введите название валюты: ")
                price_per_unit = float(input("Введите цену за единицу: "))
                currency = Currency(currency_name, price_per_unit)
                game.add_currency(currency)
                print("Валюта добавлена в игру успешно!")
            except KeyError:
                print("Игра не найдена!")

        elif choice == '3':
            user_id = int(input("Введите ID пользователя: "))
            username = input("Введите имя пользователя: ")
            email = input("Введите email: ")
            user = User(user_id, username, email)
            users[user_id] = user
            print("Пользователь добавлен успешно!")

        elif choice == '4':
            method_name = input("Введите название способа оплаты: ")
            details = input("Введите детали способа оплаты: ")
            payment_method = PaymentMethod(method_name, details)
            payment_methods[method_name] = payment_method
            print("Способ оплаты добавлен успешно!")

        elif choice == '5':
            user_id = int(input("Введите ID пользователя для совершения покупки: "))
            try:
                user = users[user_id]
                game_name = input("Введите название игры для покупки: ")
                try:
                    game = games[game_name]
                    currency_name = input("Введите название валюты для покупки: ")
                    try:
                        currency = game.currencies[currency_name]
                        amount = int(input("Введите количество для покупки: "))
                        payment_method_name = input("Введите название способа оплаты: ")
                        try:
                            payment_method = payment_methods[payment_method_name]
                            purchase = Purchase(user, game, currency, amount, payment_method)
                            purchase.confirm_purchase()
                            print("Покупка совершена успешно!")
                        except KeyError:
                            print("Способ оплаты не найден!")
                    except KeyError:
                        print("Валюта не найдена в игре!")
                except KeyError:
                    print("Игра не найдена!")
            except KeyError:
                print("Пользователь не найден!")

        elif choice == '6':
            print("\nВсе данные:")
            for game in games.values():
                print(game)
            for user in users.values():
                print(user)
            for payment_method in payment_methods.values():
                print(payment_method)
            print(f"Общее количество игр: {Game.get_total_games()}")

        elif choice == '7':
            print("Выход...")
            break

        else:
            print("Неверный выбор! Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()

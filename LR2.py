class Game:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.currencies = []

    def add_currency(self, currency):
        self.currencies.append(currency)

    def __str__(self):
        currency_names = [currency.name for currency in self.currencies]
        return f"Игра: {self.name}, Описание: {self.description}, Валюты: {currency_names}"

class Currency:
    def __init__(self, name, price_per_unit):
        self.name = name
        self.price_per_unit = price_per_unit

    def __str__(self):
        return f"Валюта: {self.name}, Цена за единицу: {self.price_per_unit}"

class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.purchase_history = []

    def make_purchase(self, purchase):
        self.purchase_history.append(purchase)

    def __str__(self):
        purchase_details = [str(purchase) for purchase in self.purchase_history]
        return f"Пользователь: {self.username}, Email: {self.email}, История покупок: {purchase_details}"

class Purchase:
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
        return f"Покупка: Пользователь: {self.user.username}, Игра: {self.game.name}, Валюта: {self.currency.name}, Количество: {self.amount}, Способ оплаты: {self.payment_method}, Статус: {self.status}"

class PaymentMethod:
    def __init__(self, method_name, details):
        self.method_name = method_name
        self.details = details

    def __str__(self):
        return f"Способ оплаты: {self.method_name}, Детали: {self.details}"

def main():
    # Создание объектов
    games = []
    users = []
    payment_methods = []

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
            games.append(game)
            print("Игра добавлена успешно!")

        elif choice == '2':
            game_name = input("Введите название игры для добавления валюты: ")
            game = next((g for g in games if g.name == game_name), None)
            if game:
                currency_name = input("Введите название валюты: ")
                price_per_unit = float(input("Введите цену за единицу: "))
                currency = Currency(currency_name, price_per_unit)
                game.add_currency(currency)
                print("Валюта добавлена в игру успешно!")
            else:
                print("Игра не найдена!")

        elif choice == '3':
            user_id = int(input("Введите ID пользователя: "))
            username = input("Введите имя пользователя: ")
            email = input("Введите email: ")
            user = User(user_id, username, email)
            users.append(user)
            print("Пользователь добавлен успешно!")

        elif choice == '4':
            method_name = input("Введите название способа оплаты: ")
            details = input("Введите детали способа оплаты: ")
            payment_method = PaymentMethod(method_name, details)
            payment_methods.append(payment_method)
            print("Способ оплаты добавлен успешно!")

        elif choice == '5':
            user_name = input("Введите имя пользователя для совершения покупки: ")
            user = next((u for u in users if u.username == user_name), None)
            if user:
                game_name = input("Введите название игры для покупки: ")
                game = next((g for g in games if g.name == game_name), None)
                if game:
                    currency_name = input("Введите название валюты для покупки: ")
                    currency = next((c for c in game.currencies if c.name == currency_name), None)
                    if currency:
                        amount = int(input("Введите количество для покупки: "))
                        payment_method_name = input("Введите название способа оплаты: ")
                        payment_method = next((pm for pm in payment_methods if pm.method_name == payment_method_name), None)
                        if payment_method:
                            purchase = Purchase(user, game, currency, amount, payment_method)
                            purchase.confirm_purchase()
                            print("Покупка совершена успешно!")
                        else:
                            print("Способ оплаты не найден!")
                    else:
                        print("Валюта не найдена в игре!")
                else:
                    print("Игра не найдена!")
            else:
                print("Пользователь не найден!")

        elif choice == '6':
            print("\nВсе данные:")
            for game in games:
                print(game)
            for user in users:
                print(user)
            for payment_method in payment_methods:
                print(payment_method)

        elif choice == '7':
            print("Выход...")
            break

        else:
            print("Неверный выбор! Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
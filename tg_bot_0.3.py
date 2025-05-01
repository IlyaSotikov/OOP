import sys
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget,
                             QTabWidget, QMessageBox, QComboBox, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


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
        self.purchase_history = {}

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления игровыми валютами")
        self.setGeometry(100, 100, 900, 600)

        # Инициализация данных
        self.games = {}
        self.users = {}
        self.payment_methods = {}

        # Создание основного виджета и layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Создание вкладок
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        # Создание вкладок интерфейса
        self.create_game_tab()
        self.create_currency_tab()
        self.create_user_tab()
        self.create_payment_method_tab()
        self.create_purchase_tab()
        self.create_view_data_tab()

        # Применение стилей
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background: white;
            }
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #ccc;
                padding: 8px;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background: #4CAF50;
                color: white;
            }
            QLabel {
                font-size: 12px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                font-size: 12px;
                margin: 4px 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QListWidget {
                border: 1px solid #ccc;
                background: white;
                font-size: 12px;
            }
        """)

    def create_game_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Форма добавления игры
        form_layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название игры:"))
        self.game_name_input = QLineEdit()
        name_layout.addWidget(self.game_name_input)
        form_layout.addLayout(name_layout)

        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("Описание:"))
        self.game_desc_input = QTextEdit()
        self.game_desc_input.setMaximumHeight(100)
        desc_layout.addWidget(self.game_desc_input)
        form_layout.addLayout(desc_layout)

        add_game_btn = QPushButton("Добавить игру")
        add_game_btn.clicked.connect(self.add_game)
        form_layout.addWidget(add_game_btn)

        layout.addLayout(form_layout)

        # Список игр
        self.games_list = QListWidget()
        layout.addWidget(QLabel("Список игр:"))
        layout.addWidget(self.games_list)

        self.tabs.addTab(tab, "Игры")

    def create_currency_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Форма добавления валюты
        form_layout = QVBoxLayout()

        # Выбор игры
        game_layout = QHBoxLayout()
        game_layout.addWidget(QLabel("Выберите игру:"))
        self.currency_game_combo = QComboBox()
        game_layout.addWidget(self.currency_game_combo)
        form_layout.addLayout(game_layout)

        # Название валюты
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название валюты:"))
        self.currency_name_input = QLineEdit()
        name_layout.addWidget(self.currency_name_input)
        form_layout.addLayout(name_layout)

        # Цена за единицу
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("Цена за единицу:"))
        self.currency_price_input = QDoubleSpinBox()
        self.currency_price_input.setMinimum(0.01)
        self.currency_price_input.setMaximum(9999.99)
        price_layout.addWidget(self.currency_price_input)
        form_layout.addLayout(price_layout)

        add_currency_btn = QPushButton("Добавить валюту")
        add_currency_btn.clicked.connect(self.add_currency)
        form_layout.addWidget(add_currency_btn)

        layout.addLayout(form_layout)

        # Список валют для выбранной игры
        self.currencies_list = QListWidget()
        layout.addWidget(QLabel("Валюты в игре:"))
        layout.addWidget(self.currencies_list)

        # Обновляем список игр при переключении
        self.currency_game_combo.currentTextChanged.connect(self.update_currencies_list)

        self.tabs.addTab(tab, "Валюты")

    def create_user_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Форма добавления пользователя
        form_layout = QVBoxLayout()

        # ID пользователя
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel("ID пользователя:"))
        self.user_id_input = QSpinBox()
        self.user_id_input.setMinimum(1)
        self.user_id_input.setMaximum(999999)
        id_layout.addWidget(self.user_id_input)
        form_layout.addLayout(id_layout)

        # Имя пользователя
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Имя пользователя:"))
        self.user_name_input = QLineEdit()
        name_layout.addWidget(self.user_name_input)
        form_layout.addLayout(name_layout)

        # Email
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("Email:"))
        self.user_email_input = QLineEdit()
        email_layout.addWidget(self.user_email_input)
        form_layout.addLayout(email_layout)

        add_user_btn = QPushButton("Добавить пользователя")
        add_user_btn.clicked.connect(self.add_user)
        form_layout.addWidget(add_user_btn)

        layout.addLayout(form_layout)

        # Список пользователей
        self.users_list = QListWidget()
        layout.addWidget(QLabel("Список пользователей:"))
        layout.addWidget(self.users_list)

        self.tabs.addTab(tab, "Пользователи")

    def create_payment_method_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Форма добавления способа оплаты
        form_layout = QVBoxLayout()

        # Название способа
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название способа оплаты:"))
        self.payment_method_name_input = QLineEdit()
        name_layout.addWidget(self.payment_method_name_input)
        form_layout.addLayout(name_layout)

        # Детали
        details_layout = QVBoxLayout()
        details_layout.addWidget(QLabel("Детали:"))
        self.payment_method_details_input = QTextEdit()
        self.payment_method_details_input.setMaximumHeight(100)
        details_layout.addWidget(self.payment_method_details_input)
        form_layout.addLayout(details_layout)

        add_payment_method_btn = QPushButton("Добавить способ оплаты")
        add_payment_method_btn.clicked.connect(self.add_payment_method)
        form_layout.addWidget(add_payment_method_btn)

        layout.addLayout(form_layout)

        # Список способов оплаты
        self.payment_methods_list = QListWidget()
        layout.addWidget(QLabel("Способы оплаты:"))
        layout.addWidget(self.payment_methods_list)

        self.tabs.addTab(tab, "Способы оплаты")

    def create_purchase_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Форма совершения покупки
        form_layout = QVBoxLayout()

        # Выбор пользователя
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Пользователь:"))
        self.purchase_user_combo = QComboBox()
        user_layout.addWidget(self.purchase_user_combo)
        form_layout.addLayout(user_layout)

        # Выбор игры
        game_layout = QHBoxLayout()
        game_layout.addWidget(QLabel("Игра:"))
        self.purchase_game_combo = QComboBox()
        game_layout.addWidget(self.purchase_game_combo)
        form_layout.addLayout(game_layout)

        # Выбор валюты
        currency_layout = QHBoxLayout()
        currency_layout.addWidget(QLabel("Валюта:"))
        self.purchase_currency_combo = QComboBox()
        currency_layout.addWidget(self.purchase_currency_combo)
        form_layout.addLayout(currency_layout)

        # Количество
        amount_layout = QHBoxLayout()
        amount_layout.addWidget(QLabel("Количество:"))
        self.purchase_amount_input = QSpinBox()
        self.purchase_amount_input.setMinimum(1)
        self.purchase_amount_input.setMaximum(9999)
        amount_layout.addWidget(self.purchase_amount_input)
        form_layout.addLayout(amount_layout)

        # Способ оплаты
        payment_method_layout = QHBoxLayout()
        payment_method_layout.addWidget(QLabel("Способ оплаты:"))
        self.purchase_payment_method_combo = QComboBox()
        payment_method_layout.addWidget(self.purchase_payment_method_combo)
        form_layout.addLayout(payment_method_layout)

        make_purchase_btn = QPushButton("Совершить покупку")
        make_purchase_btn.clicked.connect(self.make_purchase)
        form_layout.addWidget(make_purchase_btn)

        layout.addLayout(form_layout)

        # История покупок для выбранного пользователя
        self.purchases_list = QListWidget()
        layout.addWidget(QLabel("История покупок:"))
        layout.addWidget(self.purchases_list)

        # Обновляем списки при изменении выбора
        self.purchase_user_combo.currentTextChanged.connect(self.update_purchases_list)
        self.purchase_game_combo.currentTextChanged.connect(self.update_purchase_currencies)

        self.tabs.addTab(tab, "Покупки")

    def create_view_data_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Общая статистика
        stats_layout = QVBoxLayout()
        self.total_games_label = QLabel(f"Всего игр: 0")
        stats_layout.addWidget(self.total_games_label)

        self.total_users_label = QLabel(f"Всего пользователей: 0")
        stats_layout.addWidget(self.total_users_label)

        self.total_payment_methods_label = QLabel(f"Всего способов оплаты: 0")
        stats_layout.addWidget(self.total_payment_methods_label)

        layout.addLayout(stats_layout)

        # Кнопка обновления данных
        refresh_btn = QPushButton("Обновить данные")
        refresh_btn.clicked.connect(self.update_view_data)
        layout.addWidget(refresh_btn)

        self.tabs.addTab(tab, "Обзор данных")

    def add_game(self):
        name = self.game_name_input.text().strip()
        description = self.game_desc_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название игры!")
            return

        if name in self.games:
            QMessageBox.warning(self, "Ошибка", "Игра с таким названием уже существует!")
            return

        game = Game(name, description)
        self.games[name] = game

        # Обновляем списки
        self.update_games_list()
        self.currency_game_combo.addItem(name)
        self.purchase_game_combo.addItem(name)

        # Очищаем поля ввода
        self.game_name_input.clear()
        self.game_desc_input.clear()

        QMessageBox.information(self, "Успех", "Игра добавлена успешно!")

    def add_currency(self):
        game_name = self.currency_game_combo.currentText()
        currency_name = self.currency_name_input.text().strip()
        price = self.currency_price_input.value()

        if not game_name:
            QMessageBox.warning(self, "Ошибка", "Выберите игру!")
            return

        if not currency_name:
            QMessageBox.warning(self, "Ошибка", "Введите название валюты!")
            return

        game = self.games[game_name]

        if currency_name in game.currencies:
            QMessageBox.warning(self, "Ошибка", "Валюта с таким названием уже существует в этой игре!")
            return

        currency = Currency(currency_name, price)
        game.add_currency(currency)

        # Обновляем список валют
        self.update_currencies_list()

        # Очищаем поля ввода
        self.currency_name_input.clear()
        self.currency_price_input.setValue(0.01)

        QMessageBox.information(self, "Успех", "Валюта добавлена успешно!")

    def add_user(self):
        user_id = self.user_id_input.value()
        username = self.user_name_input.text().strip()
        email = self.user_email_input.text().strip()

        if not username:
            QMessageBox.warning(self, "Ошибка", "Введите имя пользователя!")
            return

        if not email:
            QMessageBox.warning(self, "Ошибка", "Введите email!")
            return

        if user_id in self.users:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким ID уже существует!")
            return

        user = User(user_id, username, email)
        self.users[user_id] = user

        # Обновляем списки
        self.update_users_list()
        self.purchase_user_combo.addItem(username, userData=user_id)

        # Очищаем поля ввода
        self.user_name_input.clear()
        self.user_email_input.clear()
        self.user_id_input.setValue(1)

        QMessageBox.information(self, "Успех", "Пользователь добавлен успешно!")

    def add_payment_method(self):
        method_name = self.payment_method_name_input.text().strip()
        details = self.payment_method_details_input.toPlainText().strip()

        if not method_name:
            QMessageBox.warning(self, "Ошибка", "Введите название способа оплаты!")
            return

        if method_name in self.payment_methods:
            QMessageBox.warning(self, "Ошибка", "Способ оплаты с таким названием уже существует!")
            return

        payment_method = PaymentMethod(method_name, details)
        self.payment_methods[method_name] = payment_method

        # Обновляем списки
        self.update_payment_methods_list()
        self.purchase_payment_method_combo.addItem(method_name)

        # Очищаем поля ввода
        self.payment_method_name_input.clear()
        self.payment_method_details_input.clear()

        QMessageBox.information(self, "Успех", "Способ оплаты добавлен успешно!")

    def make_purchase(self):
        user_id = self.purchase_user_combo.currentData()
        game_name = self.purchase_game_combo.currentText()
        currency_name = self.purchase_currency_combo.currentText()
        amount = self.purchase_amount_input.value()
        payment_method_name = self.purchase_payment_method_combo.currentText()

        if not user_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя!")
            return

        if not game_name:
            QMessageBox.warning(self, "Ошибка", "Выберите игру!")
            return

        if not currency_name:
            QMessageBox.warning(self, "Ошибка", "Выберите валюту!")
            return

        if not payment_method_name:
            QMessageBox.warning(self, "Ошибка", "Выберите способ оплаты!")
            return

        try:
            user = self.users[user_id]
            game = self.games[game_name]
            currency = game.currencies[currency_name]
            payment_method = self.payment_methods[payment_method_name]

            purchase = Purchase(user, game, currency, amount, payment_method)
            purchase.confirm_purchase()

            # Обновляем список покупок
            self.update_purchases_list()

            QMessageBox.information(self, "Успех", "Покупка совершена успешно!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при совершении покупки: {str(e)}")

    def update_games_list(self):
        self.games_list.clear()
        for game in self.games.values():
            self.games_list.addItem(str(game))

    def update_currencies_list(self):
        self.currencies_list.clear()
        game_name = self.currency_game_combo.currentText()

        if game_name and game_name in self.games:
            game = self.games[game_name]
            for currency in game.currencies.values():
                self.currencies_list.addItem(str(currency))

    def update_users_list(self):
        self.users_list.clear()
        for user in self.users.values():
            self.users_list.addItem(str(user))

    def update_payment_methods_list(self):
        self.payment_methods_list.clear()
        for method in self.payment_methods.values():
            self.payment_methods_list.addItem(str(method))

    def update_purchases_list(self):
        self.purchases_list.clear()
        user_id = self.purchase_user_combo.currentData()

        if user_id and user_id in self.users:
            user = self.users[user_id]
            for purchase in user.purchase_history.values():
                self.purchases_list.addItem(str(purchase))

    def update_purchase_currencies(self):
        self.purchase_currency_combo.clear()
        game_name = self.purchase_game_combo.currentText()

        if game_name and game_name in self.games:
            game = self.games[game_name]
            for currency_name in game.currencies:
                self.purchase_currency_combo.addItem(currency_name)

    def update_view_data(self):
        self.total_games_label.setText(f"Всего игр: {Game.get_total_games()}")
        self.total_users_label.setText(f"Всего пользователей: {len(self.users)}")
        self.total_payment_methods_label.setText(f"Всего способов оплаты: {len(self.payment_methods)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Установка шрифта для всего приложения
    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
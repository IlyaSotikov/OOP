class Parent:
    def __init__(self, name):
        self.name = name
        print(f" Имя: {self.name}")

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age
        print(f"Возраст: {self.age}")

child = Child("Алиса", 25)

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} издает звук.")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def speak(self):
        print(f"{self.name} скажи: Гав!")

    def demonstrate(self, condition):
        if condition:
            super().speak()
            self.speak()
        else:
            self.speak()
            super().speak()


dog = Dog("Арес", "Немецкая овчарка")
dog.demonstrate(True)
dog.demonstrate(False)
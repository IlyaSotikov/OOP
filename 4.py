class BaseClass:
    def __init__(self, value):
        self._protected_attribute = value

    def display(self):
        print(f"Защищенный атрибут: {self._protected_attribute}")

class DerivedClass(BaseClass):
    def __init__(self, value):
        super().__init__(value)

    def modify_protected_attribute(self, new_value):
        self._protected_attribute = new_value

    def display(self):
        super().display()
        print(f"Мод защищенный атрибу: {self._protected_attribute}")


base = BaseClass(100)
base.display()

derived = DerivedClass(200)
derived.display()
derived.modify_protected_attribute(300)
derived.display()

class CustomError(Exception):
    pass

class SpecificError(CustomError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class AnotherError(CustomError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def process_data(value):
    try:
        if value < 0:
            raise SpecificError("Значение не может быть отрицательным!")
        elif value > 100:
            raise AnotherError("Значение превышает допустимый предел!")
        else:
            print(f"Обработано значение: {value}")
    except SpecificError as e:
        print(f"Ошибка: {e}")
    except AnotherError as e:
        print(f"Ошибка: {e}")
    except CustomError as e:
        print(f"Произошла ошибка: {e}")
    finally:
        print("Обязательный код выполнен.")

process_data(150)
process_data(-5)
process_data(50)

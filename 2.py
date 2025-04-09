import pickle
import shelve
import json

# Власний тип винятку
class InvalidWineDataError(Exception):
    pass

class Wine:
    def __init__(self, brand, description, strength):
        assert 0 <= strength <= 100, "Міцність має бути у межах від 0 до 100%"
        self.brand = brand
        self.description = description  # Приклад: "біле сухе"
        self.strength = strength  # У відсотках

    def __str__(self):
        return f"{self.brand} ({self.description}) - {self.strength}%"

    def __repr__(self):
        return f"Wine('{self.brand}', '{self.description}', {self.strength})"

    def matches_type(self, wine_type):
        return wine_type in self.description

    def __lt__(self, other):
        return self.strength < other.strength


class BottledWine(Wine):
    def __init__(self, brand, description, strength, volume, container):
        super().__init__(brand, description, strength)
        if container not in ["скло", "тетрапак"]:
            raise InvalidWineDataError("Невірний тип тари. Можна тільки 'скло' або 'тетрапак'.")
        if volume <= 0:
            raise InvalidWineDataError("Обʼєм повинен бути більше нуля.")
        self.volume = volume  # У літрах
        self.container = container

    def __str__(self):
        return f"{super().__str__()}, {self.volume}л, {self.container}"

    def __repr__(self):
        return f"BottledWine('{self.brand}', '{self.description}', {self.strength}, {self.volume}, '{self.container}')"

    def change_container(self):
        self.container = "тетрапак" if self.container == "скло" else "скло"

    def __truediv__(self, factor):
        if factor <= 0:
            raise ValueError("Коефіцієнт поділу має бути більше нуля")
        return BottledWine(self.brand, self.description, self.strength, self.volume / factor, self.container)


class WineCollection:
    def __init__(self):
        self.wines = []

    def add_wine(self, wine):
        if isinstance(wine, BottledWine):
            self.wines.append(wine)

    def display_wines(self):
        for wine in sorted(self.wines, reverse=True):
            print(wine)

    def total_volume_by_color(self):
        volumes = {"біле": 0.0, "червоне": 0.0, "рожеве": 0.0}
        for wine in self.wines:
            for color in volumes:
                if color in wine.description:
                    volumes[color] += wine.volume
        return volumes

    def save_pickle(self, filename):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.wines, file)
        except Exception as e:
            print("Помилка при збереженні у pickle:", e)

    def load_pickle(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.wines = pickle.load(file)
        except FileNotFoundError:
            print("Файл pickle не знайдено")
        except Exception as e:
            print("Помилка завантаження pickle:", e)

    def save_shelve(self, filename):
        try:
            with shelve.open(filename) as db:
                db['wines'] = self.wines
        except Exception as e:
            print("Помилка при роботі з shelve:", e)

    def load_shelve(self, filename):
        try:
            with shelve.open(filename) as db:
                self.wines = db.get('wines', [])
        except Exception as e:
            print("Помилка завантаження з shelve:", e)

    def save_text(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(repr(self.wines))
        except Exception as e:
            print("Помилка при збереженні тексту:", e)

    def load_text(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.wines = eval(file.read())
        except SyntaxError:
            print("Синтаксична помилка при зчитуванні тексту")
        except Exception as e:
            print("Помилка завантаження тексту:", e)



# Демонстрація з обробкою винятків
print("\n Спроба створити вина: ")
try:
    A = BottledWine("Аліготе", "біле сухе", 10.5, 0.75, "скло")
    B = BottledWine("Каберне", "червоне напівсолодке", 12.0, 0.7, "тетрапак")  # Міцність 
    print(A)
    print(B)
except AssertionError as ae:
    print("AssertionError:", ae)
except InvalidWineDataError as ive:
    print("InvalidWineDataError:", ive)
else:
    print("Успішно створено вина")
finally:
    print("Блок finally: завершення спроби створення вин")

print("\n Перевірка ділення об’єму: ")
try:
    C = BottledWine("Мерло", "червоне сухе", 13.0, 0.75, "скло")
    D = C / 2  
    print(D)
except ValueError as ve:
    print("ValueError:", ve)

print("\n Програма продовжує працювати.")


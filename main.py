
class Point: # класс будет хранить в себе информацию о точках на поле (плоскости в системе координат "х" и "у")
    def __init__(self, x, y): # атрибутика со значениями
        self.x = x
        self.y = y
# для сравнения точек (==) и вывода информации будем переопределять методами __eq__ и __repr__ внутри класса:
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y}'

# Классы для "отлова" исключений
class BoardException(Exception): # создаем дочерний класс от встроенного (со встроенными модулями) отлова общих исключений
    pass

class BoardWrongShipException(BoardException): # для отлова исключений при размещении кораблей на поле
    pass

class BoardOutException(BoardException): # дочерний класс для отлова пользовательского исключения
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы поля!"

class BoardUsedException(BoardException): # дочер. класс для отлова пользоват. исключения
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"


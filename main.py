
class Point: # класс будет хранить в себе информацию о точках на поле (плоскости в системе координат "х" и "у")
    def __init__(self, x, y): # атрибутика со значениями
        self.x = x
        self.y = y
# для сравнения точек (==) и вывода информации будем переопределять методами __eq__ и __repr__ внутри класса:
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y}'


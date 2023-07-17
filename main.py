
class Point: # класс будет хранить в себе информацию о точках на поле (плоскости в системе координат "х" и "у")
    def __init__(self, x, y): # атрибутика со значениями
        self.x = x
        self.y = y
# для сравнения точек (==) и вывода информации будем переопределять методами __eq__ и __repr__ внутри класса:
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

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

class Ship:
    def __init__(self, ship_head, l, o): # первая точка (нос) корабля, l и o - длина и ориентация корабля на поле
        self.ship_head = ship_head
        self.l = l
        self.o = o
        self.lives = l

    @property # для создания виртуального "поля" класса Ship
    def points(self): # метод который будет хранить все точки корабля
        ship_points = [] # пустой список для хранения точек корабля
        for i in range(self.l):
            cur_x = self.ship_head.x
            cur_y = self.ship_head.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_points.append(Point(cur_x, cur_y))

        return  ship_points

    def shoot(self, fire):
        return fire in self.points

s = Ship(Point(1, 3), 4, 1) # проверка создания крейсера по вертикали
print(s.points) # [[Point(1, 3), Point(1, 4), Point(1, 5), Point(1, 6)]
print(s.shoot(Point(1, 4))) # True
print(s.shoot(Point(2, 4))) # False
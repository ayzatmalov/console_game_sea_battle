
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

# s = Ship(Point(1, 3), 4, 1) # проверка создания крейсера по вертикали
# print(s.points) # [[Point(1, 3), Point(1, 4), Point(1, 5), Point(1, 6)]
# print(s.shoot(Point(1, 4))) # True
# print(s.shoot(Point(2, 4))) # False

# создание игрового поля 6 х 6
class Board:
    def __init__(self, hid = False, size = 6):
        self.size = size # значение размера (по умолчанию = 6)
        self.hid = hid # скрывать поле (по умолчанию - нет)
        self.count = 0 # счетчик для потопленных кораблей
        self.field = [ ['O'] * size for _ in range(size) ] # визуализация клеток и состояния поля (по умолчанию в каждой клетке "0" - т.е. клетка пока пустая)
        self.busy = [] # атрибут busy, в котором будем хранить "занятые" точки (там где есть вирт корабль, и там куда уже стреляли)
        self.ships = [] # атрибут для списка кораблей пользователя (которые будут добавляться с помощью метода add_ship)

    def __str__(self): # "отрисовка" корабля на поле
        res = ''
        res +=  '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field): # цикл прохода по строчкам игрового поля (где берем индекс строчки при помощи встроенной фукнции enumerate)
            res += f'\n{i + 1} | ' + ' | '.join(row) + ' |' # вывод номера строчки и клетки данной строчки
        if self.hid: # изменение параметра hid, если он true
            res = res.replace('■', 'O')
        return res

    def out(self, p): # метод для проверки находится ли точка за пределами игрового поля
        return not ((0 <= p.x < self.size) and (0 <= p.y < self.size)) # инлайновое отрицание условия нахождения точки в пределах поля (от 0 до size)

    # создадим метод для "обвода" созданного коробля (клетки которые будут busy)
    def contour(self, ship, verb = False): # для чего вводим список-условие сдвигов от выбранной пользователем точки (она в этом условие будет с относительными координатами x, y = 0, 0)
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for p in ship.points:
            for px, py in near:
                cur = Point(p.x + px, p.y + py)
                self.field[cur.x][cur.y] = '.'

b = Board()
b.contour(Ship(Point(2, 1), 4, 1))
print(b)
#   | 1 | 2 | 3 | 4 | 5 | 6 |
# 1 | O | O | O | O | O | O |
# 2 | . | . | . | . | . | . |
# 3 | . | . | . | . | . | . |
# 4 | . | . | . | . | . | . |
# 5 | O | O | O | O | O | O |
# 6 | O | O | O | O | O | O |

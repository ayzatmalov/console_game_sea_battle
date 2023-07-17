from random import randint
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
        self.size = size # значение размера (по умолчанию = 9)
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

    def add_ship(self, ship): # метод добавления корабля на игровое поле

        for p in ship.points: # цикл для проверки, того что точки корабля не выходят за пределы игрового поля, а также то что они не пересекают уже занятые точки
            if self.out(p) or p in self.busy:
                raise BoardWrongShipException()

        for p in ship.points: # цикл для того чтобы обозначить наш корабль на игровом поле с помощью "■"
            self.field[p.x][p.y] = '■'
            self.busy.append(p) # добавим точки коробля и список занятых точек

        self.ships.append(ship) # добавляем корабль в список кораблей
        self.contour(ship) # добавляем контур в список контуров кораблей

    # создадим метод для "обвода" созданного коробля (клетки которые будут busy)
    def contour(self, ship, verb = False): # для чего вводим список-условие сдвигов от выбранной пользователем точки (она в этом условие будет с относительными координатами x, y = 0, 0)
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0 , 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for p in ship.points:
            for px, py in near:
                cur = Point(p.x + px, p.y + py)
                if not (self.out(cur)) and cur not in self.busy: # добавили проверку, что точка не выходит за пределы доски и что точка еще не занята
                    if verb: # параметр с помощью которого будем определять нужно ли ставить "точки" вокруг корабля
                        self.field[cur.x][cur.y] = '.' # если все ок, то "ставим" (виртуально) в клетку "точку"
                    self.busy.append(cur) # если точка не выходит за пределы и она ранее не занята, то добавляем ее в список занятых

    def fire(self, p):
        if self.out(p): # проверка выходит ли заданная при выстреле точка за пределы поля, и при необ-ти генерация исключения
            raise BoardOutException
        if p in self.busy: # проверка занята ли клетка точкой, если да то генерируем исключение
            raise BoardUsedException
        self.busy.append(p) # добавляем точку в список busy (как отстреленную), если еще не было по ней огня

        for ship in self.ships: # цикл проверки попадания
            if p in ship.shoot(p): # если попали...
                ship.lives -= 1 # то, уменьшаем кол-во клеток для корабля на 1
                self.field[p.x][p.y] = 'X' # и ставим X вместо ■
                if ship.lives == 0: # если корабль полностью потоплен, то...
                    self.count += 1 # то прибавляем единицу к счетчику
                    self.contour(ship, verb=True) # очерчиваем контур подбитого корабля
                    print('Корабль потоплен!') # выводим сообщение о потоплении корабля
                    return False # возвращаем false, что остановить огонь по данному кораблю
                else: # в противном случае...
                    print('Корабль ранен!') # выводим сообщение о ранении, и...
                    return True # возвращаем ход, чтобы продолжить огонь по данному кораблю
        self.field[p.x][p.y] = '.' # если в ходе огня попадания не было по кораблю, то заменяем в клетке "О" на "точку"
        print('Мимо!') # выводим сообщение о непопадании по кораблю
        return False # возвращаем false, что остановить продолжение огня

    def begin(self):
        self.busy = []  # обнуление списка busy перед началом игры (до начала игры он был нужен только чтобы корректно расставить корабли)
                        # а в ходе игры у него новая роль = хранить точки по которым ведется огонь и точки контуров потопленных кораблей

class Player: # класс с общими атрибутами и методами для классов (игроков) User и AI (artificial intelligence)
    def __init__(self, board, enemy): # конструктор содержащий два поля
        self.board = board # значение поля игрока
        self.enemy = enemy # значение поля противника
    def ask(self): # определяем метод ask, потребуется для использования в дочерних классах от Player (User и AI)
        raise NotImplementedError() # на случай прямого вызова метода генерация исключения (как защита от дурака)
    def move(self):
        while True: # создаем бесконечный цикл в котором
            try:
                target = self.ask() # запрос произвести огонь
                repeat = self.enemy.fire(target) # выполнение выстрела
                return repeat # если выстрел прошел, то возвращаем новый ход или переход (в зависимости от события)
            except BaseException as e: # если огонь нанесен неверно, то обрабатываем исключение и продолжаем выполнение цикла
                print(e) # печатаем уведомление в зависимости от сгенерированного исключения

class AI(Player): # дочерний класс Игрок-компьютер
    def ask(self):
        p = Point(randint(0, 8), randint(0, 8)) # генерация случайных точек от 0 до 8, для чего импор-м функ-ю randint из библиотеки random
        print(f'Ход компьютера: {p.x + 1} {p.y + 1}')
        return p

class User(Player): # дочерний класс Игрок-пользователь
    def ask(self):
        while True:
            coords = input('Ваш ход: ').split() # запрос координат
            if len(coords) != 2: # проверка правильности ввода 2-х координат
                print('Введите 2 координаты!')
                continue
            x, y = coords

            if not(x.isdigit()) or not(y.isdigit()): # проверка, что координаты - это числа
                print('Введите числа!')
                continue
            x, y = int(x), int(y)
            return Point(x-1, y-1) # возвращаем с учетом индексации размещения точек на поле

class Game:
    def try_board(self): # создание поля
        lens = [3, 2, 2, 1, 1, 1, 1] # список кораблей и их длинной
        board = Board(size = self.size) # генерируем доску в соответствии с параметрами заданными в классе Board
        attempts = 0 # счетчик для определения количества попыток расстановки кораблей на поле
        for l in lens:
            while True: # бесконечный цикл расстановки кораблей на поле
                attempts += 1
                if attempts > 2000: # лимит попыток, если условие верно, то...
                    return None # возвращаем None
                ship = Ship(Point(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship) # если корабль успешно расположен на поле, то...
                    break # принудительно завершаем
                except BoardWrongShipException: # если генерируется исключение, то запускаем цикл еще раз
                    pass
        board.begin() # после того как мы разместили на доске все корабли из списка lens, возвращаем поле чтобы подготовить его к игре
        return board

    def random_board(self): # метод для гарантированного размещения кораблей на доске (если в методе try_board был достигнут лимит)
        board = None
        while board is None:
            board = self.try_board()
        return board

g = Game()
g.size = 6
print(g.try_board())
#   | 1 | 2 | 3 | 4 | 5 | 6 |
# 1 | ■ | O | O | ■ | ■ | O |
# 2 | O | O | O | O | O | O |
# 3 | ■ | O | ■ | O | ■ | O |
# 4 | ■ | O | O | O | O | O |
# 5 | O | O | ■ | ■ | ■ | O |
# 6 | ■ | O | O | O | O | O |

from random import randint


class Dot:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __eq__(self, other):
        return self.x==other.x and self.y==other.y


    def __repr__(self):
        return f"({self.x},{self.y})"

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы доски!"

class BoaradUsedException(BoardException):
    def __str__(self):
        return "Вы уже совершали такой ход"

class BoardBusyException(BoardException):
    pass

class BoardWrongShipException(BoardException):
    def __str__(self):
        return "Рядом стоит другой корабль"

class Ship:
    def __init__(self, bow, l, o):
        self.bow=bow
        self.l=l
        self.o=o
        self.lives = self.l

    @property
    def dots(self):
        ship_dots = []

        for i in range(self.l):
            cur_x=self.bow.x
            cur_y=self.bow.y

            if self.o==0:
                cur_x +=i
            elif self.o==1:
                cur_y +=i

            ship_dots.append(Dot(cur_x,cur_y))
        return ship_dots


    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self,hid=False, size=6):
        self.size=size
        self.hid=hid

        self.count=0

        self.field=[["O"]*size for _ in range(size)]

        self.busy=[]
        self.ships=[]

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y]="*"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self,ship,verb = False):
        near = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for d in ship.dots:
            for dx,dy in near:
                cur = Dot(d.x+dx,d.y+dy)
                if not(self.out(cur)) and cur not in self.busy and not cur in ship.dots:
                    if verb:
                        self.field[cur.x][cur.y]="."
                    self.busy.append(cur)
    def __str__(self):
        res = ""
        res+= " | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res+=f"\n{i+1}| "+" | ".join(row)+" | "

        if self.hid:
            res=res.replace("*","O")
        return res

    def out(self,d):
        return not((0<=d.x<self.size) and (0<=d.y<self.size))

    def shot(self,d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoaradUsedException()
        for ship in self.ships:
            self.busy.append(d)
            if d in ship.dots:
                ship.lives -=1
                self.field[d.x][d.y] = 'X'
                if ship.lives ==0:
                    self.count +=1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    if self.count == 7:
                        return False
                    else:
                        return True
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."

        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

class Player:
    board: object

    def __init__(self,board,enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                if not(repeat):
                    break
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        d= Dot(randint(0,5), randint(0,5))
        print (f'Ход компьютера',d)
        return d

class User(Player):
    def ask(self):
        while True:
            coords = input("Ваш ход: ")
            r = [i for i in coords if i.isdigit()]

            if len(r) !=2:
                print(" Введите 2 координаты! ")
                continue

            x,y=r
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue

            x,y=int(x),int(y)

            return Dot(x-1,y-1)

class Geme:
    def __init__(self,size = 6,):
        self.size=size
        co = self.random_board()
        co.hid=True

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def USER_board(self):
        board = None
        while board is None:
            board = self.pl_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def pl_place(self):
        Lens=[3, 2, 2, 1, 1, 1, 1]
        board = Board()
        for i in Lens:
            while True:
                coor=input(f"Укажите координату начала {i}-палубного корабля  ")
                r = [i for i in coor if i.isdigit()]
                if len(r) != 2:
                    print(" Введите 2 координаты! Пример: 1 2 ")
                    continue
                else:
                    x, y = r
                    x, y = int(x), int(y)
                    Dot(x-1,y-1)

                    while True:
                        if i != 1:
                            b=input("Укажите направление корабля: 1 - вниз, 2 - в право  ")
                            r_=int(b) if b.isdigit() else False
                            if not r_:
                                print("Введите число!")
                                continue
                            if 0 < r_ < 3:
                                r_ = r_ - 1
                                break
                            else:
                                continue
                        else:
                            break


                    ship = Ship(Dot(x-1,y-1), i, r_,)
                    try:
                        board.add_ship(ship)
                        print(board)
                        break
                    except BoardWrongShipException:
                        print("Неправильное расположение коробля \n рядом стоит другой корабль\n или он выходит за пределы поля")
                        continue

        board.begin()
        return board

    def res_(self):
        rec = {}
        for i, row in enumerate(self.us.board.field):
            rec[i]=row
        for i, row in enumerate(self.ai.board.field):
            r=rec[i]
            s=[]
            b=[]

            for j in row:
                if j == '*':
                    b.append('O')
                else:
                    b.append(j)
            s.append(r)
            s.append(b)
            rec[i]=s

        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |      | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i in range(6):
            a,b=rec[i]
            res+=f"\n{i + 1} | "+" | ".join(b)+ " |    "+f"{i + 1} | "+" | ".join(a)+ " | "

        return res

    def greet(self):
        print("--------------------")
        print("  Приветствую Вас   ")
        print("      в игре        ")
        print("    Морской бой!     ")
        print("--------------------")
        print(" Формат ввода: x y  ")
        print(" x - номер строки   ")
        print(" y - номер столбца  ")
        print("--------------------")


    def greet_start(self):
        print("   Для начала игры   ")
        print("  расставьте корабли ")
        print('(Параметр "1" или "2")')
        print("   и начните игру   ")
        print('   (Параметр "3")   ')
        print("    1 - Автоматическая расстановка кораблей игрока")
        print("    2 - Самостоятельная расстановка кораблей игрока")
        print("    3 - Начать игру")
        print("    4 - Выход")
        print("----------------------")
        while True:
            k=input("Введите параметр:  ")
            k=int(k) if k.isdigit() else False
            if k:
                if 1<= k <=4:
                    print(k)
                    self.play_=k
                    break
                else:
                    print("Введен не корректный параметр")
            else:
                print("Ведите число!")


    def loop(self):

        num=0
        while True:
            print('-' * 58)
            print("    Корабли компьютера:                Ваши корабли:")
            print(self.res_())
            if num%2 ==0:
                print('-'*20)
                print("Ходит пользователь!")
                #self.us.move()
                while True:
                    try:
                        target = self.us.ask()
                        repeat = self.us.enemy.shot(target)
                        print(self.res_())
                        if not (repeat):
                            break
                    except BoardException as e:
                        print(e)
            elif num%2==1:
                print("-"*20)
                print("Ходит компьютер!")
                self.ai.move()

            if self.ai.board.count ==7 :
                print("-"*20)
                print("Игрок выиграл!")
                print("----------------------")
                break
            if self.us.board.count==7:
                print("-" * 20)
                print("Компьютер выиграл!")
                print("----------------------")
                break
            num +=1

    def start(self):
        self.greet()
        board = Board()
        print(board)
        while True:
            self.greet_start()
            if self.play_==1:
                co = self.random_board()
                pl = self.random_board()
                self.ai = AI(co, pl)
                self.us = User(pl, co)
                print("    Корабли компьютера:                Ваши корабли:")
                print(self.res_())

            elif self.play_==2:
                pl=self.USER_board()
                co = self.random_board()
                self.ai = AI(co, pl)
                self.us = User(pl, co)
                print("    Корабли компьютера:                Ваши корабли:")
                print(self.res_())

            elif self.play_==3:
                self.loop()
            elif self.play_==4:
                print("_____ До встречи в игре! _____")
                break

g = Geme()
g.start()

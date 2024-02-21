import keyboard
import time
import os
import random

# Глобальные переменные
global Game, score, gone
Game = True
score = 0
gone = 0
Ant_Eater, Ant_Hill, Ant, Grass, Stone = '☺', '▲', '¤', '░', '█'

size = 10
X = Y = size // 2

Field = []
for i in range(size):
    Field.append([])
    for j in range(size):
        Field[i].append(Grass)

Field[Y][X] = Ant_Eater

for i in range(random.randint(5, 10)):
    rnd_X = random.randint(0, size - 1)
    rnd_Y = random.randint(0, size - 1)
    Field[rnd_Y][rnd_X] = Stone

anthills = []
for i in range(random.randint(2, 4)):
    anthills.append([])
    rnd_X = random.randint(3, size - 3)
    rnd_Y = random.randint(3, size - 3)
    rnd_N = random.randint(20, 100)
    anthills[i].append([rnd_X, rnd_Y, rnd_N])
    Field[rnd_Y][rnd_X] = Ant_Hill


def draw():
    # Очистка экрана и вывод текущего состояния поля
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Счет: ", score)
    print("Исчезло: ", gone)
    for i in range(size):
        for j in range(size):
            print(Field[i][j], end="")
        print()


def exit1():
    # Функция для выхода из игры
    global Game
    Game = False


def can_move(current_x, current_y, delta_x, delta_y):
    # Проверка, можно ли сделать ход в указанном направлении
    x = current_x + delta_x
    y = current_y + delta_y
    if (x < 0) or (y < 0) or (x >= size) or (y >= size):
        return False
    if (Field[y][x] == Stone) or (Field[y][x] == Ant_Hill) or (Field[y][x] == Ant_Eater):
        return False
    return True


def move_ant_eater(current_x, current_y, delta_x, delta_y):
    # Перемещение муравьеда в указанном направлении
    Field[current_y][current_x] = Grass
    global X, Y, score, gone
    X = current_x + delta_x
    Y = current_y + delta_y
    if Field[Y][X] == Ant:
        score += 1
    if X >= size or Y >= size or X > 10 or Y > 10:
        gone += 1
        Field[current_y][current_x] = Grass
    else:
        Field[Y][X] = Ant_Eater


def move_left():
    # Движение муравьеда влево
    if can_move(X, Y, -1, 0):
        move_ant_eater(X, Y, -1, 0)
        draw()


def move_right():
    # Движение муравьеда вправо
    if can_move(X, Y, 1, 0):
        move_ant_eater(X, Y, 1, 0)
        draw()


def move_up():
    # Движение муравьеда вверх
    if can_move(X, Y, 0, -1):
        move_ant_eater(X, Y, 0, -1)
        draw()


def move_down():
    # Движение муравьеда вниз
    if can_move(X, Y, 0, 1):
        move_ant_eater(X, Y, 0, 1)
        draw()


def spawn_ant():
    # Спавн муравья на случайной пустой клетке поля
    rnd_X = random.randint(0, size - 1)
    rnd_Y = random.randint(0, size - 1)
    if Field[rnd_Y][rnd_X] == Grass and rnd_X <= 10 and rnd_Y <= 10:
        Field[rnd_Y][rnd_X] = Ant


last_t = time.time()
keyboard.add_hotkey('left', move_left)
keyboard.add_hotkey('right', move_right)
keyboard.add_hotkey('up', move_up)
keyboard.add_hotkey('down', move_down)
keyboard.add_hotkey('esc', exit1)
while Game:
    t = time.time()
    if t - last_t > 2:
        draw()
        print(t)
        last_t = t
    if score < len(anthills):
        spawn_ant()
    else:
        Game = False
    time.sleep(1)

keyboard.unhook_all_hotkeys()

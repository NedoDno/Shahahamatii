import os
import sys
from random import randint

import pygame

pygame.init()
display_inf = pygame.display.Info()
size = w, h = display_inf.current_w, display_inf.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
state = 0  # Состояние программы: 0 - главное меню, 1 - игра, 2 - магазин
player = 1

statss = {'Победы': 0, 'Поражения': 0, 'Купленные_вещи': '[]', 'Деньги': 0}
file = open('data/stats.txt', 'r')

for i in file.readlines():
    statss[i.split(':')[0]] = i.split(':')[1]
statss['Купленные_вещи'] = [i[2:] for i in statss['Купленные_вещи'][1:-1].split(',')]
print(statss['Купленные_вещи'])


def render_text(screen, text, x, y, color):
    font = pygame.font.Font('16881.otf', 45)
    text = font.render(text, True, color)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


def exit(code):
    global statss
    file = open('data/stats.txt', 'w')
    res = ''
    for i in statss.keys():
        res += i + ':' + str(statss[i]) + '\n'
    file.write(res[:-1])
    file.close()
    sys.exit(0)


def window_of_warning(text, screen):
    global timer_on, timer, warning_text
    timer_on = True
    warning_text = 'YOU WILL FAIL. ARE YOU SURE?'
    pygame.draw.rect(screen, (50, 50, 50), (w // 2 - w // 10 * 3, h // 2 - h // 8 * 2.5, w // 10 * 6, h // 8 * 5))
    render_text(screen, text,
                w // 2,
                h // 2, (255, 255, 255))
    render_text(screen, str(timer // 10),
                w // 2,
                h // 2 + h // 8, (255, 255, 255))
    if timer == 0:
        warning_text = ''
        timer_on = False
        timer = 500


def KtoHoditBlin():
    global player
    if player == 1:
        pygame.draw.circle(screen, (14, 117, 86), (0, 0), 50)
    else:
        pygame.draw.circle(screen, (150, 26, 29), (0, 0), 50)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


class BoardNacl:
    def __init__(self):
        # Выбранная фигура
        self.select_figure = None
        global h, w
        # цвета и буквы
        self.colors = [(31, 0, 0), (235, 255, 241), (0, 90, 171), pygame.Color('#e60404')]
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        # настройки параметров доски относительно окна
        self.cell_size = h // 10
        self.left = w // 2 - 4 * self.cell_size
        self.top = self.cell_size
        self.points = []
        left = self.left
        cel_s = self.cell_size
        self.lightting_cell = []
        for i in range(9):
            self.points.append([])
            for j in range(9):
                self.points[-1].append((left + cel_s * j, self.top + i * self.cell_size))
            cel_s += 10
            left = w // 2 - 4 * cel_s

    def render_text(self, scrn, i):
        font = pygame.font.Font('16881.otf', 35)

        text = font.render(str(i + 1), True, pygame.Color('black'))
        text_x = self.left + i * self.cell_size + self.cell_size // 2 - text.get_width() // 2
        text_y = h // 2 - text.get_height() // 2 + -1 * (4 * self.cell_size + self.cell_size // 2)
        screen.blit(text, (text_x, text_y))

        text = font.render(str(i + 1), True, pygame.Color('black'))
        text_x = (w // 2 - 4 * (self.cell_size + 10 * 8)) + i * (self.cell_size + 10 * 8) + (
                self.cell_size + 10 * 8) // 2 - text.get_width() // 2
        text_y = h // 2 - text.get_height() // 2 + 1 * (4 * self.cell_size + self.cell_size // 2)
        screen.blit(text, (text_x, text_y))

        text2 = font.render(self.letters[i], True, pygame.Color('black'))
        text2_x = w // 2 - text2.get_width() // 2 + 1 * (
                4 * (self.cell_size + 10 * i) + (self.cell_size + 10 * 2) // 2) + 10
        text2_y = (1 + i) * self.cell_size + self.cell_size // 2 - text2.get_height() // 2
        screen.blit(text2, (text2_x, text2_y))

        text2 = font.render(self.letters[i], True, pygame.Color('black'))
        text2_x = w // 2 - text2.get_width() // 2 + -1 * (
                4 * (self.cell_size + 10 * i) + (self.cell_size + 10 * 2) // 2)
        text2_y = (1 + i) * self.cell_size + self.cell_size // 2 - text2.get_height() // 2
        screen.blit(text2, (text2_x, text2_y))

    def render(self, scrn):
        global h, w

        for i in range(8):
            self.render_text(scrn, i)
            for j in range(8):
                pygame.draw.polygon(scrn, self.colors[(i + j) % 2],
                                    (self.points[i][j], self.points[i + 1][j], self.points[i + 1][j + 1],
                                     self.points[i][j + 1]))

        pygame.draw.polygon(scrn, self.colors[0],
                            (self.points[0][0], self.points[0][-1], self.points[-1][-1],
                             self.points[-1][0]), 2)
        try:
            for i in self.lightting_cell:
                pygame.draw.polygon(scrn, self.colors[i[1]], i[0], 7)
        except:
            print('Клетка не выбрана')

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        a, b = None, None
        for i in range(8):
            for j in range(8):
                if ((self.points[i][j][0] <= x <= self.points[i + 1][j + 1][0]) and
                        (self.points[i][j][1] <= y <= self.points[i + 1][j + 1][1])):
                    a = i
                    b = j
        if a == None or b == None:
            return None
        return a, b

    def on_click(self, cell_coords):
        global level_map, player
        if not cell_coords is None:
            self.lightting_cell.clear()
            if not self.select_figure is None:
                if player == self.select_figure.color:
                    move = self.select_figure.move(cell_coords, self)
                    if move:
                        player = -player
                self.select_figure = None
            else:
                try:
                    light = level_map[cell_coords[0]][cell_coords[1]].get_go_att_cells()
                    self.select_figure = level_map[cell_coords[0]][cell_coords[1]]
                    for i in light:
                        self.lightting_cell.append(((self.points[i[0][0]][i[0][1]],
                                                     self.points[i[0][0]][i[0][1] + 1],
                                                     self.points[i[0][0] + 1][i[0][1] + 1],
                                                     self.points[i[0][0] + 1][i[0][1]]), i[1]))
                except:
                    pass

                # self.light_cell(cell_coords, 2)
        else:
            self.lightting_cell.clear()

    def light_cell(self, cell_coords, colr):
        self.lightting_cell.append(((
                                        self.points[cell_coords[0]][cell_coords[1]],
                                        self.points[cell_coords[0]][cell_coords[1] + 1],
                                        self.points[cell_coords[0] + 1][cell_coords[1] + 1],
                                        self.points[cell_coords[0] + 1][cell_coords[1]]), colr))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Pawn(pygame.sprite.Sprite):
    image_w = load_image('Pawn_elf.png')
    image_w = pygame.transform.scale(image_w,
                                     (int(((h // 5 - 20) / image_w.get_height())
                                          * image_w.get_width()), h // 5 - 20))
    image_b = load_image('Pawn_man.png')
    image_b = pygame.transform.scale(image_b,
                                     (int(((h // 5 - 20) / image_b.get_height()) * image_b.get_width()), h // 5 - 20))

    # Изменить
    def __str__(self):
        '''Возвращает букву, которая обозначает фигуру.
        Возвращает большую букву, если цвет белый, и маленькую - если чёрный'''
        return 'p'

    # Изменить
    def __init__(self, color, pos, all_sprites, board):
        '''Инициализирует фигуру'''
        # Вызов конструктора родительского класса
        super().__init__(all_sprites)
        # Присвоения цвета
        self.color = color
        # Присвоение картинки в зависимости от цвета
        if color == 1:
            self.image = Pawn.image_w
        else:
            self.image = Pawn.image_b

        self.cell = ''  # Координаты клетки, на которой стоит данная фигура
        self.move(pos, board)  # передвигаем фигуру на данную клетку

    # Не меняй
    def get_go_att_cells(self):
        '''Возвращает координаты клеток, куда может пойти фигура в формате:
                    ((координата_х, координата_у), цвет_выделения{значения: 2 - можно походить, 3 - можно съесть})'''
        points = []
        points.extend(self.get_go_coords())
        points.extend(self.get_attack_coords())
        return points

    # Изменить
    def get_attack_coords(self):
        '''Возвращает координаты клеток, куда может атаковать фигура в формате:
                            ((координата_х, координата_у), 3)'''
        attack_p = []  # Список клеток, которые может атаковать данная фигура

        # находим координаты клетки, которая теоритически может быть атакована
        if 0 <= self.cell[0] + 1 * self.color < 8 and 0 <= self.cell[1] + 1 * self.color < 8:
            attack_p.append(((self.cell[0] + 1 * self.color, self.cell[1] + 1 * self.color), 3))
        if 0 <= self.cell[0] - 1 * self.color < 8 and 0 <= self.cell[1] + 1 * self.color < 8:
            attack_p.append(((self.cell[0] - 1 * self.color, self.cell[1] + 1 * self.color), 3))

        # Исключаем клетки, в которых не содержится фигуры
        attack_p = [i for i in attack_p if
                    level_map[i[0][0]][i[0][1]].__class__.__name__ != 'Tile' and level_map[i[0][0]][
                        i[0][1]].color != self.color]

        return attack_p

    # Изменить
    def get_go_coords(self):
        '''Возвращает координаты клеток, куда может пойти фигура в формате:
                            ((координата_х, координата_у), 2)'''
        go_p = []  # список клеток, на которые фигура может пойти

        # находим координаты клетки, на которые фигура может пойти
        if 0 <= self.cell[1] + 1 * self.color < 8:
            go_p.append(((self.cell[0], self.cell[1] + 1 * self.color), 2))
        if (0 <= self.cell[1] + 2 * self.color < 8 and
                ((self.cell[1] == 1 and self.color == 1) or (self.cell[1] == 6 and self.color != 1))
                and level_map[self.cell[0]][self.cell[1] + 1 * self.color].__class__.__name__ == 'Tile'):
            go_p.append(((self.cell[0], self.cell[1] + 2 * self.color), 2))

        # Исключаем клетки, которые содержат фигуры или которые находятся за фигурами
        go_p = [i for i in go_p if level_map[i[0][0]][i[0][1]].__class__.__name__ == 'Tile']
        return go_p

    # Не меняй
    def eat(self, pos, board):
        '''Данная фигура съедает фигуру, которая находится на позиции pos, если она там есть'''
        if pos != (-5, -5):
            if len(level_map) == 8 and len(level_map[-1]) == 8:
                # Если есть фигура делаем её съеденой
                if level_map[pos[0]][pos[1]].__class__.__name__ != 'Tile':
                    level_map[pos[0]][pos[1]].be_eaten(board)

                level_map[self.cell[0]][self.cell[1]] = Tile(0, 0, 0, 0)
                level_map[pos[0]][pos[1]] = self

    # Не меняй
    def be_eaten(self, board):
        '''Делает фигуру съеденой: добавляем её в список съеденых и передвигаем на несуществующие кординаты'''
        global eaten_figure
        eaten_figure.append(self)
        self.move((-5, -5), board)

    # Не меняй
    def move(self, pos, board):
        '''Двигает фигуру на координаты pos'''
        # Импортируем в метод карту уровня
        global level_map
        # Если можем подвинуть - двигаем
        if (not (len(level_map) == 8 and len(level_map[-1]) == 8)
                or pos == (-5, -5) or pos in [i[0] for i in self.get_go_att_cells()]):
            self.eat(pos, board)  # едим фигуру или воздух

            self.cell = pos  # присваиваем фигуре новые координаты

            # переделываем прямоугольник
            self.rect = self.image.get_rect()
            self.rect.x = board.points[self.cell[0]][self.cell[1]][0] + (
                    board.cell_size + 10 * (self.cell[1])) // 2 - self.rect.width // 2 - 8
            self.rect.y = board.top + board.cell_size * (self.cell[0] + 1) - self.rect.height - 15
            return True
        else:
            return False

    def update(self):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            pass


class Queen(Pawn):
    image_w = load_image('Queen_elfe.png')
    image_w = pygame.transform.scale(image_w,
                                     (int(((h // 5 - 20) / image_w.get_height())
                                          * image_w.get_width()), h // 5 - 20))
    image_b = load_image('Queen_man.png')
    image_b = pygame.transform.scale(image_b,
                                     (int(((h // 5 - 20) / image_b.get_height()) * image_b.get_width()), h // 5 - 20))

    # Изменить
    def __str__(self):
        return 'q'

    def __init__(self, color, pos, all_sprites, board):
        '''Инициализирует фигуру'''
        # Вызов конструктора родительского класса
        super().__init__(all_sprites, pos, all_sprites, board)
        # Присвоения цвета
        self.color = color
        # Присвоение картинки в зависимости от цвета
        if color == 1:
            self.image = Queen.image_w
        else:
            self.image = Queen.image_b

        self.cell = ''  # Координаты клетки, на которой стоит данная фигура
        self.move(pos, board)  # передвигаем фигуру на данную клетку

    def get_attack_coords(self):
        '''Возвращает координаты клеток, куда может атаковать фигура в формате:
                            ((координата_х, координата_у), 3)'''
        attack_p = []  # Список клеток, которые может атаковать данная фигура

        # находим координаты клетки, которая теоритически может быть атакована
        i = 1
        # находим координаты клетки, на которые фигура может пойти
        while self.cell[0] + i < 8:
            if level_map[self.cell[0] + i][self.cell[1]].__class__.__name__ != 'Tile':
                attack_p.append(((i + self.cell[0], self.cell[1]), 3))
                break
            i += 1
        i = 1
        while self.cell[0] - i > -1:
            if level_map[self.cell[0] - i][self.cell[1]].__class__.__name__ != 'Tile':
                attack_p.append(((self.cell[0] - i, self.cell[1]), 3))
                break
            i += 1
        i = 1
        while self.cell[1] + i < 8:
            if level_map[self.cell[0]][self.cell[1] + i].__class__.__name__ != 'Tile':
                attack_p.append(((self.cell[0], self.cell[1] + i), 3))
                break
            i += 1
        i = 1
        while self.cell[1] - i > -1:
            if level_map[self.cell[0]][self.cell[1] - i].__class__.__name__ != 'Tile':
                attack_p.append(((self.cell[0], self.cell[1] - i), 3))
                break
            i += 1

        # Исключаем клетки, в которых не содержится фигуры
        attack_p = [i for i in attack_p if level_map[i[0][0]][i[0][1]].color != self.color]

        return attack_p

    # Изменить
    def get_go_coords(self):
        '''Возвращает координаты клеток, куда может пойти фигура в формате:
                            ((координата_х, координата_у), 2)'''
        go_p = []  # список клеток, на которые фигура может пойти
        i = 1
        # находим координаты клетки, на которые фигура может пойти
        while self.cell[0] + i < 8 and level_map[self.cell[0] + i][self.cell[1]].__class__.__name__ == 'Tile':
            go_p.append(((i + self.cell[0], self.cell[1]), 2))
            i += 1
        i = 1
        while self.cell[0] - i > -1 and level_map[self.cell[0] - i][self.cell[1]].__class__.__name__ == 'Tile':
            go_p.append(((self.cell[0] - i, self.cell[1]), 2))
            i += 1
        i = 1
        while self.cell[1] + i < 8 and level_map[self.cell[0]][self.cell[1] + i].__class__.__name__ == 'Tile':
            go_p.append(((self.cell[0], self.cell[1] + i), 2))
            i += 1
        i = 1
        while self.cell[1] - i > -1 and level_map[self.cell[0]][self.cell[1] - i].__class__.__name__ == 'Tile':
            go_p.append(((self.cell[0], self.cell[1] - i), 2))
            i += 1
        #    go_p.append(((i, self.cell[1]), 2))
        return go_p


class Tora(Pawn):
    image_w = load_image('Tora_elf.png')
    image_w = pygame.transform.scale(image_w,
                                     (int(((h // 5 - 20) / image_w.get_height())
                                          * image_w.get_width()), h // 5 - 20))
    image_b = load_image('Tora_man.png')
    image_b = pygame.transform.scale(image_b,
                                     (int(((h // 5 - 20) / image_b.get_height()) * image_b.get_width()), h // 5 - 20))

    # Изменить
    def __str__(self):
        return 'q'

    def __init__(self, color, pos, all_sprites, board):
        '''Инициализирует фигуру'''
        # Вызов конструктора родительского класса
        super().__init__(all_sprites, pos, all_sprites, board)
        # Присвоения цвета
        self.color = color
        # Присвоение картинки в зависимости от цвета
        if color == 1:
            self.image = Tora.image_w
        else:
            self.image = Tora.image_b

        self.cell = ''  # Координаты клетки, на которой стоит данная фигура
        self.move(pos, board)  # передвигаем фигуру на данную клетку

    def get_attack_coords(self):
        '''Возвращает координаты клеток, куда может атаковать фигура в формате:
                            ((координата_х, координата_у), 3)'''
        attack_p = []  # Список клеток, которые может атаковать данная фигура

        # находим координаты клетки, которая теоритически может быть атакована
        i = 1
        # находим координаты клетки, на которые фигура может пойти
        while self.cell[0] + i < 8:
            if level_map[self.cell[0] + i][self.cell[1]].__class__.__name__ != 'Tile':
                attack_p.append(((i + self.cell[0], self.cell[1]), 3))
                break
            i += 1
        i = 1
        while self.cell[0] - i > -1:
            if level_map[self.cell[0] - i][self.cell[1]].__class__.__name__ != 'Tile':
                attack_p.append(((self.cell[0] - i, self.cell[1]), 3))
                break
            i += 1
        i = 1
        while self.cell[1] + i < 8:
            if level_map[self.cell[0]][self.cell[1] + i].__class__.__name__ != 'Tile':
                attack_p.append(((self.cell[0], self.cell[1] + i), 3))
                break
            i += 1
        i = 1
        while self.cell[1] - i > -1:
            if level_map[self.cell[0]][self.cell[1] - i].__class__.__name__ != 'Tile':
                attack_p.append(((self.cell[0], self.cell[1] - i), 3))
                break
            i += 1

        # Исключаем клетки, в которых не содержится фигуры
        attack_p = [i for i in attack_p if level_map[i[0][0]][i[0][1]].color != self.color]

        return attack_p

    # Изменить
    def get_go_coords(self):
        '''Возвращает координаты клеток, куда может пойти фигура в формате:
                            ((координата_х, координата_у), 2)'''
        go_p = []  # список клеток, на которые фигура может пойти
        i = 1
        # находим координаты клетки, на которые фигура может пойти
        while self.cell[0] + i < 8 and level_map[self.cell[0] + i][self.cell[1]].__class__.__name__ == 'Tile':
            go_p.append(((i + self.cell[0], self.cell[1]), 2))
            i += 1
        i = 1
        while self.cell[0] - i > -1 and level_map[self.cell[0] - i][self.cell[1]].__class__.__name__ == 'Tile':
            go_p.append(((self.cell[0] - i, self.cell[1]), 2))
            i += 1
        i = 1
        while self.cell[1] + i < 8 and level_map[self.cell[0]][self.cell[1] + i].__class__.__name__ == 'Tile':
            go_p.append(((self.cell[0], self.cell[1] + i), 2))
            i += 1
        i = 1
        while self.cell[1] - i > -1 and level_map[self.cell[0]][self.cell[1] - i].__class__.__name__ == 'Tile':
            go_p.append(((self.cell[0], self.cell[1] - i), 2))
            i += 1
        return go_p


class Slon(Pawn):
    image_w = load_image('Slon_elf.png')
    image_w = pygame.transform.scale(image_w,
                                     (int(((h // 5 - 20) / image_w.get_height())
                                          * image_w.get_width()), h // 5 - 20))
    image_b = load_image('Slon_human.png')
    image_b = pygame.transform.scale(image_b,
                                     (int(((h // 5 - 20) / image_b.get_height()) * image_b.get_width()), h // 5 - 20))

    # Изменить
    def __str__(self):
        return 's'

    def __init__(self, color, pos, all_sprites, board):
        '''Инициализирует фигуру'''
        # Вызов конструктора родительского класса
        super().__init__(all_sprites, pos, all_sprites, board)
        # Присвоения цвета
        self.color = color
        # Присвоение картинки в зависимости от цвета
        if color == 1:
            self.image = Slon.image_w
        else:
            self.image = Slon.image_b

        self.cell = ''  # Координаты клетки, на которой стоит данная фигура
        self.move(pos, board)  # передвигаем фигуру на данную клетку

    def get_attack_coords(self):
        '''Возвращает координаты клеток, куда может атаковать фигура в формате:
                            ((координата_х, координата_у), 3)'''
        attack_p = []  # Список клеток, которые может атаковать данная фигура

        # находим координаты клетки, которая теоритически может быть атакована
        i = 1
        # находим координаты клетки, на которые фигура может пойти
        while self.cell[0] + i < 8 and self.cell[1] + i < 8:
            if level_map[self.cell[0] + i][self.cell[1] + i].__class__.__name__ != 'Tile':
                attack_p.append(((i + self.cell[0], self.cell[1] + i), 3))
                break
            i += 1
        i = 1
        while self.cell[0] - i > -1 and self.cell[1] - i > -1:
            if level_map[self.cell[0] - i][self.cell[1] - i].__class__.__name__ != 'Tile':
                attack_p.append(((self.cell[0] - i, self.cell[1] - i), 3))
                break
            i += 1
        i = 1
        while self.cell[1] + i < 8 and self.cell[0] - i > - 1:
            if level_map[self.cell[0] - i][self.cell[1] + i].__class__.__name__ != 'Tile':
                attack_p.append(((self.cell[0] - i, self.cell[1] + i), 3))
                break
            i += 1
        i = 1
        while self.cell[1] - i > -1 and self.cell[0] + i < 8:
            if level_map[self.cell[0] + i][self.cell[1] - i].__class__.__name__ != 'Tile':
                attack_p.append(((self.cell[0] + i, self.cell[1] - i), 3))
                break
            i += 1

        # Исключаем клетки, в которых не содержится фигуры
        attack_p = [i for i in attack_p if level_map[i[0][0]][i[0][1]].color != self.color]

        return attack_p

    # Изменить
    def get_go_coords(self):
        '''Возвращает координаты клеток, куда может пойти фигура в формате:
                            ((координата_х, координата_у), 2)'''
        go_p = []  # список клеток, на которые фигура может пойти
        i = 1
        # находим координаты клетки, на которые фигура может пойти
        while self.cell[0] + i < 8 and self.cell[1] + i < 8 \
                and level_map[self.cell[0] + i][self.cell[1] + i].__class__.__name__ == 'Tile':
            go_p.append(((i + self.cell[0], self.cell[1] + i), 2))
            i += 1
        i = 1
        while self.cell[0] - i > -1 and self.cell[1] - i > -1 \
                and level_map[self.cell[0] - i][self.cell[1] - i].__class__.__name__ == 'Tile':
            go_p.append(((self.cell[0] - i, self.cell[1] - i), 2))
            i += 1
        i = 1
        while self.cell[1] + i < 8 and self.cell[0] - i > - 1 \
                and level_map[self.cell[0] - i][self.cell[1] + i].__class__.__name__ == 'Tile':
            go_p.append(((self.cell[0] - i, self.cell[1] + i), 2))
            i += 1
        i = 1
        while self.cell[1] - i > -1 and self.cell[0] + i < 8 \
                and level_map[self.cell[0] + i][self.cell[1] - i].__class__.__name__ == 'Tile':
            go_p.append(((self.cell[0] + i, self.cell[1] - i), 2))
            i += 1
        return go_p


class King(Pawn):
    image_w = load_image('king_elf.png')
    image_w = pygame.transform.scale(image_w,
                                     (int(((h // 5 - 20) / image_w.get_height())
                                          * image_w.get_width()), h // 5 - 20))
    image_b = load_image('king_human.png')
    image_b = pygame.transform.scale(image_b,
                                     (int(((h // 5 - 20) / image_b.get_height()) * image_b.get_width()), h // 5 - 20))

    # Изменить
    def __str__(self):
        return 'k'

    def __init__(self, color, pos, all_sprites, board):
        '''Инициализирует фигуру'''
        # Вызов конструктора родительского класса
        super().__init__(all_sprites, pos, all_sprites, board)
        # Присвоения цвета
        self.color = color
        # Присвоение картинки в зависимости от цвета
        if color == 1:
            self.image = King.image_w
        else:
            self.image = King.image_b

        self.cell = ''  # Координаты клетки, на которой стоит данная фигура
        self.move(pos, board)  # передвигаем фигуру на данную клетку

    def get_attack_coords(self):
        '''Возвращает координаты клеток, куда может атаковать фигура в формате:
                            ((координата_х, координата_у), 3)'''
        attack_p = []  # Список клеток, которые может атаковать данная фигура

        # находим координаты клетки, которая теоритически может быть атакована
        for u in range(-1, 2):
            for i in range(-1, 2):
                if 0 <= self.cell[0] + u <= 7 and 0 <= self.cell[1] + i <= 7:
                    attack_p.append(((self.cell[0] + u, self.cell[1] + i), 3))

        attack_p = [i for i in attack_p if
                    level_map[i[0][0]][i[0][1]].__class__.__name__ != 'Tile' and level_map[i[0][0]][
                        i[0][1]].color != self.color]

        return attack_p

    # Изменить
    def get_go_coords(self):
        '''Возвращает координаты клеток, куда может пойти фигура в формате:
                            ((координата_х, координата_у), 2)'''
        go_p = []  # список клеток, на которые фигура может пойти

        # находим координаты клетки, на которые фигура может пойти
        for u in range(-1, 2):
            for i in range(-1, 2):
                if 0 <= self.cell[0] + u <= 7 and 0 <= self.cell[1] + i <= 7:
                    go_p.append(((self.cell[0] + u, self.cell[1] + i), 2))

        # Исключаем клетки, которые содержат фигуры или которые находятся за фигурами
        go_p = [i for i in go_p if level_map[i[0][0]][i[0][1]].__class__.__name__ == 'Tile']
        # Рокировка через жопу
        if self.cell[0] == 0 and self.cell[1] == 4 and self.color == 1 and level_map[0][7].__class__.__str__ == 'T':
            go_p.append(((0, 6), 2))
        elif self.cell[0] == 7 and self.cell[1] == 4 and self.color == 1 and level_map[0][7].__class__.__str__ == 't':
            go_p.append(((7, 6), 2))
        return go_p


class Konyaka(Pawn):
    image_w = load_image('Horse_elf.png')
    image_w = pygame.transform.scale(image_w,
                                     (int(((h // 5 - 20) / image_w.get_height())
                                          * image_w.get_width()), h // 5 - 20))
    image_b = load_image('Horse_human.png')
    image_b = pygame.transform.scale(image_b,
                                     (int(((h // 5 - 20) / image_b.get_height()) * image_b.get_width()), h // 5 - 20))

    # Изменить
    def __str__(self):
        return 'h'

    def __init__(self, color, pos, all_sprites, board):
        '''Инициализирует фигуру'''
        # Вызов конструктора родительского класса
        super().__init__(all_sprites, pos, all_sprites, board)
        # Присвоения цвета
        self.color = color
        # Присвоение картинки в зависимости от цвета
        if color == 1:
            self.image = Konyaka.image_w
        else:
            self.image = Konyaka.image_b

        self.cell = ''  # Координаты клетки, на которой стоит данная фигура
        self.move(pos, board)  # передвигаем фигуру на данную клетку

    def get_attack_coords(self):
        attack_p = []  # Список клеток, которые может атаковать данная фигура

        # находим координаты клетки, которая теоритически может быть атакована
        if 0 <= self.cell[1] + 2 < 8 and 0 <= self.cell[0] + 1 < 8:
            attack_p.append(((self.cell[0] + 1, self.cell[1] + 2), 3))
        if 0 <= self.cell[1] + 1 < 8 and 0 <= self.cell[0] + 2 < 8:
            attack_p.append(((self.cell[0] + 2, self.cell[1] + 1), 3))
        if 0 <= self.cell[1] - 1 < 8 and 0 <= self.cell[0] + 2 < 8:
            attack_p.append(((self.cell[0] + 2, self.cell[1] - 1), 3))
        if 0 <= self.cell[1] - 2 < 8 and 0 <= self.cell[0] + 1 < 8:
            attack_p.append(((self.cell[0] + 1, self.cell[1] - 2), 3))
        if 0 <= self.cell[1] - 2 < 8 and 0 <= self.cell[0] - 1 < 8:
            attack_p.append(((self.cell[0] - 1, self.cell[1] - 2), 3))
        if 0 <= self.cell[1] - 1 < 8 and 0 <= self.cell[0] - 2 < 8:
            attack_p.append(((self.cell[0] - 2, self.cell[1] - 1), 3))
        if 0 <= self.cell[1] + 1 < 8 and 0 <= self.cell[0] - 2 < 8:
            attack_p.append(((self.cell[0] - 2, self.cell[1] + 1), 3))
        if 0 <= self.cell[1] + 2 < 8 and 0 <= self.cell[0] - 1 < 8:
            attack_p.append(((self.cell[0] - 1, self.cell[1] + 2), 3))
        # Исключаем клетки, в которых не содержится фигуры
        attack_p = [i for i in attack_p if
                    level_map[i[0][0]][i[0][1]].__class__.__name__ != 'Tile' and level_map[i[0][0]][
                        i[0][1]].color != self.color]

        return attack_p

    # Изменить
    def get_go_coords(self):
        go_p = []  # список клеток, на которые фигура может пойти

        # находим координаты клетки, на которые фигура может пойти
        if 0 <= self.cell[1] + 2 < 8 and 0 <= self.cell[0] + 1 < 8:
            go_p.append(((self.cell[0] + 1, self.cell[1] + 2), 2))
        if 0 <= self.cell[1] + 1 < 8 and 0 <= self.cell[0] + 2 < 8:
            go_p.append(((self.cell[0] + 2, self.cell[1] + 1), 2))
        if 0 <= self.cell[1] - 1 < 8 and 0 <= self.cell[0] + 2 < 8:
            go_p.append(((self.cell[0] + 2, self.cell[1] - 1), 2))
        if 0 <= self.cell[1] - 2 < 8 and 0 <= self.cell[0] + 1 < 8:
            go_p.append(((self.cell[0] + 1, self.cell[1] - 2), 2))
        if 0 <= self.cell[1] - 2 < 8 and 0 <= self.cell[0] - 1 < 8:
            go_p.append(((self.cell[0] - 1, self.cell[1] - 2), 2))
        if 0 <= self.cell[1] - 1 < 8 and 0 <= self.cell[0] - 2 < 8:
            go_p.append(((self.cell[0] - 2, self.cell[1] - 1), 2))
        if 0 <= self.cell[1] + 1 < 8 and 0 <= self.cell[0] - 2 < 8:
            go_p.append(((self.cell[0] - 2, self.cell[1] + 1), 2))
        if 0 <= self.cell[1] + 2 < 8 and 0 <= self.cell[0] - 1 < 8:
            go_p.append(((self.cell[0] - 1, self.cell[1] + 2), 2))

        # Исключаем клетки, которые содержат фигуры или которые находятся за фигурами
        go_p = [i for i in go_p if level_map[i[0][0]][i[0][1]].__class__.__name__ == 'Tile']
        return go_p


class Spell:
    def __str__(self):
        return f'sp-{self.name}-{self.cost}'

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def cast(self):
        pass


class Emojy:

    def __str__(self):
        return f'em-{self.name}-{self.cost}'

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


class ItemToBy:

    def __init__(self, item, y, but_group):
        global statss
        self.y = y
        self.item = item
        self.button = Button((w // 2 + w // 10 - 10, self.y + 10),
                             self.buy_item, 'BUY', but_group, scale=(w // 10 * 2, 100))
        if str(self.item) not in statss['Купленные_вещи']:
            self.state_of_bougth = True
        else:
            self.state_of_bougth = False

    def buy_item(self, n):
        global statss
        statss['Купленные_вещи'].append(str(self.item))
        self.state_of_bougth = False
        if self.button.scale != (1, 1):
            self.button.image = pygame.transform.scale(Button.image_b, self.button.scale)
        else:
            self.button.image = Button.image_b

    def render(self, screen):
        if not self.state_of_bougth:
            pygame.draw.rect(screen, (116, 116, 116), (w // 2 - w // 10 * 3, self.y, w // 10 * 6, 120), 0)
            pygame.draw.rect(screen, (160, 160, 160), (w // 2 - w // 10 * 3, self.y, w // 10 * 6, 120), 10)
        else:
            pygame.draw.rect(screen, (116, 61, 21), (w // 2 - w // 10 * 3, self.y, w // 10 * 6, 120), 0)
            pygame.draw.rect(screen, (160, 108, 59), (w // 2 - w // 10 * 3, self.y, w // 10 * 6, 120), 10)
        font = pygame.font.Font('16881.otf', 45)
        text = font.render(self.item.name + ' --------- ' + str(self.item.cost), True, pygame.Color('white'))
        text_x = w // 2 - w // 10 * 3 + 30
        text_y = self.y + 60 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))

    def update(self, event):
        if self.state_of_bougth:
            self.button.update(event)


class Shooop():
    def __init__(self):
        self.groups = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]
        self.page = 1
        self.buttons = [Button((w // 2 - (w // 4) // 2 - (w // 4) // 2, h // 8),
                               self.change_page, 'Spells', self.groups[2], scale=(w // 4, h // 8)),
                        Button((w // 2 - w // 4 // 2 + w // 4 // 2, h // 8),
                               self.change_page, 'Emojy', self.groups[2], scale=(w // 4, h // 8))
                        ]
        self.items_to_buy = [ItemToBy(Spell('Hit Figure', 666), h // 8 * 2, self.groups[0])]
        self.items_to_buy1 = [ItemToBy(Emojy('Emojy: Rats', 50), h // 8 * 2, self.groups[1])]

    def change_page(self, n):
        self.page = -self.page

    def buy(self, n):
        pass

    def update(self, args):
        for i in self.buttons:
            i.update(args)
        if self.page == 1:
            for i in self.items_to_buy:
                i.update(args)
        else:
            for i in self.items_to_buy1:
                i.update(args)

    def render(self, screen):
        global render_text
        render_text(screen, str(statss['Деньги']), w // 30, w // 30, (0, 0, 0))
        self.groups[2].draw(screen)
        for i in self.buttons:
            i.rendel()
        if self.page == 1:
            for i in self.items_to_buy:
                i.render(screen)
            self.groups[0].draw(screen)
            for i in self.items_to_buy:
                i.button.rendel()
        else:
            for i in self.items_to_buy1:
                i.render(screen)
            self.groups[1].draw(screen)
            for i in self.items_to_buy1:
                i.button.rendel()


class Button(pygame.sprite.Sprite):
    image_b = load_image('button.png')
    image_k = load_image('button1.png')

    def __init__(self, pos, met, txt, all_sprites1, scale=(1, 1)):
        super().__init__(all_sprites1)
        self.scale = scale
        if scale != (1, 1):
            self.image = pygame.transform.scale(Button.image_b, scale)
        else:
            self.image = Button.image_b
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.zhamk = met
        self.txt = txt

    def update(self, args):
        if args.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(args.pos):
                if self.scale != (1, 1):
                    self.image = pygame.transform.scale(Button.image_k, self.scale)
                else:
                    self.image = Button.image_k
            else:
                if self.scale != (1, 1):
                    self.image = pygame.transform.scale(Button.image_b, self.scale)
                else:
                    self.image = Button.image_b
        elif args.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args.pos) and args:
            self.zhamk(0)

    def rendel(self):
        font = pygame.font.Font('16881.otf', 45)
        text = font.render(self.txt, True, pygame.Color('white'))
        text_x = self.rect.x + self.image.get_width() // 2 - text.get_width() // 2
        text_y = self.rect.y + self.image.get_height() // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))

    def zhamk(self, n):
        pass


def star(n):
    global state
    state = 1


def shop(n):
    global state
    state = 2


# Класс который обозначает пустую клетку
class Tile:
    def __init__(self, color, pos, sprite, board):
        pass

    def __str__(self):
        return '.'


# Словарь с обозначениями фигур
PIECES = {'P': (Pawn, 1), 'p': (Pawn, -1), '.': (Tile, 0), 'Q': (Queen, 1), 'q': (Queen, -1),
          'T': (Tora, 1), 't': (Tora, -1), 'S': (Slon, 1), 's': (Slon, -1), 'K': (King, 1), 'k': (King, -1),
          'H': (Konyaka, 1), 'h': (Konyaka, -1)}
level_map = []  # карта уровня
eaten_figure = []  # Съеденые фигуры


# Генерация уровня по файлу
def generate_level(level, all_sprites, board):
    global level_map
    for y in range(8):
        level_map.append([])
        for x in range(8):
            level_map[-1].append(PIECES[level[y][x]][0](PIECES[level[y][x]][1], (y, x), all_sprites, board))


def background(screen):
    for i in range(50):
        pygame.draw.ellipse(screen, (randint(230, 254), randint(230, 254), randint(230, 254)),
                            (randint(0, w), randint(0, h), randint(1, 42), randint(1, 42)), 0)


timer = 500
if __name__ == '__main__':
    # Глобальные штуки
    running = True
    timer_on = False
    all_sprites1 = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    warning_text = 'YOU WILL FAIL. ARE YOU SURE?'

    # Игровые элементы
    board = BoardNacl()
    shoop = Shooop()
    generate_level(load_level('pole.txt'), all_sprites, board)
    fps = 0
    # Элементы меню
    ext = Button((w // 2 - 150, h // 8 * 6), exit, 'EXIT', all_sprites1, scale=(300, 150))
    start = Button((w // 2 - 150, h // 8 * 3), star, 'START', all_sprites1, scale=(300, 150))
    shopp = Button((w // 2 - 150, h // 8 * 5), shop, 'SHOP', all_sprites1, scale=(300, 150))
    stats = Button((w // 2 - 150, h // 2), lambda y: y, 'STATS', all_sprites1, scale=(300, 150))

    while running:

        screen.fill((255, 255, 255))
        if state == 0:
            all_sprites1.draw(screen)
            ext.rendel()
            start.rendel()
            shopp.rendel()
            stats.rendel()
        elif state == 1:
            fps += 1
            if fps == 20:
                background(screen)
            if fps == 60:
                background(screen)
            if fps == 200:
                fps = 0
                background(screen)
            board.render(screen)
            KtoHoditBlin()
            all_sprites.draw(screen)
        elif state == 2:
            shoop.render(screen)
        if timer_on:
            timer -= 1
            window_of_warning(warning_text, screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if state == 0:
                start.update(event)
                ext.update(event)
                shopp.update(event)
                stats.update(event)
            elif state == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
            elif state == 2:
                shoop.update(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == 0:
                        running = False
                    else:
                        if state == 1:
                            if not timer_on:
                                window_of_warning('YOU WILL FAIL. ARE YOU SURE?', screen)
                            else:
                                timer_on = False
                                timer = 500
                                state = 0
                                statss['Деньги'] = int(statss['Деньги']) + 10
                        else:
                            state = 0
    pygame.quit()

import os
import sys
import pygame

pygame.init()
display_inf = pygame.display.Info()
size = w, h = display_inf.current_w, display_inf.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
player = 1


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
        self.colors = [pygame.Color('black'), pygame.Color('white'), pygame.Color('#0b3189'), pygame.Color('#e60404')]
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

        text = font.render(str(i + 1), True, pygame.Color('white'))
        text_x = self.left + i * self.cell_size + self.cell_size // 2 - text.get_width() // 2
        text_y = h // 2 - text.get_height() // 2 + -1 * (4 * self.cell_size + self.cell_size // 2)
        screen.blit(text, (text_x, text_y))

        text = font.render(str(i + 1), True, pygame.Color('white'))
        text_x = (w // 2 - 4 * (self.cell_size + 10 * 8)) + i * (self.cell_size + 10 * 8) + (
                self.cell_size + 10 * 8) // 2 - text.get_width() // 2
        text_y = h // 2 - text.get_height() // 2 + 1 * (4 * self.cell_size + self.cell_size // 2)
        screen.blit(text, (text_x, text_y))

        text2 = font.render(self.letters[i], True, pygame.Color('white'))
        text2_x = w // 2 - text2.get_width() // 2 + 1 * (
                    4 * (self.cell_size + 10 * i) + (self.cell_size + 10 * 2) // 2) + 10
        text2_y = (1 + i) * self.cell_size + self.cell_size // 2 - text2.get_height() // 2
        screen.blit(text2, (text2_x, text2_y))

        text2 = font.render(self.letters[i], True, pygame.Color('white'))
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

        pygame.draw.polygon(scrn, self.colors[1],
                            (self.points[0][0], self.points[0][-1], self.points[-1][-1],
                             self.points[-1][0]), 2)
        try:
            for i in self.lightting_cell:
                pygame.draw.polygon(scrn, self.colors[i[1]], i[0], 4)
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
                    self.select_figure.move(cell_coords, self)
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
    image_w = load_image('Queen_elfe.png')
    image_w = pygame.transform.scale(image_w,
                                     (int(((h // 5 - 20) / image_w.get_height())
                                      * image_w.get_width()), h // 5 - 20))
    image_b = load_image('Queen_man.png')
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
        print(self.rect)

    # Не меняй
    def get_go_att_cells(self):
        '''Возвращает координаты клеток, куда может пойти фигура в формате:
                    ((координата_х, координата_у), цвет_выделения{значения: 2 - можно походить, 3 - можно съесть})'''
        points = []
        points.extend(self.get_attack_coords())
        points.extend(self.get_go_coords())
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

    def update(self):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            pass


# Класс который обозначает пустую клетку
class Tile:
    def __init__(self, color, pos, sprite, board):
        pass

    def __str__(self):
        return '.'


# Словарь с обозначениями фигур
PIECES = {'P': (Pawn, 1), 'p': (Pawn, -1), '.': (Tile, 0)}
level_map = []  # карта уровня
eaten_figure = []  # Съеденые фигуры


# Генерация уровня по файлу
def generate_level(level, all_sprites, board):
    global level_map
    for y in range(8):
        level_map.append([])
        for x in range(8):
            level_map[-1].append(PIECES[level[y][x]][0](PIECES[level[y][x]][1], (y, x), all_sprites, board))


if __name__ == '__main__':

    board = BoardNacl()
    all_sprites = pygame.sprite.Group()
    generate_level(load_level('pole.txt'), all_sprites, board)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        board.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

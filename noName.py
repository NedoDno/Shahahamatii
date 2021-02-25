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
        font = pygame.font.Font(None, 60)

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
        text2_x = w // 2 - text2.get_width() // 2 + 1 * (4 * (self.cell_size + 10 * i) + (self.cell_size + 10 * 2) // 2)
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


class Board:
    def __init__(self):
        self.board = [[0] * 8 for _ in range(8)]
        global h, w
        self.cell_size = h // 10
        self.left = w // 2 - 4 * self.cell_size
        self.top = self.cell_size

        self.colors = [pygame.Color('black'), pygame.Color('white')]
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scrn):
        global h, w
        font = pygame.font.Font(None, 60)
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(scrn, self.colors[(i + j) % 2], (self.left + j * self.cell_size,
                                                                  self.top + i * self.cell_size,
                                                                  self.cell_size, self.cell_size), 0)
            for j in [-1, 1]:
                text = font.render(str(i + 1), True, pygame.Color('white'))
                text_x = self.left + i * self.cell_size + self.cell_size // 2 - text.get_width() // 2
                text_y = h // 2 - text.get_height() // 2 + j * (4 * self.cell_size + self.cell_size // 2)
                screen.blit(text, (text_x, text_y))

                text2 = font.render(self.letters[i], True, pygame.Color('white'))
                text2_x = w // 2 - text2.get_width() // 2 + j * (4 * self.cell_size + self.cell_size // 2)
                text2_y = (1 + i) * self.cell_size + self.cell_size // 2 - text2.get_height() // 2
                screen.blit(text2, (text2_x, text2_y))

        pygame.draw.rect(scrn, pygame.Color('white'), (self.left, self.top, self.cell_size * 8, self.cell_size * 8), 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        a, b = None, None
        for i, k in enumerate(range(self.left, self.left + self.cell_size * 8, self.cell_size)):
            if k <= x <= k + self.cell_size:
                a = i
                break
        for i, k in enumerate(range(self.top, self.top + self.cell_size * 8, self.cell_size)):
            if k <= y <= k + self.cell_size:
                b = i
                break
        if a == None or b == None:
            return None
        return a, b

    def on_click(self, cell_coords):
        print(cell_coords)
        Pawn(1, cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Pawn(pygame.sprite.Sprite):
    image_w = pygame.transform.scale(load_image('pawn_w.png'), (h // 5, h // 5 - h // 45))
    image_b = pygame.transform.scale(load_image('pawn_b.png'), (h // 5, h // 5 - h // 45))

    def __str__(self):
        return 'p'

    def __init__(self, color, pos, all_sprites, board):
        super().__init__(all_sprites)
        self.color = color
        if color == 1:
            self.image = Pawn.image_w
        else:
            self.image = Pawn.image_b
        self.cell = ''
        self.move(pos, board)

    def get_go_att_cells(self):
        points = []
        points.extend(self.get_attack_coords())
        points.extend(self.get_go_coords())
        return points

    def get_attack_coords(self):
        attack_p = []
        if 0 <= self.cell[0] + 1* self.color < 8 and 0 <= self.cell[1] + 1* self.color < 8:
            attack_p.append(((self.cell[0] + 1 * self.color, self.cell[1] + 1 * self.color), 3))
        if 0 <= self.cell[0] - 1* self.color < 8 and 0 <= self.cell[1] + 1* self.color < 8:
            attack_p.append(((self.cell[0] - 1 * self.color, self.cell[1] + 1 * self.color), 3))
        attack_p = [i for i in attack_p if
                    level_map[i[0][0]][i[0][1]].__class__.__name__ != 'Tile' and level_map[i[0][0]][
                        i[0][1]].color != self.color]

        return attack_p

    def get_go_coords(self):
        go_p = []
        if 0 <= self.cell[1] + 1* self.color < 8:
            go_p.append(((self.cell[0], self.cell[1] + 1 * self.color), 2))
        if (0 <= self.cell[1] + 2* self.color < 8 and
                ((self.cell[1] == 1 and self.color == 1) or (self.cell[1] == 6 and self.color != 1))
                and level_map[self.cell[0]][self.cell[1] + 1* self.color].__class__.__name__ == 'Tile'):
            go_p.append(((self.cell[0], self.cell[1] + 2 * self.color), 2))
        go_p = [i for i in go_p if level_map[i[0][0]][i[0][1]].__class__.__name__ == 'Tile']
        return go_p

    def eat(self, pos, board):
        if pos != (-5, -5):
            if len(level_map) == 8 and len(level_map[-1]) == 8:
                if level_map[pos[0]][pos[1]].__class__.__name__ != 'Tile':
                    level_map[pos[0]][pos[1]].be_eaten(board)
                level_map[self.cell[0]][self.cell[1]] = Tile(0, 0, 0, 0)
                level_map[pos[0]][pos[1]] = self

    def be_eaten(self, board):
        eaten_figure.append(self)
        self.move((-5, -5), board)
        print(self)

    def move(self, pos, board):
        global level_map
        try:
            print(self.get_go_att_cells())
        except:
            pass
        if not (len(level_map) == 8 and len(level_map[-1]) == 8) or pos == (-5, -5) or pos in [i[0] for i in
                                                                                               self.get_go_att_cells()]:
            self.eat(pos, board)

            self.cell = pos
            self.rect = self.image.get_rect()
            self.rect.x = board.points[self.cell[0]][self.cell[1]][0] + (
                    board.cell_size + 15 * (self.cell[1] + 1)) // 2 - self.rect.width // 2
            self.rect.y = board.top + board.cell_size * (self.cell[0] + 1) - self.rect.height - 15

    def update(self):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            print(1)


class Tile:
    def __init__(self, color, pos, sprite, board):
        pass

    def __str__(self):
        return '.'


PIECES = {'P': (Pawn, 1), 'p': (Pawn, -1), '.': (Tile, 0)}
level_map = []
eaten_figure = []


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
        screen.fill((0, 0, 0))
        board.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

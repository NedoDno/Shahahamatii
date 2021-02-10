import os
import sys

import pygame

pygame.init()
display_inf = pygame.display.Info()
size = w, h = display_inf.current_w, display_inf.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


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
                text_x = self.left + i * self.cell_size + self.cell_size // 2 + text.get_width() // 2
                text_y = h // 2 + j * (4 * self.cell_size + self.cell_size // 3 * 2)
                screen.blit(text, (text_x, text_y))

                text2 = font.render(self.letters[i], True, pygame.Color('white'))
                text2_x = w // 2 + j * (4 * self.cell_size + self.cell_size // 3 * 2)
                text2_y =  (1+i) * self.cell_size + self.cell_size // 2 - text2.get_height() // 2
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
    image_w = pygame.transform.scale(load_image('pawn_w.png'), (50, 50))
    image_b = pygame.transform.scale(load_image('pawn_b.png'), (50, 50))

    def __init__(self, color, pos):
        super().__init__(all_sprites)
        if color:
            self.image = Pawn.image_w
        else:
            self.image = Pawn.image_b
        self.rect = self.image.get_rect()
        self.rect.x = board.left + board.cell_size * pos[0]
        self.rect.y = board.top + board.cell_size * pos[1]

    def update(self):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            print(1)


class Tile:
    def __init__(self, color, pos):
        pass


PIECES = {'P': (Pawn, 1), 'p': (Pawn, 0), '.': (Tile, 0)}


def generate_level(level):
    for y in range(8):
        for x in range(8):
            PIECES[level[y][x]][0](PIECES[level[y][x]][1], (x, y))


if __name__ == '__main__':
    board = Board()
    all_sprites = pygame.sprite.Group()
    generate_level(load_level('pole.txt'))
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

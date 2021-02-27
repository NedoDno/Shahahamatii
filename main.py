import os
import sys

import pygame
from games_thing import BoardNacl, generate_level, load_level

pygame.init()
state = 0  # Состояние программы: 0 - главное меню, 1 - игра, 2 - магазин
display_inf = pygame.display.Info()
size = w, h = display_inf.current_w, display_inf.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

spels = []


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


class Shooop():
    def __init__(self):
        self.groups = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]
        self.page = 1
        self.buttons = [Button((w // 2 - Button.image_b.get_width() // 2 - Button.image_b.get_width() // 2, h // 8),
                               self.change_page, 'Spells', self.groups[2]),
                        Button((w // 2 - Button.image_b.get_width() // 2 + Button.image_b.get_width() // 2, h // 8),
                               self.change_page, 'Emojy',  self.groups[2])
            ]
        self.page_1_buttons = [Button(
                (w // 2 - Button.image_b.get_width() // 2 + Button.image_b.get_width() // 2 - w // 6 * 2, h // 8 * 2),
                self.change_page, 'Hit figure ---------------------- 30', self.groups[0],
                (w // 6 * 4, Button.image_b.get_height())),
                        Button((w // 2 - Button.image_b.get_width() // 2 + Button.image_b.get_width() // 2 - w // 6 * 2,
                                h // 8 * 3),
                               self.change_page, 'Repair figure ---------------------- 500', self.groups[0],
                               (w // 6 * 4, Button.image_b.get_height()))]
        self.page_2_buttons = [Button(
                (w // 2 - Button.image_b.get_width() // 2 + Button.image_b.get_width() // 2 - w // 6 * 2, h // 8 * 2),
                self.change_page, 'Rat emojy ---------------------- 40', self.groups[1],
                (w // 6 * 4, Button.image_b.get_height()))]

    def change_page(self, n):
        self.page = -self.page

    def buy(self, n):
        pass

    def update(self, args):
        for i in self.buttons:
            i.update(args)
        if self.page == 1:
            for i in self.page_1_buttons:
                i.update(args)
        else:
            for i in self.page_2_buttons:
                i.update(args)

    def render(self):
        self.groups[2].draw(screen)
        for i in self.buttons:
            i.rendel()
        if self.page == 1:
            self.groups[0].draw(screen)
            for i in self.page_1_buttons:
                i.rendel()
        else:
            self.groups[1].draw(screen)
            for i in self.page_2_buttons:
                i.rendel()

class Button(pygame.sprite.Sprite):
    image_b = load_image('but.png')
    image_k = load_image('but1.png')

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


if __name__ == '__main__':
    # Глобальные штуки
    running = True
    all_sprites1 = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()


    # Игровые элементы
    board = BoardNacl()
    shoop = Shooop()
    generate_level(load_level('pole.txt'), all_sprites, board)

    # Элементы меню
    shp = Button((w // 2 - Button.image_b.get_width() // 2, h // 8 * 3), shop, 'SHOP', all_sprites1)
    ext = Button((w // 2 - Button.image_b.get_width() // 2, h // 2), exit, 'EXIT', all_sprites1)
    start = Button((w // 2 - Button.image_b.get_width() // 2, h // 8 * 2), star, 'START', all_sprites1)

    while running:
        screen.fill((0, 0, 0))
        if state == 0:
            all_sprites1.draw(screen)
            ext.rendel()
            shp.rendel()
            start.rendel()
        elif state == 1:
            board.render(screen)
            all_sprites.draw(screen)
        elif state == 2:

            shoop.render()
        pygame.display.flip()
        for event in pygame.event.get():
            if state == 0:
                shp.update(event)
                start.update(event)
                ext.update(event)
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
                        state = 0
    pygame.quit()

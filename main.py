import os
import sys

import pygame
from games_thing import BoardNacl, generate_level, load_level

pygame.init()
state = 0  # Состояние программы: 0 - главное меню, 1 - игра, 2 - магазин
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


class Button(pygame.sprite.Sprite):
    image_b = load_image('but.png')
    image_k = load_image('but1.png')

    def __init__(self, pos, met, txt):
        super().__init__(all_sprites1)
        self.image = Button.image_b
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.zhamk = met
        self.txt = txt

    def update(self, args):
        if args.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(args.pos):
                self.image = Button.image_k
            else:
                self.image = Button.image_b
        elif args.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args.pos) and args:
            self.zhamk(0)

    def rendel(self):
        font = pygame.font.Font('16881.otf', 35
                                )
        text = font.render(self.txt, True, pygame.Color('white'))
        text_x = self.rect.x + Button.image_b.get_width() // 2 - text.get_width() // 2
        text_y = self.rect.y + Button.image_b.get_height() // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))

    def zhamk(self, n):
        pass


def star(n):
    global state
    state = 1


if __name__ == '__main__':
    # Глобальные штуки
    running = True
    all_sprites1 = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # Игровые элементы
    board = BoardNacl()
    generate_level(load_level('pole.txt'), all_sprites, board)

    # Элементы меню
    ext = Button((w // 2 - Button.image_b.get_width() // 2, h // 2), exit, 'EXIT')
    start = Button((w // 2 - Button.image_b.get_width() // 2, h // 8 * 3), star, 'START')

    while running:
        screen.fill((0, 0, 0))
        if state == 0:
            all_sprites1.draw(screen)
            ext.rendel()
            start.rendel()
        elif state == 1:
            board.render(screen)
            all_sprites.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if state == 0:
                start.update(event)
                ext.update(event)
            elif state == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == 0:
                        running = False
                    else:
                        state = 0
    pygame.quit()

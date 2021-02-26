from random import randint

import pygame

pygame.init()
display_inf = pygame.display.Info()
size = w, h = 600, 600  # display_inf.current_w, display_inf.current_h
screen = pygame.display.set_mode(size)


def background(screen):
    screen.fill((255, 255, 255))
    for i in range(50):
        pygame.draw.ellipse(screen, (randint(230, 254), randint(230, 254), randint(230, 254)),
                         (randint(0, w), randint(0, h), randint(1, 10), randint(1, 10)), 0)


if __name__ == '__main__':

    running = True
    fps = 0
    while running:

        # Конструкция для заднего фона
        fps += 1
        if fps == 200:
            fps = 0
            background(screen)



        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    pygame.quit()

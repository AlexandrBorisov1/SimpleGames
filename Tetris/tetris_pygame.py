# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random

WIDTH = 360
HEIGHT = 660
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Blok(pygame.sprite.Sprite):
    def __init__(self, xy):
        self.xy = xy
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
                
    def update(self):
        self.rect.y += 1
        if self.rect.bottom > HEIGHT-30:
            self.__init__()
        if self.rect.left < 30:
        	self.rect.left = 30
        if self.rect.right > 330:
        	self.rect.right = 330
         
    def move_left(self):
    	self.rect.x -= 30
    
    def move_right(self):
    	self.rect.x += 30


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
blok1 = Blok((150,30))
blok2 = Blok((180, 30))
all_sprites.add(blok1, blok2)


# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                blok1.move_left()
                blok2.move_left()
            elif event.key == pygame.K_d:
                blok1.move_right()
                blok2.move_right()
    # Обновление
    all_sprites.update()
    
    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.draw.rect(screen, (128,128,128), (0,0,30,660))
    pygame.draw.rect(screen, (128,128,128),(30,630,300,30))
    pygame.draw.rect(screen, (128,128,128),(330,0,30,660))
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
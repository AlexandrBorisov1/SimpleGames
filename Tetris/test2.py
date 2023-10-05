import pygame as pg
from random import randrange

# Константы
WIDTH = 360 + 200
HEIGHT = 660
WINDOW = 1000		# размер игрового поля
FPS = 60			# частота обновления экрана
TILE_SIZE = 30		# стандартный размер деталей игры
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE) # 
time = 0			# данные 2 значения понадобятся чтобы сделать движение
time_step = 450		# змейки не плавным а дискретным и в тоже время это скорость змейки

# Инициализация объектов
pg.init()
gameScreen = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Tetris")
clock = pg.time.Clock()

# Параметры змейки
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = [135, 15]
length = 1								# длина змейки
segments = [snake.copy()]				# список сегментов змейки
down_dir = (0, 0)
snake_dir = (0, 0)						# смещение змейки по игровому полю


# Главный цикл игры
while True:
    # Частота обновления экрана
    clock.tick(FPS)
    # Цикл обработки событий
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:		# обработка нажатия клавиш
            if event.key == pg.K_UP:
                snake_dir = (0, -TILE_SIZE)
            if event.key == pg.K_DOWN:
                down_dir = (0, TILE_SIZE)
            if event.key == pg.K_LEFT:
                snake_dir = (-TILE_SIZE, 0)
            if event.key == pg.K_RIGHT:
                snake_dir = (TILE_SIZE, 0)

    
    gameScreen.fill((0, 0, 0))							# заливаем фон каким либо цветом
    pg.draw.rect(gameScreen, (128, 128, 128), (30, 630, 300, 30))
    pg.draw.rect(gameScreen, (128, 128, 128), (0, 0, 30, 660))	# эти две границы мне понадобились во время
    pg.draw.rect(gameScreen, (128, 128, 128), (330, 0, 30, 660))	# запуска интерпретатора с игрой на мобилке (по сути они не нужны)

    # Перемещаем змейку
    if snake.left >= 30 or snake.right < 330:
        snake.move_ip(snake_dir)		# перемещаем змейку на стандартный шаг в сторону snake_dir
        segments.append(snake.copy())	# добавляем новый сегмент
        segments = segments[-length:]	# и обрезаем по длине
        snake_dir = (0, 0)    
    
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:		# проверяем что прошёл необходимый интервал времени
        time = time_now
        snake.move_ip(down_dir)        
        segments.append(snake.copy())	# добавляем новый сегмент
        segments = segments[-length:]	# и обрезаем по длине
        
    #if snake.left < 30:
       # snake.move_ip((TILE_SIZE, 0))
        
    # Отображаем змейку
    [pg.draw.rect(gameScreen, (255, 255, 255), segment) for segment in segments]

    pg.display.flip() # обновляем экран

pg.quit()
# Классическая игра "Змейка" с использованием библиотеки pygame.

import pygame as pg
from random import randrange

# Константы
WINDOW = 1000		# размер игрового поля
FPS = 60			# частота обновления экрана
TILE_SIZE = 50		# стандартный размер деталей игры
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE) # 
time = 0			# данные 2 значения понадобятся чтобы сделать движение
time_step = 150		# змейки не плавным а дискретным и в тоже время это скорость змейки

# Инициализация объектов
pg.init()
gameScreen = pg.display.set_mode([WINDOW] * 2)
pg.display.set_caption("Snake")
clock = pg.time.Clock()

# Функция для определения координат случайной позиции на игровом поле
get_random_position = lambda:[randrange(*RANGE), randrange(*RANGE)]

# Параметры змейки
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1								# длина змейки
segments = [snake.copy()]				# список сегментов змейки
snake_dir = (0, 0)						# смещение змейки по игровому полю

# Параметры еды
food = snake.copy()
food.center = get_random_position()


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
				snake_dir = (0, TILE_SIZE)
			if event.key == pg.K_LEFT:
				snake_dir = (-TILE_SIZE, 0)
			if event.key == pg.K_RIGHT:
				snake_dir = (TILE_SIZE, 0)
    
	gameScreen.fill((155, 188, 15))								# заливаем фон каким либо цветом
	pg.draw.rect(gameScreen, (0, 0, 0), (1000, 0, 50, 1050))	# эти две границы мне понадобились во время
	pg.draw.rect(gameScreen, (0, 0, 0), (0, 1000, 1000, 50))	# запуска интерпретатора с игрой на мобилке (по сути они не нужны)

	# Перемещаем змейку
	time_now = pg.time.get_ticks()
	if time_now - time > time_step:		# проверяем что прошёл необходимый интервал времени
		time = time_now
		snake.move_ip(snake_dir)		# перемещаем змейку на стандартный шаг в сторону snake_dir
		segments.append(snake.copy())	# добавляем новый сегмент
		segments = segments[-length:]	# и обрезаем по длине
  
	# Отображаем змейку
	[pg.draw.rect(gameScreen, (128, 128, 128), segment) for segment in segments]
	# Отображаем еду
	pg.draw.rect(gameScreen, (128, 0, 0), food)
 
	# Поедание
	if snake.center == food.center:			# если съели
		food.center = get_random_position()	# перемещаем еду в другое место
		length += 1							# добавляем длину змейки
  
	# Столкновение с границами и телом змейки
	snake_collision = pg.Rect.collidelist(snake, segments[:-1]) != -1				# флаг столкновения змейки с собой
 
	if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or snake_collision:
		snake.center, food.center = get_random_position(), get_random_position()	# обновляем позиции змейки и еды
		length, snake_dir = 1, (0, 0)												# обнуляем длину и смещение
		segments = [snake.copy()]
	
	pg.display.flip() # обновляем экран

pg.quit()
import pygame as pg
import random

# Константы
WIDTH = 360 + 200
HEIGHT = 660
FPS = 60			# частота обновления экрана
T_S = 30		# стандартный размер деталей игры
time = 0			# данные 2 значения понадобятся чтобы сделать движение
time_step = 450		# змейки не плавным а дискретным и в тоже время это скорость змейки

# Инициализация объектов
pg.init()
gameScreen = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Tetris")
clock = pg.time.Clock()

# Параметры блока
T_blok = [[165, 15], [165, 45], [165, 75], [195, 45]]   # вращение [[0*T_S + 165, 0*T_S + 15], [0, 1], [0, 2], [1, 1]] [[]]
L_blok = [[165, 15], [165, 45], [165, 75], [195, 75]]
L_inv_blok = [[195, 15], [195, 45], [195, 75], [165, 75]]
sq_blok = [[165, 15], [195, 15], [165, 45], [195, 45]]
line_blok = [[135, 15], [165, 15], [195, 15], [225, 15]]

blok = pg.rect.Rect([0, 0, T_S - 2, T_S - 2])

def init_blok():
    segments = [blok.copy(), blok.copy(), blok.copy(), blok.copy()]
    rand_blok = random.choice([T_blok, L_blok, L_inv_blok, sq_blok, line_blok])
    for i in range(4):
        segments[i].center = rand_blok[i]
    
    return segments

down_dir = (0, 0)
blok_dir = (0, 0)						# смещение змейки по игровому полю
blok_rotate = False

segments = init_blok()
segments_filling = []
# Главный цикл игры
while True:
    # Частота обновления экрана
    clock.tick(FPS)
    # Цикл обработки событий
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:		# обработка нажатия клавиш
            if event.key in [pg.K_DOWN, pg.K_s]:
                down_dir = (0, T_S)
                blok_dir = (0, T_S)
            if event.key in [pg.K_LEFT, pg.K_a]:
                blok_dir = (-T_S, 0)
            if event.key in [pg.K_RIGHT, pg.K_d] and blok.right < 300:
                blok_dir = (T_S, 0)
            if event.key in [pg.K_SPACE, pg.K_w, pg.K_UP]:
                blok_rotate = True

    
    gameScreen.fill((0, 0, 0))							# заливаем фон каким либо цветом
    pg.draw.rect(gameScreen, (128, 128, 128), (30, 630, 300, 30))
    pg.draw.rect(gameScreen, (128, 128, 128), (0, 0, 30, 660))	# эти две границы мне понадобились во время
    pg.draw.rect(gameScreen, (128, 128, 128), (330, 0, 30, 660))	# запуска интерпретатора с игрой на мобилке (по сути они не нужны)
    
    # вращение блока
    if blok_rotate:
        bias_x = segments[1].centerx - segments[1].centery
        bias_y = segments[1].centerx + segments[1].centery
        for i in range(4):
            segments[i].centerx, segments[i].centery = segments[i].centery + bias_x, (segments[i].centerx * -1) + bias_y
        blok_rotate = False

    # Перемещаем блок
    for i in range(4):
        segments[i].move_ip(blok_dir)
    # Столкновение с левой стеной
    left_wall_collision = pg.Rect.collidelist(pg.rect.Rect([0, 0, 30, 660]), segments) != -1
    if left_wall_collision:
        for i in range(4):
            segments[i].move_ip((T_S, 0))
    # Столкновение с правой стеной
    right_wall_collision = pg.Rect.collidelist(pg.rect.Rect([330, 0, 30, 660]), segments) != -1
    if right_wall_collision:
        for i in range(4):
            segments[i].move_ip((-T_S, 0))
    
    blok_dir = (0, 0)
    
    # движение блока вниз
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:		# проверяем что прошёл необходимый интервал времени
        time = time_now
        for i in range(4):
            segments[i].move_ip(down_dir)        
    
    # столкновение с дном или с другими блоками
    bottom_wall_collision = pg.Rect.collidelist(pg.rect.Rect([30, 630, 300, 30]), segments) != -1 # Столкновение с дном
    bottom_segment_collision = False
    for i in range(4):                                                                            # Столкновение с другим блоком
        if pg.Rect.collidelist(segments[i], segments_filling) != -1:                              # работает плохо срабатывает не только когда столкновение сверху вниз
            bottom_segment_collision = True
            break
    
    if bottom_wall_collision or bottom_segment_collision:
        for i in range(4):
            segments[i].move_ip((0, -T_S))
        segments_filling.extend(segments)
        segments = init_blok()
    
    # стирание полных строк
    '''segments_dict = {}
    for i, segment in enumerate(segments_filling):
        if segment.centery not in segments_dict:
            segments_dict[segment.centery] = [1, i]
        else:
            segments_dict[segment.centery][0] += 1
            segments_dict[segment.centery].append(i)
        if segments_dict[segment.centery][0] == 10:
            for j in range(1, 11):
                segments_filling.pop(segments_dict[segment.centery][j])'''
            
    # Отображаем змейку
    [pg.draw.rect(gameScreen, (255, 255, 255), segment) for segment in segments]
    [pg.draw.rect(gameScreen, (255, 255, 255), segment) for segment in segments_filling]

    pg.display.flip() # обновляем экран

pg.quit()
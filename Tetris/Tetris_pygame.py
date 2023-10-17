import pygame as pg
import random

# Константы
WIDTH = 360 + 200   # Ширина окна
HEIGHT = 660        # Высота окна
FPS = 60			# Частота обновления экрана
T_S = 30		    # Стандартный размер деталей игры
time = 0

# Инициализация объектов
pg.init()
gameScreen = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Tetris")
clock = pg.time.Clock()

# Классы

# Класс_фигуры_________________________________________________________________________________________________________________________________________
class Blok():
    def __init__(self):
        self.T_blok = [[165, 15], [165, 45], [165, 75], [195, 45]]      # Координаты центров елементов блоков
        self.L_blok = [[165, 15], [165, 45], [165, 75], [195, 75]]      #
        self.L_inv_blok = [[195, 15], [195, 45], [195, 75], [165, 75]]  #
        self.sq_blok = [[165, 15], [195, 15], [165, 45], [195, 45]]     #
        self.line_blok = [[135, 15], [165, 15], [195, 15], [225, 15]]   #
        
        self.segments = []          # Список сегментов блока (всегда 4 сегмента)
        self.time = 0
    
    # Инициализация случайного блока    
    def rand_blok_init(self):
        blok = pg.rect.Rect([0, 0, T_S - 2, T_S - 2])                           # Сегмент блока
        self.segments = [blok.copy(), blok.copy(), blok.copy(), blok.copy()]    # Заполняем список сегментами
        rand_blok = random.choice([self.T_blok, self.L_blok, self.L_inv_blok, self.sq_blok, self.line_blok])
        for i in range(4):                                                      # Случайно выбираем форму блока
            self.segments[i].center = rand_blok[i]                              # И расставляем сегменты списка согласно вбранной форме

    # Вращение блока
    def rotate_blok(self):
        bias_x = self.segments[1].centerx - self.segments[1].centery            # Смещение сегмента по оси X
        bias_y = self.segments[1].centerx + self.segments[1].centery            # Смещение сегмента по оси Y
        for i in range(4):                                                      # Поворачиваем фигуру на 90 градусов и смещаем на необходимые расстояния
            self.segments[i].centerx, self.segments[i].centery = self.segments[i].centery + bias_x, (self.segments[i].centerx * -1) + bias_y
        
    # Автоматическое падение фигуры
    def auto_move_down_blok(self, cup, interface):
        time_now = pg.time.get_ticks()
        if time_now - self.time > interface.time_step and interface.game_start: # Проверяем что прошёл необходимый интервал времени
            self.time = time_now
            for i in range(4):                                                  # Смещаем фигру вниз
                self.segments[i].move_ip((0, T_S))                              #
        # Столкновение с дном либо с наполнением стакана
        bottom_wall_collision = pg.Rect.collidelist(cup.bottom_wall, self.segments) != -1 # Флаг столкновения с дном
        bottom_segment_collision = False                                                  # Флаг столкновени с наполнением стакана
        for i in range(4):
            bottom_segment_collision = pg.Rect.collidelist(self.segments[i], cup.segments_filling) != -1
            if bottom_segment_collision:
                break
        if bottom_wall_collision or bottom_segment_collision:                             # Если столкнулись
            self.move_up_blok()                                                           # Смещаем фигру на один шаг вверх
            cup.add_segments(self.segments)                                               # Передаём сегменты фигры стакану
            self.rand_blok_init()                                                         # И создаём новую случайную фигуру
    
    # Движение фигуры вниз
    def move_down_blok(self): 
        for i in range(4):
            self.segments[i].move_ip((0, T_S))

    # Движение фигуры влево и обработка столкновения
    def move_left_blok(self, cup):
        for i in range(4):
            self.segments[i].move_ip((-T_S, 0))
        # Столкновение с левой стеной
        left_wall_collision = pg.Rect.collidelist(cup.left_wall, self.segments) != -1    # Флаг столкновения со стеной
        left_segment_collision = False                                                   # Флаг столкновения с сегментами стакана
        for i in range(4):
            left_segment_collision = pg.Rect.collidelist(self.segments[i], cup.segments_filling) != -1
            if left_segment_collision:
                break
        if left_wall_collision or left_segment_collision:                                # При столкновении, смещаем фигуру вправо
            self.move_right_blok(cup)

    # Движение фигуры вправо и обработка столкновения
    def move_right_blok(self, cup):
        for i in range(4):
            self.segments[i].move_ip((T_S, 0))
        # Столкновение с правой стеной
        right_wall_collision = pg.Rect.collidelist(cup.right_wall, self.segments) != -1  # Флаг столкновения со стеной
        right_segment_collision = False                                                  # Флаг столкновения с сегментами стакана
        for i in range(4):
            right_segment_collision = pg.Rect.collidelist(self.segments[i], cup.segments_filling) != -1
            if right_segment_collision:
                break
        if right_wall_collision or right_segment_collision:                              # При столкновении, смещаем фигуру влево
            self.move_left_blok(cup)

    # Движение фигуры вверх
    def move_up_blok(self):
        for i in range(4):
            self.segments[i].move_ip((0, -T_S))

    # Отрисовка фигуры
    def render_blok(self):
    	[pg.draw.rect(gameScreen, (255, 255, 255), segment) for segment in self.segments]

#Класс_игрового_поля(стакана)__________________________________________________________________________________________________________________________
class GameField():
    def __init__(self):
        self.segments_filling = []                                  # Список сегментов наполненияя стакана
        self.left_wall = pg.rect.Rect([0, 0, 30, 660])              # Стенки стакана
        self.right_wall = pg.rect.Rect([330, 0, 30, 660])           #
        self.bottom_wall = pg.rect.Rect([30, 630, 300, 30])         #

    # Добавление фигуры в стакан
    def add_segments(self, segments):
        self.segments_filling.extend(segments)

    # Отрисовка стенок стакана
    def draw_cup_walls(self):
        pg.draw.rect(gameScreen, (128, 128, 128), self.bottom_wall)
        pg.draw.rect(gameScreen, (128, 128, 128), self.left_wall)
        pg.draw.rect(gameScreen, (128, 128, 128), self.right_wall)

    # Удаление заполненой строки стакана
    def remove_full_line(self, score_counter):
        # стирание полных строк
        segments_dict = {}
        for i, segment in enumerate(self.segments_filling):         # Упрощённо говоря:
            if segment.centery not in segments_dict:                # Создаём словарь где ключи это Y координаты сегментов стакана,
                segments_dict[segment.centery] = [1, i]             # а значения, это список с количеством сегментов в строке и их индексы.
            else:                                                   # Если накапливается 10 сегментов в строке, то её удаляем, а все сегменты
                segments_dict[segment.centery][0] += 1              # что находились выше, опускаются на соответствующее количество шагов.
                segments_dict[segment.centery].append(i)
            if segments_dict[segment.centery][0] == 10:
                temp = []
                remove_list = segments_dict[segment.centery][1:11]
                for j in range(len(self.segments_filling)):
                    if j not in remove_list:
                        temp.append(self.segments_filling[j])
                self.segments_filling = temp
                score_counter.score_counter()
                for segm in self.segments_filling:
                    if segm.centery < segment.centery:
                        segm.move_ip(0, T_S)
                break

    # Отрисовка сегментов наполнения стакана
    def render_segments_filling(self):
        [pg.draw.rect(gameScreen, (255, 255, 255), segment) for segment in self.segments_filling]

#Класс_интерфейса_______________________________________________________________________________________________________________________________________
class GameInterface():
    def __init__(self):
        self.time_step = 400                                    # Интервал времени через который фигура смещаетсяя вниз (скорость фигуры)
        self.game_start = False                                 # Флаг старта игры
        self.current_score = 0                                  # Текущий счёт

        with open('tetris_best_score.txt', "r") as f:
            self.best_score = int(f.read())                     # Лучший счёт(подгружается из файла)
        
        self.level = 1                                          # Уровень сложности

    # Повышение уровня
    def level_up(self):
        for lev in range(1, 10):
            if self.current_score >= (10 * lev):                # Если текущий счёт увеличивается на 10 очков,
                self.level = lev + 1                            # то уровень увеличивается на 1,
                self.time_step = round(400 / (lev + 1))         # а скорость падения фигур увеличивается пропорционально уровню
    
    # Счётчик очков
    def score_counter(self):
        self.current_score += 1

    # Game Over
    def game_over(self, cup):
        for segm in cup:
            if 90 > segm.centery > 0:
                self.game_start = False
                if self.current_score > self.best_score:        # Если во время гейм овера текущий счёт выше лучшего,
                    f = open('tetris_best_score.txt', "w")      # то сохраняем его в файл как лучший
                    f.write(str(self.current_score))
                    f.close()
                blok.__init__()                                 # И инициализируем все обьекты заново
                blok.rand_blok_init()                           #
                gameField.__init__()                            #
                gameInterface.__init__()                        #
                break

    # Отрисовка интерфейса
    def render_interface(self):
        f1 = pg.font.Font(None, 25)
        curr_sc_text = f1.render(f'Текущий счёт: {self.current_score}', 1, (128, 128, 128))
        gameScreen.blit(curr_sc_text, (390, 30))
        best_sc_text = f1.render(f'Лучший счёт: {self.best_score}', 1, (128, 128, 128))
        gameScreen.blit(best_sc_text, (390, 60))
        level_text = f1.render(f'Уровень: {self.level}', 1, (128, 128, 128))
        gameScreen.blit(level_text, (390, 90))
        if not self.game_start:
            start_text = f1.render('Для начала игры нажмите "s"', 1, (128, 0, 0))
            gameScreen.blit(start_text, (50, 300))


# Создаём все необходимые объекты
blok = Blok()
blok.rand_blok_init()
gameField = GameField()
gameInterface = GameInterface()

# Главный цикл игры
while True:
    clock.tick(FPS)                                         # Частота обновления экрана
    for event in pg.event.get():                            # Цикл обработки событий
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:		                # Обработка нажатия клавиш
            if event.key in [pg.K_DOWN, pg.K_s]:
                blok.move_down_blok()
                gameInterface.game_start = True
            if event.key in [pg.K_LEFT, pg.K_a]:
                blok.move_left_blok(gameField)
            if event.key in [pg.K_RIGHT, pg.K_d]:
                blok.move_right_blok(gameField)
            if event.key in [pg.K_SPACE, pg.K_w, pg.K_UP]:
                blok.rotate_blok()

    
    gameScreen.fill((0, 0, 0))							    # Заливаем фон чёрным цветом
    gameField.draw_cup_walls()                              # Отрисовка стенок стакана
    blok.auto_move_down_blok(gameField, gameInterface)      # Движение блока вниз
    gameInterface.game_over(gameField.segments_filling)     # Проверка гейм овера
    gameField.remove_full_line(gameInterface)               # Стирание полных строк

    blok.render_blok()                                      # Отображаем блоки
    gameField.render_segments_filling()                     # Отображаем наполнение стакана
    gameInterface.level_up()                                # Проверка на увеличение уровня
    gameInterface.render_interface()                        # Отображаем интерфейс
    
    pg.display.flip()                                       # Обновляем экран

pg.quit()
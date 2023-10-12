import pygame as pg
import random

# Константы
WIDTH = 360 + 200
HEIGHT = 660
FPS = 60			# частота обновления экрана
T_S = 30		# стандартный размер деталей игры
time = 0			# данные 2 значения понадобятся чтобы сделать движение блока
time_step = 450		#  не плавным а дискретным и в тоже время это скорость блока
GAME_START = False

# Инициализация объектов
pg.init()
gameScreen = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Tetris")
clock = pg.time.Clock()

class Blok():
    def __init__(self):
        self.T_blok = [[165, 15], [165, 45], [165, 75], [195, 45]]
        self.L_blok = [[165, 15], [165, 45], [165, 75], [195, 75]]
        self.L_inv_blok = [[195, 15], [195, 45], [195, 75], [165, 75]]
        self.sq_blok = [[165, 15], [195, 15], [165, 45], [195, 45]]
        self.line_blok = [[135, 15], [165, 15], [195, 15], [225, 15]]
        
        self.segments = []
        #self.blok_rotate = False
        self.time = 0
        
    def rand_blok_init(self):
        # Инициализация случайного блока
        blok = pg.rect.Rect([0, 0, T_S - 2, T_S - 2])

        self.segments = [blok.copy(), blok.copy(), blok.copy(), blok.copy()]
        rand_blok = random.choice([self.T_blok, self.L_blok, self.L_inv_blok, self.sq_blok, self.line_blok])
        for i in range(4):
            self.segments[i].center = rand_blok[i]
    
    def rotate_blok(self):
        # Вращение блока
        #if self.blok_rotate:
        bias_x = self.segments[1].centerx - self.segments[1].centery
        bias_y = self.segments[1].centerx + self.segments[1].centery
        for i in range(4):
            self.segments[i].centerx, self.segments[i].centery = self.segments[i].centery + bias_x, (self.segments[i].centerx * -1) + bias_y
        #self.blok_rotate = False
        
    def auto_move_down_blok(self, cup):
        time_now = pg.time.get_ticks()
        if time_now - self.time > time_step and GAME_START:		# проверяем что прошёл необходимый интервал времени
            self.time = time_now
            for i in range(4):
                self.segments[i].move_ip((0, T_S))
        # Столкновение с дном
        bottom_wall_collision = pg.Rect.collidelist(cup.bottom_wall, self.segments) != -1
        bottom_segment_collision = False
        for i in range(4):
            bottom_segment_collision = pg.Rect.collidelist(self.segments[i], cup.segments_filling) != -1
            if bottom_segment_collision:
                break
        if bottom_wall_collision or bottom_segment_collision:
            self.move_up_blok()
            cup.add_segments(self.segments)
            self.rand_blok_init()
    
    def move_down_blok(self): # хз делать ограничение или нет
        for i in range(4):
            self.segments[i].move_ip((0, T_S))
    
    def move_left_blok(self, cup):
        for i in range(4):
            self.segments[i].move_ip((-T_S, 0))
        # Столкновение с левой стеной
        left_wall_collision = pg.Rect.collidelist(cup.left_wall, self.segments) != -1
        left_segment_collision = False
        for i in range(4):
            left_segment_collision = pg.Rect.collidelist(self.segments[i], cup.segments_filling) != -1
            if left_segment_collision:
                break
        if left_wall_collision or left_segment_collision:
            self.move_right_blok(cup)
    
    def move_right_blok(self, cup):
        for i in range(4):
            self.segments[i].move_ip((T_S, 0))
        # Столкновение с правой стеной
        right_wall_collision = pg.Rect.collidelist(cup.right_wall, self.segments) != -1
        right_segment_collision = False
        for i in range(4):
            right_segment_collision = pg.Rect.collidelist(self.segments[i], cup.segments_filling) != -1
            if right_segment_collision:
                break
        if right_wall_collision or right_segment_collision:
            self.move_left_blok(cup)
    
    def move_up_blok(self):
        for i in range(4):
            self.segments[i].move_ip((0, -T_S))
    
    def render_blok(self):
    	[pg.draw.rect(gameScreen, (255, 255, 255), segment) for segment in self.segments]

        
class GameField():
    def __init__(self):
        self.segments_filling = []
        self.left_wall = pg.rect.Rect([0, 0, 30, 660])
        self.right_wall = pg.rect.Rect([330, 0, 30, 660])
        self.bottom_wall = pg.rect.Rect([30, 630, 300, 30])

    def add_segments(self, segments):
        self.segments_filling.extend(segments)

    def draw_cup_walls(self):
        pg.draw.rect(gameScreen, (128, 128, 128), self.bottom_wall)
        pg.draw.rect(gameScreen, (128, 128, 128), self.left_wall)
        pg.draw.rect(gameScreen, (128, 128, 128), self.right_wall)

    def remove_full_line(self, score_counter):
        # стирание полных строк
        segments_dict = {}
        for i, segment in enumerate(self.segments_filling):
            if segment.centery not in segments_dict:
                segments_dict[segment.centery] = [1, i]
            else:
                segments_dict[segment.centery][0] += 1
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
	
    def render_segments_filling(self):
	    [pg.draw.rect(gameScreen, (255, 255, 255), segment) for segment in self.segments_filling]


class GameInterface():
    def __init__(self):
        self.current_score = 0
        f = open('tetris_best_score.txt')
        self.best_score = f.read()
        f.close()
        self.level = 1
    def score_counter(self):
        self.current_score += 1
        '''if self.current_score > self.best_score:
            self.best_score = self.current_score'''
    def game_over(self, cup):
        for segm in cup:
            if segm.centery == 300:
                GAME_START = False
                break
    def render_interface(self):
        f1 = pg.font.Font(None, 25)
        curr_sc_text = f1.render(f'Текущий счёт: {self.current_score}', 1, (128, 128, 128))
        gameScreen.blit(curr_sc_text, (390, 30))
        best_sc_text = f1.render(f'Лучший счёт: {self.best_score}', 1, (128, 128, 128))
        gameScreen.blit(best_sc_text, (390, 60))
        level_text = f1.render(f'Уровень: {self.level}', 1, (128, 128, 128))
        gameScreen.blit(level_text, (390, 90))
        if not GAME_START:
            start_text = f1.render('Для начала игры нажмите "s"', 1, (128, 0, 0))
            gameScreen.blit(start_text, (50, 300))



blok = Blok()
blok.rand_blok_init()
gameField = GameField()
gameInterface = GameInterface()

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
                blok.move_down_blok()
                GAME_START = True
            if event.key in [pg.K_LEFT, pg.K_a]:
                blok.move_left_blok(gameField)
            if event.key in [pg.K_RIGHT, pg.K_d]:
                blok.move_right_blok(gameField)
            if event.key in [pg.K_SPACE, pg.K_w, pg.K_UP]:
                blok.rotate_blok()

    
    gameScreen.fill((0, 0, 0))							# заливаем фон каким либо цветом
    gameField.draw_cup_walls()
    # движение блока вниз
    blok.auto_move_down_blok(gameField)
    gameInterface.game_over(gameField.segments_filling)
    # стирание полных строк
    gameField.remove_full_line(gameInterface)
    # Отображаем блоки
    blok.render_blok()
    gameField.render_segments_filling()
    gameInterface.render_interface()
    
    pg.display.flip() # обновляем экран

pg.quit()
# python C:\Users\admin\DSPR-2.0\data\ML_4\game.py
import numpy as np
import random as rn
import time
import os
import keyboard
from threading import Thread

class GameField():
    def __init__(self, y=20, x=10) -> None:
        self.field_arr = np.zeros((y+1, x+2), dtype=int) # игровое поле в тетрисе 10*20
        
        y_walls = [i for i in range(y+1)]*2     # сразу 2 стены
        x_walls = [0]*(y+1)
        x_walls.extend([x+1]*(y+1))
        self.field_walls = (y_walls, x_walls)
        self.field_arr[self.field_walls] = 2
        
        y_bottom = [y]*(x+2)                    # рисуем пол
        x_bottom = [i for i in range(x+2)]
        self.field_bottom = (y_bottom, x_bottom)
        self.field_arr[self.field_bottom] = 2
    
    def redrawField(self):  #  chr(9689) у некоторых данный символ не пашет
        self.str_field_arr = '\n'.join([''.join([' ' if self.field_arr[i, j]==0 else '#' for j in range(self.field_arr.shape[1])]) for i in range(self.field_arr.shape[0])])
        print(self.str_field_arr)
    
    def sysRedrawField(self):   # прорисовка поля в изначальном виде, числовая матрица
        print(self.field_arr)

class Blok():
    def __init__(self) -> None:
        self.blok_L = ([0, 1, 2, 2],[0, 0, 0, 1])
        self.blok_L_inv = ([0, 1, 2, 2],[1, 1, 1, 0])
        self.blok_sq = ([0, 0, 1, 1],[0, 1, 0, 1])
        self.blok_line = ([0, 0, 0, 0],[0, 1, 2, 3])
        self.blok_T = ([0, 1, 2, 1],[0, 0, 0, 1])
    
        self.rand_blok = rn.choice([self.blok_L, self.blok_L_inv, self.blok_sq, self.blok_line, self.blok_T]) # выбираем случайный блок
        
        self.new_blok = (np.array(self.rand_blok[0]), np.array(self.rand_blok[1])+5) # начальное положение блока
    
    def moveDownBlok(self):
        self.new_blok = (self.new_blok[0]+1, self.new_blok[1]) # опускаем блок на одну клетку вниз
    def moveRightBlok(self):
        self.new_blok = (self.new_blok[0], self.new_blok[1]+1) # двигаем блок вправо    
    def moveLeftBlok(self):
        self.new_blok = (self.new_blok[0], self.new_blok[1]-1) # двигаем блок влево    


blok = Blok()
game = GameField()
keyboard.add_hotkey("right", blok.moveRightBlok)
keyboard.add_hotkey("left", blok.moveLeftBlok)

game.field_arr[blok.new_blok] = 2
game.redrawField()

def render_func(interval):
    while True:
        os.system('cls')
        game.redrawField()
        time.sleep(interval)
thread = Thread(target=render_func, args=(0.04, ))
thread.deamon = True
thread.start()

for i in range(game.field_arr.shape[0]-3):
    game.field_arr[blok.new_blok] = 0
    
    blok.moveDownBlok()  
    game.field_arr[blok.new_blok] = 2
    
    
    time.sleep(1)
    
    
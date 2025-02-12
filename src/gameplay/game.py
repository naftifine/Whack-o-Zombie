import pygame as pg
import sys

from src.gameplay.graveyard import Graveyard, load_graveyards
from src.gameplay.zombie import Zombie

zombies = [] 

pg.init()
pg.mixer.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

graveyards = load_graveyards("resources/data/graveyard.csv")    

class game:
    hit = 0
    miss = 0

    @staticmethod
    def start_game():
        global background_image
        print("Game is starting")
        background_image = pg.image.load("resources/graphic/game_background.png")
        
        for graveyard in graveyards:
            graveyard.start_rising()
        game.change_music()
    @staticmethod
    def change_music():
        pg.mixer.music.stop()  
        pg.mixer.music.load("resources/sounds/game_bgm.mp3") 
        pg.mixer.music.set_volume(0.01)
        pg.mixer.music.play(-1, 0.0)  

    def draw():
        screen.blit(background_image, (0, 0))
        for graveyard in graveyards:  
            graveyard.draw(screen)
            graveyard.update()
        
        
        
import pygame as pg
import sys
import random

from src.mouse import CustomMouse
from src.gameplay.game import game
from src.gameplay.zombie import Zombie, graveyard_positions

pg.init()
clock = pg.time.Clock()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Toi danh dau zombie yessir")

background_image = pg.image.load("resources/graphic/menu_background.png")
background_image = pg.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

custom_mouse = CustomMouse(screen, offset=(-20,-25))
custom_mouse.hide_default_cursor()

pg.mixer.init()
pg.mixer.music.load("resources/sounds/menu_bgm.mp3")
pg.mixer.music.set_volume(0.01)
pg.mixer.music.play(-1, 0.0)

font = pg.font.Font(None, 40)
text = font.render("PvZ 2-5 revival", True, (255, 255, 255))
text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

def reset_game():
    global game_active, zombies, spawn_timer, spawn_interval, start_time, total_click, hit
    game_active = False
    zombies.clear()
    spawn_timer = 1
    spawn_interval = 180
    start_time = None
    
    total_click = 0
    hit = 0

    pg.mixer.music.load("resources/sounds/menu_bgm.mp3") 
    pg.mixer.music.set_volume(0.01)
    pg.mixer.music.play(-1, 0.0)  

def show_end_screen(message):
    end_font = pg.font.Font(None, 80)
    text = end_font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pg.display.flip()
    pg.time.delay(5000)
    reset_game()

def main():
    global background_image, game_active, zombies, spawn_timer, spawn_interval, start_time, total_click, hit
    running = True
    game_active = False
    zombies = []
    spawn_timer = 1
    spawn_interval = 180
    start_time = None

    total_click = 0
    hit = 0

    limit_time = 30

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_SPACE and not game_active:
                    game_active = True
                    game.start_game()
                    start_time = pg.time.get_ticks()
                if event.key == pg.K_p:
                    pg.mixer.music.stop()
                    game_active = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    custom_mouse.start_animation(game_active)
                    if game_active:
                        total_click += 1
                        for zombie in zombies:
                            if zombie.check_click(event.pos):
                                hit += 1
                    print(total_click, hit)

        if game_active:
            game.draw()
            spawn_timer += 1
            if spawn_timer > spawn_interval:
                spawn_x, spawn_y = random.choice(graveyard_positions)
                zombies.append(Zombie(spawn_x - 110, spawn_y - 144))
                spawn_timer = 0
                spawn_interval = random.randint(45, 75)

            for zombie in zombies:
                if zombie.update():
                    zombie.draw(screen)
                    if zombie.x <= 100:  
                        show_end_screen("You Lose")
                else:
                    zombies.remove(zombie)

            if start_time and pg.time.get_ticks() - start_time >= limit_time*1000:
                show_end_screen("You Win")

        else:
            screen.blit(background_image, (0, 0))
            screen.blit(text, text_rect)

        pos = pg.mouse.get_pos()
        custom_mouse.update(pos)

        pg.display.flip()
        clock.tick(60)

    pg.quit()
    sys.exit()

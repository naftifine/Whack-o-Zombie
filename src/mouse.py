import pygame as pg
import time

class CustomMouse:
    def __init__(self, screen, sprite_images, offset=(0, 0)):
        self.screen = screen
        self.sprites = [
            pg.transform.scale(pg.image.load(img).convert_alpha(), (pg.image.load(img).get_width() // 4, pg.image.load(img).get_height() // 4))
            for img in sprite_images
        ]
        self.animation_sequence = list(range(len(self.sprites))) + list(range(len(self.sprites) - 2, 0, -1))
        self.current_sprite = 0
        self.animation_time = 0.015
        self.last_update = 0
        self.animating = False
        self.offset = offset 

        self.sound_effect = pg.mixer.Sound("resources/sounds/mouse.mp3")
        self.sound_effect.set_volume(0.2)

    def start_animation(self, game_active):

        self.animating = True
        self.current_sprite = 0
        self.last_update = time.time()

        if game_active:
            self.sound_effect.play()
        pos = pg.mouse.get_pos()
        # print(pos)
        return pos

    def update(self, pos):
        if self.animating:
            now = time.time()
            if now - self.last_update >= self.animation_time:
                self.current_sprite += 1
                self.last_update = now
                if self.current_sprite >= len(self.animation_sequence):
                    self.current_sprite = 0
                    self.animating = False

        frame = self.animation_sequence[self.current_sprite]
        x, y = pos
        offset_x, offset_y = self.offset
        self.screen.blit(self.sprites[frame], (x + offset_x, y + offset_y))
        
    @staticmethod
    def hide_default_cursor():
        pg.mouse.set_visible(False)

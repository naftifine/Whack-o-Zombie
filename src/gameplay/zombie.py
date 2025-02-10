import pygame as pg
import os
import random

graveyard_positions = [
    (620, 170), (700, 170), (780, 170), (860, 170), (940, 170),
    (620, 270), (700, 270), (780, 270), (860, 270), (940, 270),
    (620, 370), (700, 370), (780, 370), (860, 370), (940, 370),
    (620, 470), (700, 470), (780, 470), (860, 470), (940, 470),
    (620, 570), (700, 570), (780, 570), (860, 570), (940, 570)
]

class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y + 50  
        self.target_y = y  
        self.sprites = self.load_sprites()
        self.current_frame = 0
        self.image = self.sprites[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.alpha = 0  
        self.fading_in = True
        self.rising = True  
        self.moving = False  
        self.dead = False
        original_death_image = pg.image.load("resources/graphic/Pow.png").convert_alpha()
        width, height = original_death_image.get_size()  # Lấy kích thước gốc
        self.death_image = pg.transform.scale(original_death_image, (width // 2, height // 2))
        self.death_timer = 0
    
    def load_sprites(self):
        sprites = []
        for i in range(1, 22):
            path = f"resources/graphic/zombie/Zombie_{i}.png"
            sprite = pg.image.load(path).convert_alpha()
            sprites.append(sprite)
        return sprites
    
    def update(self):
        if not self.dead:
            if self.fading_in:
                self.alpha += 15
                if self.alpha >= 255:
                    self.alpha = 255
                    self.fading_in = False
            
            if self.rising:
                self.y -= 5
                if self.y <= self.target_y:
                    self.y = self.target_y
                    self.rising = False
                    self.moving = True  # Bắt đầu di chuyển sau khi trồi lên
            
            if self.moving:
                self.x -= 2
            
            self.image = self.sprites[self.current_frame]
            self.image.set_alpha(self.alpha)
            
            self.rect.x = self.x
            self.rect.y = self.y
            
            self.current_frame = (self.current_frame + 1) % len(self.sprites)
        else:
            self.death_timer += 1
            if self.death_timer >= 22:  # Khoảng 0.75s với 30 FPS
                return False  # Xóa zombie
        return True
    
    def draw(self, screen):
        if self.dead:
            offset_x = 50
            offset_y = 72
            screen.blit(self.death_image, (self.rect.x + offset_x, self.rect.y + offset_y))
        else:
            screen.blit(self.image, self.rect.topleft)
    
    def check_click(self, pos):
        if self.rect.collidepoint(pos) and not self.dead:
            self.dead = True
            self.death_timer = 0
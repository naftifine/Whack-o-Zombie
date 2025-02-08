import pygame as pg
import random
import csv

class Graveyard:
    IMAGE_PATHS = [
        "resources/graphic/graveyard/graveyard1.png",
        "resources/graphic/graveyard/graveyard2.png",
        "resources/graphic/graveyard/graveyard3.png"
    ]

    def __init__(self, x, y, speed):
        image_path = random.choice(self.IMAGE_PATHS)
        sound_path = "resources/sounds/graveyard.mp3"

        self.image = pg.image.load(image_path).convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(midbottom=(x, y + 50))

        self.sound = pg.mixer.Sound(sound_path)
        self.sound.set_volume(0.1)

        self.speed = speed
        self.alpha = 0  # Bắt đầu ẩn
        self.image.set_alpha(self.alpha)
        self.is_rising = False
        self.target_y = y

    def start_rising(self):
        if self.is_rising == False:
            self.sound.play()

        self.is_rising = True

    def update(self):
        if self.is_rising:
            if self.rect.bottom > self.target_y:
                self.rect.y -= self.speed  
            if self.alpha < 255:
                self.alpha += 5
                if self.alpha > 255:
                    self.alpha = 255
                self.image = self.original_image.copy()
                self.image.set_alpha(self.alpha)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def load_graveyards(filename):
    graveyards = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            x = int(row['x'])
            y = int(row['y'])
            speed = float(row['speed'])
            graveyards.append(Graveyard(x, y, speed))
    return graveyards


import pygame as pg

class TimerBar:
    def __init__(self, x, y, width, height, max_time, screen):
        self.x = x
        self.y = y
        self.width = width * 2
        self.height = height * 2
        self.max_time = max_time
        self.remaining_time = max_time
        self.screen = screen
        
        self.bg_image = pg.image.load("resources/graphic/progressbar/Bar_1.png")
        self.fg_image = pg.image.load("resources/graphic/progressbar/Bar_2.png")
        self.part_image = pg.image.load("resources/graphic/progressbar/Bar_part.png")  
        
        self.bg_image = pg.transform.scale(self.bg_image, (self.width, self.height))
        self.fg_image = pg.transform.scale(self.fg_image, (self.width, self.height))
        self.part_image = pg.transform.scale(self.part_image, (self.height, self.height))  
        
    def update(self, dt):
        self.remaining_time -= dt
        if self.remaining_time < 0:
            self.remaining_time = 0
        
    def draw(self):
        """Draw the timer bar and moving part on the screen."""
        self.screen.blit(self.bg_image, (self.x, self.y))
        
        fg_width = int((self.remaining_time / self.max_time) * (151 - 7) * 2) 
        if fg_width > 0:
            fg_clip = self.fg_image.subsurface((0, 0, fg_width, self.height))
            self.screen.blit(fg_clip, (self.x, self.y))
        
        part_x = self.x + fg_width - self.part_image.get_width() // 2
        part_y = self.y + (self.height - self.part_image.get_height()) // 2
        
        self.screen.blit(self.part_image, (part_x + 14, part_y))
    def reset(self, max_time):
        self.max_time = max_time
        self.remaining_time = max_time

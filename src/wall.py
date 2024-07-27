import pygame
from random import randint


wall = pygame.image.load("src/wall.png")

class Wall():
    def __init__(self, display_w: int, display_h: int):
        self.display_w = display_w
        self.display_h = display_h
        self.gap_width = 2  # Gånger bildens bredd

        self.clear()

    def clear(self):
        """Nollställer position och hastighet och antal klarade."""
        self.img_width, img_height = wall.get_size()
        self.y_start = -img_height - 1
        self.y = self.y_start
        self.speed = 2
        self.walls_completed = 0
        self.random_gap()

    def update(self):
        """Uppdaterar positionen på väggen."""
        self.y += self.speed
        if self.y > self.display_h:
            self.y = self.y_start
            self.random_gap()
            self.speed += 1
            self.walls_completed += 1

    def random_gap(self):
        """Uppdaterar vart hålet i väggen ska vara."""
        self.gap = randint(0, self.display_w // self.img_width - self.gap_width)

    def render(self, screen: pygame.Surface):
        """Rita ut väggbilden om dess position är lägre eller högre än hålet."""
        self.walls = []
        for i in range(0, self.display_w//self.img_width+1):
            if i < self.gap or i >= self.gap + self.gap_width:
                self.walls.append(screen.blit(wall, (i*self.img_width, self.y)))

    def collide(self, player_rect: pygame.Rect):
        """Kontrollera om spelaren krockar med väggen."""
        if player_rect.collidelist(self.walls) >= 0:
            return True
        return False

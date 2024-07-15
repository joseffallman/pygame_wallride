# 1 - Import library
from typing import Any
import pygame
from pygame.event import Event
from pygame.locals import *
from random import randint

# 2 - Initialize the game
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 60)

info = pygame.display.Info()
width, height = info.current_w,info.current_h

width, height = 64*10, 64*8
screen=pygame.display.set_mode((width, height))
player_x = 256
player_y = height//2

frame = 50
clock = pygame.time.Clock()


# 3 - Load images
player = pygame.image.load("src/plan.png")
playerH = pygame.image.load("src/plan_H.png")
playerV = pygame.image.load("src/plan_V.png")
wall = pygame.image.load("src/wall.png")
walls = []
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

class Screen():
    def __init__(self):
        self.next_screen = self

    def update(self):
        """Update or make changes to the screen. """

    def render(self, screen: pygame.Surface):
        """Render the layout of the screen."""
        raise NotImplementedError

    def handle_events(self, events: list[pygame.event.Event], screen: pygame.Surface):
        """Handle all events on this screen."""
        raise NotImplementedError


class Wall():
    def __init__(self, wall: pygame.Surface, display_w: int, display_h: int):
        w, h = wall.get_size()
        self.y_start = -h - 1
        self.display_w = display_w
        self.display_h = display_h
        self.img_width = w
        self.gap_width = 2  # Gånger bildens bredd
        self.wall = wall

        self.clear()

    def clear(self):
        """Nollställer position och hastighet och antal klarade."""
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
                self.walls.append(screen.blit(self.wall, (i*self.img_width, self.y)))

    def collide(self, player_rect: pygame.Rect):
        """Kontrollera om spelaren krockar med väggen."""
        if player_rect.collidelist(self.walls) >= 0:
            return True
        return False

class GameOver(Screen):
    def __init__(self):
        super().__init__()
        self.walls_completed = 0

    def render(self, screen: pygame.Surface):
        screen.fill((255,255,255))          # Rita ut en vit spelplan
        text = "Game over"
        text2 = f"You did {self.walls_completed} walls."
        text_w, text_h = myfont.size(text)
        text2_w, text2_h = myfont.size(text2)
        textsurface = myfont.render(text, False, (0, 0, 0))
        textsurface2 = myfont.render(text2, False, (0,0,0))
        # Skapa en textrad
        screen.blit(textsurface,(width//2-text_w/2, height//2))
        screen.blit(textsurface2, (width//2-text2_w/2, height//2+text_h))

    def handle_events(self, events: list[Event], screen: pygame.Surface):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if (event.type == pygame.KEYDOWN and event.key == K_RETURN) or event.type == pygame.FINGERUP:
                self.next_screen = StartScreen()


class StartScreen(Screen):
    def __init__(self):
        super().__init__()
    
    def render(self, screen: pygame.Surface):
        
        # Rita ut en vit spelplan
        screen.fill((255,255,255))
        text = "Press enter to start"
        text_w, text_h = myfont.size(text)
        # Skapa en textrad
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(width//2-text_w/2, height//2))
    
    def handle_events(self, events: list[Event], screen: pygame.Surface):
        for event in events:
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit(0)

            if (event.type == pygame.KEYDOWN and event.key==K_RETURN) or event.type == pygame.FINGERUP:
                # Start game
                self.next_screen = PlayScreen()


class PlayScreen(Screen):
    def __init__(self):
        super().__init__()

        # Skapa en ny vägg
        self.wall = Wall(wall, width, height)
        self.player_x = player_x
        self.player_y = player_y
        
        self.keys = [False, False, False, False]

    def update(self):
        self.wall.update()

        # Uppdatera spelarens position
        if self.keys[UP]:
            if self.player_y > 0:
                self.player_y -= 10
        elif self.keys[DOWN]:
            if self.player_y < height-64: 
                self.player_y += 10
        if self.keys[LEFT]: 
            if self.player_x > 0:
                self.player_x -= 10
        elif self.keys[RIGHT]:
            if self.player_x < width-64:
                self.player_x += 10

    def render(self, screen: pygame.Surface):
        screen.fill((255,255,255))

        # Bestäm vilken bild som ska synas för spelaren
        if self.keys[LEFT]:
            playerImage = playerV
        elif self.keys[RIGHT]:
            playerImage = playerH
        else:
            playerImage = player
        player_rect = screen.blit(playerImage, (self.player_x, self.player_y))

        textsurface = myfont.render(str(self.wall.walls_completed), False, (0, 0, 0))
        screen.blit(textsurface,(10, 0))

        self.wall.render(screen)

        if self.wall.collide(player_rect):
            self.next_screen = GameOver()
            self.next_screen.walls_completed = self.wall.walls_completed

    def handle_events(self, events: list[Event], screen: pygame.Surface):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit() 
                exit(0) 

            if event.type == pygame.KEYDOWN:
                if event.key==K_UP:
                    self.keys[UP]=True
                elif event.key==K_LEFT:
                    self.keys[LEFT]=True
                elif event.key==K_DOWN:
                    self.keys[DOWN]=True
                elif event.key==K_RIGHT:
                    self.keys[RIGHT]=True

            if event.type == pygame.KEYUP:
                if event.key==pygame.K_UP:
                    self.keys[UP]=False
                elif event.key==pygame.K_LEFT:
                    self.keys[LEFT]=False
                elif event.key==pygame.K_DOWN:
                    self.keys[DOWN]=False
                elif event.key==pygame.K_RIGHT:
                    self.keys[RIGHT]=False

            # Touch
            if event.type == pygame.FINGERDOWN:
                finger_x = event.x * screen.get_width()
                finger_y = event.y * screen.get_height()
                if finger_x < player_x:
                    self.keys[LEFT] = True
                else:
                    self.keys[RIGHT] = True
                #if finger_y < player_y:
                    #keys[UP] = True
                #else:
                    #keys[DOWN] = True

            if event.type == pygame.FINGERUP:
                self.keys[RIGHT] = False
                self.keys[LEFT] = False
                self.keys[UP] = False
                self.keys[DOWN] = False


running_screen: Screen = StartScreen()
# Loopa föralltid
while 1:
    event_list = pygame.event.get()

    # Hantera knapptryckningar
    running_screen.handle_events(event_list, screen)

    # Uppdatera vad som ska synas.
    running_screen.update()

    # Rita upp allt igen.
    running_screen.render(screen)

    # Uppdatera skärmen
    pygame.display.flip()

    running_screen = running_screen.next_screen

    clock.tick(frame)

        
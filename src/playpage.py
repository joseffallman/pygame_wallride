import pygame
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT
from page import Page, Pages
from wall import Wall

player = pygame.image.load("src/plan.png")
playerH = pygame.image.load("src/plan_H.png")
playerV = pygame.image.load("src/plan_V.png")


# Skapa några konstanter som underlättar åt vilket håll spelaren rör sig
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

class PlayPage(Page):

    def __init__(self, all_pages, screen, font):
        super().__init__(all_pages, screen, font)

        # Spara skärmen i en variabel för att återanvända den senare.
        self.screen = screen
        self.new()

    def restore(self):
        super().restore()
        self.new()

    def new(self):
        # Skapa en ny vägg med skärmens storlekar.
        self.screen_w, self.screen_h = self.screen.get_size()
        self.wall = Wall(self.screen_w, self.screen_h)

        # Bestäm var spelaren ska vara i början
        self.player_x = self.screen_w//2
        self.player_y = self.screen_h//2
        
        # Skapa variabeln som håller åt vilket håll spelaren vill röra sig.
        self.keys = [False, False, False, False]

    def update(self):
        # Uppdatera väggen.
        self.wall.update()

        # Uppdatera spelarens position
        if self.keys[UP]:
            if self.player_y > 0:
                self.player_y -= 10
        elif self.keys[DOWN]:
            if self.player_y < self.screen_h-64: 
                self.player_y += 10

        if self.keys[LEFT]: 
            if self.player_x > 0:
                self.player_x -= 10
        elif self.keys[RIGHT]:
            if self.player_x < self.screen_w-64:
                self.player_x += 10

    def render(self, screen: pygame.Surface):
        # Rita ut en vit spelplan
        screen.fill((255,255,255))

        # Bestäm vilken bild som ska synas för spelaren
        if self.keys[LEFT]:
            playerImage = playerV
        elif self.keys[RIGHT]:
            playerImage = playerH
        else:
            playerImage = player
        # Skapa spelarbilden på spelarens position.
        player_rect = screen.blit(playerImage, (self.player_x, self.player_y))

        # Skriv ut antal avklarade väggar.
        textsurface = self.myfont.render(str(self.wall.walls_completed), False, (0, 0, 0))
        screen.blit(textsurface,(10, 0))

        # Lägg till väggen på skärmen.
        self.wall.render(screen)

        # Kontrollera om väggen krockar med spelaren.
        if self.wall.collide(player_rect):
            # Gå till GameOver sidan och spara antal avklarade väggar.
            self.next_page = self.all_pages[Pages.GameOver]
            self.next_page.walls_completed = self.wall.walls_completed

    def handle_events(self, events: list[pygame.event.Event], screen: pygame.Surface):
        # Hantera alla tangentryckningar och touch
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
                if event.key==K_UP:
                    self.keys[UP]=False
                elif event.key==K_LEFT:
                    self.keys[LEFT]=False
                elif event.key==K_DOWN:
                    self.keys[DOWN]=False
                elif event.key==K_RIGHT:
                    self.keys[RIGHT]=False

            # Om ett finger trycks ned på touchskärmen.
            if event.type == pygame.FINGERDOWN:
                # Kontrollera vart fingret trycks ned.
                finger_x = event.x * screen.get_width()
                finger_y = event.y * screen.get_height()

                # Om fingret är till vänster eller höger om spelaren.
                if finger_x < self.player_x:
                    self.keys[LEFT] = True
                else:
                    self.keys[RIGHT] = True

                # Om fingret är ovanför eller under spelaren.
                if finger_y < self.player_y:
                    self.keys[UP] = True
                else:
                    self.keys[DOWN] = True

            # Om fingret lyfts upp från touchskärmen.
            if event.type == pygame.FINGERUP:
                self.keys[RIGHT] = False
                self.keys[LEFT] = False
                self.keys[UP] = False
                self.keys[DOWN] = False
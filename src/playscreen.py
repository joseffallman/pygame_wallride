import pygame
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT
from screens import Screen, Screens
from wall import Wall

wall = pygame.image.load("src/wall.png")
player = pygame.image.load("src/plan.png")
playerH = pygame.image.load("src/plan_H.png")
playerV = pygame.image.load("src/plan_V.png")

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

class PlayScreen(Screen):

    def __init__(self, all_screens, screen, font):
        super().__init__(all_screens, screen, font)

        self.screen = screen
        self.clear()

    def restore(self):
        super().restore()
        self.clear()

    def clear(self):
        # Skapa en ny vägg
        self.screen_w, self.screen_h = self.screen.get_size()
        self.wall = Wall(wall, self.screen_w, self.screen_h)
        self.player_x = self.screen_w//2
        self.player_y = self.screen_h//2
        
        self.keys = [False, False, False, False]

    def update(self):
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
        screen.fill((255,255,255))

        # Bestäm vilken bild som ska synas för spelaren
        if self.keys[LEFT]:
            playerImage = playerV
        elif self.keys[RIGHT]:
            playerImage = playerH
        else:
            playerImage = player
        player_rect = screen.blit(playerImage, (self.player_x, self.player_y))

        textsurface = self.myfont.render(str(self.wall.walls_completed), False, (0, 0, 0))
        screen.blit(textsurface,(10, 0))

        self.wall.render(screen)

        if self.wall.collide(player_rect):
            self.next_screen = self.all_screens[Screens.GameOver]
            self.next_screen.walls_completed = self.wall.walls_completed

    def handle_events(self, events: list[pygame.event.Event], screen: pygame.Surface):
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
                if finger_x < self.player_x:
                    self.keys[LEFT] = True
                else:
                    self.keys[RIGHT] = True
                #if finger_y < self.player_y:
                    #keys[UP] = True
                #else:
                    #keys[DOWN] = True

            if event.type == pygame.FINGERUP:
                self.keys[RIGHT] = False
                self.keys[LEFT] = False
                self.keys[UP] = False
                self.keys[DOWN] = False
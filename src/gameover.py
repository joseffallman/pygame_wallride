import pygame
from pygame.locals import K_RETURN
from screens import Screen, Screens


class GameOver(Screen):
    walls_completed: int

    def __init__(self, all_screens, screen, font):
        super().__init__(all_screens, screen, font)
        self.walls_completed = 0

    def render(self, screen: pygame.Surface):
        screen.fill((255,255,255))          # Rita ut en vit spelplan
        screen_w, screen_h = screen.get_size()
        text = "Game over"
        text2 = f"You did {self.walls_completed} walls."
        text_w, text_h = self.myfont.size(text)
        text2_w, text2_h = self.myfont.size(text2)
        textsurface = self.myfont.render(text, False, (0, 0, 0))
        textsurface2 = self.myfont.render(text2, False, (0,0,0))
        # Skapa en textrad
        screen.blit(textsurface,(screen_w//2-text_w/2, screen_h//2))
        screen.blit(textsurface2, (screen_w//2-text2_w/2, screen_h//2+text_h))

    def handle_events(self, events: list[pygame.event.Event], screen: pygame.Surface):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if (event.type == pygame.KEYDOWN and event.key == K_RETURN) or event.type == pygame.FINGERUP:
                self.next_screen = self.all_screens[Screens.StartScreen]

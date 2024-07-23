import pygame
from pygame.locals import K_RETURN
from screens import Screen, Screens

from playscreen import PlayScreen


class StartScreen(Screen):

    def __init__(self, all_screens, screen, font):
        super().__init__(all_screens, screen, font)
    
    def render(self, screen: pygame.Surface):
        # Rita ut en vit spelplan
        screen.fill((255,255,255))
        screen_w, screen_h = screen.get_size()
        text = "Press enter to start"
        text_w, text_h = self.myfont.size(text)
        # Skapa en textrad
        textsurface = self.myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(screen_w//2-text_w/2, screen_h//2))
    
    def handle_events(self, events: list[pygame.event.Event], screen: pygame.Surface):
        for event in events:
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit(0)

            if (event.type == pygame.KEYDOWN and event.key==K_RETURN) or event.type == pygame.FINGERUP:
                # Start game
                # self.all_screens[Screens.PlayScreen] = PlayScreen(self.all_screens, screen, self.myfont)
                # self.all_screens[Screens.PlayScreen].clear(screen)
                # self.next_screen = PlayScreen(self.all_screens, screen, self.myfont)
                self.next_screen = self.all_screens[Screens.PlayScreen]

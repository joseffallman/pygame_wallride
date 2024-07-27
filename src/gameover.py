import pygame
from pygame.locals import K_RETURN
from page import Page, Pages


class GameOver(Page):
    def __init__(self, all_pages, screen, font):
        super().__init__(all_pages, screen, font)
        self.walls_completed: int = 0

    def render(self, screen: pygame.Surface):
        # Rita ut en vit spelplan
        screen.fill((255,255,255))

        # Hämta storleken på skärmen för att senare räkna ut mitten
        screen_w, screen_h = screen.get_size()

        # Bestäm vilken text som ska skrivas.
        text = "Game over"
        text2 = f"You did {self.walls_completed} walls."

        # Räkna ut hur stor texten kommer bli
        text_w, text_h = self.myfont.size(text)
        text2_w, text2_h = self.myfont.size(text2)

        # Skapa en bild med texten
        textsurface = self.myfont.render(text, False, (0, 0, 0))
        textsurface2 = self.myfont.render(text2, False, (0,0,0))
        
        # Placera text-bilden på sidan
        screen.blit(textsurface,(screen_w//2-text_w/2, screen_h//2))
        screen.blit(textsurface2, (screen_w//2-text2_w/2, screen_h//2+text_h))

    def handle_events(self, events: list[pygame.event.Event], screen: pygame.Surface):
        # Hantera alla tangentryckningar och touch
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            # Om tangen trycks ner och den tangenten är 'return' eller om fingret lyfts upp från skärmen.
            if (event.type == pygame.KEYDOWN and event.key == K_RETURN) or event.type == pygame.FINGERUP:
                # Gå tillbaka till startskärmen
                self.next_page = self.all_pages[Pages.Start]

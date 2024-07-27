import pygame
from pygame.locals import K_RETURN
from page import Page, Pages


class StartPage(Page):
    def __init__(self, all_pages, screen, font):
        super().__init__(all_pages, screen, font)

    def render(self, screen: pygame.Surface):
        # Rita ut en vit spelplan
        screen.fill((255,255,255))

        # Hämta storleken på skärmen för att senare räkna ut mitten
        screen_w, screen_h = screen.get_size()

        # Bestäm vilken text som ska skrivas.
        text = "Press enter to start"

        # Räkna ut hur stor texten kommer bli
        text_w, text_h = self.myfont.size(text)

        # Skapa en bild med texten
        textsurface = self.myfont.render(text, False, (0, 0, 0))

        # Placera text-bilden på sidan
        screen.blit(textsurface,(screen_w//2-text_w/2, screen_h//2))

    def handle_events(self, events: list[pygame.event.Event], screen: pygame.Surface):
        # Hantera alla tangentryckningar och touch
        for event in events:
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit(0)

            # Om tangen trycks ner och den tangenten är 'retur' eller om fingret lyfts upp från skärmen.
            if (event.type == pygame.KEYDOWN and event.key==K_RETURN) or event.type == pygame.FINGERUP:
                # Starta spelet
                self.next_page = self.all_pages[Pages.Play]

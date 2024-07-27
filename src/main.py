# Importa biblioteken som behövs.
import pygame

from page import Page, Pages
from gameover import GameOver
from startpage import StartPage
from playpage import PlayPage

# Initialize the game
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 60)

# Räkna ut skärmens storlek.
info = pygame.display.Info()
windoWidth, windowHeight = info.current_w,info.current_h
display = pygame.display.set_mode(size=(windoWidth, windowHeight), flags=pygame.RESIZABLE)

# Skapa en ny rityta i önskad storlek som skalas upp till att passa skärmen.
width, height = 64*10, 64*8
screen = pygame.transform.scale(pygame.Surface((width, height)), (windoWidth, windowHeight))

# Bestäm hur snabbt skärmen ska uppdateras, hur många "bilder i sekunden" ska visas på skärmen.
frame = 50
clock = pygame.time.Clock()

# Skapa alla sidor som ska visas.
all_pages = {}
all_pages[Pages.Start] = StartPage(all_pages, screen, myfont)
all_pages[Pages.Play] = PlayPage(all_pages, screen, myfont)
all_pages[Pages.GameOver] = GameOver(all_pages, screen, myfont)

running_screen: Page = all_pages[Pages.Start]
# Loopa föralltid
while 1:
    event_list = pygame.event.get()

    # Hantera knapptryckningar.
    running_screen.handle_events(event_list, screen)

    # Uppdatera vad som ska synas.
    running_screen.update()

    # Rita upp allt igen.
    running_screen.render(screen)

    # Placera den uppskalade ritytan på skärmen.
    display.blit(screen,(0,0))

    # Gå till nästa sida.
    if running_screen is not running_screen.next_screen:
        new_screen = running_screen.next_screen
        running_screen.restore()
        running_screen = new_screen

    # Uppdatera skärmen.
    pygame.display.flip()

    # Vänta tills det är dags att uppdatera skärmen igen så vi håller önskad antal "bilder i sekunden".
    clock.tick(frame)


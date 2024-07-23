# 1 - Import library
import pygame

from screens import Screen, Screens
from gameover import GameOver
from startscreen import StartScreen
from playscreen import PlayScreen

# 2 - Initialize the game
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 60)

info = pygame.display.Info()
width, height = info.current_w,info.current_h

width, height = 64*10, 64*8
screen=pygame.display.set_mode((width, height))

frame = 50
clock = pygame.time.Clock()

# 3 - Skapa alla sidor som ska visas
all_screens = {}
all_screens[Screens.StartScreen] = StartScreen(all_screens, screen, myfont)
all_screens[Screens.PlayScreen] = PlayScreen(all_screens, screen, myfont)
all_screens[Screens.GameOver] = GameOver(all_screens, screen, myfont)

running_screen: Screen = all_screens[Screens.StartScreen]
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

    if running_screen is not running_screen.next_screen:
        new_screen = running_screen.next_screen
        running_screen.restore()
        running_screen = new_screen


    clock.tick(frame)


from abc import ABC, abstractmethod
import pygame
from enum import Enum


# Bara för att förenkla vilka olika sidor vi vill använda
class Pages(Enum):
    Start = 1
    Play = 2
    GameOver = 3

# Definera vad en sida ska innehålla för funktioner.
class Page(ABC):
    """Abstract class to define a page."""
    myfont: pygame.font.Font

    def __init__(self, all_pages: dict, screen: pygame.Surface, font: pygame.font.Font):
        self.next_screen: Page = self
        self.all_pages = all_pages
        self.myfont = font

    def restore(self):
        self.next_screen = self

    def update(self):
        """Update or make changes to the screen. """

    @abstractmethod
    def render(self, screen: pygame.Surface):
        """Render the layout of the screen."""
        raise NotImplementedError

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event], screen: pygame.Surface):
        """Handle all events on this screen."""
        raise NotImplementedError
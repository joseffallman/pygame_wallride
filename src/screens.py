from abc import ABC, abstractmethod
import pygame
from enum import Enum

class Screens(Enum):
    StartScreen = 1
    PlayScreen = 2
    GameOver = 3

class Screen(ABC):
    myfont: pygame.font.Font

    """Abstract class to define a screen or page."""
    def __init__(self, all_screens: dict, screen: pygame.Surface, font: pygame.font.Font):
        self.next_screen: Screen = self
        self.all_screens = all_screens
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
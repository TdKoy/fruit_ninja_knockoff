import pygame
import pygame.freetype


class GameScreen:
    def __init__(self, display_size):
        self.init_pygame_screen()
        self.screen = pygame.display.set_mode(display_size)
        self.background = ()

    def init_pygame_screen(self):
        pygame.init()
        pygame.display.set_caption("Shitty Fruit Ninja")



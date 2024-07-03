import pygame


class Score:
    def __init__(self):
        self.score = 0
        self.SCORE_TICK = 10

    def draw_score(self, surface, text, font, color=pygame.Color("tomato")):
        text_surface = font.render(text, True, color)

        rect = text_surface.get_rect()
        rect.center = pygame.math.Vector2(surface.get_size()[0] * 0.5, surface.get_size()[1] * (1 / 8))

        surface.blit(text_surface, rect)

    def display_score(self, surface, font, color=pygame.Color("tomato")):
        text = f"Score: {self.score}"
        self.draw_score(surface, text, font, color)

    def tick_up_score(self):
        if self.score > 500:
            self.SCORE_TICK = 25
        if self.score > 1750:
            self.SCORE_TICK = 50
        if self.score > 3250:
            self.SCORE_TICK = 50
        if self.score > 7500:
            self.SCORE_TICK = 100
        self.score += self.SCORE_TICK

    def add_to_score(self, number):
        self.score += number

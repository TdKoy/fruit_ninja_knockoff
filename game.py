import pygame
import pygame.freetype
from game_screen import GameScreen
from models import Pointer, Fruit
from score import Score
from utilities import print_text, print_bust

SCREEN_SIZE = (800, 600)

class FruitNinja:
    BREAK_TIME = 180
    spawn_rate = 60
    TICKER = 0
    def __init__(self):
        self.game_screen = GameScreen(SCREEN_SIZE)
        self.game_screen.init_pygame_screen()
        self.clock = pygame.time.Clock()

        #game objects
        self.pointer = Pointer((400, 300))

        self.message = ""
        self.bust_message = ""
        self.font = pygame.font.Font(None, 64)

        self.fruits = []
        self.sliced_fruits = []
        self.bust = False
        self.bust_time = 120
        self.bust_start = 0
        self.score_class = Score()
    def main_loop(self):
        while True:
            self.handle_input()
            self.process_game_logic()
            self.draw_objects()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()
            if not self.bust:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                    self.pointer.slash_mode(self.bust)

        if pygame.mouse.get_rel():
            if self.pointer:
                self.pointer.accelerate(pygame.mouse.get_pos())

    def draw_game_over_screen(self):
        text = "Game Over"
        title_font = pygame.freetype.Font("game_font.ttf", 200)
        title, _ = title_font.render(text, (255, 255, 255))
        self.game_screen.screen.blit(title, (self.game_screen.screen.get_width() / 2 - title.get_width() / 2,
                                             self.game_screen.screen.get_height() / 2.5 - title.get_height() / 2.5))

    def bust_logic(self):
        if not self.bust:
            return

        if (self.pointer.counter - self.bust_start) > self.bust_time:
            self.bust = False

    def slash_time_logic(self):
        self.pointer.counter += 1
        if self.pointer.slash_mode_toggle:
            if self.pointer.counter > self.pointer.SLASH_TIME:
                self.pointer.run_mode()
                self.bust_start = self.pointer.counter
                self.bust = True

    def process_game_logic(self):
        for game_object in self.get_game_objects():
            game_object.move()

        for sliced_fruit in self.sliced_fruits:
            sliced_fruit.decelerate()
            sliced_fruit.spin()


        for fruit in self.fruits:
            fruit.decelerate()
            fruit.spin()

            if fruit.position[1] > 800:
                self.fruits.remove(fruit)

            if self.pointer:
                if fruit.collides_with(self.pointer):
                    if self.pointer.slash_mode_toggle:
                        sliced_1, sliced_2 = fruit.collision(self.pointer)
                        self.sliced_fruits.append(sliced_1)
                        self.sliced_fruits.append(sliced_2)
                        self.fruits.remove(fruit)
                        self.score_class.add_to_score(fruit.score_value)
                    else:
                        self.pointer = None
                        self.message = "Game Over"
                        break
                if not self.pointer:
                    break

        if (self.TICKER / self.spawn_rate).is_integer():
            new_fruit = Fruit(self.score_class.score)
            self.fruits.append(new_fruit)

        if self.pointer:
            self.slash_time_logic()
            self.bust_logic()
            self.spawn_rate_logic()
            if self.TICKER % 60 == 1:
                self.score_class.tick_up_score()

    def bust_counter(self):
        if not self.pointer:
            return
        if not self.bust:
            return

        if (self.pointer.counter - self.bust_start) == 0:
            self.bust_message = 3
        elif ((self.pointer.counter - self.bust_start)/(self.bust_time/3)).is_integer():
            self.bust_message = self.bust_message - 1
        print_bust(self.game_screen.screen, str(self.bust_message), self.font)

    def spawn_rate_logic(self):
        if self.score_class.score > 500:
            self.spawn_rate = 30
        if self.score_class.score > 1750:
            self.spawn_rate = 20
        if self.score_class.score > 3250:
            self.spawn_rate = 15
        if self.score_class.score > 7500:
            self.spawn_rate = 10

    def draw_objects(self):
        self.game_screen.screen.fill((0, 0, 0))

        self.score_class.display_score(self.game_screen.screen, self.font)

        for game_object in self.get_game_objects():
            game_object.draw(self.game_screen.screen)

        self.bust_counter()

        if self.message:
            print_text(self.game_screen.screen, self.message, self.font)

        pygame.display.flip()

        self.TICKER += 1
        self.TICKER = self.TICKER % 60
        self.clock.tick(60)

    def get_game_objects(self):
        if self.pointer:
            game_objects = [*self.fruits, *self.sliced_fruits, self.pointer]
        else:
            game_objects = []
        return game_objects

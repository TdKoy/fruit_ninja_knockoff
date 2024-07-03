import pygame.sprite
from pygame.math import Vector2
from pygame.transform import rotozoom, rotate
from pygame import image
from utilities import load_sprite, watermelon_velocity_rules, lime_velocity_rules, point_to_edge_distance
from random import randint, choice

UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, velocity, sprite):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.counter = 0

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)  # blit draws from the top left, hence why we need line 11

    def redraw(self, sprite):
        self.sprite = sprite

    def collides_with(self, other_obj):
        # copy pasted over, will see if need this
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

    def move(self):
        self.position = self.position + self.velocity


class Pointer(GameObject):
    SLASH_TIME = 30

    def __init__(self, position):
        self.slash_mode_toggle = 0
        self.slash_start_time = 0
        self.acceleration = 10
        self.set_velocity = 15
        scale = 1.5
        sprite = rotozoom(load_sprite("ball"), 0, scale)

        super().__init__(position, (0, 0), sprite)

    def accelerate(self, mouse_position):
        self.velocity = Vector2(min(max(mouse_position[0] - self.position[0], -self.set_velocity),
                                    self.set_velocity), min(max(mouse_position[1] - self.position[1],
                                                                -self.set_velocity),
                                                            self.set_velocity))

    def slash_mode(self, bust):
        if bust:
            return

        if self.slash_mode_toggle == 0:
            self.counter = 0  # work on this

        if self.counter > self.SLASH_TIME:
            self.run_mode()
            print('ggs')
            bust = True
            return bust

        self.slash_mode_toggle = 1
        self.acceleration = 100
        self.set_velocity = 100
        sprite = rotozoom(load_sprite("red_ball"), 0, 1.5)
        self.redraw(sprite)

    def run_mode(self):
        self.slash_mode_toggle = 0
        self.acceleration = 10
        self.set_velocity = 15
        sprite = rotozoom(load_sprite("ball"), 0, 1.5)
        self.redraw(sprite)


class Fruit(GameObject):
    SCALES = {'lemon': 1,
              'lime': .7,
              'coconut': 1,
              'watermelon': 1
              }

    SCORES = {'lemon': 150,
              'lime': 250,
              'coconut': 100,
              'watermelon': 50
              }

    GRAVITY = 0.22

    rotation_velocity_constant = 1

    def __init__(self, score):
        pos_and_vel = {'lemon': self.lemons_position_and_velocity(),
                       'lime': self.lime_position_and_velocity(),
                       'coconut': self.coconut_position_and_velocity(),
                       'watermelon': self.watermelon_position_and_velocity()
                       }

        self.list = self.create_list(score)
        number = randint(0, len(self.list) - 1)
        self.type = self.list[number]
        self.score_value = self.SCORES[self.type]
        self.position, self.velocity = pos_and_vel[self.type]
        self.angle = 0
        self.rotation_direction = choice([-1, 1])
        scale = self.SCALES[self.type]
        self.sprite = rotozoom(load_sprite(self.type), 0, scale)
        self.original_sprite = self.sprite
        self.rect = self.sprite.get_rect(center=self.position)
        super().__init__(self.position, self.velocity, self.sprite)

    def decelerate(self):
        self.velocity[1] = self.velocity[1] + self.GRAVITY

    def spin(self):
        self.angle += self.rotation_velocity_constant * self.rotation_direction
        self.sprite = rotate(self.original_sprite, self.angle)

        # Get a new rect with the center of the old rect
        self.rect = self.sprite.get_rect(center=self.position)

    def watermelon_position_and_velocity(self):
        upper_velocity = 50
        lower_velocity = -40
        position = Vector2((randint(0, 600), 800))
        velocity = watermelon_velocity_rules(position, upper_velocity, lower_velocity)
        return position, velocity

    def coconut_position_and_velocity(self):
        position = Vector2((randint(0, 600), -100))
        velocity = Vector2(0, 0)
        return position, velocity

    def lime_position_and_velocity(self):
        upper_velocity = 30
        side_velocity = 20

        position_var = randint(1, 4)

        if position_var == 1:
            position = Vector2((randint(0, 600), -100))
        elif position_var == 2:
            position = Vector2((randint(0, 600), 800))
        elif position_var == 3:
            position = Vector2((-50, randint(0, 600)))
        else:
            position = Vector2((850, randint(0, 600)))

        velocity = lime_velocity_rules(position, upper_velocity, side_velocity, position_var)
        return position, velocity

    def lemons_position_and_velocity(self):
        upper_velocity = 10
        side_velocity = 5

        position_var = randint(3, 4)

        if position_var == 3:
            position = Vector2(-50, randint(0, 600))
        else:
            position = Vector2(850, randint(0, 600))

        velocity = lime_velocity_rules(position, upper_velocity, side_velocity, position_var)

        return position, velocity

    def create_list(self, score):
        list = ['watermelon']
        if score > 2500:
            list.append('coconut')
        if score > 1000:
            list.append('lemon')
        if score > 5000:
            list.append('lime')

        return list

    def collision(self, pointer, threshold=10):
        # Create a slightly larger bounding box
        enlarged_rect = self.rect.inflate(threshold * 2, threshold * 2)

        if not enlarged_rect.collidepoint(pointer.position):
            return None, None

        horizontal_distance, vertical_distance = point_to_edge_distance(pointer.position, self.rect)

        new_sprite_1 = None
        new_sprite_2 = None

        if horizontal_distance <= threshold and vertical_distance <= threshold:
            if horizontal_distance < vertical_distance:
                new_sprite_1 = SlicedFruit(Vector2(self.rect.centerx - self.rect.width // 4, self.rect.centery),
                                           self.type, 'left', self.angle)
                new_sprite_2 = SlicedFruit(Vector2(self.rect.centerx + self.rect.width // 4, self.rect.centery),
                                           self.type, 'right', self.angle)
            else:
                new_sprite_1 = SlicedFruit(Vector2(self.rect.centerx, self.rect.centery - self.rect.height // 4),
                                           self.type, 'top', self.angle)
                new_sprite_2 = SlicedFruit(Vector2(self.rect.centerx, self.rect.centery + self.rect.height // 4),
                                           self.type, 'bottom', self.angle)
        elif horizontal_distance <= threshold:
            new_sprite_1 = SlicedFruit(Vector2(self.rect.centerx - self.rect.width // 4, self.rect.centery), self.type,
                                       'left', self.angle)
            new_sprite_2 = SlicedFruit(Vector2(self.rect.centerx + self.rect.width // 4, self.rect.centery), self.type,
                                       'right', self.angle)
        elif vertical_distance <= threshold:
            new_sprite_1 = SlicedFruit(Vector2(self.rect.centerx, self.rect.centery - self.rect.height // 4), self.type,
                                       'top', self.angle)
            new_sprite_2 = SlicedFruit(Vector2(self.rect.centerx, self.rect.centery + self.rect.height // 4), self.type,
                                       'bottom', self.angle)

        return new_sprite_1, new_sprite_2


    def draw(self, screen):
        screen.blit(self.sprite, self.rect.topleft)

    # def draw(self, surface):
    #     rotated_surface = self.sprite
    #     rotated_surface_size = Vector2(rotated_surface.get_size())
    #     blit_position = self.position - rotated_surface_size * 0.5
    #     surface.blit(self.sprite, blit_position)

class SlicedFruit(GameObject):
    GRAVITY = 0.22
    SCALES = {'lemon': 1,
              'lime': .7,
              'coconut': 1,
              'watermelon': 1
              }

    rotation_velocity_constant = 1

    def __init__(self, position, type, portion, angle):
        self.type = type
        self.velocity = Vector2(0, 0)
        self.position = position
        self.angle = angle
        self.rotation_direction = choice([-1, 1])
        scale = self.SCALES[self.type]
        self.sprite = rotozoom(load_sprite(self.type + '_' + portion), 0, scale)
        self.original_sprite = self.sprite
        self.rect = self.sprite.get_rect(center=self.position)
        super().__init__(self.position, self.velocity, self.sprite)

    def decelerate(self):
        self.velocity[1] = self.velocity[1] + self.GRAVITY

    def spin(self):
        self.angle += self.rotation_velocity_constant * self.rotation_direction
        self.sprite = rotate(self.original_sprite, self.angle)

        # Get a new rect with the center of the old rect
        self.rect = self.sprite.get_rect(center=self.position)

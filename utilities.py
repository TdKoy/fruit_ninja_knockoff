from pygame.image import load
from pygame.math import Vector2
from pygame import Color
from random import randint


def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

def watermelon_velocity_rules(position, velocity_upper, velocity_lower):
    if position[0] < 800/3:
        velocity = Vector2(randint(0, velocity_upper) / 10, randint(-17, -15))
    elif position[0] >(800/3) * 2:
        velocity = Vector2(randint(velocity_lower, 0) / 10, randint(-17, -15))
    else:
        velocity = Vector2(randint(velocity_lower, velocity_upper) / 10, randint(-17, -15))

    return velocity

def lime_velocity_rules(position, velocity_upper, side_velocity, mode):
    if mode == 1:
        velocity = Vector2(randint(-side_velocity, side_velocity), velocity_upper)
    elif mode == 2:
        velocity = Vector2(randint(-side_velocity, side_velocity), -velocity_upper)
    elif mode == 3:
        velocity = Vector2(velocity_upper, randint(-side_velocity, side_velocity))
    else:
        velocity = Vector2(-velocity_upper, randint(-side_velocity, side_velocity))
    return velocity

def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)

def print_bust(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()[0] * (7/8), surface.get_size()[1] * (1/8))

    surface.blit(text_surface, rect)

def point_to_edge_distance(point, rect):
    left = rect.left
    right = rect.right
    top = rect.top
    bottom = rect.bottom

    # Calculate horizontal distance
    if left <= point.x <= right:
        horizontal_distance = 0
    else:
        horizontal_distance = min(abs(point.x - left), abs(point.x - right))

    # Calculate vertical distance
    if top <= point.y <= bottom:
        vertical_distance = 0
    else:
        vertical_distance = min(abs(point.y - top), abs(point.y - bottom))

    return horizontal_distance, vertical_distance


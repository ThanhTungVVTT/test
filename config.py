import pygame
from pygame.math import Vector2


pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

pygame.mixer.init()

sound_background=pygame.mixer.Sound("Sounds/sound_background.mp3")
sound_background.play(-1)

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

GREEN = (173, 204, 96)
DARK_GREEN = (43, 40, 24)
OFFSET = 65

cell_size = 25
cell_number = 25

pygame.display.set_caption("Snake Game")
fps = pygame.time.Clock()
screen = pygame.display.set_mode(
    (2 * OFFSET + cell_size * cell_number, 2 * OFFSET + cell_size * cell_number)
)


SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

food_surface = pygame.image.load("Graphics/apple.png").convert_alpha()
food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size))

special_food_surface = pygame.image.load("Graphics/watermelon.png").convert_alpha()
special_food_surface = pygame.transform.scale(
    special_food_surface, (cell_size, cell_size)
)

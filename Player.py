# Player.py
import pygame
import os
from DataConfig import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load player image (facing right)
        self.player_image_right = pygame.image.load(os.path.join(IMAGE_PATH, 'hooman.png')).convert_alpha()
        self.player_image_right = pygame.transform.scale(self.player_image_right, (PLAYER_WIDTH, PLAYER_HEIGHT))

        # Load player image (facing left)
        self.player_image_left = pygame.transform.flip(self.player_image_right, True, False)

        self.image = self.player_image_right  # Assign player image (initially facing right)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT

        self.lives = DEFAULT_LIFES  # Initialize lives to 5
        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = self.player_image_left  # Set image to face left
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = self.player_image_right  # Set image to face right

        # Boundary check
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLAYER_WIDTH

    def lose_life(self):
        self.lives -= 1

import pygame
import os
import random
from DataConfig import *

class Item(pygame.sprite.Sprite):
    def __init__(self, item_type):
        super().__init__()
        self.item_type = item_type
        
        # Load images based on item type
        if self.item_type == 'beer':
            self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'beer.jpg')).convert()
        elif self.item_type == 'beer2':
            self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'beer2.jpg')).convert()
        elif self.item_type == 'beer3':
            self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'paulaner.jpg')).convert()
        elif self.item_type == 'beer4':
            self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'bitburger.jpg')).convert()
        elif self.item_type == 'vodka':
            self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'vodka.jpg')).convert()
        elif self.item_type == 'apple':
            self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'apple.jpg')).convert()
        elif self.item_type == 'double_points':
            self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'doublePwp.png')).convert_alpha()
        elif self.item_type == 'vgr':
            self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'vgr.png')).convert_alpha()
        elif self.item_type == '1up':
            self.image = pygame.image.load(os.path.join(IMAGE_PATH, '1up.png')).convert_alpha()

        self.image = pygame.transform.scale(self.image, (ITEM_WIDTH, ITEM_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ITEM_WIDTH)
        self.rect.y = random.randint(-SCREEN_HEIGHT, -ITEM_HEIGHT - ITEM_SPAWN_DISTANCE)  # Ensure initial spread out
        self.speedy = ITEM_SPEED  # Set a common speed for all items

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # Remove the item from all groups when it goes off-screen

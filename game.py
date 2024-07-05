import pygame
import os
import random
from DataConfig import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize mixer for music and sound effects

# Initialize Player and Item Class
from Player import Player
from Item import Item

# Setup display
pygame.display.set_icon(pygame.image.load('resources/appico.ico')
)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Michaels Abenteuer")

# Load images
bg_image = pygame.image.load(os.path.join(IMAGE_PATH, 'bg.jpeg')).convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

ts_bg_image = pygame.image.load(os.path.join(IMAGE_PATH, 'ts-bg.jpeg')).convert()
ts_bg_image = pygame.transform.scale(ts_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load heart image for lives display
heart_image = pygame.image.load(os.path.join(IMAGE_PATH, 'heart.png')).convert_alpha()
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Load background music
try:
    pygame.mixer.music.load(os.path.join(SOUND_PATH, 'bg.mp3'))
    pygame.mixer.music.play(-1)  # Play the music in a loop
except pygame.error as e:
    print(f"Error loading or playing background music: {e}")

# Load sound effects
try:
    noice_sound = pygame.mixer.Sound(os.path.join(SFX_PATH, 'noice.mp3'))
    game_over_sound = pygame.mixer.Sound(os.path.join(SFX_PATH, 'gvyeh.mp3'))
    last_life_sound = pygame.mixer.Sound(os.path.join(SFX_PATH, 'last_life.mp3'))
except pygame.error as e:
    print(f"Error loading 'noice.mp3' sound effect: {e}")

# Initialize player and groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

items = pygame.sprite.Group()

# Flags
double_points_active = False
vgr_active = False
play_noice = False
last_noice_played_time = 0
last_life_text_displayed = False
collected100pts1up = False
daytime = False

# Chances
vodka_spawn_rate = 0
paulaner_spawn_rate = 0
spawn_chance_1up = 0.000
apple_chance = 0.50

# Milestones
last_score_milestone = 0

# Variables for "LAST LIFE" text flashing
last_life_flash_timer = 0
last_life_flash_color = RED

# Main game loop
clock = pygame.time.Clock()
score = 0
running = True
paused = False
font = pygame.font.SysFont(None, 36)

# Function to convert screen to grayscale
def grayscale(surface):
    arr = pygame.surfarray.pixels3d(surface)
    arr = arr.dot([0.2989, 0.587, 0.114])  # Convert to grayscale using luminosity method
    arr = arr.reshape((*arr.shape, 1)).repeat(3, axis=2)
    return pygame.surfarray.make_surface(arr)

# Title screen loop
show_title_screen = True
while show_title_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_title_screen = False
            running = False
        elif event.type == pygame.KEYDOWN:
            show_title_screen = False

    # Draw title screen background
    screen.blit(ts_bg_image, (0, 0))

    # Draw game title
    title_font = pygame.font.SysFont(None, 72)
    title_text = title_font.render("Michaels Abenteuer", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(title_text, title_rect)

    # Draw creator's name
    creator_font = pygame.font.SysFont(None, 24)
    creator_text = creator_font.render("(c) Copy05 2019", True, WHITE)
    creator_rect = creator_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
    screen.blit(creator_text, creator_rect)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused  # Toggle pause

    if paused:
        # Pause the music
        pygame.mixer.music.pause()

        # Draw background (grayscale)
        screen.blit(grayscale(bg_image), (0, 0))

        # Draw "Paused" text
        paused_text = font.render("PAUSED", True, WHITE)
        paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(paused_text, paused_rect)

        # Draw the score below "Paused" text
        score_text = font.render(f'Score: {score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(score_text, score_rect)

        # Flip the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)
        continue

    # Unpause the music
    pygame.mixer.music.unpause()

    # Draw background
    screen.blit(bg_image, (0, 0))
    
    # FPS Counter [You can remove this in production]
    # pygame.display.set_caption(f"Michaels Abenteuer | FPS: {int(clock.get_fps())}")

    # Spawn new items
    if len(items) < 10:  # Limit the number of items on screen
        item_types = ['beer', 'beer2', "beer3", 'vodka', 'apple', 'double_points', 'vgr', '1up']
        probabilities = [0.49, 0.29, paulaner_spawn_rate, vodka_spawn_rate, apple_chance, 0.002, 0.003, spawn_chance_1up]  # Example probabilities (49% beer, 39% beer2, 50% apple, 0.02% double points, 0.00% - 0.09% 1up)
        
        
        item_type = random.choices(item_types, weights=probabilities)[0]
        item = Item(item_type)
        
        # Check for overlapping items
        overlapping = pygame.sprite.spritecollide(item, items, False)
        while overlapping:  # Keep repositioning until no overlap
            item.rect.x = random.randint(0, SCREEN_WIDTH - ITEM_WIDTH)
            item.rect.y = random.randint(-SCREEN_HEIGHT, -ITEM_HEIGHT - ITEM_SPAWN_DISTANCE)
            overlapping = pygame.sprite.spritecollide(item, items, False)
        
        all_sprites.add(item)
        items.add(item)

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.spritecollide(player, items, dokill=True)  # Remove items on collision
    for hit in hits:
        
        if hit.item_type == 'beer':
            if apple_chance < MAX_APPLE_CHANCE:
                apple_chance += 0.001
            score += 2 if double_points_active else 1
            
        elif hit.item_type == 'beer2':
            if apple_chance < MAX_APPLE_CHANCE:
                apple_chance += 0.001
            score += 4 if double_points_active else 2
            
        elif hit.item_type == 'beer3':
            if apple_chance < MAX_APPLE_CHANCE:
                apple_chance += 0.001
            score += 4 if double_points_active else 2
            
        elif hit.item_type == 'vodka':
            if apple_chance < MAX_APPLE_CHANCE:
                apple_chance += 0.001
            score += 8 if double_points_active else 4
            
        elif hit.item_type == 'apple':
            if not vgr_active:
                player.lose_life()

                if player.lives == 1:
                    last_life_sound.play()
                    last_life_text_displayed = True
                    last_life_text_timer = 2 * FPS

                score -= 2 if double_points_active else 1
            else:
                score += 2 if double_points_active else 1
                
        elif hit.item_type == 'double_points':
            # Activate double points
            double_points_active = True
            double_points_timer = DOUBLE_POINTS_TIMER * FPS  # 10 seconds
        elif hit.item_type == 'vgr':
            # Activate double points
            vgr_active = True
            vgr_timer = VGR_TIMER * FPS  # 10 seconds
        elif hit.item_type == '1up':
            player.lives += 1
            spawn_chance_1up = 0.000
            collected100pts1up = False
            
    # Check if score contains "69" and play "noice.mp3"
    if '69' in str(score):
        current_time = pygame.time.get_ticks()
        if not play_noice and current_time - last_noice_played_time > NOICE_COOLDOWN:
            noice_sound.play()
            play_noice = True
            last_noice_played_time = current_time
    else:
        play_noice = False
        
        
    # Increasse Speed and Apple Chance for every 100 score and Unlock more stuff
    if score // 100 > last_score_milestone:
        
        apple_chance += 0.001
        last_score_milestone = score // 100
        
        if player.lives < DEFAULT_LIFES:
            spawn_chance_1up += UP_POINT_INCREASE # +0,1% Spawn Rate for 1up
        
        if last_score_milestone == 0:
            paulaner_spawn_rate = 0.30 # Paulaner Spawn Rate: 30%
            apple_chance += 0.003
            
        if last_score_milestone == 1:
            vodka_spawn_rate = 0.25 # Vodka Spawn Rate: 25%
            apple_chance += 0.004
        
        # Switch Between Day and Night Time
        if last_score_milestone % 9 == 0:
            daytime = not daytime
            if daytime:
                bg_image = pygame.image.load(os.path.join(IMAGE_PATH, 'bg.jpeg')).convert()
            else:
                bg_image = pygame.image.load(os.path.join(IMAGE_PATH, 'bg-night.jpg')).convert()
            bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
        

    # Draw / render
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw Apple Protection status
    if vgr_active:
        vgr_text = font.render(f'Invincibility: 0:{vgr_timer // FPS:02}', True, YELLOW)
        screen.blit(vgr_text, (10, 50))

        # Update VGR timer
        vgr_timer -= 1
        if vgr_timer <= 0:
            vgr_active = False

    # Draw Double Points status
    if double_points_active:
        double_points_text = font.render(f'Double Score: 0:{double_points_timer // FPS:02}', True, YELLOW)
        screen.blit(double_points_text, (10, 50))

        # Update double points timer
        double_points_timer -= 1
        if double_points_timer <= 0:
            double_points_active = False

    # Draw lives
    for i in range(player.lives):
        screen.blit(heart_image, (SCREEN_WIDTH - (i + 1) * 35, 10))
    
    # Show the "LAST LIFE" Text at the center of the game to warn the user that it is their last life.
    if last_life_text_displayed:
        # Update the flash timer and toggle color if necessary
        last_life_flash_timer += 1
        if last_life_flash_timer >= 0.5 * FPS:  # 0.5 seconds
            last_life_flash_timer = 0
            last_life_flash_color = YELLOW if last_life_flash_color == RED else RED
        
        last_life_text = font.render("LAST LIFE", True, last_life_flash_color)
        last_life_rect = last_life_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(last_life_text, last_life_rect)
        last_life_text_timer -= 1
        if last_life_text_timer <= 0:
            last_life_text_displayed = False

    # Check game over condition
    if player.lives <= 0 or score < 0:
        pygame.mixer.music.pause()
        game_over_sound.play()

        # Display game over text
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        # Flip the display
        pygame.display.flip()

        # Wait for the sound effect to finish playing
        pygame.time.wait(3000)

        # Exit the game loop
        running = False

    # Flip the display
    pygame.display.flip()

    # Ensure program maintains a rate of FPS frames per second
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
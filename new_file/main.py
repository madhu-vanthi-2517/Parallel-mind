# main.py

import pygame
import os
from player import Player
from game import Game
from ui import UI
import random

# List of levels
LEVELS = ["levels/level1.txt", "levels/level2.txt"]  # Make sure you have level2 or remove it later!

def reset_game(level_index):
    """Reset players and game state for the given level."""
    player_blue = Player(100, 300, "player_blue.png")  # Adjusted spawn position
    player_red = Player(700, 300, "player_red.png")
    game = Game(screen, [player_blue, player_red], LEVELS[level_index])
    return player_blue, player_red, game

def generate_level(width, height):
    level = []
    for y in range(height):
        row = []
        for x in range(width):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                row.append('P')  # Walls
            else:
                # Randomly place platforms, goals, enemies, etc.
                if random.random() < 0.1:
                    row.append('P')
                elif random.random() < 0.05:
                    row.append('G')
                elif random.random() < 0.05:
                    row.append('E')
                elif random.random() < 0.05:
                    row.append('S')
                elif random.random() < 0.05:
                    row.append('D')
                else:
                    row.append(' ')
        level.append(''.join(row))
    return level

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Parallel Minds")
clock = pygame.time.Clock()

# Setup initial game state
current_level = 0
player_blue, player_red, game = reset_game(current_level)
ui = UI(screen)

show_menu = True
running = True
game_over = False
win = False
game_completed = False
player_blue_reached = False
player_red_reached = False

class LevelEditor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[' ' for _ in range(width)] for _ in range(height)]
        self.selected_tile = 'P'

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            tile_x = x // TILE_SIZE
            tile_y = y // TILE_SIZE
            if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
                self.tiles[tile_y][tile_x] = self.selected_tile

    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile != ' ':
                    pygame.draw.rect(screen, (255, 255, 255), 
                                   (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def create_level(self, level_data):
    for y, row in enumerate(level_data):
        for x, char in enumerate(row):
            world_x = x * TILE_SIZE
            world_y = y * TILE_SIZE

            if char == 'P':
                self.platforms.add(Platform(world_x, world_y))
            elif char == 'G':
                self.goals.add(Goal(world_x + TILE_SIZE//2, world_y + TILE_SIZE//2))
            elif char == 'E':
                self.enemies.add(Enemy(world_x, world_y))
            elif char == 'S':
                self.switches.add(Switch(world_x + TILE_SIZE//2, world_y + TILE_SIZE//2))
            elif char == 'D':
                self.doors.add(Door(world_x + TILE_SIZE//2, world_y + TILE_SIZE//2))

# Main loop
while running:
    screen.fill((0, 0, 50))  # Blue side
    pygame.draw.rect(screen, (50, 0, 0), (400, 0, 400, 600))  # Red side

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if show_menu:
        ui.draw_main_menu()
        if keys[pygame.K_RETURN]:
            show_menu = False

    elif game_over:
        if game_completed:
            ui.draw_text_center("YOU COMPLETED ALL LEVELS!", size=50, color=(0, 255, 0))
        elif win:
            ui.draw_win_screen()
        else:
            ui.draw_lose_screen()

        if keys[pygame.K_r]:
            player_blue, player_red, game = reset_game(current_level)
            player_blue_reached = False
            player_red_reached = False
            game_over = False
            show_menu = False
            win = False
            game_completed = False

    else:
        # Handle player movement
        dx = 0
        jump = False

        if keys[pygame.K_LEFT]:
            dx = -player_blue.speed
        if keys[pygame.K_RIGHT]:
            dx = player_blue.speed
        if keys[pygame.K_UP]:
            jump = True

        # Move players
        player_blue.move(game.platforms, dx, jump)
        player_red.move(game.platforms, -dx, jump)

        # Update game objects
        game.update()

        # Draw game objects
        game.draw()

        # Draw players
        player_blue.draw(screen)
        player_red.draw(screen)

        # Check if players reach goals
        if not player_blue_reached and game.check_goal(player_blue):
            player_blue_reached = True
        if not player_red_reached and game.check_goal(player_red):
            player_red_reached = True

        # Level progression
        if player_blue_reached and player_red_reached:
            ui.draw_text_center("Level Complete!", size=50, color=(0, 255, 0))
            pygame.display.flip()
            pygame.time.delay(1500)  # 1.5 seconds pause

            current_level += 1
            if current_level < len(LEVELS):
                player_blue, player_red, game = reset_game(current_level)
                player_blue_reached = False
                player_red_reached = False
            else:
                game_over = True
                win = True
                game_completed = True

        # Check losing conditions
        if (game.check_enemy_collision(player_blue) or
            game.check_enemy_collision(player_red) or
            game.check_door_block(player_blue) or
            game.check_door_block(player_red)):
            game_over = True
            win = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

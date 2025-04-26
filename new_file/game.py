# game.py

import pygame
import os
from utils import get_asset_path

TILE_SIZE = 50

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(get_asset_path("platform.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(get_asset_path("goal_light.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        # Draw a glowing circle behind the goal
        glow_color = (255, 255, 100)
        pygame.draw.circle(screen, glow_color, self.rect.center, 25)  # Glow effect
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(get_asset_path("enemy.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = 2

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left < 100 or self.rect.right > 700:
            self.direction *= -1

class Switch(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_inactive = pygame.image.load(get_asset_path("switch_off.png")).convert_alpha()
        self.image_active = pygame.image.load(get_asset_path("switch_on.png")).convert_alpha()
        self.image = self.image_inactive
        self.rect = self.image.get_rect(center=(x, y))
        self.activated = False

    def update(self, players):
        self.activated = any(self.rect.colliderect(player.rect) for player in players)
        self.image = self.image_active if self.activated else self.image_inactive

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(get_asset_path("door.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.opened = False

    def update(self, switches):
        self.opened = all(switch.activated for switch in switches)

    def draw(self, screen):
        if not self.opened:
            screen.blit(self.image, self.rect)

class Game:
    def __init__(self, screen, players, level_file):
        self.screen = screen
        self.players = players
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.switches = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.load_level(level_file)

    def load_level(self, filename):
        if not os.path.exists(filename):
            print(f"Level file {filename} not found!")
            return
        
        with open(filename, 'r') as f:
            lines = f.readlines()

        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
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

    def update(self):
        self.enemies.update()
        self.switches.update(self.players)
        for door in self.doors:
            door.update(self.switches)

    def draw(self):
        self.platforms.draw(self.screen)
        for goal in self.goals:
            goal.draw(self.screen)  # Custom draw with glow
        self.enemies.draw(self.screen)
        self.switches.draw(self.screen)
        for door in self.doors:
            door.draw(self.screen)

    def check_goal(self, player):
        return any(player.rect.colliderect(goal.rect) for goal in self.goals)

    def check_enemy_collision(self, player):
        return any(player.rect.colliderect(enemy.rect) for enemy in self.enemies)

    def check_door_block(self, player):
        return any(not door.opened and player.rect.colliderect(door.rect) for door in self.doors)

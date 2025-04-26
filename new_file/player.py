import pygame
from utils import get_asset_path

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name):
        super().__init__()
        self.image = pygame.image.load(get_asset_path(image_name)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.jump_power = -12
        self.gravity = 0.6
        self.speed = 5
        self.on_ground = False

    def move(self, platforms, dx=0, jump=False):
        dy = 0

        if jump and self.on_ground:
            self.vel_y = self.jump_power

        self.vel_y += self.gravity
        dy += self.vel_y

        # Horizontal
        self.rect.x += dx
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                elif dx < 0:
                    self.rect.left = platform.rect.right

        # Vertical
        self.rect.y += dy
        self.on_ground = False
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Screen boundaries
        screen_width = 800
        screen_height = 600
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.on_ground = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)

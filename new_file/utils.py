import os
import pygame

def get_asset_path(name):
    return os.path.join("assets", "images", name)

def draw_text(screen, text, x, y, size=30, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

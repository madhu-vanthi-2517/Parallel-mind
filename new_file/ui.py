import pygame
from utils import draw_text

class UI:
    def __init__(self, screen):
        self.screen = screen

    def draw_main_menu(self):
        self.screen.fill((30, 30, 30))
        draw_text(self.screen, "Parallel Minds", 250, 150, 60)
        draw_text(self.screen, "Press ENTER to Start", 250, 250, 40)
        pygame.display.flip()

    def draw_win_screen(self):
        self.screen.fill((0, 100, 0))
        draw_text(self.screen, "YOU WIN!", 300, 250, 60)
        pygame.display.flip()

    def draw_lose_screen(self):
        self.screen.fill((100, 0, 0))
        draw_text(self.screen, "YOU LOST!", 300, 250, 60)
        pygame.display.flip()

    def draw_text_center(self, text, size=30, color=(255, 255, 255)):
        self.screen.fill((30, 30, 30))
        draw_text(self.screen, text, 150, 250, size=size, color=color)
        pygame.display.flip()

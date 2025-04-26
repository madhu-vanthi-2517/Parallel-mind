import os
import pygame

pygame.init()

OUTPUT_DIR = "assets/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_asset(color, size, filename):
    surf = pygame.Surface(size)
    surf.fill(color)
    pygame.image.save(surf, os.path.join(OUTPUT_DIR, filename))

def generate_assets():
    print("Generating assets...")
    create_asset((0, 100, 255), (40, 40), "player_blue.png")
    create_asset((255, 50, 50), (40, 40), "player_red.png")
    create_asset((200, 200, 200), (50, 20), "platform.png")
    create_asset((255, 200, 0), (20, 20), "goal_light.png")
    create_asset((100, 100, 100), (40, 40), "enemy.png")
    create_asset((100, 100, 0), (30, 10), "switch_off.png")
    create_asset((0, 200, 0), (30, 10), "switch_on.png")
    create_asset((150, 0, 150), (40, 80), "door.png")

if __name__ == "__main__":
    generate_assets()
    pygame.quit()

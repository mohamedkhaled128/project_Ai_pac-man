# utils.py
import pygame
import os

def load_sprite(path, size=None):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img

import pygame

class LifeBar(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        super().__init__()
        self.barColor = (110, 210, 46)
        self.image = 1
        self.rect = self.image.get_rect()
        self.position = [x, y, hp, 5] # Prend les coordonnée du personnage
        # ------------------------------





        # Dessiner la bar
       # pygame.draw.rect(surface, barColor, barPosition)
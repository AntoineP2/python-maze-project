import pygame

class LifeBar(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, color):
        super().__init__()
        self.barColor = color #(110, 210, 46) pour vert , (200, 68, 29) pour Rouge
        self.width = hp
        self.image = pygame.Surface([self.width, 5])
        self.image.fill(self.barColor)
        self.rect = self.image.get_rect()
        self.position = [x, y -3] # Prend les coordonnée du personnage
        # ------------------------------


    def update(self):  # Cette méthode actualise la position de la bar
        self.rect.topleft = self.position

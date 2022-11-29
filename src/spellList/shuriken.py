import pygame
from ..spell import Spell

class Shuriken(Spell) :
    def __init__(self, x, y, posPlayer):
        super().__init__(x, y, posPlayer) # Ajouter Shuriken pour remplacer l'image dans notre Spell
        self.dammage = 100
        self.speed = 8
        self.angle = 0
        self.manaCost = 10



    def rotate(self): # Cette fonction fait tourné le projectil sur lui même
        self.angle += 17
        self.image = pygame.transform.rotate(self.originImage, self.angle)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect(center=self.rect.center) # Aucun effet, a corriger ou trouver une solution
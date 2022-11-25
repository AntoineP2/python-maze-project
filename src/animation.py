import pygame
from abc import ABC, abstractmethod
# abc est le module pour créer des classes et méthode abstraite
class AnimationPersonnageSprite(pygame.sprite.Sprite, ABC):

    def __init__(self, sprite_name):
        super().__init__()
        self.sprite_sheet = pygame.image.load('../assets/personnage/' + sprite_name + '.png')
        self.image = self.get_image(0, 0)  # Definie l'image du personnage (Par 32)
        self.image.set_colorkey([0, 0, 0])  # Supprime le backGround
        self.indexAnimation = 0
        self.clockAnimation = 0
        #Position joueur pour direction du projectil, 0 = vers le bas, 1 vers haut, 2 vers gauche, 3 vers droite
        self.position_joueur = 0
        self.aLive = True

    @abstractmethod
    def get_image(self, x, y):
        pass

    @abstractmethod
    def set_sprite_img(self, y): # Methode Pour rdéfinir l'image du personnage suivant sont déplacement
        pass


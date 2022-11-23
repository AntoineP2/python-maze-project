import pygame

class AnimationPersonnageSprite(pygame.sprite.Sprite):

    def __init__(self, sprite_name):
        super().__init__()
        self.sprite_sheet = pygame.image.load('../assets/personnage/' + sprite_name + '.png')
        self.image = self.get_image(0, 0)  # Definie l'image du personnage (Par 32)
        self.image.set_colorkey([0, 0, 0])  # Supprime le backGround
        self.indexAnimation = 0
        self.clockAnimation = 0
        #Position joueur pour direction du projectil, 0 = vers le bas, 1 vers haut, 2 vers gauche, 3 vers droite
        self.position_joueur = 0


    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def set_sprite_img(self, y): # Methode Pour rdéfinir l'image du personnage suivant sont déplacement
        self.image = self.get_image(32*self.indexAnimation, 32*y)
        self.image.set_colorkey([0, 0, 0])
        self.clockAnimation += self.speed
        if self.clockAnimation > 16:
            self.indexAnimation += 1
            self.clockAnimation = 1

        if self.indexAnimation > 2:
            self.indexAnimation = 0


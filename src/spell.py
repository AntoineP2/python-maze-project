import pygame

class Spell(pygame.sprite.Sprite):

    def __init__(self, x,y, posPlayer):
        super().__init__()
        self.damage = 100
        self.speed = 7
        self.image = pygame.image.load('../assets/spell/spell.png') # Definie l'image du personnage (Par 32)
        self.image.set_colorkey([0, 0, 0])  # Supprime le backGround
        self.rect = self.image.get_rect()
        self.impactPoint = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.position = [x, y]
        self.positionPlayer = posPlayer
        self.originImage = self.image
        self.angle = 0

    def update(self): # Fonction qui s'utilise dans le Game.py lorsque l'ont fait group.update() !
        self.rect.topleft = self.position
        self.impactPoint = pygame.Rect((self.position),(self.rect.width * 0.1, 12))
        self.rotate()
        self.spellDirection()


    def rotate(self): # Cette fonction fait tourné le projectil sur lui même
        self.angle += 17
        self.image = pygame.transform.rotate(self.originImage, self.angle)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect(center=self.rect.center) # Aucun effet, a corriger ou trouver une solution


    def spellDirection(self): # On definie la direction du Lancer en fonction de la direction du joueur
        if self.positionPlayer == 0:
            self.position[1] += self.speed
        if self.positionPlayer == 1:
            self.position[1] -= self.speed
        if self.positionPlayer == 2:
            self.position[0] -= self.speed
        if self.positionPlayer == 3:
            self.position[0] += self.speed
import pygame
import animation

from spell import Spell
from lifeBar import LifeBar

class Player(animation.AnimationPersonnageSprite):
    def __init__(self, x, y):
        super().__init__("player")
        self.speed = 2  # Defini la vitesse du joueur ainsi que la vitesse du changement de son animation
        self.Hp = 500
        self.MaxHp = 500
        self.rect = self.image.get_rect()
        self.position = [x, y] # Prend les coordonnée du personnage
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.8, 12) # On définit un rectangle au pied du joueur (Le 12 est pour la hauteur du rectangle)
        self.old_position = self.position.copy() # On vas sauvegarder l'ancienne position, .copy() permet de copier la valeur.
        self.position_joueur = 0
        self.cooldownMax = 30
        self.cooldownCurrent = self.cooldownMax
        self.spellList = []
        self.spellGroupRect = []
        self.manualMove = True  # Si le joueur peu bouger manuellement
        self.indexManualMoveCount = 0
        self.lifeBareEmpty = LifeBar(self.position[0], self.position[1], 50, (98, 98, 98))
        self.lifeBare = LifeBar(self.position[0], self.position[1], 50, (110, 210, 46))



    def set_hp(self, hp):
        self.Hp = hp

    # Cette methode va mettre a jour a chaque frame la barre de vie
    def updateLifeBar(self):

        self.lifeBare.position = [self.position[0] - 10, self.position[1]-10]
        self.lifeBareEmpty.position = [self.position[0] - 10, self.position[1] - 10]
        width = (self.Hp / self.MaxHp)*50
        self.lifeBare.image = pygame.Surface([width, 5])
        self.lifeBare.image.fill(self.lifeBare.barColor)


    def getDamage(self, damage):
        self.Hp -= damage
        print(damage)
        if self.Hp <= 0:
            self.Hp = 0

    def useSpellA(self): # Quand  l'utilisateur utilise un spell avec A
        if self.cooldownCurrent >= self.cooldownMax:
            spellUsed = Spell(self.position[0], self.position[1], self.position_joueur)
            self.spellList.append(spellUsed)
            self.spellGroupRect.append(spellUsed.rect)
            self.cooldownCurrent = 0



# Methode qui fais reculer le joueur sans changer son animation si evenement exterieur
    def forcedMove(self):
        if self.indexManualMoveCount < 7:
            if self.position_joueur == 0:
                self.position[1] -= 4
            if self.position_joueur == 1:
                self.position[1] += 4
            if self.position_joueur == 2:
                self.position[0] += 4
            if self.position_joueur == 3:
                self.position[0] -= 4
            self.indexManualMoveCount += 1
        else:
            self.indexManualMoveCount = 0
            self.manualMove = True

    def save_position(self):
        self.old_position = self.position.copy() # Sauvegarder l'ancienne position

    def update(self) :  # Cette méthode actualise la position du joueur
        if self.cooldownCurrent > self.cooldownMax:
            pass
        else:
            self.cooldownCurrent += 1

        self.updateLifeBar()
        self.rect.topleft = self.position # PLace le personnage suivant les coordonée depuis haut gauche
        self.feet.midbottom = self.rect.midbottom # On place le rectangle des pieds au meme niveau que le rectangle du joueur

        if self.Hp <= 0:
            print('Vous êtes mort')

    def move_back(self):  # Cette méthode nous permet de mettre de le personnage a sa position antérieur
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


# toutes les methodes pour bouger le personnage
    def deplacement_player(self, action):
        if self.manualMove: # Si manualmove active, alors le joueur peu se deplacer librement
            if action[pygame.K_UP]:
                self.position_joueur = 1
                self.set_sprite_img(3)
                self.position[
                    1] -= self.speed  # position[1] car on agis sur l'axe Y et on rajoute la valeur de speed pour le déplacement
            elif action[pygame.K_DOWN]:
                self.position_joueur = 0
                self.set_sprite_img(0)
                self.position[1] += self.speed
            elif action[pygame.K_LEFT]:
                self.position_joueur = 2
                self.set_sprite_img(1)
                self.position[0] -= self.speed
            elif action[pygame.K_RIGHT]:
                self.position_joueur = 3
                self.set_sprite_img(2)
                self.position[0] += self.speed

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


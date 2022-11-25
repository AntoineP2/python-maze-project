import pygame
import animation
from random import randint
from lifeBar import LifeBar



class Monster(animation.AnimationPersonnageSprite):
    def __init__(self, x, y):
        super().__init__("boss")
        self.speed = 1  # Defini la vitesse du joueur ainsi que la vitesse du changement de son animation
        self.Hp = 500
        self.MaxHp = 500
        self.attack = 100
        self.rect = self.image.get_rect()
        self.position = [x, y] # Prend les coordonnée du personnage
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.8, 20) # On définit un rectangle au pied du joueur (Le 12 est pour la hauteur du rectangle)
        self.old_position = self.position.copy() # On vas sauvegarder l'ancienne position, .copy() permet de copier la valeur.
        # Variable Deplacement + colision
        self.position_joueur = 0
        self.movCount = 0
        self.indexColision = 0
        self.indexMove = 0
        self.positionJoueurColision = 0
        self.lifeBareEmpty = LifeBar(self.position[0], self.position[1], 50, (98, 98, 98))
        self.lifeBare = LifeBar(self.position[0], self.position[1], 50, (200, 68, 29))

        # ------------------------------

# Cette methode va mettre a jour a chaque frame la barre de vie
    def updateLifeBar(self):

        self.lifeBare.position = [self.position[0] - 10, self.position[1]-10]
        self.lifeBareEmpty.position = [self.position[0] - 10, self.position[1] - 10]
        width = (self.Hp / self.MaxHp)*50
        self.lifeBare.image = pygame.Surface([width, 5])
        self.lifeBare.image.fill(self.lifeBare.barColor)

    def set_hp(self, hp):
        self.Hp = hp


    # Méthode utiliser lorsque le monstre meurt
    def deathMonster(self):
        self.aLive = False
        self.image = pygame.image.load('../assets/autre/tombstone.png')  # si le monstre meurs alors on change le skin
        self.feet = pygame.Rect(0, 0, 0, 0)
        self.attack = 0

    def getDamage(self, damage):
        self.Hp -= damage
        print(self.Hp)
        if self.Hp <= 0:
            self.Hp = 0
            self.deathMonster()

    def save_position(self):
        self.old_position = self.position.copy() # Sauvegarder l'ancienne position

    def rageMode(self):
        if self.Hp <=200:
            self.speed = 2

    def update(self):  # Cette méthode actualise la position du joueur
        self.rageMode()
        self.updateLifeBar()
        self.rect.topleft = self.position # PLace le personnage suivant les coordonée depuis haut gauche
        self.feet.midbottom = self.rect.midbottom # On place le rectangle des pieds au meme niveau que le rectangle du joueur




# ----------- Méthode qui actualise et déplace le monstre suivant les collision...
    def updateMove(self, collision, collisionJoueur):
        if collision != -1 or collisionJoueur != -1:
           self.indexColision = 6
           self.movCount = 21
           self.positionJoueurColision = self.position_joueur

        if self.indexColision > 0:
            self.collisionMove()
            self.indexColision -= 1
        else:
            self.movCount += 1
            if self.movCount > 20:
                self.movCount = 0
                self.indexMove = randint(0, 3)
            self.moveMonster(self.indexMove)  # Fais bouger le monstre


# Methode pour Gerer le déplacement du monstre si collision, cette méthode est appelé dans note méthode updateMove
    def collisionMove(self):
        if self.positionJoueurColision == 0:
            self.moveMonster(1)
        elif self.positionJoueurColision == 1:
            self.moveMonster(0)
        elif self.positionJoueurColision == 2:
            self.moveMonster(3)
        else:
            self.moveMonster(2)


# ----------toutes les methodes pour bouger le monstre --------------
    def up(self):
        self.position_joueur = 1
        self.set_sprite_img(3)
        self.position[1] -= self.speed  # position[1] car on agis sur l'axe Y et on rajoute la valeur de speed pour le déplacement

    def down(self):
        self.position_joueur = 0
        self.set_sprite_img(0)
        self.position[1] += self.speed

    def left(self):
        self.position_joueur = 2
        self.set_sprite_img(1)
        self.position[0] -= self.speed

    def right(self):
        self.position_joueur = 3
        self.set_sprite_img(2)
        self.position[0] += self.speed


    def moveMonster(self, indexMove):
        if indexMove == 1:
            self.up()
        if indexMove == 0:
            self.down()
        if indexMove == 2:
            self.left()
        if indexMove == 3:
            self.right()

# ---------------------------------------------------------------

# ------------------ Animation ----------------------------------
    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def set_sprite_img(self, y):  # Methode Pour rdéfinir l'image du personnage suivant sont déplacement
        self.image = self.get_image(32 * self.indexAnimation, 32 * y)
        self.image.set_colorkey([0, 0, 0])
        self.clockAnimation += self.speed
        if self.clockAnimation > 16:
            self.indexAnimation += 1
            self.clockAnimation = 1

        if self.indexAnimation > 2:
            self.indexAnimation = 0

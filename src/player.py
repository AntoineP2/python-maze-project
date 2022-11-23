import pygame
import animation



class Player(animation.AnimationPersonnageSprite):
    def __init__(self, x, y):
        super().__init__("player")
        self.speed = 2  # Defini la vitesse du joueur ainsi que la vitesse du changement de son animation
        self.Hp = 500
        self.MaxHp = 500
        self.rect = self.image.get_rect()
        self.position = [x, y] # Prend les coordonnée du personnage
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12) # On définit un rectangle au pied du joueur (Le 12 est pour la hauteur du rectangle)
        self.old_position = self.position.copy() # On vas sauvegarder l'ancienne position, .copy() permet de copier la valeur.
        self.position_joueur = 0

    def set_hp(self, hp):
        self.Hp = hp


    def save_position(self):
        self.old_position = self.position.copy() # Sauvegarder l'ancienne position

    def update(self) :  # Cette méthode actualise la position du joueur
        self.rect.topleft = self.position # PLace le personnage suivant les coordonée depuis haut gauche
        self.feet.midbottom = self.rect.midbottom # On place le rectangle des pieds au meme niveau que le rectangle du joueur

    def move_back(self):  # Cette méthode nous permet de mettre de le personnage a sa position antérieur
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


# toutes les methodes pour bouger le personnage

    def deplacement_player(self, action):
        if action[pygame.K_UP]:
            self.position_joueur = 1
            self.set_sprite_img(3)
            self.position[1] -= self.speed #position[1] car on agis sur l'axe Y et on rajoute la valeur de speed pour le déplacement
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

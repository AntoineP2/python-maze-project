import pygame
import pytmx
import pyscroll

from spell import Spell
from player import Player
from monster import Monster


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Le jeu trop cool")

        #Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('../assets/map/MapAntoine.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2 # Pour zoomer sur map
        #Generer un joueur
        player_position = tmx_data.get_object_by_name("Player") #On utilise le calque position de la map pour placer le joueur
        self.player = Player(player_position.x, player_position.y) # Les paramètres place le joueur sur la map
        self.thisSpell = []

        #Generer un monstre
        monster_position = tmx_data.get_object_by_name("Monster1")
        self.monster = Monster(monster_position.x, monster_position.y)

        self.monstersRect = []
        self.monstersRect.append(self.monster.rect)


        #Definir une liste pour stocker les collision avec décors
        self.walls = [] # On va stoquer nos element de collision ici

        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) #append sert a rajouter un element dans une liste, Ici on rajoute toutes les zones de collision


        #Dessiner groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player) # On dessine le joueur
        self.group.add(self.monster)

    def update(self):

        self.group.update()
        #Verification de collision
        if self.player.feet.collidelist(self.walls) > -1:
           self.player.move_back()

        if self.player.feet.collidelist(self.monstersRect) > -1:
            self.player.move_back()

        # On ajoute les spell utilisé par l'utilisateur
        for spell in self.thisSpell:
            self.group.add(spell)
            if spell.rect.collidelist(self.walls) > -1:
                self.group.remove(spell)

        """
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
        """

    def keyboard_input(self):
        bouton_pressed = pygame.key.get_pressed()
        self.player.deplacement_player(bouton_pressed)



    def run(self):
        clock = pygame.time.Clock() # Sert a gérer la vitesse de boucle du jeu

        running = True
        while running:

            self.player.save_position()
            self.keyboard_input()
            self.update() #Actualise la map pour placer le joueur au bonne coordonnées
            self.group.center(self.player.rect) # On centre la cam sur le joueur
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.thisSpell.append(Spell(self.player.position[0], self.player.position[1], self.player.position_joueur))
                        print("Spell lancé !")


            clock.tick(60) # Definie le jeu a 60FPS

        pygame.quit()


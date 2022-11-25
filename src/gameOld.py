import pygame
import pytmx
import pyscroll

from player import Player
from monster import Monster
from map import Map


class Game:
    def __init__(self):

# ------------------ INITIALISATION GAME -------------------------------------
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Le jeu trop cool")

        #Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('../assets/map/MapAntoine.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2 # Pour zoomer sur map
        #Generer un joueur
        player_position = tmx_data.get_object_by_name("Player") #On utilise le calque position de la map pour placer le joueur
        self.player = Player(player_position.x, player_position.y) # Les paramètres place le joueur sur la map$
        #Generer un monstre

        self.monsterList = []
        self.monstersRect = []
        for obj in tmx_data.objects:
            if obj.name == "Monster":
                monsterTempo = Monster(obj.x, obj.y)
                self.monsterList.append(monsterTempo)
                self.monstersRect.append(monsterTempo.feet)

        # ------------------------- Definir une liste pour stocker les collision avec décors ----------------------

        self.walls = [] # On va stoquer nos element de collision ici

        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) #append sert a rajouter un element dans une liste, Ici on rajoute toutes les zones de collision


        # -----------------------------------------------------------------------

        # Dessiner groupe de calque de tous les Sprites
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player, self.player.lifeBareEmpty, self.player.lifeBare) # On dessine le joueur
        for monster in self.monsterList: # On dessine les monstres
            self.group.add(monster.lifeBareEmpty, monster.lifeBare,  monster)
# ----------------------------------------------------- FIN INIT -------------------------------------------------


# -------------------------------  UPDATE METHDOE -----------------------------------------------
    def update(self):

        self.group.update()
        # ---- Fait reculer le joueur si impact avec monstre ----
        if not self.player.manualMove:
            self.player.forcedMove()



        #------------------Verification toutes les collisions -------------------
        if self.player.feet.collidelist(self.walls) > -1 or self.player.feet.collidelist(self.monstersRect) > -1:
           self.player.move_back()

        # ------ On applique les degat du monstre si il touche le joueur -----------------
        for monster in self.monsterList:
            if self.player.feet.colliderect(monster.feet):
                self.player.getDamage(monster.attack)
                self.player.manualMove = False

        # On ajoute les spell utilisé par l'utilisateur et on gère ses collision avec les murs et les monstres
        for spell in self.player.spellList:
            self.group.add(spell)
            if spell.rect.collidelist(self.walls) > -1:
                self.group.remove(spell)
                self.player.spellList.remove(spell)
            # ------------------ Applique les degats du sort au monstre ---------------------
            for monster in self.monsterList:
                if pygame.Rect.colliderect(monster.feet, spell.rect):
                    monster.getDamage(spell.damage)
                    self.group.remove(spell)
                    self.player.spellList.remove(spell)
                    if monster.Hp <= 0:
                        self.monstersRect.remove(monster.feet)
                        self.monsterList.remove(monster)
                        self.group.remove(monster, monster.lifeBare, monster.lifeBareEmpty)
            # --------------------------------------------------------------------
        self.updateMonstersMove()
    # ------------------------------- FIN UPDATE METHDOE -----------------------------------------------

    # ---- Methode pour déplacer les monsters
    def updateMonstersMove(self):
        for monster in self.monsterList:
            monster.updateMove(monster.feet.collidelist(self.walls), self.player.feet.collidelist(self.monstersRect))
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
                        self.player.useSpellA()


            clock.tick(60) # Definie le jeu a 60FPS

        pygame.quit()


import pygame
import pytmx
import pyscroll
from player import Player
from monster import Monster

class Map:

    def __init__(self, screen, map):
        # Charger la carte
        self.tmx_data = pytmx.util_pygame.load_pygame('../assets/map/' + map + '.tmx')
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, screen.get_size())
        self.map_layer.zoom = 2 # Pour zoomer sur map

        # Générer Player
        player_position = self.tmx_data.get_object_by_name("Player") #On utilise le calque position de la map pour placer le joueur
        self.player = Player(player_position.x, player_position.y) # Les paramètres place le joueur sur la map$

        # Variable pour Monstre
        self.monsterList = []
        self.monstersRect = []
        self.setMonsters()

        # Variable pour Collision
        self.walls = []
        self.setWalls()

        # On affiche toutes les Sprites
        # self.group = []
        self.spawnSprites()

    # ----------------------- Methode de SET --------------------------
    def setMonsters(self):
        for obj in self.tmx_data.objects:
            if obj.name == "Monster":
                monsterTempo = Monster(obj.x, obj.y)
                self.monsterList.append(monsterTempo)
                self.monstersRect.append(monsterTempo.feet)


    def setWalls(self):
        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


    def spawnSprites(self):
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.group.add(self.player, self.player.lifeBareEmpty, self.player.lifeBare)  # On dessine le joueur
        for monster in self.monsterList:  # On dessine les monstres
            self.group.add(monster.lifeBareEmpty, monster.lifeBare, monster)

    # -------------------------------  Methode UPDATE ----------------------------------------------
    def update(self):

        self.group.update()
        # ---- Fait reculer le joueur si impact avec monstre ----
        if not self.player.manualMove:
            self.player.forcedMove()

        # ------------------Verification toutes les collisions -------------------
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()


        # ------ On applique les degat du monstre si il touche le joueur -----------------
        for monster in self.monsterList:
            if self.player.feet.colliderect(monster.feet) and monster.aLive:
                self.player.getDamage(monster.attack)
                self.player.manualMove = False


        # ------------------------  LES SPELLS + DEGATS SPELL --------------------------------------------
        # On ajoute les spell utilisé par l'utilisateur et on gère ses collision avec les murs et les monstres
        for spell in self.player.spellList:
            self.group.add(spell)
            print(spell.impactPoint.collidelist(self.walls))
            if spell.impactPoint.collidelist(self.walls) > -1:
                self.group.remove(spell)
                self.player.spellList.remove(spell)

            # Applique les degats du sort au monstre
            for monster in self.monsterList:
                if pygame.Rect.colliderect(monster.feet, spell.rect):
                    monster.getDamage(spell.damage)
                    self.group.remove(spell)
                    self.player.spellList.remove(spell)
                    if monster.Hp <= 0:
                        self.group.remove(monster.lifeBare, monster.lifeBareEmpty)

            # -----------------------------FIN SPELL ET DEGATS SPELL-----------------------------


        self.updateMonstersMove()
    # ------------------------------- FIN UPDATE METHDOE -----------------------------------------------

    # --- Methode pour Mettre a jours les déplacements des monstres -----------------------------
    def updateMonstersMove(self):
        for monster in self.monsterList:
            if monster.aLive :
                monster.updateMove(monster.feet.collidelist(self.walls), self.player.feet.collidelist(self.monstersRect))
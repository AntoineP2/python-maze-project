from map import Map
import pygame

class Game:
    def __init__(self):

# ------------------ INITIALISATION GAME -------------------------------------
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Le jeu trop cool")

        #Charger la carte
        self.map = Map(self.screen, "MapAntoine")




    # ---- Methode pour déplacer les monsters

    def keyboard_input(self):
        bouton_pressed = pygame.key.get_pressed()
        self.map.player.deplacement_player(bouton_pressed)



    def run(self):
        clock = pygame.time.Clock() # Sert a gérer la vitesse de boucle du jeu

        running = True
        while running:

            self.map.player.save_position()
            self.keyboard_input()
            self.map.update() #Actualise la map pour placer le joueur au bonne coordonnées
            self.map.group.center(self.map.player.rect) # On centre la cam sur le joueur
            self.map.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.map.player.useSpellA()


            clock.tick(60) # Definie le jeu a 60FPS

        pygame.quit()


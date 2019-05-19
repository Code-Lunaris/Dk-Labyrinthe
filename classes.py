import pygame
from pygame.locals import *
from constante import *

"""fichier comportant toute les classe nécessaire au fonctionnement du jeux"""

class Niveau ():
    """Classe qui permet de générer le niveau"""
    def __init__(self, fichier):
        self.file =fichier
        self.structure =0

    def generate(self):
        """Fonction qui permet de générer le niveau a partir du fichier"""
        with open(self.file, 'r') as file:  #permet d'ouvrir le fichier et de le refermer a la fin
            lvl_struct =[]      #on créer une liste qui vas récupérer le contenu du fichier

            for ligne in file:
                line_lvl =[]

                for sprite in ligne:

                    if sprite != '\n':  #si le cractère n'est pas un retour chariot
                        line_lvl.append(sprite)     #on ajoute le sprite dans le liste

                #on ajoute alors la ligne a la structure du niveau
                lvl_struct.append(line_lvl)

        self.structure =lvl_struct      #on sauvegarde la strucutre du niveau


    def affiche(self, frame):
        """Méthode qui permet d'afficher le niveau sur l'écran"""

        #init des variables utiles

        wall = pygame.image.load(im_mur).convert()
        start = pygame.image.load(im_depart).convert()
        end = pygame.image.load(im_fin).convert_alpha()

        lin_numb =0 #conteur de ligne

        for line in self.structure:

            case =0     #compteur de case

            for sprite in line:
                #on calcul la postion de l'image
                x = case * sprite_size
                y = lin_numb * sprite_size

                if sprite == 'm':   #présence d'un mur
                    frame.blit(wall, (x, y) )
                elif sprite == 'd':   #case départ
                    frame.blit(start, (x, y) )

                elif sprite == 'a':
                    frame.blit(end, (x, y))

                case +=1
            lin_numb +=1



class Perso():
    """Classe définissant toutes la action du personnage"""

    def __init__(self, droite, gauche, haut, bas, niveau):

        #chargement des images
        self.right = pygame.image.load(droite).convert_alpha()
        self.left = pygame.image.load(gauche).convert_alpha()
        self.up = pygame.image.load(haut).convert_alpha()
        self.down = pygame.image.load(bas).convert_alpha()
        #paramétrage du niveau
        self.lvl =niveau
        #position du personnage
        self.case_x =0  #sprite x
        self.case_y =0  #sprite y
        self.x =0       #position du personnage en x
        self.y =0       #position du personnage en y
        self.direction =self.right    #direction par défaut


    def deplacer(self, move):
        """méthode permettant le déplacement du personnage et les collisions"""
        """move peut prendre les valeur "droite" "gauche" "haut" "bas" """

        #déplacement a droite
        if move == "droite":
            #on détecte si on est a la fin de l'écran
            if self.case_x < (sprite_numb-1) :
                #on vérifie que le sprite n'est pas un mûr
                if self.lvl.structure[self.case_y][self.case_x+1] != 'm':
                    #on se dépalce alors d'une case
                    self.case_x +=1
                    self.x =self.case_x*sprite_size

            self.direction =self.right

        #déplacement a gauche
        if move == "gauche":
            #on vérifie si ont est pas a la fin de l'écran
            if self.case_x > 0:
                #on détecte la présence d'un mûr
                if self.lvl.structure[self.case_y][self.case_x-1] != 'm':
                    self.case_x -=1
                    self.x =self.case_x*sprite_size

            self.direction =self.left

        #déplacement vers la haut
        if move == "haut":
            if self.case_y > 0:
                #détection de mûr
                if self.lvl.structure[self.case_y-1][self.case_x] != 'm':
                    self.case_y -=1
                    self.y =self.case_y*sprite_size

            self.direction =self.up

        #déplacement vers le bas
        if move == "bas":
            if self.case_y < (sprite_numb-1):
                #détection d'un mûr
                if self.lvl.structure[self.case_y+1][self.case_x] != 'm':
                    self.case_y +=1
                    self.y =self.case_y*sprite_size

            self.direction =self.down

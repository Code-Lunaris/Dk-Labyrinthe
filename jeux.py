import pygame
from constante import *
from constante import *
from classes import *
from time import sleep

"""scritp principal du jeux DK"""

pygame.init()

# ouverture de la fenêtre
frame = pygame.display.set_mode((frame_size, frame_size))

#paramétrage de la fenêtre
icon = pygame.image.load(icone)
pygame.display.set_icon(icon)
pygame.display.set_caption(titre)

pygame.key.set_repeat(100, 100)

#gestion de la musique
game = pygame.mixer.Sound(m_jeux)
end_mus = pygame.mixer.Sound(m_cong)

#lancement de la musique principale
game.play(loops =-1, maxtime =0, fade_ms =0)

#on définie une liste contenant les niveaux
levels =["levels\_n1", "levels\_n2", "levels\_n3", "levels\_n4", "levels\_n5"]
levels_numbs =len(levels)

lvl_count =0    #compteur de niveau

continuer =1
while continuer == 1:

    #on affiche le menu
    select = pygame.image.load(main_menu).convert()
    frame.blit(select, (0, 0))

    pygame.display.flip()

    #on rentre dans la gestion de l'écran menu
    menu, jeux, choix, congrate = 1, 0, 0, 0

    while menu == 1:

        #on limite le nombre de boucles par sencondes
        pygame.time.Clock().tick(30)

        #détection des évènement
        for event in pygame.event.get():

            #évènement qui permet de quitter
            if event.type == QUIT or ( event.type == KEYDOWN and event.key == K_F2 ):
                menu, jeux, continuer =0, 0, 0
                choix =0

            elif event.type == KEYDOWN:

                if event.key == K_F1: #si on veux jouer
                    choix=levels[0]

        #si l'utilisateur a choisis de jouer
        if choix !=0:

            #création de la fenetre de jeux
            back = pygame.image.load(im_bg).convert()

            #on génère le niveau
            lvl = Niveau(choix)
            lvl.generate()
            lvl.affiche(frame)

            #on génère le perso
            dk = Perso(dk_droite, dk_gauche, dk_haut, dk_bas, lvl)

            #on gère les boucle
            menu, jeux =0, 1 #on passe dans la boucle de jeux


    #boucle du jeux
    while jeux == 1:

        pygame.time.Clock().tick(30)

        for event in pygame.event.get():

            #quitter le jeux
            if event.type == QUIT:
                continuer, jeux =0, 0

            #évènement clavier
            elif event.type == KEYDOWN:

                #déplacement
                if event.key == K_UP:
                    dk.deplacer("haut")
                elif event.key == K_DOWN:
                    dk.deplacer("bas")
                elif event.key == K_RIGHT:
                    dk.deplacer("droite")
                elif event.key == K_LEFT:
                    dk.deplacer("gauche")

                #retour au menu
                elif event.key == K_SPACE:
                    jeux, menu, lvl_count, choix =0, 1, 0, 0

        #on remet à jour l'affichage
        frame.blit(back, (0,0) )
        lvl.affiche(frame)
        frame.blit(dk.direction, (dk.x, dk.y) )
        pygame.display.flip()

        #victoire
        if lvl.structure[dk.case_y][dk.case_x] == 'a':

            sleep(1)    #temps d'attente de une seconde

            lvl_count +=1   #on passe au niveau suivant

            #on détecte la fin des niveaux
            if lvl_count != levels_numbs:

                choix = levels[lvl_count]

                lvl = Niveau(choix)
                lvl.generate()
                lvl.affiche(frame)

                dk = Perso(dk_droite, dk_gauche, dk_haut, dk_bas, lvl)

            #si le jeux est finis
            else:
                end_mus.play(loops=-1)  # et on lance celle de la fin
                congrate, jeux =1, 0    #on quitte le jeux et on passe sur l'écran de fin

    #boucle de l'écran de fin
    while congrate == 1:

        #on configure la fenêtre
        cong = pygame.image.load(congratulations).convert()

        game.stop()     #on arrête la musique du jeux

        frame.blit(cong, (0,0) )    #affichage

        pygame.display.flip()

        #détection des évènements
        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_SPACE:

                #retour au menu
                end_mus.stop()  #on stop la musique de fin
                game.play(loops =-1)    #et on relance celle du jeux

                congrate, menu =0, 1    #on reviens ensuite sur la boucle de menu

            if event.type == QUIT:
                continuer, congrate= 0, 0

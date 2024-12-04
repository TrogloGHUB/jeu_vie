"""
Nom du fichier : main.py
Description    : Implémentation du Jeu de la vie de Conway
Auteur         : François Mercier
Date           : 2024-12-02
Version        : 1.0

Pré-requis :
- Python 3.8 ou supérieur
- Librairies nécessaires : pygame, numpy
"""

import pygame
import numpy
import sys
import random

pygame.init()

taille_cellule = 8  # dimension des unités de vie en pixels
largeur_fenetre = 2048  # doit être un multiple de taille_unite
hauteur_fenetre = 1536  # doit être un multiple de taille_unite
nb_largeur = int(largeur_fenetre / taille_cellule)  # nombre de cellules en largeur
nb_hauteur = int(hauteur_fenetre / taille_cellule)  # nombre de cellules en hauteur

# Définir les couleurs
coul_fond = (0, 0, 0)
coul_cellule = (255, 255, 255)
coul_alea = 1 # mettre à vrai pour avoir des couleurs variées

# Création du tableau vide
tableau_source = numpy.empty((nb_largeur, nb_hauteur))
tableau_source.fill(0)

# Afficher le nombre d'éléments dans chaque dimension
print("nb_largeur=" + str(nb_largeur))
print("nb_hauteur=" + str(nb_hauteur))

# Créer la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption('Jeu de la Vie de Conway')

def rempli_tableau_hasard(pourcent_depart):
    # Utilisé au départ pour remplir le tableau selon un pourcentage de départ
    # :pourcent_depart: entier entre 0 et 100
    for i in range(tableau_source.shape[0]):
        for j in range(tableau_source.shape[1]):
            if random.randint(1, 100) <= pourcent_depart:
                tableau_source[i, j] = 1
            else:
                tableau_source[i, j] = 0

def execute_cycle(tableau):
    # Appelé à chaque cycle pour mettre à jour le tableau
    # :tableau: tableau numpy de cellules de vies
    tableau_temp = numpy.empty((nb_largeur, nb_hauteur))
    tableau_temp.fill(0)
    # Boucler pour chaque cellule
    for i in range(tableau.shape[0]):
        for j in range(tableau.shape[1]):
            # Compter le nombre de cellules voisines vivantes
            nb_vivantes = 0

            if tableau[i - 1, j - 1] == 1:
                nb_vivantes += 1
            if tableau[i - 1, j] == 1:
                nb_vivantes += 1
            if j < tableau.shape[1]-1:
                if tableau[i - 1, j + 1] == 1:
                    nb_vivantes += 1
            if tableau[i, j - 1] == 1:
                nb_vivantes += 1
            if j < tableau.shape[1]-1:
                if tableau[i, j + 1] == 1:
                    nb_vivantes += 1
            if i < tableau.shape[0] - 1:
                if tableau[i + 1, j - 1] == 1:
                    nb_vivantes += 1
            if i < tableau.shape[0] - 1:
                if tableau[i + 1, j] == 1:
                    nb_vivantes += 1
            if i < tableau.shape[0] - 1 and j < tableau.shape[1] - 1:
                if tableau[i + 1, j + 1] == 1:
                    nb_vivantes += 1

            # Placer la cellule du tableau destination selon les règles du jeu de la vie
            #  si la cellule a exactement trois voisines vivantes, elle vie
            #  si elle a exactement deux voisines vivantes, elle reste dans son état actuel
            #  si elle a moins de deux ou plus de trois voisines vivantes, elle meurt
            if (nb_vivantes < 2 or nb_vivantes > 3):
                tableau_temp[i, j] = 0
            elif tableau[i, j] == 1 and (nb_vivantes == 2 or nb_vivantes == 3):
                tableau_temp[i, j] = 1
            elif tableau[i, j] == 0 and nb_vivantes ==3:
                tableau_temp[i, j] = 1

    tableau = tableau_temp  # copie du résultat dans le tableau source
    return tableau

# Boucle principale

fenetre.fill(coul_fond)

rempli_tableau_hasard(25)
execution = True

while execution:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            execution = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                execution = False

    # Affiche le tableau
    for i in range(tableau_source.shape[0]):
        for j in range(tableau_source.shape[1]):
            if tableau_source[i, j] == 0:
                couleur = coul_fond
            else:
                if coul_alea==1:
                    couleur = (20, 20, random.randint(100, 255))
                else:
                    couleur = coul_cellule
            pygame.draw.rect(fenetre, couleur, (i*taille_cellule, j*taille_cellule, taille_cellule, taille_cellule))

    # Executer un cycle de vie
    tableau_source = execute_cycle(tableau_source)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter PyGame
pygame.quit()
sys.exit()

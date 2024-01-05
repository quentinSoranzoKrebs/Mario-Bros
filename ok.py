import pygame
from constantes import *
import sys

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur),pygame.RESIZABLE)
pygame.display.set_caption("Dessiner un segment")

with open('map2.pg', 'r') as fichier:
    # Lire toutes les lignes du fichier dans une liste
    lignes = fichier.readlines()
    fichier.seek(0)
    lines = fichier.read()

point1 = (0, 0)
point2 = (0, 0)
nb = 0
point_sol = []
point = 0
def map(lignes,lines):
    global point1
    global point2
    global nb


    XX = 0
    YY = 0
    nb = 0
    for l in range(len(lignes)):
        for s in range(len(lignes[l])):
            map_return = lines[nb]
            if lines[nb]==".":
                point_sol.append((XX*TUILE_TAILLE, YY*TUILE_TAILLE))
                
            XX = XX + 1
            nb+=1
        XX = 0
        YY = YY + 1

map(lignes,lines)


# Définir les couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Définir les positions des points pour le segment
#point1 = (100, 100)
#point2 = (100, 550)

# Calculer la différence entre les coordonnées des points
dx = point_sol[point+1][0] - point_sol[point][0]
dy = point_sol[point+1][1] - point_sol[point][1]

# Calculer le nombre d'itérations nécessaires
num_steps = max(abs(dx), abs(dy))

# Calculer les incréments pour chaque itération
inc_x = dx / num_steps if num_steps != 0 else 0
inc_y = dy / num_steps if num_steps != 0 else 0

print(point_sol[0], point_sol[1])

# Convertir les coordonnées en entiers
x, y = int(point1[0]), int(point1[1])

continuer = True

# Boucle principale
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Effacer l'écran
    #fenetre.fill(blanc)

    # Dessiner le pixel actuel
    fenetre.set_at((round(x), round(y)), blanc)

    # Mettre à jour les coordonnées pour la prochaine itération
    x += inc_x
    y += inc_y

    # Rafraîchir l'écran
    pygame.display.flip()

    #lines[nb] = map_return

    if x == round(int(point[point+1][0])) and y == round(int(point[point+1][1])):
        print("ok")
        point += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

# Quitter Pygame
pygame.quit()

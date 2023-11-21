import pygame

lines = [0]*14

# Ouvrir le fichier en mode lecture
with open('map2.pg', 'r') as fichier:
    # Lire toutes les lignes du fichier dans une liste
    lignes = fichier.readlines()

def map(av)
    for l in range(14):
        #print(l)
        for c in range(30):
            lines[l] = lignes[l][c]
        

print(lines)
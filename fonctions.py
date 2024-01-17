import pygame
from tkinter import messagebox
import pygame_gui
import subprocess

pygame.init()

# fonction pour écrire
def ecrire(surface,couleur,text,place,taille):
    POLICE_ARIAL = pygame.font.SysFont("Arial",taille,1,1)
    text = POLICE_ARIAL.render(text,1,couleur)
    text_rect = text.get_rect()
    surface.blit(text,place)

    
# Fonction pour dessiner un rectangle avec des coins arrondis
def draw_rounded_rect(surface, color, rect, radius):
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)


def quitter():
    # Afficher une boîte de dialogue Zenity sur Linux (pour les bureaux basés sur GTK)
    response = subprocess.run(['zenity', '--question', '--text', 'Voulez-vous vraiment quitter?', '--ok-label=Quitter', '--cancel-label=Annuler'], capture_output=True, text=True)

    if response.returncode == 0:
        pygame.quit()
    else:
        print("Vous avez annulé la fermeture de l'application.")
        # Ajoutez ici le code pour gérer l'annulation de la fermeture
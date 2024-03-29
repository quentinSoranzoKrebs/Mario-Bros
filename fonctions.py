import pygame
import platform
import datetime
from math import *
import sys
from typing import *


system = platform.system()

if system == 'Windows':
    import ctypes
elif system == 'Linux':
    import subprocess
elif system == 'Darwin':
    print("Le programme s'exécute sous macOS.")
else:
    print("Système d'exploitation non reconnu:", system)

pygame.init()

def draw_bord(surface, color, rect, radius, épaisseur, color_line = (0,0,0)):
    draw_rounded_rect(surface, color_line, rect, radius)
    rect2 = pygame.Rect(rect[0]+épaisseur,rect[1]+épaisseur,rect[2]-épaisseur*2,rect[3]-épaisseur*2)
    draw_rounded_rect(surface, color, rect2, radius)
    
# Fonction pour dessiner un rectangle avec des coins arrondis
def draw_rounded_rect(surface, color, rect, radius, bord=None):
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)
    if bord:
        pygame.draw.arc(surface, (0,0,255), (x, y + h - 2 * radius, radius * 2, radius * 2), deg_2_rad(180), deg_2_rad(270), 1)
        pygame.draw.line(surface, (0,0,255), (x + radius, y + h-1), (x + w - radius, y + h-1),1)
        pygame.draw.arc(surface, (0,0,255), (x, y, radius * 2, radius * 2), deg_2_rad(90), deg_2_rad(180), 1)
        pygame.draw.line(surface, (0,0,255), (x + radius, y), (x + w - radius, y),1)
        pygame.draw.arc(surface, (0,0,255), (w - radius*2 , y, radius * 2, radius * 2), deg_2_rad(0), deg_2_rad(90), 1)
        pygame.draw.line(surface, (0,0,255), (x + w-1, y + radius), (x + w-1, y + h - radius),1)
        pygame.draw.arc(surface, (0,0,255), (w - radius*2 , y + h - 2 * radius, radius * 2, radius * 2), deg_2_rad(270), deg_2_rad(360), 1)
        pygame.draw.line(surface, (0,0,255), (x, y + radius), (x, y + h - radius),1)



def quitter():
    if system == "Windows":
        import ctypes
        # Définition des constantes de MessageBox
        MB_YESNO = 0x00000004
        MB_ICONQUESTION = 0x00000020
        MB_ICONWARNING = 0x00000030
        response = ctypes.windll.user32.MessageBoxW(0, "Voulez-vous vraiment quitter?", "Avertissement",  MB_YESNO | MB_ICONQUESTION | MB_ICONWARNING)
        if response == 6:
            response = True
        else:
            response = False
    elif system == "Linux":
        import os
        desktop = os.environ.get('XDG_CURRENT_DESKTOP')
        print(desktop)
        if desktop == 'ubuntu:GNOME':
            # Afficher une boîte de dialogue Zenity sur Linux (pour les bureaux basés sur GTK)
            response = subprocess.run(['zenity', '--question', '--text', 'Voulez-vous vraiment quitter?', '--ok-label=Quitter', '--cancel-label=Annuler'], capture_output=True, text=True)
        if desktop == 'KDE':
            response = subprocess.run(['kdialog', '--title', 'Question', '--yesno', 'Voulez-vous vraiment quitter?', '--yes-label', "Quitter", '--no-label', "Annuler"], capture_output=True, text=True)
            
        if response.returncode == 0:
            response = True
        else:
            response = False



    if response:
        pygame.quit()
        sys.exit()
    else:
        print("Vous avez annulé la fermeture de l'application.")
        # Ajoutez ici le code pour gérer l'annulation de la fermeture

def key_pass():
    if system == "Windows":
        pass



def screenshot(surface):
    now1 = datetime.datetime.now()
    format = "%Y-%m-%d %H:%M:%S"
    now2 = now1.strftime(format)
    pygame.image.save(surface, "screenshot/screenshot"+str(now2)+".png")

def change_window(w,h,fond):
    fond = pygame.transform.scale(fond, (w,h))
    print("ici")

def deg_2_rad(deg:float) -> float:
    '''Cette fonction permet de convertir les degré du paramètre `deg` en radian.'''
    return deg*(2*pi)/360

def rad_2_deg(rad:float) -> float:
    '''Cette fonction permet de convertir les radian du paramètre `rad` en degré.'''
    return 360*rad/(2*pi)

def select_egal(bloc):
    global select
    select = bloc
    print(select)

def ecrire(couleur: Tuple[int,int,int],
           text: str,
           taille:int,
           police:str = None
           ) -> pygame.surface:

        #font = pygame.font.Font(police, taille)
        font = pygame.font.Font("calibri-font/calibri-regular.ttf", taille)
        text_rend = font.render(text,1,couleur)
        text_rect = text_rend.get_rect()
        surface = pygame.Surface((text_rect[2], text_rect[3]), pygame.SRCALPHA)
        surface.blit(text_rend,(0,0))
        return surface

def rgb_to_hex(rgb):
    """
    Convertit un tuple RGB en valeur hexadécimale.
    
    Args:
        rgb (tuple): Un tuple de trois nombres entiers représentant les valeurs
                     rouge, vert et bleu (dans cet ordre).
    
    Returns:
        str: La valeur hexadécimale représentant la couleur.
    """
    # Assurez-vous que chaque composante est dans la plage de 0 à 255
    r, g, b = map(lambda x: min(255, max(0, x)), rgb)
    # Convertir chaque composante en sa représentation hexadécimale et les concaténer
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

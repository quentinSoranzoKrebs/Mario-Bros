import pygame
#from tk import messagebox
import pygame_gui
import platform
import datetime
from math import *
import sys


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


    
# Fonction pour dessiner un rectangle avec des coins arrondis
def draw_rounded_rect(surface, color, rect, radius):
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)


def quitter(arg):
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
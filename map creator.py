import pygame
import imageio
from gif import *
from fonctions import *
from classe import *
from time import sleep
import pygame_gui
import json


liste_boutons = []
   


pygame.init()

clic = 0

info = pygame.display.Info()

largeur_ecran = info.current_w
hauteur_ecran = info.current_h




with open('version.txt', 'r', encoding='utf-8') as file:
    v = file.readline().rstrip('\n\r')

ecran = pygame.display.set_mode((1300,650),pygame.RESIZABLE)
w,h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Mario Bros Map Creator "+str(v),"Mario Bros Map Creator "+str(v))
#pygame.display.(400, 300)

# Lecture des données depuis un fichier JSON
with open("map_créator.json", "r") as fichier_json:
    donnees = json.load(fichier_json)

for objet in donnees:
    if donnees[objet]["type"] == "bouton":
        if donnees[objet]["element"] == "image":
            origine = pygame.image.load(donnees[objet]['image']).convert_alpha()
            _bouton = btn(origine,eval(donnees[objet]["suite"]),TUILE_TAILLE,donnees[objet]["marge"],donnees[objet]["round"])
        elif donnees[objet]["element"] == "text":
            _bouton = btn(donnees[objet]["text"],eval(donnees[objet]["suite"]),TUILE_TAILLE,donnees[objet]["marge"],donnees[objet]["round"])
        liste_boutons.append([_bouton,objet])



C_origine = pygame.image.load("tuiles/C.png").convert_alpha()
T_origine = pygame.image.load("tuiles/T.png").convert_alpha()
S_origine = pygame.image.load("tuiles/Sancien.png").convert_alpha()
F_origine = pygame.image.load("tuiles/Sancien.png").convert_alpha()
M_origine = pygame.image.load("tuiles/M.png").convert_alpha()

# Style pour le bouton avec coins arrondis
style_bouton = {
    'border_width': 0,
    'border_color': (0, 0, 0),
    'border_radius': 10,
    'padding': (10, 10),
    'margin': (10, 10),
    'hover_border_color': (255, 0, 0),
    'hover_bg_color': (200, 200, 200),
    'focus_border_color': (0, 255, 0),
    'focus_bg_color': (150, 150, 150),
}

manager = pygame_gui.UIManager((w, h), 'theme1.json')

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Cliquez-moi', manager=manager, object_id="rounded_button")

# Charger l'icône
icone = pygame.image.load("ico_edit.png")


# Définir l'icône de la fenêtre
pygame.display.set_icon(icone)



background = pygame.Surface(ecran.get_size())
background.fill(NOIR)

continuer=True
clock = pygame.time.Clock()

save = btn("Sauvegarder",quitter,round(w/1300*50))

C = btn(C_origine,quitter,TUILE_TAILLE,2,4)
T = btn(T_origine,quitter,TUILE_TAILLE,5,4)
S = btn(S_origine,quitter,TUILE_TAILLE,5,4)
F = btn(F_origine,quitter,TUILE_TAILLE,5,4)
M = btn(M_origine,quitter,TUILE_TAILLE,5,4)

liste_tuiles = [[C,TUILE_TAILLE],[T,TUILE_TAILLE],[S,TUILE_TAILLE],[F,TUILE_TAILLE]]
    

titre = ecrire(BLANC,"Map creator v"+str(v),round(w/35))

_mur = MUR(w/2,h/2)
LISTE_GLOBALE_SPRITES.add(_mur)
LISTE_AFFICH.add(_mur)

while continuer:
    time_delta = clock.tick(60) / 1000.0


    w,h = pygame.display.get_surface().get_size()

    ecran.fill(NOIR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter()
        if event.type == pygame.VIDEORESIZE:
            save = btn("Sauvegarder",quitter,round(w/1300*50))
            TUILE_TAILLE = h/14
            for sprite in LISTE_GLOBALE_SPRITES:
                
                sprite.resize(TUILE_TAILLE,TUILE_TAILLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clic = 1

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clic = 0


    ecran.blit(background,(0,0))
    for i in range(round(w/(h/14))):
        pygame.draw.line(ecran,BLANC,(i*h/14,0),(i*h/14,h))

    for i in range(round(h/(h/14))):
        pygame.draw.line(ecran,BLANC,(0,i*(h/14)),(w,i*(h/14)))

    pygame.draw.line(ecran,BLANC,(0,h-1),(w,h-1))

    marge = pygame.Surface((w/4,h), pygame.SRCALPHA)
    marge.fill((20,20,20))
    LISTE_AFFICH.draw(ecran)
    marge.blit(titre(),(0,10))
    print(marge.get_offset())

    save.draw(marge,[3,h-save.get_height()-5],clic)
    for objet in liste_boutons:
        objet[0].draw(eval(donnees[objet[1]]["surface"]), eval(donnees[objet[1]]["place"]), clic)

    ecran.blit(marge,(w-w/4,0))
    manager.update(30)
    pygame.display.flip()

pygame.quit()
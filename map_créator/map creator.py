import pygame
import imageio
from gif import *
from fonctions import *
from classe import *
from time import sleep
import pygame_gui
import json

   


pygame.init()

clic = 0

info = pygame.display.Info()

largeur_ecran = info.current_w
hauteur_ecran = info.current_h

select = "0"


with open('version.txt', 'r', encoding='utf-8') as file:
    v = file.readline().rstrip('\n\r')

ecran = pygame.display.set_mode((1300,650),pygame.RESIZABLE)
w,h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Mario Bros Map Creator "+str(v),"Mario Bros Map Creator "+str(v))
#pygame.display.(400, 300)

# Lecture des données depuis un fichier JSON
with open("map_créator.json", "r") as fichier_json:
    donnees = json.load(fichier_json)

liste_boutons = [0]*len(donnees)

print(donnees["Bord"].get("taille", TUILE_TAILLE))

def import_json(donnees,TUILE_TAILLE):
    for i, objet in enumerate(donnees):
        if donnees[objet]["type"] == "bouton":
            if donnees[objet]["element"] == "image":
                origine = pygame.image.load(donnees[objet]['image']).convert_alpha()
                _bouton = btn(origine,eval(donnees[objet]["suite"]),donnees[objet].get("taille", TUILE_TAILLE),donnees[objet]["marge"],donnees[objet]["round"],arg = donnees[objet]["arg"],initial_color = eval(donnees[objet].get("initial_color", "(200,200,200,40)")),final_color = eval(donnees[objet].get("final_color", "(0,115,229,100)")))
            elif donnees[objet]["element"] == "text":
                _bouton = btn(donnees[objet]["text"],eval(donnees[objet]["suite"]),TUILE_TAILLE,donnees[objet]["marge"],donnees[objet]["round"],arg = donnees[objet]["arg"])
            liste_boutons[i] = [_bouton,objet]

import_json(donnees,TUILE_TAILLE)

print(liste_boutons)




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

bar1 = setting_bar("tuiles/parametres.png","ceci est un exemple de text","sous text",quitter,None)    

titre = ecrire(BLANC,"Map creator v"+str(v),round(w/35))

_mur = MUR(w/2,h/2)
LISTE_GLOBALE_SPRITES.add(_mur)
LISTE_AFFICH.add(_mur)

while continuer:
    TUILE_TAILLE = h/14
    time_delta = clock.tick(60) / 1000.0


    w,h = pygame.display.get_surface().get_size()

    ecran.fill(NOIR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter(None)
        if event.type == pygame.VIDEORESIZE:
            save = btn("Sauvegarder",quitter,round(w/1300*50))
            import_json(donnees,TUILE_TAILLE)
            for sprite in LISTE_GLOBALE_SPRITES:
                
                sprite.resize(TUILE_TAILLE,TUILE_TAILLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clic = 1
                point = pygame.mouse.get_pos()
                x = round(point[0] / TUILE_TAILLE) * TUILE_TAILLE
                if x > point[0]:
                    x-=TUILE_TAILLE
                y = round(point[1] / TUILE_TAILLE) * TUILE_TAILLE
                if y > point[1]:
                    y-=TUILE_TAILLE
                _mur = MUR(x,y)
                LISTE_GLOBALE_SPRITES.add(_mur)
                LISTE_AFFICH.add(_mur)

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
    ecran.blit(marge,(w-w/4,0))
    #ecran.blit(bar1(),(0,0))

    save.draw(ecran,[0.76*w,h-save.get_height()-5],clic)
    for objet in liste_boutons:
        objet[0].draw(eval(donnees[objet[1]]["surface"]), eval(donnees[objet[1]]["place"]), clic)

  
    manager.update(30)
    pygame.display.flip()

pygame.quit()
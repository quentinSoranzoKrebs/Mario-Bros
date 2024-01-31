import pygame
import imageio
from gif import *
from fonctions import *
from classe import *
from time import sleep
import pygame_gui

pygame.init()

clic = 0

info = pygame.display.Info()

largeur_ecran = info.current_w
hauteur_ecran = info.current_h

with open('version.txt', 'r') as fichier:
    premiere_ligne = fichier.readline()

ecran = pygame.display.set_mode((1300,650),pygame.RESIZABLE)
w,h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Mario Bros","Mario Bros "+str(premiere_ligne))
#pygame.display.(400, 300)

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

_mur = MUR(w-w/8,h/2)
LISTE_GLOBALE_SPRITES.add(_mur)
LISTE_AFFICH.add(_mur)

while continuer:
    time_delta = clock.tick(60) / 1000.0


    w,h = pygame.display.get_surface().get_size()

    background = pygame.Surface(ecran.get_size())
    background.fill(NOIR)


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

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print('Hello World!')

        manager.process_events(event)



    ecran.blit(background,(0,0))
    for i in range(round(w/(h/14))):
        pygame.draw.line(ecran,BLANC,(i*h/14,0),(i*h/14,h))

    for i in range(round(h/(h/14))):
        pygame.draw.line(ecran,BLANC,(0,i*(h/14)),(w,i*(h/14)))

    pygame.draw.line(ecran,BLANC,(0,h-1),(w,h-1))

    marge = pygame.Surface((w/4,h), pygame.SRCALPHA)
    marge.fill((70,70,70))
    ecran.blit(marge,(w-w/4,0))
    LISTE_AFFICH.draw(ecran)

    ecrire(ecran,BLANC,"Map creator v"+str(premiere_ligne),(w-w/4,10),round(w/35))

    save.draw(ecran,[w-save.get_width()-5,h-save.get_height()-5],clic)



    manager.update(30)
    #manager.draw_ui(ecran)
    pygame.display.flip()
            
    pygame.display.flip()

pygame.quit()
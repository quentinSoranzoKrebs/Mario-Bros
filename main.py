import pygame
import imageio
from gif import *
from classe import *
pygame.init()

left = 0
right = 0
space = 0
fondx = 0

xblocs = 0
yblocs = 0

colision_yperso = True
colision_xperso = True

ecran = pygame.display.set_mode((1300,650),pygame.RESIZABLE)
w,h = pygame.display.get_surface().get_size()

background = pygame.Surface(ecran.get_size())
background.fill(NOIR)



fond = pygame.image.load("fond.png").convert_alpha()


def afich_map(av):
    
    global yblocs
    global xblocs
    lines = [0]*461


    # Ouvrir le fichier en mode lecture
    with open('map1.pg', 'r') as fichier:
        # Lire toutes les lignes du fichier dans une liste
        lignes = fichier.readlines()


    for l in range(14):
        for c in range(30):
            lines[l*31+c] = lignes[l][c+av]

    XX = 0
    YY = 0
    LISTE_MURS.empty()
    #print("main",LISTE_MURS)
    LISTE_GLOBALE_SPRITES.empty()
    for l in range(14):
        for s in range(30):
            if lines[l*31+s]=="M" or lines[l*31+s]=="C":
                _mur = MUR(XX, YY, lines[l*31+s])
                LISTE_MURS.add(_mur)
                LISTE_GLOBALE_SPRITES.add(_mur)
            if lines[l*31+s]=="S":
                _sol = SOL(XX, YY)
                LISTE_SOLS.add(_sol)
                LISTE_GLOBALE_SPRITES.add(_sol)
            XX = XX + 1
        XX = 0
        YY = YY + 1



personnag = perso()



continuer=True

while continuer:
    w,h = pygame.display.get_surface().get_size()
    
    #print(personnag.rect.y)

    #colision(xperso,yperso)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left=1
            if event.key == pygame.K_RIGHT:
                right=1
            if event.key == pygame.K_SPACE:
                space=1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left=0
            if event.key == pygame.K_RIGHT:
                right=0
            if event.key == pygame.K_SPACE:
                space=0


    if left==1 and personnag.rect.x>0:
        fondx=fondx+10
    elif right==1:
        fondx=fondx-10
    if fondx>0:
        fondx=0


    symmetrical_frame = pygame.transform.flip(frames[current_frame], True, False)


    ecran.blit(fond,(fondx,0))
    LISTE_MURS.empty()
    LISTE_SOLS.empty()
    afich_map(personnag.rect.x)
    LISTE_MURS.update()
    LISTE_SOLS.update()
    personnag.avancer(right, left,space, ecran)

    LISTE_GLOBALE_SPRITES.draw(ecran)



    #print(personnag.xperso)


 

    # Limiter la vitesse de l'animation
    clock.tick(personnag.frame_rate)


    #ecran.blit(mur, (10, 10))

    pygame.display.flip()

pygame.quit()
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
pygame.display.set_caption("Mario Bros","Mario Bros")

background = pygame.Surface(ecran.get_size())
background.fill(NOIR)



fond = pygame.image.load("fond.png").convert_alpha()


def afich_map(av,a):
    
    global yblocs
    global xblocs


    # Ouvrir le fichier en mode lecture
    with open('map1.pg', 'r') as fichier:
        # Lire toutes les lignes du fichier dans une liste
        lignes = fichier.readlines()
        fichier.seek(0)
        lines = fichier.read()




    XX = -av
    YY = 0
    global nb
    nb = 0
    LISTE_MURS.empty()
    #print("main",LISTE_MURS)
    LISTE_GLOBALE_SPRITES.empty()
    for l in range(len(lignes)):
        #print(len(lignes[l]))
        
        for s in range(len(lignes[l])):
            if lines[XX]=="M" or lines[nb]=="C"  or lines[nb]=="B":
                if lines[XX]=="B":
                    _mur = MUR(XX, YY, lines[nb],"S")
                else:
                    _mur = MUR(XX, YY, lines[nb],"B")
                LISTE_MURS.add(_mur)
                LISTE_GLOBALE_SPRITES.add(_mur)
            if lines[nb]=="S":
                _sol = SOL(XX, YY)
                LISTE_SOLS.add(_sol)
                LISTE_GLOBALE_SPRITES.add(_sol)
            XX = XX + 1
            nb+=1
        XX = -av
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
    #personnag.avancer(right, left,space, ecran)
    #print("bc",personnag.a)
    afich_map(personnag.rect.x-9,personnag.a)
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
import pygame
import imageio
from gif import *
from classe import *
from time import sleep


pygame.init()

info = pygame.display.Info()

largeur_ecran = info.current_w
hauteur_ecran = info.current_h
'''
loading = pygame.display.set_mode((largeur_ecran/2,hauteur_ecran/2),pygame.NOFRAME | pygame.SWSURFACE)
w,h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Loading")

POLICE_ARIAL = pygame.font.SysFont("Arial",35,1,1)
with open('version.txt', 'r') as fichier:
    v = fichier.readline()
version = "version: "+str(v)
Text = POLICE_ARIAL.render(version,1,BLANC)
text_rect = Text.get_rect()
#print(text_rect[3],text_rect)
loading.blit(Text,(w/2-text_rect[2]/2,h/2-text_rect[3]/2))

pygame.display.flip()

sleep(4)

pygame.quit()
'''



left = 0
right = 0
space = 0
fondx = 0

elapsed_time = 0

marge = 0.1

xblocs = 0
yblocs = 0

colision_yperso = True
colision_xperso = True

ecran = pygame.display.set_mode((1300,650),pygame.RESIZABLE)
w,h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Mario Bros","Mario Bros")

nombre_manettes = pygame.joystick.get_count()
for i in range(nombre_manettes):
    manette = pygame.joystick.Joystick(i)
    manette.init()

background = pygame.Surface(ecran.get_size())
background.fill(NOIR)



fond = pygame.image.load("fond.png").convert_alpha()


# Ouvrir le fichier en mode lecture
with open('map1.pg', 'r') as fichier:
    # Lire toutes les lignes du fichier dans une liste
    lignes = fichier.readlines()
    fichier.seek(0)
    lines = fichier.read()

XX = 0
YY = 0
nb = 0
for l in range(len(lignes)):
    for s in range(len(lignes[l])):
        if lines[nb]=="C":
            _box = BOX(XX*TUILE_TAILLE, YY*TUILE_TAILLE)
            LISTE_BOX.add(_box)
            LISTE_GLOBALE_SPRITES.add(_box)
        if lines[nb]=="M":
            _mur = MUR(XX*TUILE_TAILLE, YY*TUILE_TAILLE)
            LISTE_MURS.add(_mur)
            LISTE_GLOBALE_SPRITES.add(_mur)
        if lines[nb]=="S":
            _sol = SOL(XX*TUILE_TAILLE, YY*TUILE_TAILLE)
            LISTE_SOLS.add(_sol)
            LISTE_GLOBALE_SPRITES.add(_sol)
        if lines[nb]=="G":
            _gomb = goomba(XX*TUILE_TAILLE, YY*TUILE_TAILLE)
            LISTE_GOOMBA.add(_gomb)
            LISTE_GLOBALE_SPRITES.add(_gomb)
        XX = XX + 1
        nb+=1
    XX = 0
    YY = YY + 1


def affich_map(av):
    LISTE_AFFICH.empty()
    for sprite in LISTE_GLOBALE_SPRITES:
        if left == 1:
            sprite.rect.x += 10
        if right ==1:
            sprite.rect.x -= 10

        
        if sprite.rect.x < w and sprite.rect.x > -45:
            LISTE_AFFICH.add(sprite)


personnag = perso()
goomb = goomba(500,0)




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
                start_time = pygame.time.get_ticks()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left=0
            if event.key == pygame.K_RIGHT:
                right=0
            if event.key == pygame.K_SPACE:
                space=0
                elapsed_time = pygame.time.get_ticks() - start_time
                if elapsed_time > 110:
                    elapsed_time = 110

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:
                space = 1

        if event.type == pygame.JOYBUTTONUP:
            if event.button == 1:
                space = 0


        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:

                if event.value < -0.5:
                    left = 1
                elif event.value > 0.5:
                    right = 1
                elif -marge < event.value < marge:
                    left = 0
                    right = 0


    if left==1 and personnag.rect.x>0:
        fondx=fondx+10
    elif right==1:
        fondx=fondx-10
    if fondx>0:
        fondx=0


    symmetrical_frame = pygame.transform.flip(frames[current_frame], True, False)


    ecran.blit(fond,(fondx,0))
    #personnag.avancer(right, left,space, ecran)
    #print("bc",personnag.a)
    affich_map(personnag.av)
    LISTE_AFFICH.update(ecran)
    if personnag.etat > 0:
        personnag.avancer(right, left,space, ecran, elapsed_time)
    elapsed_time = 0
    #LISTE_GOOMBA.draw(ecran)


    LISTE_AFFICH.draw(ecran)

    if personnag.etat == 0:
        #del personnag
        POLICE_ARIAL = pygame.font.SysFont("Arial",100,1,1)
        gameover = POLICE_ARIAL.render("GAMEOVER",1,ROUGE)
        gameover_rect = gameover.get_rect()
        ecran.blit(gameover,(w/2-gameover_rect[2]/2,h/2-gameover_rect[3]/2))
        #sleep(4)



    #print(personnag.xperso)


 

    # Limiter la vitesse de l'animation
    clock.tick(personnag.frame_rate)


    #ecran.blit(mur, (10, 10))

    pygame.display.flip()

pygame.quit()

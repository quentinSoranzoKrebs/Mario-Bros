import pygame
#from tk import messagebox
import imageio
from gif import *
from fonctions import *
from classe import *
from time import sleep ,time
import pygame_gui
from math import *
import sys



pygame.init()

info = pygame.display.Info()

largeur_ecran = info.current_w
hauteur_ecran = info.current_h

print(largeur_ecran,hauteur_ecran)

# intro

loading = pygame.display.set_mode((largeur_ecran/2,hauteur_ecran/2),pygame.HWSURFACE | pygame.NOFRAME | pygame.SRCALPHA)
w,h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Loading")

# Activer l'anti-aliasing sur la surface
loading.set_alpha(None)

with open('version.txt', 'r', encoding='utf-8') as file:
    v = file.readline().rstrip('\n\r')
version = "version: "+str(v)

vs = ecrire(BLANC, version, 50)

print(w,h)

start_time = time()

duree = 5

surface_ok = pygame.Surface((40,40), pygame.SRCALPHA)

r=100


start_angle = 0
end_angle = 3.14

a = 1
r=0

surface_2 = pygame.transform.rotate(surface_ok,r)

while time() - start_time < 5:
    r += -rad_2_deg(0.01)
    if r==360:
        r=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    if a==1:
        end_angle -= 0.01
    else:
        start_angle -= 0.01

    if end_angle < start_angle+0.01:
        a = 2
    elif start_angle < -pi:
        a = 1

    if start_angle < -pi and end_angle < -pi:
        start_angle = 3.14
        end_angle = 3.14

    if start_angle < -0 and end_angle > 3 and end_angle < pi:
        start_angle = 0.001
        end_angle = 3.14
        a = 1

    loading.fill(NOIR)
    surface_2.fill(NOIR)
    surface_ok.fill(NOIR)
    loading.blit(vs,(w/2-vs.get_width()/2,h/2-vs.get_height()/2))
    pygame.draw.arc(surface_ok, BLANC, pygame.Rect(0,0,surface_ok.get_width(),surface_ok.get_height()), start_angle, end_angle, 5)
    surface_2 = pygame.transform.rotate(surface_ok,r)

    loading.blit(surface_2,(surface_2.get_rect(center=(100//2,100//2))))
    pygame.display.flip()



pygame.quit()

pygame.init()



left = 0
right = 0
space = 0
fondx = 0

elapsed_time = 0
start_time = 0

marge = 0.1

clic = 0

xblocs = 0
yblocs = 0

colision_yperso = True
colision_xperso = True

avencement = 0

boutons = []

manettes = []

ecran = pygame.display.set_mode((largeur_ecran,hauteur_ecran),pygame.SHOWN | pygame.FULLSCREEN | pygame.SCALED , display=0)
w,h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Mario Bros","Mario Bros")

# Charger l'icône
icon = pygame.image.load("ico.png")


# Définir l'icône de la fenêtre
pygame.display.set_icon(icon)

coeur = pygame.image.load("ico.png").convert_alpha()
coeur = pygame.transform.scale(coeur, (TUILE_TAILLE*1.5,TUILE_TAILLE*1.5))

nombre_manettes = pygame.joystick.get_count()
for i in range(nombre_manettes):
    manettes.append(pygame.joystick.Joystick(i))
    manettes[i].init()
    print(manettes[i].get_name())




fond_load = pygame.image.load("fond.png").convert_alpha()
setting = pygame.image.load("tuiles/parametres.png").convert_alpha()
fond = pygame.transform.scale(fond_load, (h/607*3000,h))



# Ouvrir le fichier en mode lecture
with open('map4.pg', 'r') as fichier:
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
        if lines[nb]=="S" or lines[nb]== "s" or lines[nb]== "T" or lines[nb]== "-":
            _sol = SOL(XX*TUILE_TAILLE, YY*TUILE_TAILLE,lines[nb])
            LISTE_SOLS.add(_sol)
            LISTE_GLOBALE_SPRITES.add(_sol)
        if lines[nb]=="G":
            _gomb = goomba(XX*TUILE_TAILLE, YY*TUILE_TAILLE)
            LISTE_GOOMBA.add(_gomb)
            VIVANT.add(_gomb)
            LISTE_GLOBALE_SPRITES.add(_gomb)
        if lines[nb]=="." or lines[nb]=="*":
            ma_liste.append([XX*TUILE_TAILLE, YY*TUILE_TAILLE, lines[nb]])
        if lines[nb]=="|":
            pass


        XX = XX + 1
        nb+=1
    XX = 0
    YY = YY + 1

# Fonction de tri personnalisée
def custom_sort(item):
    return (item[0], item[2] != '*')

# Trier la liste en utilisant la fonction de tri personnalisée
lp = sorted(ma_liste, key=custom_sort)


for element in lp:
    del element[2]





w,h = pygame.display.get_surface().get_size()

surface_tuiles = pygame.Surface((w,5000), pygame.SRCALPHA)

surfaces = []

sol = pygame.image.load("tuiles/S.png").convert_alpha()

for i in range(len(lp)-1):
    x1,y1 = lp[i][0],lp[i][1]
    x2,y2 = lp[i+1][0],lp[i+1][1]
    try:
        pente = (y2-y1)/(x2-x1)
    except ZeroDivisionError:
        pente = 222
    coté1 = lp[i+1][0]-lp[i][0]
    coté2 = lp[i+1][1]-lp[i][1]
    coté3 = sqrt(coté1*coté1+coté2*coté2)
    angle = degrees(atan2(coté1, coté2))-90
    surfaces.append([0,0,0])
    surfaces[i][0] = pygame.Surface((coté3,TUILE_TAILLE), pygame.SRCALPHA)
    for n in range(round(coté3/TUILE_TAILLE)):
        surfaces[i][0].blit(sol,(n*TUILE_TAILLE,0))

    surfaces[i][0] = pygame.transform.rotate(surfaces[i][0], angle)
    surfaces[i][1],surfaces[i][2] = x1,y1
    if pente > 0:
        AB = TUILE_TAILLE
        C = 90
        B = angle
        print("angle",B)
        A = 180 - B - C
        CA = AB*sin(B)
        print(CA)
        surfaces[i][1],surfaces[i][2] = x1,y1
    elif pente < 0:
        surfaces[i][1],surfaces[i][2] = x1,y1+(y2-y1)



        
lp.insert(0, [0,h])
lp.append([lp[len(lp)-1][0],h])

def affich_map():
    for element in surfaces:
        if left == 1:
            personnag.direction = "l"
            element[1] += personnag.avance_gauche*1.4
                
        if right ==1:
            personnag.direction = "r"
            element[1] -= personnag.avance_droite*1.4
    
    LISTE_AFFICH.empty()
    if personnag.vie > 0:
        LISTE_AFFICH.add(personnag)
        
    for sprite in LISTE_GLOBALE_SPRITES:
        if left == 1:
            personnag.direction = "l"
            sprite.rect.x += personnag.avance_gauche*1.4
            
        if right ==1:
            personnag.direction = "r"
            sprite.rect.x -= personnag.avance_droite*1.4

        
        if sprite.rect.x < w and sprite.rect.x > -TUILE_TAILLE and sprite.etat and sprite.vie == 1:
            LISTE_AFFICH.add(sprite)

    for point in lp:
        if left == 1:
            personnag.direction = "l"
            point[0] += personnag.avance_gauche*1.4
        if right == 1:
            personnag.direction = "r"
            point[0] -= personnag.avance_droite*1.4

    
    if left == 1:
        personnag.avence += personnag.avance_gauche*1.4
        personnag.rect = pygame.Rect(personnag.rect.x, personnag.rect.y, 100, 100)
    if right == 1:
        personnag.avence -= personnag.avance_droite*1.4
        personnag.rect = pygame.Rect(personnag.rect.x, personnag.rect.y, 100, 100)
    else:
        personnag.rect = pygame.Rect(personnag.rect.x, personnag.rect.y, 30, 100)

personnag = perso()
VIVANT.add(personnag)
LISTE_AFFICH.add(personnag)


continuer=True
clock = pygame.time.Clock()

Quitter = btn("Quitter",quitter,50)
Setting = btn(setting,quitter,50)
text = ecrire(BLANC,"x"+str(personnag.vie), 50)


while continuer:
    time_delta = clock.tick(60) / 1000.0
    
    w,h = pygame.display.get_surface().get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter(None)
        if event.type == pygame.VIDEORESIZE:
            fond = pygame.transform.scale(fond_load, (h/607*3000,h))
            personnag.rect.x = w/2 - personnag.rect[2]/2
            lp[0][1] = h
            lp[len(lp)-1][1] = h
            print(lp)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                screenshot(ecran)
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
                elapsed_time = pygame.time.get_ticks() - start_time + 50
                if elapsed_time > 150:
                    elapsed_time = 150



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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clic = 1

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clic = 0


    if left==1 and personnag.rect.x>0 and personnag.avance_gauche>0:
        fondx=fondx+1
    elif right==1 and personnag.avance_droite>0:
        fondx=fondx-1
    if fondx>0:
        fondx=0

    if pygame.time.get_ticks() - start_time > 180 and space == 1:
        space = 0
        elapsed_time = 170


    ecran.blit(fond,(fondx,0))
    affich_map()
    pygame.draw.polygon(ecran, (227, 153, 76), lp)
    LISTE_GLOBALE_SPRITES.update(ecran)
    for sprite in VIVANT:
        sprite.collision(ecran, lp, right, left)
    if personnag.vie > 0:
        personnag.avancer(right, left, space, ecran, elapsed_time, lp)
        personnag.collision(ecran, lp, right, left)
        ecran.blit(coeur,(0,3))
        ecran.blit(text,(TUILE_TAILLE*1.5+1,9))

    elapsed_time = 0


    LISTE_AFFICH.draw(ecran)
    CADEAUX.draw(ecran)
    for i in range(len(surfaces)):
        ecran.blit(surfaces[i][0],(surfaces[i][1],surfaces[i][2]))


    if personnag.vie < 0:
        POLICE_ARIAL = pygame.font.SysFont("Arial",100,0,0)
        gameover = POLICE_ARIAL.render("GAMEOVER",1,ROUGE)
        gameover_rect = gameover.get_rect()
        ecran.blit(gameover,(w/2-gameover_rect[2]/2,h/2-gameover_rect[3]/2))

    for p in range(len(lp)-1):
        pygame.draw.line(ecran,ROUGE,(lp[p][0],lp[p][1]),(lp[p+1][0],lp[p+1][1]))


    clock.tick(personnag.frame_rate)

    #bouton(ecran,BLANC,"salut Machin",dire_bonjour,(50,50),50)

    Quitter.draw(ecran,[w-Quitter.get_width()-5,5],clic)
    Setting.draw(ecran,[Quitter.place[0]-Setting.get_width()-5,5],clic)


    ecran.blit(coeur,(0,0))

    pygame.display.flip()


pygame.quit()

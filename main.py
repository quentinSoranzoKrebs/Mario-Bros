import pygame
#from tk import messagebox
import imageio
from gif import *
from fonctions import *
from classe import *
from time import sleep
import pygame_gui



pygame.init()

info = pygame.display.Info()

largeur_ecran = info.current_w
hauteur_ecran = info.current_h

# intro
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
start_time = 0

marge = 0.1

clic = 0

xblocs = 0
yblocs = 0

colision_yperso = True
colision_xperso = True

boutons = []

ecran = pygame.display.set_mode((1300,650),pygame.RESIZABLE)
w,h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Mario Bros","Mario Bros")

# Charger l'icône
icone = pygame.image.load("ico.png")

# Définir l'icône de la fenêtre
pygame.display.set_icon(icone)

coeur = pygame.image.load("coeur.png").convert_alpha()
coeur = pygame.transform.scale(coeur, (30,30))

nombre_manettes = pygame.joystick.get_count()
for i in range(nombre_manettes):
    manette = pygame.joystick.Joystick(i)
    manette.init()

background = pygame.Surface(ecran.get_size())
background.fill(NOIR)



fond = pygame.image.load("fond.png").convert_alpha()
wt = round(h/(h-fond.get_height())*w)
print(wt)
fond = pygame.transform.scale(fond, (wt,h))


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

        XX = XX + 1
        nb+=1
    XX = 0
    YY = YY + 1

# Fonction de tri personnalisée
def custom_sort(item):
    return (item[0], item[2] != '*')

# Fonction de tri personnalisée
'''def custom_sort2(item):
    it = item[2]
    del item[2]
    return (item[0], it != '*')'''



# Trier la liste en utilisant la fonction de tri personnalisée
lp = sorted(ma_liste, key=custom_sort)


for element in lp:
    del element[2]


print(lp)


w,h = pygame.display.get_surface().get_size()

for i in range(len(lp)-1):
    x1,y1 = lp[i][0],lp[i][1]
    x2,y2 = lp[i+1][0],lp[i+1][1]
    if (x2-x1) == 0:
        pente = 1
    else:
        pente = (y2-y1)/(x2-x1)
    coté1 = lp[i+1][0]-lp[i][0]
    coté2 = lp[i+1][1]-lp[i][1]
    coté3 = math.sqrt(coté1*coté1+coté2*coté2)
    angle = math.degrees(math.atan2(coté1, coté2))-90
    test = Sol_line(0,0,angle,"S")
    larg = test.rect[2]
    rect = test.image.get_rect()
    for n in range(int(coté3/TUILE_TAILLE)):
        x = x1+n*TUILE_TAILLE
        y = y1+(x1 +n*TUILE_TAILLE-x1)*pente  #-math.sqrt(TUILE_TAILLE*TUILE_TAILLE-.rect[2]*)
        if pente > 0:
            _sol = Sol_line(x,y-rect[3]+18*2,angle,"S")
        else:
            _sol = Sol_line(x,y-rect[3]+18,angle,"S")

        LISTE_GLOBALE_SPRITES.add(_sol)

lp.insert(0, [0,h])
end = lp[len(lp)-1][0]
lp.insert(0, [end,h])

def affich_map(av):
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
        personnag.rect = pygame.Rect(personnag.rect.x, personnag.rect.y, 74, 74)
    if right == 1:
        personnag.rect = pygame.Rect(personnag.rect.x, personnag.rect.y, 74, 74)
    else:
        personnag.rect = pygame.Rect(personnag.rect.x, personnag.rect.y, 30, 74)

personnag = perso()
VIVANT.add(personnag)
LISTE_AFFICH.add(personnag)


continuer=True
clock = pygame.time.Clock()

Quitter = btn(BLANC,"Quitter",quitter,50)

while continuer:
    time_delta = clock.tick(60) / 1000.0
    
    w,h = pygame.display.get_surface().get_size()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter()
            

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

    #symmetrical_frame = pygame.transform.flip(frames[current_frame], True, False)


    ecran.blit(fond,(fondx,0))
    affich_map(personnag.av)
    pygame.draw.polygon(ecran, (227, 153, 76), lp)
    LISTE_AFFICH.update(ecran)
    liste_de_sprites = list(LISTE_point)
    for sprite in VIVANT:
        sprite.collision(ecran, lp, right, left)
    if personnag.vie > 0:
        personnag.avancer(right, left, space, ecran, elapsed_time, lp)
        personnag.collision(ecran, lp, right, left)
        ecran.blit(coeur,(0,3))
        ecrire(ecran,NOIR,"x"+str(personnag.vie),(35,0),40)

    elapsed_time = 0


    LISTE_AFFICH.draw(ecran)
    CADEAUX.draw(ecran)
    #LISTE_point.update(ecran)

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

    pygame.display.flip()

pygame.quit()

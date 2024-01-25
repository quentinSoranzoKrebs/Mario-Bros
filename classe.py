import pygame
import imageio
from constantes import *
from fonctions import *
from time import sleep
from random import randint
import math
#from tkinter import messagebox

pygame.init()

LISTE_OBJETS = pygame.sprite.Group()
LISTE_MURS = pygame.sprite.Group()
LISTE_SOLS = pygame.sprite.Group()
LISTE_GLOBALE_SPRITES = pygame.sprite.Group()
LISTE_BOX = pygame.sprite.Group()
CADEAUX = pygame.sprite.Group()
LISTE_GOOMBA = pygame.sprite.Group()
LISTE_AFFICH = pygame.sprite.Group()
LISTE_point = pygame.sprite.Group()
liste_point = pygame.sprite.Group()
VIVANT = pygame.sprite.Group()
lp = ()
ma_liste = []
ma_liste2 = []





class vivant():
    def __init__(self):
        self.direction = "l"
        self.sol = False
        self.etat = True
        self.pente = 0
        self.chute_vitesse = 20

    def collision(self, right, left, ecran, lp):
        self.sol = False
        X_COURANT = self.rect.x
        Y_COURANT = self.rect.y

        # collision avec le sol
        for i in range(len(lp)-1):
            if self.rect.clipline((lp[i][0],lp[i][1]),(lp[i+1][0],lp[i+1][1])):
                x1,y1 = lp[i][0],lp[i][1]
                x2,y2 = lp[i+1][0],lp[i+1][1]
                self.saut=0
                self.chute_vitesse = 0
                self.sol = True
                try:
                    self.pente = (y2-y1)/(x2-x1)
                except ZeroDivisionError:
                    pass
                self.rect.y = y1+self.pente*(self.rect.x-x1) - 70
        
        # collision avec les mur
        LISTE_COLLISION_MUR = pygame.sprite.spritecollide(self, LISTE_MURS, False)

        for bloc in LISTE_COLLISION_MUR:
            position_x = bloc.rect.x
            position_y = bloc.rect.y
            if position_y>self.rect.y+74/2:
                self.rect.y = position_y-73
                self.saut=0

            if position_y+45<self.rect.y+70:
                bloc.rect.y = bloc.rect.y - 10
                self.rect.y = Y_COURANT
                self.chute_vitesse = 40


            if position_x<self.rect.x and not position_y>self.rect.y+74/2:
                self.avance_gauche = 0
            if position_x>self.rect.x and not position_y>self.rect.y+74/2:
                self.avance_droite = 0

        if len(LISTE_COLLISION_MUR) > 0 :
            self.sol = True

        # aucune collision
        if not self.sol:    
            self.saut=1
            self.chute_vitesse += 1
            self.rect.y = self.rect.y + self.chute_vitesse
            self.avance_gauche = 10
            self.avance_droite = 10
        elif self.sol:
            self.chute_vitesse = 0



class MUR(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tuiles/M.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TUILE_TAILLE,TUILE_TAILLE))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.origine_y = y
        self.origine_x = x
        self.etat = True
        self.vie = 1
    def update(self,ecran):
        self.rect.y = self.origine_y
        


class SOL(pygame.sprite.Sprite):
    def __init__(self, x, y, B):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tuiles/S.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TUILE_TAILLE,TUILE_TAILLE))
        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.x = x
        self.etat = True
        self.vie = 1



class BOX(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tuiles/C.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TUILE_TAILLE,TUILE_TAILLE))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.etat = True
        self.vie = 1
        #print("ok")



class TUI(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tuiles/C.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TUILE_TAILLE,TUILE_TAILLE))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.etat = True
        self.vie = 1



class Sol_line(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, type):
        pygame.sprite.Sprite.__init__(self)
        if type == "S":
            self.image = pygame.image.load("tuiles/S.png").convert_alpha()
            self.rect = self.image.get_rect(center=(self.image.get_width()/2,self.image.get_height()/2))
            self.image = pygame.transform.rotate(self.image,angle)
            self.rect = self.image.get_rect(center=(self.image.get_width()/2,self.image.get_height()/2))
        elif type == "T":
            self.image = pygame.image.load("tuiles/T.png").convert_alpha()
            self.rect = self.image.get_rect(center=(self.image.get_width()/2,self.image.get_height()/2))
        self.rect.y = y
        self.rect.x = x
        self.etat = True
        self.vie = 1



class CAD(pygame.sprite.Sprite,vivant):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("champignon.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (TUILE_TAILLE,TUILE_TAILLE))
        self.image = pygame.transform.scale(self.image, (TUILE_TAILLE, TUILE_TAILLE))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.etat = True
        self.direction = "r"
        self.vie = 1

    def update(self,ecran):
        if self.etat:
            if self.direction == "r":
                self.rect.x -= 8
            else:
                self.rect.x += 8

            LISTE_COLLISION_SOL = pygame.sprite.spritecollide(self, LISTE_SOLS, False)
            LISTE_COLLISION_MUR = pygame.sprite.spritecollide(self, LISTE_MURS, False)

            for bloc in LISTE_COLLISION_SOL:
                position_x = bloc.rect.x
                position_y = bloc.rect.y
                self.rect.y = position_y-44

            for bloc in LISTE_COLLISION_MUR:
                position_x = bloc.rect.x
                position_y = bloc.rect.y
                if position_x+TUILE_TAILLE < self.rect.x+69 and not position_y > self.rect.y + 40:
                    self.direction = "l"

                if position_x > self.rect.x and not position_y > self.rect.y + 40:
                    self.direction = "r"

                if position_y > self.rect.y + 40:
                    self.rect.y = position_y-44

            if not len(LISTE_COLLISION_SOL) > 0 and not len(LISTE_COLLISION_MUR) > 0:
                self.rect.y +=20



class goomba(pygame.sprite.Sprite, vivant):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        vivant.__init__(self)


        gif_path = 'goomba.gif'

        self.imag = imageio.get_reader(gif_path)

        first_frame = self.imag.get_data(0)

        self.frames = [pygame.surfarray.make_surface(frame.swapaxes(0, 1)) for frame in self.imag]

        first_frame_surface = pygame.surfarray.make_surface(first_frame.swapaxes(0, 1))

        color_at_0_0 = first_frame_surface.get_at((0, 0))

        for frame in self.frames:
            frame.set_colorkey(color_at_0_0)

        clock = pygame.time.Clock()
        self.frame_rate = 15
        self.current_frame = 0

        self.symmetrical_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)
        self.image = self.frames[self.current_frame]
        self.rect = pygame.Rect(x, y, 70, 70)
        self.rect.y = y
        self.rect.x = x
        self.vie = 1


    def update(self,ecran):
        if self.vie > 0:
            self.symmetrical_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)
            if self.direction == "r":
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.rect.x -= 5
            elif self.direction == "l":
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.symmetrical_frame
                self.rect.x +=5

    def collision(self, right, left, ecran, lp):
        LISTE_COLLISION_MONSTRE = pygame.sprite.spritecollide(self, LISTE_GOOMBA, False)

        for bloc in LISTE_COLLISION_MONSTRE:
            position_x = bloc.rect.x
            position_y = bloc.rect.y
            if bloc.etat:
                if position_y-10 > self.rect.y:
                    self.sol = True
                    self.rect.y = bloc.rect.y-71
                    

        super().collision(right, left, ecran, lp)




class perso(pygame.sprite.Sprite, vivant):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        vivant.__init__(self)

        gif_path = 'mario2.gif'

        self.imge = imageio.get_reader(gif_path)
        self.img_stabler = pygame.image.load("stabler1.png").convert_alpha()
        self.img_stabler = pygame.transform.scale(self.img_stabler, (75,75))
        self.img_stablel = pygame.image.load("stablel1.png").convert_alpha()
        self.img_stablel = pygame.transform.scale(self.img_stablel, (75,75))


        first_frame = self.imge.get_data(0)

        self.frames = [pygame.surfarray.make_surface(frame.swapaxes(0, 1)) for frame in self.imge]

        first_frame_surface = pygame.surfarray.make_surface(first_frame.swapaxes(0, 1))

        color_at_0_0 = first_frame_surface.get_at((0, 0))

        for frame in self.frames:
            frame.set_colorkey(color_at_0_0)

        clock = pygame.time.Clock()
        self.frame_rate = 15
        self.current_frame = 0


        self.image = self.img_stabler
        self.rect =  pygame.Rect(500, 0, 74, 74)
        self.rect.x = 500
        self.rect.y = 0
        self.av = 0
        #self.direction = "r"
        self.saut = 0
        self.chute_vitesse = 20
        self.av_vitesse = 5
        self.vie = 4

        self.ldirect=True
        self.rdirect=True
        self.avance_droite = 10
        self.avance_gauche = 10
        
        #print("self.rect: ",self.rect)

    def avancer(self, right, left, space, ecran, time, lp):

        if self.pente > 0:
            self.avance_gauche = self.pente*10
        elif self.pente < 0:
            self.avance_droite = self.pente*10
        else:
            self.avance_gauche = 10
            self.avance_droite = 10


        if time > 0 and self.saut == 0 and space == 0:
            self.saut = 1
            self.chute_vitesse = -time/10
            self.rect.y = self.rect.y + self.chute_vitesse
            self.saut_vitesse = time/3
        self.symmetrical_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)

        if self.saut == 1:
            #self.rect.y -= self.saut_vitesse
            self.current_frame = 1
            if self.direction == "l":
                self.symmetrical_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)
                self.image = self.symmetrical_frame
            else:
                self.image = self.frames[self.current_frame]


        if self.saut == 0:
            if self.direction == "r":
                self.image = self.img_stabler
            elif self.direction == "l":
                self.image = self.img_stablel


            if right==1 and self.rdirect:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
            elif left==1 and self.ldirect:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.symmetrical_frame
            
    def collision(self, right, left, ecran, lp):
        super().collision(right, left, ecran, lp)

        LISTE_COLLISION_MONSTRE = pygame.sprite.spritecollide(self, LISTE_GOOMBA, False)

        for bloc in LISTE_COLLISION_MONSTRE:
            position_x = bloc.rect.x
            position_y = bloc.rect.y
            if bloc.etat:
                if position_y > self.rect.y + 50:
                    bloc.vie = 0
                    bloc.etat=False
                    self.saut = 1
                    self.chute_vitesse = -5

                self.vie -= 1


        LISTE_COLLISION_BOX = pygame.sprite.spritecollide(self, LISTE_BOX, False)
        if len(LISTE_COLLISION_BOX) > 0:
            for bloc in LISTE_COLLISION_BOX:
                position_x = bloc.rect.x
                position_y = bloc.rect.y
                self.saut_vitesse = 0
                if position_y+45<self.rect.y+70 and bloc.vie == 1:
                    bloc.vie = 0
                    self.rect.y=position_y+TUILE_TAILLE+10
                    _cad = CAD(position_x,position_y-100)
                    CADEAUX.add(_cad)
                    #LISTE_AFFICH.add(_cad)
                    LISTE_GLOBALE_SPRITES.add(_cad)
                    #print("cadeau")



class btn:
    def __init__(self,couleur,text,suite,taille):
        self.place = [0,0]
        font = pygame.font.Font("calibri-font/calibri-regular.ttf", taille)
        self.text = font.render(text,1,couleur)
        self.text_rect = self.text.get_rect()
        self.rect = pygame.Rect(self.place[0], self.place[1], self.text_rect[2]+taille/2*2, self.text_rect[3]+taille/3*2)
        self.rect_rect = pygame.Rect(0,0, self.text_rect[2]+taille/2*2, self.text_rect[3]+taille/3*2)
        self.surface = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        self.taille = taille
        self.suite = suite
    def draw(self,surface,place,clic):
        self.place = place
        self.rect = pygame.Rect(self.place[0], self.place[1], self.text_rect[2]+self.taille/2*2, self.text_rect[3]+self.taille/3*2)
        self.surface = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        point = pygame.mouse.get_pos()
        collide = self.rect.collidepoint(point)
        if collide:
            color = (0,115,229,255)
            if clic == 1:
                self.suite()
        else:
            color = (200,200,200,200)
        draw_rounded_rect(self.surface, color, self.rect_rect, self.taille/1.2)
        self.surface.blit(self.text,(self.taille/2,self.taille/3))
        surface.blit(self.surface,(self.rect[0],self.rect[1]))
    def get_width(self):
        return self.rect[2]
    def get_height(self):
        return self.rect[3]
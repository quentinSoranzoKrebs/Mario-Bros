import pygame
import imageio
from constantes import *
from fonctions import *
from time import sleep
from random import randint
from typing import *    
import platform

'''
system = platform.system()

if system == 'Linux':

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess
#from tkinter import messagebox
'''
pygame.init()

LISTE_OBJETS = pygame.sprite.Group()
LISTE_MURS = pygame.sprite.Group()
LISTE_SOLS = pygame.sprite.Group()
LISTE_GLOBALE_SPRITES = pygame.sprite.Group()
LISTE_BOX = pygame.sprite.Group()
CADEAUX = pygame.sprite.Group()
LISTE_GOOMBA = pygame.sprite.Group()
LISTE_AFFICH = pygame.sprite.Group()
VIVANT = pygame.sprite.Group()
lp = ()
ma_liste = []



class vivant():
    def __init__(self):
        self.direction = "l"
        self.sol = False
        self.etat = True
        self.pente = 0
        self.chute_vitesse = 20

    def collision(self, ecran, lp, right=0, left=0):
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
                    if self.pente < 0:
                        if self.direction == "r":
                            self.rect.y = y1+((self.rect[2]+self.rect.x)-x1)*self.pente - self.rect[3]+13
                        else:
                            self.rect.y = y1+self.pente*((self.rect[2]+self.rect.x)-x1) - self.rect[3]+13
                    else:
                        if self.direction == "r":
                            self.rect.y = y1+self.pente*((self.rect.x)-x1) - self.rect[3]+13
                        else:
                            self.rect.y = y1+self.pente*((self.rect.x)-x1) - self.rect[3]+1
                except ZeroDivisionError:
                    if self.direction == "r":
                        self.avance_droite = 0
                    if self.direction == "l":
                        self.avance_gauche = 0
        
        # collision avec les mur
        LISTE_COLLISION_MUR = pygame.sprite.spritecollide(self, LISTE_MURS, False)

        for bloc in LISTE_COLLISION_MUR:
            position_x = bloc.rect.x
            position_y = bloc.rect.y
            if position_y>self.rect.y+self.rect[3]/2:
                self.rect.y = position_y-self.rect[3]+3
                self.saut=0
                self.sol = True


            if position_y+bloc.rect[3]<self.rect.y+self.rect[3]/2:
                bloc.rect.y = bloc.rect.y - 10
                self.rect.y = Y_COURANT
                self.chute_vitesse = 20

            if position_x<self.rect.x+self.rect[2] and not position_y>self.rect.y+self.rect[3]/2:
                self.collision_droite()
            if position_x>self.rect.x and not position_y>self.rect.y+self.rect[3]/2:
                self.collision_gauche()
                

        LISTE_COLLISION_BOX = pygame.sprite.spritecollide(self, LISTE_BOX, False)
        for bloc in LISTE_COLLISION_BOX:
            position_x = bloc.rect.x
            position_y = bloc.rect.y
            if position_y>self.rect.y+self.rect[3]/2:
                self.rect.y = position_y-self.rect[3]+3
                self.saut=0
                self.sol = True            




        # aucune collision
        if not self.sol:
            self.saut=1
            self.chute_vitesse += 1
            self.rect.y = self.rect.y + self.chute_vitesse
        elif self.sol:
            self.chute_vitesse = 0

    def collision_droite(self):
        self.direction = "l"

    def collision_gauche(self):
        self.direction = "r"


class tuile():
    def __init__(self):
        pass
    def resize(self,width,height):
        self.image = pygame.transform.scale(self.image, (width,height))


class MUR(pygame.sprite.Sprite,tuile):
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
    def resize(self,width,height):
        self.image = pygame.image.load("tuiles/M.png").convert_alpha()
        super().resize(width,height)
        

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
        self.origine_y = y
        self.origine_x = x
        self.etat = True
        self.vie = 1
        #print("ok")
    def update(self,ecran):
        self.rect.y = self.origine_y


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
        vivant.__init__(self)

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

    def collision(self,ecran, lp, right, left):
        super().collision(ecran, lp, right, left)


class END(pygame.sprite.Sprite):
    pass


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

    def collision(self, ecran, lp, right, left):
        LISTE_COLLISION_MONSTRE = pygame.sprite.spritecollide(self, LISTE_GOOMBA, False)

        for bloc in LISTE_COLLISION_MONSTRE:
            position_x = bloc.rect.x
            position_y = bloc.rect.y
            if bloc.etat:
                if position_y-10 > self.rect.y:
                    self.sol = True
                    self.rect.y = bloc.rect.y-71
                    

        super().collision(ecran, lp, right, left)


class perso(pygame.sprite.Sprite, vivant):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        vivant.__init__(self)

        gif_path = 'mario3.gif'

        self.imge = imageio.get_reader(gif_path)
        self.img_stabler = pygame.image.load("stabler1.png").convert_alpha()
        #self.img_stabler = pygame.transform.scale(self.img_stabler, (75,75))
        self.img_stablel = pygame.image.load("stablel1.png").convert_alpha()
        #self.img_stablel = pygame.transform.scale(self.img_stablel, (75,75))


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
        self.avence = 1
        
        #print("self.rect: ",self.rect)

    def avancer(self, right, left, space, ecran, time, lp):
        w,h = pygame.display.get_surface().get_size()

        if self.avence < 0:
            if self.pente > 0:
                self.avance_gauche = 10-self.pente*5
            elif self.pente < 0:
                self.avance_droite = 10+self.pente*5
            else:
                self.avance_gauche = 10
                self.avance_droite = 10
        else:
            self.avance_gauche = 0
        
        print(self.avence)


        if time > 0 and self.saut == 0 and space == 0:
            self.saut = 1
            self.chute_vitesse = -time/10
            self.rect.y = self.rect.y + self.chute_vitesse
            self.saut_vitesse = time/3
        self.symmetrical_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)

        if self.saut == 1:
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


        if self.rect.y > h:
            self.vie = (-1)
                       
    def collision(self, right, left, ecran, lp):
        X_COURANT = self.rect.x
        Y_COURANT = self.rect.y
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

                elif position_x<self.rect.x and not position_y>self.rect.y+74/2:
                    self.vie -= 1
                    self.rect.x+=50
                    self.rect.y-=50
                    sleep(0.3)
                elif position_x>self.rect.x and not position_y>self.rect.y+74/2:
                    self.vie -= 1
                    self.rect.x-=50
                    self.rect.y-=50
                    sleep(0.3)

                else:
                    self.vie -= 1


        LISTE_COLLISION_BOX = pygame.sprite.spritecollide(self, LISTE_BOX, False)
        for bloc in LISTE_COLLISION_BOX:
            position_x = bloc.rect.x
            position_y = bloc.rect.y
            if position_y+45<self.rect.y+70 and bloc.vie == 1:
                self.rect.y=position_y+TUILE_TAILLE+10
                bloc.rect.y = bloc.rect.y - 10
                _cad = CAD(position_x,position_y-TUILE_TAILLE)
                CADEAUX.add(_cad)
                VIVANT.add(_cad)
                LISTE_GLOBALE_SPRITES.add(_cad)
                self.rect.y = Y_COURANT
                self.chute_vitesse = 20


                

        LISTE_COLLISION_CAD = pygame.sprite.spritecollide(self, CADEAUX, True)
        if len(LISTE_COLLISION_CAD) > 0:
            self.vie += 1

    def collision_droite(self):
        self.avance_droite = 0

    def collision_gauche(self):
        self.avance_gauche = 0
        

class btn:
    def __init__(self,
                 element: Union[str,pygame.Surface],
                 suite,
                 taille,
                 marge = 2,
                 rounde = 4,
                 arg = None,
                 initial_color = (200,200,200,200),
                 final_color = (0,115,229,255),
                 effet = None):
        
        self.place = [0,0]
        self.arg = arg
        self.couleur = BLANC
        self.marge = marge
        self.initial_color = initial_color
        self.final_color = final_color
        self.is_clic = False
        if isinstance(element, pygame.Surface):
            self.element = element
            if effet:
                self.effet = effet
                self.effet = pygame.transform.scale(effet, (taille,taille))
            self.element = pygame.transform.scale(element, (taille,taille))
            self.element_rect = self.element.get_rect()
        else:
            self.text = element
            font = pygame.font.Font("calibri-font/calibri-regular.ttf", taille)
            self.element = font.render(element,1,self.couleur)
            self.element_rect = self.element.get_rect()
        self.rect = pygame.Rect(self.place[0], self.place[1], self.element_rect[2]+taille/self.marge*2, self.element_rect[3]+taille/(self.marge+1)*2)
        self.rect_rect = pygame.Rect(0,0, self.element_rect[2]+taille/self.marge*2, self.element_rect[3]+taille/(self.marge+1)*2)
        self.surface = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        self.taille = taille
        self.suite = suite
        self.rounde = self.rect_rect[3]/rounde
    
    def draw(self,surface,place,clic):
        self.place = place
        self.rect = pygame.Rect(self.place[0], self.place[1], self.element_rect[2]+self.taille/self.marge*2, self.element_rect[3]+self.taille/(self.marge+1)*2)
        self.surface = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        point = pygame.mouse.get_pos()
        collide = self.rect.collidepoint(point)
        if collide:
            self.is_clic = False
            color = self.final_color
            if clic == 1:
                self.is_clic = True
                self.suite(self.arg)
        else:
            color = self.initial_color
        draw_rounded_rect(self.surface, color, self.rect_rect, self.rounde)
        self.surface.blit(self.element,(self.taille/self.marge,self.taille/(self.marge+1)))
        surface.blit(self.surface,(self.rect[0],self.rect[1]))
    
    def set_color(self,couleur):
        self.couleur = couleur
        print(couleur)
        font = pygame.font.Font("calibri-font/calibri-regular.ttf", self.taille)
        self.element = font.render(self.text,1,self.couleur)
        self.element_rect = self.element.get_rect()

    def get_width(self):
        return self.rect[2]
    
    def get_height(self):
        return self.rect[3]
    
    def get_clic(self):
        return self.is_clic


class btn2:
    def __init__(self,
                 command,
                 text = None,
                 image = None,
                 marge = 2,
                 round = 4,
                 initial_color = (200,200,200,200),
                 final_color = (0,115,229,255),
                 text_color = BLANC,
                 text_taille = 40,
                 width = None,
                 height = None
                 ):
        
        if width and height:
            self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

        if text:
            self.text = ecrire(text_color,text,text_taille)
            if not width and not height:
                self.surface = pygame.Surface((self.text.get_width()+(marge*2), self.text.get_height()+(marge*2)), pygame.SRCALPHA)        
                self.surface.fill(ROUGE)
            self.surface.blit(self.text,(marge,10))
        if image:            
            if not width and not height:
                self.surface = pygame.Surface((image.get_width()+marge*2, image.get_width()+marge*2), pygame.SRCALPHA)
            self.surface.blit(image,(0,0))

 
    def draw(self,
             surface):
        surface.blit(self.surface,(self.pos))   
        
    def place(self,
              x,
              y):
        w,h = pygame.display.get_surface().get_size()
        self.pos = x*w,y*h

        



class setting_bar:
    def __init__(self,
                 image,
                 text,
                 sous_text,
                 suite,
                 arg = None,
                 rounde = 10,
                 initial_color = (200,200,200,200),
                 final_color = (0,115,229,255)
                 ):
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (TUILE_TAILLE*1.5,TUILE_TAILLE*1.5))
        self.text = ecrire(BLANC,text,40)
        w,h = pygame.display.get_surface().get_size()
        self.rect = pygame.Rect(0,0,round(0.94*w),round(w/17))
        self.surface = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        draw_rounded_rect(self.surface, (50, 50,50), self.rect, rounde)
        self.surface.blit(self.text,(self.image.get_width()+w/40,0))
        self.surface.blit(self.image,(0,0))


    def __call__(self) -> pygame.surface:
        return self.surface
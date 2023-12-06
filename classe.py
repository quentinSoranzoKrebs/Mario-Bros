import pygame
import imageio
from constantes import *

pygame.init()

LISTE_OBJETS = pygame.sprite.Group()
LISTE_MURS = pygame.sprite.Group()
LISTE_SOLS = pygame.sprite.Group()
LISTE_GLOBALE_SPRITES = pygame.sprite.Group()
LISTE_BOX = pygame.sprite.Group()
CADEAUX = pygame.sprite.Group()
LISTE_GOOMBA = pygame.sprite.Group()
LISTE_AFFICH = pygame.sprite.Group()


class MUR(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("M.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.origine_y = y
        self.origine_x = x
        self.etat = True
    def update(self,ecran):
        self.rect.y = self.origine_y
        


class SOL(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("S.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.x = x
        self.etat = True


class BOX(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.etat = True
        #print("ok")


class CAD(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("champignon.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.x = x
        self.etat = True


class goomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)


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
        self.direction = "right"
        self.vie = 1
        self.etat = True


    def update(self,ecran):
        if self.vie > 0:
            self.symmetrical_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)
            if self.direction == "right":
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.rect.x -= 5
            elif self.direction == "left":
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.symmetrical_frame
                self.rect.x +=5

            LISTE_COLLISION_SOL = pygame.sprite.spritecollide(self, LISTE_SOLS, False)
            LISTE_COLLISION_MUR = pygame.sprite.spritecollide(self, LISTE_MURS, False)

            for bloc in LISTE_COLLISION_SOL:
                position_x = bloc.rect.x
                position_y = bloc.rect.y
                self.rect.y = position_y-67

            for bloc in LISTE_COLLISION_MUR:
                position_x = bloc.rect.x
                position_y = bloc.rect.y
                if position_x+TUILE_TAILLE < self.rect.x+69 and not position_y > self.rect.y + 40:
                    self.direction = "left"

                if position_x > self.rect.x and not position_y > self.rect.y + 40:
                    self.direction = "right"

                if position_y > self.rect.y + 40:
                    self.rect.y = position_y-67

            if not len(LISTE_COLLISION_SOL) > 0 and not len(LISTE_COLLISION_MUR) > 0:
                self.rect.y +=20




class perso(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)



        gif_path = 'mario2.gif'

        self.imge = imageio.get_reader(gif_path)
        self.img_stabler = pygame.image.load("stabler.png").convert_alpha()
        self.img_stablel = pygame.image.load("stablel.png").convert_alpha()


        first_frame = self.imge.get_data(0)

        self.frames = [pygame.surfarray.make_surface(frame.swapaxes(0, 1)) for frame in self.imge]

        first_frame_surface = pygame.surfarray.make_surface(first_frame.swapaxes(0, 1))

        color_at_0_0 = first_frame_surface.get_at((0, 0))

        for frame in self.frames:
            frame.set_colorkey(color_at_0_0)

        clock = pygame.time.Clock()
        self.frame_rate = 15
        self.current_frame = 0

        self.image = self.img_stablel
        self.rect =  pygame.Rect(500, 0, 35, 74)
        self.rect.x = 500
        self.rect.y = 0
        self.av = 0
        self.orientation = "-"
        self.saut = 0
        self.saut_pos = 0
        self.saut_fin = 0
        self.chute_vitesse = 20
        self.saut_vitesse = 38
        self.av_vitesse = 5
        self.vie = 4

        self.ldirect=True
        self.rdirect=True
        self.a = 0
        self.etat = True
        self.avance_droite = 10
        self.avance_gauche = 10
        
        #print("self.rect: ",self.rect)

    def avancer(self, right, left, space, ecran, time):
        #self.chute_vitesse +=0.4
        if time > 0 and self.saut == 0:
            self.saut = 1
            self.saut_vitesse = time/3
        X_COURANT = self.rect.x
        Y_COURANT = self.rect.y
        AV_COURANT = self.av
        self.symmetrical_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)

        if self.saut == 1:
            self.rect.y -= self.saut_vitesse
            self.saut_vitesse -=1
            self.current_frame = 1
            if self.orientation == "l":
                self.symmetrical_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)
                self.image = self.symmetrical_frame
            else:
                self.image = self.frames[self.current_frame]


        if self.saut == 0:
            if self.orientation == "r":
                self.image = self.img_stabler
            elif self.orientation == "l":
                self.image = self.img_stablel


            if right==1 and self.rdirect:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
            elif left==1 and self.ldirect:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.symmetrical_frame
            


        
        LISTE_COLLISION_MUR = pygame.sprite.spritecollide(self, LISTE_MURS, False)

        self.avance_gauche = 10
        self.avance_droite = 10
        for bloc in LISTE_COLLISION_MUR:
            position_x = bloc.rect.x
            position_y = bloc.rect.y
            if position_y>self.rect.y+74/2:
                self.rect.y = position_y-73
                self.saut=0
                self.saut_vitesse = 38
                self.chute_vitesse = 20

            if position_y+45<self.rect.y+70:
                bloc.rect.y = bloc.rect.y - 10
                self.rect.y = Y_COURANT
                self.saut_vitesse = 0


            if position_x<self.rect.x and not position_y>self.rect.y+74/2:
                self.avance_gauche = 0
            if position_x>self.rect.x and not position_y>self.rect.y+74/2:
                self.avance_droite = 0
            


        LISTE_COLLISION_SOL = pygame.sprite.spritecollide(self, LISTE_SOLS, False)
        for bloc in LISTE_COLLISION_SOL:
            position_x = bloc.rect.x
            position_y = bloc.rect.y
            self.saut=0
            self.saut_vitesse = 38
            self.chute_vitesse = 20
            self.rect.y = position_y-73

        if not len(LISTE_COLLISION_SOL) > 0 and not len(LISTE_COLLISION_MUR) > 0:
            self.rect.y=self.rect.y+self.chute_vitesse
            self.avance_gauche = 10
            self.avance_droite = 10


        LISTE_COLLISION_MONSTRE = pygame.sprite.spritecollide(self, LISTE_GOOMBA, False)

        for bloc in LISTE_COLLISION_MONSTRE:
            position_x = bloc.rect.x
            position_y = bloc.rect.y
            if bloc.etat:
                if position_y > self.rect.y + 50:
                    bloc.vie = 0
                    bloc.etat=False
                    self.saut = 1
                    self.saut_vitesse = 30

                self.vie -= 1


'''        LISTE_COLLISION_BOX = pygame.sprite.spritecollide(self, LISTE_BOX, False)
        if len(LISTE_COLLISION_BOX) > 0:
            for bloc in LISTE_COLLISION_BOX:
                positionbloc_x = bloc.rect.x
                positionbloc_y = bloc.rect.y
                if positionbloc_y<self.rect.y:
                    self.rect.y=positionbloc_y+TUILE_TAILLE+10
                    _cad = CAD(positionbloc_x,positionbloc_y-100)
                    CADEAUX.add(_cad)
                    LISTE_GLOBALE_SPRITES.add(_cad)'''
                
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

class MUR(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("M.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class SOL(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("S.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.x = x


class BOX(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        #print("ok")


class CAD(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("champignon.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.x = x


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

        self.image = self.frames[self.current_frame]
        self.rect = pygame.Rect(x, y, 550, 550)
        self.rect.y = y
        self.rect.x = x
    def update(self,ecran):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        ecran.blit(self.frames[self.current_frame], (self.rect.x, self.rect.y))


class perso(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)



        gif_path = 'mario2.gif'

        self.image = imageio.get_reader(gif_path)
        self.img_stabler = pygame.image.load("stabler.png").convert_alpha()
        self.img_stablel = pygame.image.load("stablel.png").convert_alpha()


        first_frame = self.image.get_data(0)

        self.frames = [pygame.surfarray.make_surface(frame.swapaxes(0, 1)) for frame in self.image]

        first_frame_surface = pygame.surfarray.make_surface(first_frame.swapaxes(0, 1))

        color_at_0_0 = first_frame_surface.get_at((0, 0))

        for frame in self.frames:
            frame.set_colorkey(color_at_0_0)

        clock = pygame.time.Clock()
        self.frame_rate = 15
        self.current_frame = 0

        self.rect = self.img_stablel.get_rect()
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

        self.ldirect=True
        self.rdirect=True
        self.a = 0
        
        #print("self.rect: ",self.rect)

    def avancer(self, right, left, space, ecran):
        self.chute_vitesse +=0.4
        if self.saut == 1:
            self.saut_vitesse -=1
        X_COURANT = self.rect.x
        Y_COURANT = self.rect.y
        AV_COURANT = self.av
        self.symmetrical_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)
        if space==1:
            self.rect.y -= self.saut_vitesse
            self.saut = 1

        if right==1 and self.rdirect:
            if self.rect.x>500:
                self.orientation = "r"
                self.av += self.av_vitesse
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                ecran.blit(self.frames[self.current_frame], (self.rect.x, self.rect.y))
            else:
                self.orientation = "r"
                self.rect.x += self.av_vitesse
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                ecran.blit(self.frames[self.current_frame], (self.rect.x, self.rect.y))
        elif left==1 and self.av>-500 and self.ldirect:
            if self.av>0:
                self.orientation = "l"
                self.av -= 20
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                ecran.blit(self.symmetrical_frame, (self.rect.x, self.rect.y))
            else:
                self.orientation = "l"
                self.rect.x -= 20
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                ecran.blit(self.symmetrical_frame, (self.rect.x, self.rect.y))

        else:
            if self.orientation=="r":
                ecran.blit(self.img_stabler,(self.rect.x,self.rect.y))
            else:
                ecran.blit(self.img_stablel,(self.rect.x,self.rect.y))

        if left == 1 or right == 1:
            if self.av_vitesse < 10:
                self.av_vitesse +=0.2

        
        LISTE_COLLISION_MUR = pygame.sprite.spritecollide(self, LISTE_MURS, False)

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

            if position_x<self.rect.x and not position_y>self.rect.y+74/2 and not position_y+45<self.rect.y+70:
                self.av += (self.rect.x-position_x)

            if position_x>self.rect.x+100 and not position_y>self.rect.y+74/2 and not position_y+45<self.rect.y+70:
                self.av -= (position_x-self.rect.x)


            


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
                
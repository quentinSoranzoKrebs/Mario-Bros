import pygame
import imageio
from constantes import *

pygame.init()

LISTE_OBJETS = pygame.sprite.Group()
LISTE_MURS = pygame.sprite.Group()
LISTE_SOLS = pygame.sprite.Group()
LISTE_GLOBALE_SPRITES = pygame.sprite.Group()
murpos = []

class MUR(pygame.sprite.Sprite):
    def __init__(self, x, y, b, e):
        pygame.sprite.Sprite.__init__(self)
        if b=="M" or b=="B":
            self.image = pygame.image.load("M.png").convert_alpha()
        if b=="C":
            self.image = pygame.image.load("C.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.etat = e
        global murpos
        murpos.append(self.rect.x)
        murpos.append(self.rect.y)

class SOL(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("S.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.x = x






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

        self.rect = self.frames[self.current_frame].get_rect()
        self.rect.x = 500
        self.rect.y = 0
        self.av = 0
        self.orientation = "-"
        self.orientation_up_down = "up"

        self.ldirect=True
        self.rdirect=True
        self.a = 0
        
        print("self.rect: ",self.rect)

    def avancer(self, right, left, space, ecran):
        X_COURANT = self.rect.x
        Y_COURANT = self.rect.y
        self.symmetrical_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)
        if space==1 and self.rect.y>350:
            self.rect.y = self.rect.y - 100
            ecran.blit(self.img_stabler,(self.rect.x,self.rect.y))
        if right==1 and self.rdirect:
            if self.rect.x>500:
                self.orientation = "r"
                self.av += 10
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                ecran.blit(self.frames[self.current_frame], (self.rect.x, self.rect.y))
            else:
                self.orientation = "r"
                self.rect.x += 10
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                ecran.blit(self.frames[self.current_frame], (self.rect.x, self.rect.y))
            print(self.av)
        elif left==1 and self.av>-500 and self.ldirect:
            if self.av>0:
                self.orientation = "l"
                self.av -= 10
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                ecran.blit(self.symmetrical_frame, (self.rect.x, self.rect.y))
            else:
                self.orientation = "l"
                self.rect.x -= 10
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                ecran.blit(self.symmetrical_frame, (self.rect.x, self.rect.y))

        else:
            if self.orientation=="r":
                ecran.blit(self.img_stabler,(self.rect.x,self.rect.y))
            else:
                ecran.blit(self.img_stablel,(self.rect.x,self.rect.y))


        
        LISTE_COLLISION_MUR = pygame.sprite.spritecollide(self, LISTE_MURS, False)
        #if self.orientation_up_down == "up":
        global murpos
        if len(LISTE_COLLISION_MUR) > 0:
            self.rect.y=self.rect.y-20
        #print("x:",self.rect.x,"      colision",LISTE_COLLISION_MUR,"    Liste mur",murpos)

        '''elif self.orientation_up_down == "down":
            if len(LISTE_COLLISION_MUR) > 0 and self.orientation=="r":
           rect.x-9     self.rdirect=False
            else:
                self.rdirect=True
            
            if len(LISTE_COLLISION_MUR) > 0 and self.orientation=="l":
                self.ldirect=False
            else:
                self.ldirect=True
            print(self.rect.x)'''

        LISTE_COLLISION_SOL = pygame.sprite.spritecollide(self, LISTE_SOLS, False)
        if len(LISTE_COLLISION_SOL) > 0:
            self.orientation_up_down = "down"

        if not len(LISTE_COLLISION_SOL) > 0:
            self.rect.y=self.rect.y+20


        if Y_COURANT<self.rect.y:
            self.orientation_up_down = "up"
        if Y_COURANT>self.rect.y:
            self.orientation_up_down = "down"
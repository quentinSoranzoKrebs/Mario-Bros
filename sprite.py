import pygame

def set_sprite():
    global M
    global C
    global S
    m = pygame.image.load("M.png").convert_alpha()
    mnt = (int(m.get_width() / 7), int(m.get_height() / 7))
    M = pygame.transform.scale(m, mnt)

    c = pygame.image.load("C.png").convert_alpha()
    cnt = (int(c.get_width() / 6), int(c.get_height() / 6))
    C = pygame.transform.scale(c, cnt)

    s = pygame.image.load("S.png").convert_alpha()
    snt = (int(s.get_width() / 6), int(s.get_height() / 6))
    S = pygame.transform.scale(s, snt)
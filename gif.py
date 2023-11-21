import pygame
import imageio
import numpy as np

pygame.init()

# Charger le GIF en utilisant imageio
gif_path = 'mario2.gif'
gif = imageio.get_reader(gif_path)


# Récupérer les dimensions du GIF en utilisant la première frame
first_frame = gif.get_data(0)
width, height = first_frame.shape[1], first_frame.shape[0]



# Initialiser Pygame
#screen = pygame.display.set_mode((width, height))
#pygame.display.set_caption('Animation GIF dans Pygame')

# Charger les frames du GIF en utilisant numpy et pygame.surfarray, en rendant le blanc transparent
frames = [pygame.surfarray.make_surface(frame.swapaxes(0, 1)) for frame in gif]

# Charger la première frame du GIF en utilisant numpy et pygame.surfarray
first_frame_surface = pygame.surfarray.make_surface(first_frame.swapaxes(0, 1))


# Afficher la première frame pour l'exemple
#screen.blit(first_frame_surface, (0, 0))
#pygame.display.flip()

# Obtenir la couleur du pixel en (0, 0)
color_at_0_0 = first_frame_surface.get_at((0, 0))

# Définir la couleur blanche comme transparente pour chaque surface
for frame in frames:
    frame.set_colorkey(color_at_0_0)  # La couleur (0, 230, 29) est définie comme transparente


# Paramètres de l'animation
clock = pygame.time.Clock()
frame_rate = 20
current_frame = 0

running = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacer l'écran avec une couleur de fond (noir dans cet exemple)
    screen.fill((0, 0, 0))

    # Afficher la frame courante
    screen.blit(frames[current_frame], (0, 0))

    # Passer à la frame suivante
    current_frame = (current_frame + 1) % len(frames)

    pygame.display.flip()

    # Limiter la vitesse de l'animation
    clock.tick(frame_rate)

pygame.quit()

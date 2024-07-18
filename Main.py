import pygame
import Constantes
pygame.init()

ancho = 800
alto = 600

ventana = pygame.display.set_mode((Constantes.ANCHO_VENTANA,
                                   Constantes.ALTO_VENTANA))
pygame
run = True
while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()
import pygame
import Constantes
from Personaje import Personaje

pygame.init()
ventana = pygame.display.set_mode((Constantes.ANCHO_VENTANA,
                                   Constantes.ALTO_VENTANA))
pygame.display.set_caption("Mi Primer Juego")

player_image = pygame.image.load("assets//images//characters//player//Player_0.png")

Jugador = Personaje(50, 50, player_image)

ancho = 800
alto = 600


#DEFINIR LAS VARIABLES DE MOVIMIENTO DEL JUGADOR
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

#CONTROLAR EL FRENTE RATE
reloj = pygame.time.Clock()

run = True
while run == True:

    #QUE VAYA A 60 FPS
    reloj.tick(Constantes.FPS)

    ventana.fill(Constantes.COLOR_BG)

    #CALCULAR EL MOVIMIENTO DEL JUGADOR
    delta_x = 0
    delta_y = 0

    if mover_derecha == True:
        delta_x = Constantes.VELOCIDAD
    if mover_izquierda == True:
        delta_x = -Constantes.VELOCIDAD
    if mover_arriba == True:
        delta_y = -Constantes.VELOCIDAD
    if mover_abajo == True:
        delta_y = Constantes.VELOCIDAD

    #MVOVER ALL JUGADOR
    Jugador.movimeinto(delta_x, delta_y)

    Jugador.dibujar(ventana)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True


        #PARA CUANDO SE SUELTA LA TECLA
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

    pygame.display.update()

pygame.quit()
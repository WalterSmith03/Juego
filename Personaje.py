import pygame
import Constantes

class Personaje():
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        #IMAGEN DE LA ANIMACION QUE SE ESTA MOSTRANDO ACTUALMENTE
        self.frame_index = 0
        #AQUI SE ALMACENA LA HORA ACTUAL EN MILISEGUNDOS DESDE QUE SE INICIO PYGAME
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = pygame.Rect(0, 0, Constantes.ANCHO_PERSONAJE,
                                        Constantes.ALTO_PERSONAJE)
        self.forma.center = (x,y)


    def movimeinto(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        self.forma.x = self.forma.x + delta_x
        self.forma.y = self.forma.y + delta_y

    def update(self):
        cooldown_animacion = 100
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0


    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)
        #pygame.draw.rect(interfaz, Constantes.COLOR_PERSONAJE,  self.forma, 1)



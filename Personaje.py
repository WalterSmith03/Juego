import pygame
import Constantes

class Personaje():
    def __init__(self, x, y, image):
        self.image = image
        self.forma = pygame.Rect(0, 0, Constantes.ANCHO_PERSONAJE,
                                        Constantes.ALTO_PERSONAJE)
        self.forma.center = (x,y)

    def movimeinto(self, delta_x, delta_y):
        self.forma.x = self.forma.x + delta_x
        self.forma.y = self.forma.y + delta_y

    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.forma)
        pygame.draw.rect(interfaz, Constantes.COLOR_PERSONAJE,  self.forma)



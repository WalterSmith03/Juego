import pygame

class Weapon():
    def __init__(self, image):
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.rect()

    def update(self, Personaje):
        self.forma.center = Personaje.forma.center

    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)
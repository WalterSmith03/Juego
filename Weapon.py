import pygame
import Constantes
import math

class Weapon():
    def __init__(self, image, imagen_bala):
        self.imagen_bala =
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()

    def update(self, Personaje):
        bala = None
        self.forma.center = Personaje.forma.center
        if Personaje.flip == False:
            self.forma.x = self.forma.x + Personaje.forma.width/2
            self.rotar_arma(False)
        if Personaje.flip == True:
            self.forma.x = self.forma.x - Personaje.forma.width / 2
            self.rotar_arma(True)

        #MOVER LA PISTOLA CON EL MOUSE
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.forma.centerx
        distancia_y = -(mouse_pos[1] - self.forma.centery)
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))

        #print(self.angulo)


        #DETECTAR LOS CLICK DEL MOUSE
        if pygame.mouse.get_pressed()[0]:
            bala = Bullet(self.imagen_bala, self.forma.centerx, self.forma.centery, self.angulo)





    def rotar_arma(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.imagen_original,
                                                True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original,
                                             False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)


    def dibujar(self, interfaz):
        self.imagen = pygame.transform.rotate(self.imagen,
                                              self.angulo)
        interfaz.blit(self.imagen, self.forma)
        #pygame.draw.rect(interfaz, Constantes.COLOR_ARMA, self.forma, 1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


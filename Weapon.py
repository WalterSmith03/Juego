import pygame
import Constantes
import math
import random

class Weapon():
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()
        self.disparada = False
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self, Personaje):
        disparo_cooldown = Constantes.COOLDOWN_BALAS
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
        if pygame.mouse.get_pressed()[0] and self.disparada == False and (pygame.time.get_ticks()-self.ultimo_disparo >= disparo_cooldown):
            bala = Bullet(self.imagen_bala, self.forma.centerx, self.forma.centery, self.angulo)
            self.disparada = True
            self.ultimo_disparo = pygame.time.get_ticks()
        #RESETEAR EL CLICK DEL MOUSE
        if pygame.mouse.get_pressed()[0] == False:
            self.disparada = False
        return bala




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
        #CALCULO DE VELOCIDAD
        self.delta_x =math.cos(math.radians(self.angulo))*Constantes.VELOCIDAD_BALA
        self.delta_y = -math.sin(math.radians(self.angulo)) * Constantes.VELOCIDAD_BALA

    def update(self, lista_enemigos):
        daño = 0
        pos_daño = None
        self.rect.x += self.delta_x
        self.rect.y = self.rect.y + self.delta_y

        #VERIFICAR SI LAS BALAS SALIERON DE PANTALLA
        if self.rect.right < 0 or self.rect.left > Constantes.ANCHO_VENTANA or self.rect.top > Constantes.ALTO_VENTANA:
            self.kill()

        #VERIFICAR SI HAY COLISIÓN CON LOS ENEMIGOS
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                daño = 15 + random.randint(-7, 7)
                pos_daño = enemigo.forma
                enemigo.energia -= daño
                self.kill()
                break
        return daño, pos_daño


    def dibujar(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx,
                                  self.rect.centery - int(self.image.get_height())))



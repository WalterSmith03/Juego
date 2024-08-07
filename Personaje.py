import pygame
import Constantes
import math

class Personaje():
    def __init__(self, x, y, animaciones, energia, tipo):
        self.score = 0
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones
        #IMAGEN DE LA ANIMACION QUE SE ESTA MOSTRANDO ACTUALMENTE
        self.frame_index = 0
        #AQUI SE ALMACENA LA HORA ACTUAL EN MILISEGUNDOS DESDE QUE SE INICIO PYGAME
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x,y)
        self.tipo = tipo
        self.ultimo_golpe = pygame.time.get_ticks()
        self.golpe = False
        self.ultimo_golpe = pygame.time.get_ticks()

    def actualizar_coordenadas(self, tupla):
        self.forma.center = (tupla[0], tupla[1])

    def movimeinto(self, delta_x, delta_y, obstaculos_tiles, exit_tile):
        posicion_pantalla = [0, 0]
        nivel_completado = False
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        self.forma.x = self.forma.x + delta_x
        for obstacle in obstaculos_tiles:
            if obstacle[1].colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = obstacle[1].left
                if delta_x < 0:
                    self.forma.left = obstacle[1].right



        self.forma.y = self.forma.y + delta_y
        for obstaculo in obstaculos_tiles:
            #CHEQUEO DE COLISION
            if obstaculo[1].colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = obstaculo[1].top
                if delta_y < 0:
                    self.forma.top = obstaculo[1].bottom

        # LOGICA SOO APLICA AL JUGADOR Y NO ENEMIGOS
        if self.tipo == 1:
            #CHEQUEAR COLISION CON LA SALIDA
            if exit_tile[1].colliderect(self.forma):
                nivel_completado = True
                print("nivel completado")
            #ACTUALIZAR LA PANTALLA BASADO LA POSICION DEL JUGADOR
            # MOVER LA CAMARA DE IZQUIERDA A DERECHA
            if self.forma.right > (Constantes.ANCHO_VENTANA - Constantes.LIMITE_PANTALLA):
                posicion_pantalla[0] = (Constantes.ANCHO_VENTANA - Constantes.LIMITE_PANTALLA) - self.forma.right
                self.forma.right = Constantes.ANCHO_VENTANA - Constantes.LIMITE_PANTALLA
            if self.forma.left < Constantes.LIMITE_PANTALLA:
                posicion_pantalla[0] = Constantes.LIMITE_PANTALLA- self.forma.left
                self.forma.left = Constantes.LIMITE_PANTALLA

            # MOVER LA CAMARA DE IZQUIERDA A DERECHA
            if self.forma.bottom > (Constantes.ALTO_VENTANA - Constantes.LIMITE_PANTALLA):
                posicion_pantalla[1] = (Constantes.ALTO_VENTANA - Constantes.LIMITE_PANTALLA) - self.forma.bottom
                self.forma.bottom = Constantes.ALTO_VENTANA - Constantes.LIMITE_PANTALLA
            if self.forma.top < Constantes.LIMITE_PANTALLA:
                posicion_pantalla[1] = Constantes.LIMITE_PANTALLA - self.forma.top
                self.forma.top = Constantes.LIMITE_PANTALLA


            return posicion_pantalla, nivel_completado

    def enemigos(self, Jugador, obstaculos_tiles, posicion_pantalla, exit_tile):
        clipped_line = ()
        ene_dx = 0
        ene_dy = 0

        #REPOSICIONAR ENEMIGOS BASADO EN LA POSICION DE LA PANTALLA
        self.forma.x += posicion_pantalla[0]
        self.forma.y += posicion_pantalla[1]

        #CREAR UNA LINEA DE VISION
        linea_de_vision = ((self.forma.centerx, self.forma.centery),
                           (Jugador.forma.centerx, Jugador.forma.centery))

        #CHEQUEO SI HAY OBSTACULOS EN LA LINEA DE VISION DEL ENEMIGO
        for obs in obstaculos_tiles:
            if obs[1].clipline(linea_de_vision):
                clipped_line = obs[1].clipline(linea_de_vision)


        #DISTANCIA CON EL JUGADOR
        distancia = math.sqrt(((self.forma.centerx - Jugador.forma.centerx)**2) +
                     ((self.forma.centery - Jugador.forma.centery)**2))

        if not clipped_line and distancia < Constantes.RANGO:
            if self.forma.centerx > Jugador.forma.centerx:
                ene_dx = -Constantes.VELOCIDAD_ENEMIGO
            if self.forma.centerx < Jugador.forma.centerx:
                ene_dx = Constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery > Jugador.forma.centery:
                ene_dy = -Constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery < Jugador.forma.centery:
                ene_dy = Constantes.VELOCIDAD_ENEMIGO

        self.movimeinto(ene_dx, ene_dy,obstaculos_tiles, exit_tile)

        #ATACAR AL JUGADOR
        if distancia < Constantes.RANGO_ATAQUE and Jugador.golpe == False:
            Jugador.energia -= 10
            Jugador.golpe = True
            Jugador.ultimo_golpe = pygame.time.get_ticks()

    def update(self):
        #COMPROBAR SI EL PERSONAJE HA MUERTO
        if self. energia <= 0:
            self.energia = 0
            self.vivo = False

        #TIMER PARA PODER VOLVER A RECIBIR DAÑO
        golpe_cooldown = 1000
        if self.tipo == 1:
            if self.golpe == True:
                if pygame.time.get_ticks() - self.ultimo_golpe > golpe_cooldown:
                    self.golpe = False



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



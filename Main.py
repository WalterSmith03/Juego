import pygame
import Constantes
import pygame.sprite
from Personaje import Personaje
from Weapon import Weapon
from Textos import DamageText
from Items import Item
from Mundo import Mundo
import os
import csv

#FUNCIONES:
#ESCALAR IMAGENES
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

#FUNCION PARA CONTAR ELEMENTOS
def contar_elementos(directorio):
    return len(os.listdir(directorio))

#FUNCION PARA LISTAR NOMBRES ELEMENTOS
def nombres_carpetas(directorio):
    return os.listdir(directorio)

pygame.init()

pygame.mixer.init()

ventana = pygame.display.set_mode((Constantes.ANCHO_VENTANA,
                                   Constantes.ALTO_VENTANA))
pygame.display.set_caption("Mi Primer Juego")

#VARIABLES
posicion_pantalla = [0, 0]
nivel = 1


#FUENTES
font = pygame.font.Font("assets//fonts//mago3.ttf", 25)
font_juego_terminado = pygame.font.Font("assets//fonts//mago3.ttf", 75)
font_reinicio = pygame.font.Font("assets//fonts//mago3.ttf", 30)
font_inicio = pygame.font.Font("assets//fonts//mago3.ttf", 30)
font_titulo = pygame.font.Font("assets//fonts//mago3.ttf", 75)



juego_terminado_text = font_juego_terminado.render('SIGA INTENTANDO CHICHI', True, Constantes.BLANCO)

texto_boton_reinicio = font_reinicio.render("Reiniciar", True, Constantes.NEGRO_1)


#BOTONES DE INICIO
boton_jugar = pygame.Rect(Constantes.ANCHO_VENTANA / 2 - 100, Constantes.ALTO_VENTANA / 2 - 50, 200, 50)

boton_salir = pygame.Rect(Constantes.ANCHO_VENTANA / 2 - 100, Constantes.ALTO_VENTANA / 2 + 50, 200, 50)

texto_boton_jugar = font_inicio.render("Empezar", True, Constantes.NEGRO_1)

texto_boton_salir = font_inicio.render("TERMINAR", True, Constantes.BLANCO)

#PANTALLA INICIO
def pantalla_inicio():
    ventana.fill(Constantes.ROJO)
    dibujar_texto("EL INICIO DEL FIN", font_titulo, Constantes.BLANCO, Constantes.ANCHO_VENTANA / 2- 200, Constantes.ALTO_VENTANA / 2 - 200)
    pygame.draw.rect(ventana, Constantes.BLANCO, boton_jugar)
    pygame.draw.rect(ventana, Constantes.NEGRO_1, boton_salir)
    ventana.blit(texto_boton_jugar, (boton_jugar.x + 50, boton_jugar.y + 10))
    ventana.blit(texto_boton_salir, (boton_salir.x + 50, boton_salir.y + 10))
    pygame.display.update()



#IMPORTAR IMAGENES
#ENERGIA
corazon_vacio = pygame.image.load("assets//images//items//heart_empty.png")
corazon_vacio = escalar_img(corazon_vacio, Constantes.SCALA_CORAZON)

corazon_mitad = pygame.image.load("assets//images//items//heart_half.png")
corazon_mitad = escalar_img(corazon_mitad, Constantes.SCALA_CORAZON)

corazon_lleno = pygame.image.load("assets//images//items//heart_full.png")
corazon_lleno = escalar_img(corazon_lleno, Constantes.SCALA_CORAZON)

#IMPORTAR IMAGENES
#PERSONAJE
animaciones = []
for i in range (7):
    img = pygame.image.load(f"assets//images//characters//player//Player_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones.append(img)

#ENEMIGOS
directorio_enemigos = "assets//images//characters//enemies"
tipo_enemigos = nombres_carpetas(directorio_enemigos)
animaciones_enemigos = []
for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"assets//images//characters//enemies//{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}//{eni}_{i + 1}.png")
        img_enemigo = escalar_img(img_enemigo, Constantes.SCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)
    animaciones_enemigos.append(lista_temp)

#ARMA
imagen_pistola = pygame.image.load(f"assets//images//weapons//gun.png")
imagen_pistola = escalar_img(imagen_pistola, Constantes.SCALA_ARMA)

#BALAS
imagen_balas = pygame.image.load(f"assets//images//weapons//bullet.png")
imagen_balas = escalar_img(imagen_balas, Constantes.SCALA_ARMA)

#CARGAR IMAGENES EDL MUNDO
tile_list = []
for x in range(Constantes.TILE_TYPES):
    tile_image = pygame.image.load(f"assets//images//tiles//tile ({x+1}).png")
    tile_image = pygame.transform.scale(tile_image, (Constantes.TILE_SIZE, Constantes.TILE_SIZE))
    tile_list.append(tile_image)

#ACRGAR IMAGENES DE LOS ITEMS
posion_roja = pygame.image.load("assets//images//items//potion.png")
posion_roja = escalar_img(posion_roja, 0.02)

coin_images = []
ruta_img = "assets//images//items//coin"
num_coin_images = contar_elementos(ruta_img)
print(f"Numero de imagenes de monedas: {num_coin_images}")
for i in range(num_coin_images):
    img = pygame.image.load(f"assets//images//items//coin//coin_{i+1}.png")
    img = escalar_img(img, 1)
    coin_images.append(img)

item_imagenes = [coin_images, [posion_roja]]

def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x,y))


def vida_jugador():
    c_mitad_dibujado = False
    for i in range(5):
        if Jugador.energia >= ((i+1)*20):
            ventana.blit(corazon_lleno, (5+i*50, 5))
        elif Jugador.energia % 20 > 0 and c_mitad_dibujado == False:
            ventana.blit(corazon_mitad, (5+i*50, 5))
            c_mitad_dibujado = True
        else:
            ventana.blit(corazon_vacio, (5+i*50, 5))

def resetear_mundo():
    grupo_damage_text.empty()
    grupo_balas.empty()
    grupo_items.empty()

    #CREAR UNA LISTA DE TILE VCIAS
    data = []
    for fila in range(Constantes.FILAS):
        filas = [2] * Constantes.COLUMNAS
        data.append(filas)
    return data

world_data = []

for fila in range(Constantes.FILAS):
    filas = [6] * Constantes.COLUMNAS
    world_data.append(filas)

#CARGAR EL ARCHIVO CON EL NIVEL
with open("niveles//nivel1.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data[x][y] = int(columna)
world = Mundo()
world.process_data(world_data, tile_list, item_imagenes, animaciones_enemigos)

def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana, Constantes.BLANCO, (x*Constantes.TILE_SIZE, 0), (x*Constantes.TILE_SIZE, Constantes.ALTO_VENTANA))
        pygame.draw.line(ventana, Constantes.BLANCO, (0, x * Constantes.TILE_SIZE), (Constantes.ANCHO_VENTANA, x* Constantes.TILE_SIZE))

#CREAR UN JUGADOR DE LA CLASE PERSONAJE
Jugador = Personaje(50, 50, animaciones, 100, 1)

#CREAR UNA LISTA DE ENEMIGOS
lista_enemigos = []
for ene in world.lista_enemigo:
    lista_enemigos.append(ene)


#CREAR UN ARMA DE LA CLASE WEAPON
pistola = Weapon(imagen_pistola, imagen_balas)

#CREAR UN GRUPO DE SPRITES
grupo_damage_text = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()
#AÑADIR ITEMS DESDE AL DATA DEL NIVEL
for item in world.lista_item:
    grupo_items.add(item)



#DEFINIR LAS VARIABLES DE MOVIMIENTO DEL JUGADOR
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

#CONTROLAR EL FRENTE RATE
reloj = pygame.time.Clock()

#BOTON DE REINICIO
boton_reinicio = pygame.Rect(Constantes.ANCHO_VENTANA / 2 - 100, Constantes.ALTO_VENTANA / 2 + 100, 200, 50)

pygame.mixer.music.load("assets//sonidos//fondo.mp3")
pygame.mixer.music.play(-1)

sonido_disparo = pygame.mixer.Sound("assets//sonidos//pistola.mp3")

mostrar_inicio = True
run = True
while run == True:
    if mostrar_inicio:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                if boton_salir.collidepoint(event.pos):
                    run = False
    else:
        #QUE VAYA A 60 FPS
        reloj.tick(Constantes.FPS)
        ventana.fill(Constantes.MORADO)

        if Jugador.vivo == True:
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
            posicion_pantalla, nivel_completado = Jugador.movimeinto(delta_x, delta_y, world.obstaculos_tiles, world.exit_tile)


            #ACTUALIZAR EL MAPA
            world.update(posicion_pantalla)

            #ACTUALIZA EL ESTADO DEL JUGADOR
            Jugador.update()
            #ACTUALIZA EL ESTADO DEL ENEMIGO
            for ene in lista_enemigos:
                ene.update()


            #ACTUALIZA EL ESTADO DEL ARMA
            bala = pistola.update(Jugador)
            if bala:
                grupo_balas.add(bala)
                sonido_disparo.play()
            for bala in grupo_balas:
                damage, pos_damage = bala.update(lista_enemigos, world.obstaculos_tiles)
                if damage:
                    damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, Constantes.ROJO)
                    grupo_damage_text.add(damage_text)

            #ACTUALIZAR DAÑO
            grupo_damage_text.update(posicion_pantalla)

            #ACTUALIZAR ITEMS
            grupo_items.update(posicion_pantalla, Jugador)

        #DIBUJAR MUNDO
        world.draw(ventana)

        #DIBUJAR AL JUGADOR
        Jugador.dibujar(ventana)

        # DIBUJAR A LOS ENEMIGOS
        for ene in lista_enemigos:
            if ene.energia == 0:
                lista_enemigos.remove(ene)
            if ene.energia > 0:
                ene.enemigos(Jugador, world.obstaculos_tiles, posicion_pantalla, world.exit_tile)
                ene.dibujar(ventana)

        #DIBUJAR EL ARMA
        pistola.dibujar(ventana)


        #DIBUJAR BALAS
        for bala in grupo_balas:
            bala.dibujar(ventana)


        #DIBUJAR LOS CORAZONES
        vida_jugador()

        #DIBUJAR TEXTOS
        grupo_damage_text.draw(ventana)
        dibujar_texto(f"Score: {Jugador.score}", font,(255,255,0), 700, 5)
        #NIVEL
        dibujar_texto(f"Nivel: " + str(nivel), font, Constantes.BLANCO, Constantes.ANCHO_VENTANA / 2, 5)


        #DIBUJAR ITEMS
        grupo_items.draw(ventana)

        #CHEQUEAR SI EL NIVEL FUE COMPLETADO
        if nivel_completado == True:
            if nivel < Constantes.NIVEL_MAXIMO:
                nivel +=1
                world_data = resetear_mundo()
                # CARGAR EL ARCHIVO CON EL NIVEL
                with open(f"niveles//nivel{nivel}.csv", newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, fila in enumerate(reader):
                        for y, columna in enumerate(fila):
                            world_data[x][y] = int(columna)
                world = Mundo()
                world.process_data(world_data, tile_list, item_imagenes, animaciones_enemigos)
                Jugador.actualizar_coordenadas(Constantes.COORDENADAS[str(nivel)])

                # CREAR UNA LISTA DE ENEMIGOS
                lista_enemigos = []
                for ene in world.lista_enemigo:
                    lista_enemigos.append(ene)

                # AÑADIR ITEMS DESDE AL DATA DEL NIVEL
                for item in world.lista_item:
                    grupo_items.add(item)


        if Jugador.vivo == False:
            ventana.fill(Constantes.ROJO_OSCURO)
            text_rect = juego_terminado_text.get_rect(center=(Constantes.ANCHO_VENTANA / 2, Constantes.ALTO_VENTANA / 2))

            ventana.blit(juego_terminado_text, text_rect)



            pygame.draw.rect(ventana, Constantes.VERDE, boton_reinicio)
            ventana.blit(texto_boton_reinicio,
                         (boton_reinicio.x + 50, boton_reinicio.y + 10))

        for event in pygame.event.get():
            #PARA CERRAR EL JUEGO
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
                if event.key == pygame.K_e:
                    if world.abrir_puerta(Jugador, tile_list):
                        print("puerta cambiada")


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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reinicio.collidepoint(event.pos) and not Jugador.vivo:
                    Jugador.vivo = True
                    Jugador.energia = 100
                    Jugador.score = 0
                    nivel = 1
                    world_data = resetear_mundo()
                    with open(f"niveles//nivel{nivel}.csv", newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, fila in enumerate(reader):
                            for y, columna in enumerate(fila):
                                world_data[x][y] = int(columna)
                    world = Mundo()
                    world.process_data(world_data, tile_list, item_imagenes, animaciones_enemigos)
                    Jugador.actualizar_coordenadas(Constantes.COORDENADAS[str(nivel)])
                    for item in world.lista_item:
                        grupo_items.add(item)
                    lista_enemigos = []
                    for ene in world.lista_enemigo:
                        lista_enemigos.append(ene)


        pygame.display.update()

pygame.quit()
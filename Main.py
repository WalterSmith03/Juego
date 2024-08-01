import pygame
import Constantes
import pygame.sprite
from Personaje import Personaje
from Weapon import Weapon
from Textos import DamageText
from Items import Item
from Mundo import Mundo
import os

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
ventana = pygame.display.set_mode((Constantes.ANCHO_VENTANA,
                                   Constantes.ALTO_VENTANA))
pygame.display.set_caption("Mi Primer Juego")

#FUENTES
font= pygame.font.Font("assets//fonts//mago3.ttf", 25)

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

world_data = [
    [1,1,1,1,1,15],
    [0,19,19,19,19,15],
    [0,19,19,19,19,15],
    [0,19,19,19,19,15],
    [0,19,19,19,19,15],
    [0,19,19,19,19,15],
    [0,1,1,1,1,15]
]

world = Mundo()
world.process_data(world_data, tile_list)

def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana, Constantes.BLANCO, (x*Constantes.TILE_SIZE, 0), (x*Constantes.TILE_SIZE, Constantes.ALTO_VENTANA))
        pygame.draw.line(ventana, Constantes.BLANCO, (0, x * Constantes.TILE_SIZE), (Constantes.ANCHO_VENTANA, x* Constantes.TILE_SIZE))

#CREAR UN JUGADOR DE LA CLASE PERSONAJE
Jugador = Personaje(50, 50, animaciones, 20)

#CREAR UN ENEMIGO DE LA CLASE PERSONAJE
goblin = Personaje(400, 300, animaciones_enemigos[0], 100)
honguito = Personaje(200, 200, animaciones_enemigos[1], 100)
goblin_2 = Personaje(100, 250, animaciones_enemigos[0], 100)
honguito_2 = Personaje(100, 150, animaciones_enemigos[1], 100)

#CREAR UNA LISTA DE ENEMIGOS
lista_enemigos = []
lista_enemigos.append(goblin)
lista_enemigos.append(goblin_2)
lista_enemigos.append(honguito)
lista_enemigos.append(honguito_2)

#CREAR UN ARMA DE LA CLASE WEAPON
pistola = Weapon(imagen_pistola, imagen_balas)

#CREAR UN GRUPO DE SPRITES
grupo_damage_text = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()

coin = Item(350, 25, 0, coin_images)
potion = Item(380, 55, 1, [posion_roja])

grupo_items.add(coin)
grupo_items.add(potion)

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

    dibujar_grid()

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

    #ACTUALIZA EL ESTADO DEL JUGADOR
    Jugador.update()
    #ACTUALIZA EL ESTADO DEL ENEMIGO
    for ene in lista_enemigos:
        ene.update()
        print(ene.energia)

    #ACTUALIZA EL ESTADO DEL ARMA
    bala = pistola.update(Jugador)
    if bala:
        grupo_balas.add(bala)
    for bala in grupo_balas:
        damage, pos_damage = bala.update(lista_enemigos)
        if damage:
            damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, Constantes.ROJO)
            grupo_damage_text.add(damage_text)

    #ACTUALIZAR DAÑO
    grupo_damage_text.update()

    #ACTUALIZAR ITEMS
    grupo_items.update(Jugador)

    #DIBUJAR MUNDO
    world.draw(ventana)

    #DIBUJAR AL JUGADOR
    Jugador.dibujar(ventana)

    # DIBUJAR A LOS ENEMIGOS
    for ene in lista_enemigos:
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

    #DIBUJAR ITEMS
    grupo_items.draw(ventana)


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
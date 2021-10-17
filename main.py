import pygame
import os
import random

vidas_jugadores = 3  # número de vidas que tiene el jugador
puntaje = 0  # puntaje
frutas = ['sandia', 'naranja', 'granada', 'guayaba', 'bomba']  # elementos en juego

# página inicial
ANCHO = 800
ALTURA = 500
FPS = 12  # velocidad del juego
pygame.init()
pygame.display.set_caption('Fruit Ninja')
icono = pygame.image.load('images/explosion.png')
pygame.display.set_icon(icono)
pantalla = pygame.display.set_mode((ANCHO, ALTURA))  # tamaño
reloj = pygame.time.Clock()
pygame.mixer.init()

AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

fondo = pygame.image.load('images/fondo2.png')  # FONDO
fuente = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
texto_puntaje = fuente.render('PUNTAJE : ' + str(puntaje), True, (255, 255, 255))  # PUNTAJE
pygame.mixer.music.load('Eternal Youth.wav')
pygame.mixer.music.set_volume(0.2)
sonido_corte = pygame.mixer.Sound('corte.wav')
explot = pygame.mixer.Sound('explo.wav')


def frutas_aleatorias(fruta):
    ruta_frutas = "images/" + fruta + ".png"
    data[fruta] = {
        'img': pygame.image.load(ruta_frutas),
        'x': random.randint(100, 500),  # donde debería estar posicionada la fruta en x
        'y': 800,
        'velocidad_x': random.randint(-10, 10),  # velocidad en eje x de la fruta
        'velocidad_y': random.randint(-80, -60),  # velocidad en eje y de la fruta
        'lanzar': False,  # determina si se lanza o no se lanza
        't': 0,
        'hit': False,
    }

    if random.random() >= 0.75:
        data[fruta]['lanzar'] = True
    else:
        data[fruta]['lanzar'] = False


data = {}
for fruta in frutas:
    frutas_aleatorias(fruta)


def vidas_escondidas(x, y):
    pantalla.blit(pygame.image.load("images/vidas_blancas.png"), (x, y))


letra_nombre = pygame.font.match_font('comic.ttf')


def dibujo_texto(display, texto, tamaño, x, y):
    fuente = pygame.font.Font(letra_nombre, tamaño)
    texto_superior = fuente.render(texto, True, BLANCO)
    texto_recto = texto_superior.get_rect()
    texto_recto.midtop = (x, y)
    pantalla.blit(texto_superior, texto_recto)


def dibujo_vidas(display, x, y, vidas, imagen):
    for i in range(vidas):
        img = pygame.image.load(imagen)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)


# muestra cuando es el fin del juego
def pantalla_fin_del_juego():
    pantalla.blit(fondo, (0, 0))
    dibujo_texto(pantalla, "Fruit Ninja", 90, ANCHO / 2, ALTURA / 4)
    if not fin_del_juego:
        dibujo_texto(pantalla, "Puntaje: " + str(puntaje), 50, ANCHO / 2, ALTURA / 2)
        pantalla.blit(pygame.image.load("images/game_over.png"), (500, 200))
        pantalla.blit(pygame.image.load("images/game_over.png"), (158, 200))

    dibujo_texto(pantalla, "Oprime una tecla para iniciar!", 64, ANCHO / 2, ALTURA * 3 / 4)
    pygame.display.flip()
    espera = True
    while espera:
        reloj.tick(FPS)
        for ocurrir in pygame.event.get():
            if ocurrir.type == pygame.QUIT:
                pygame.quit()
            if ocurrir.type == pygame.KEYUP:
                espera = False


pygame.mixer.music.play()
primera_ronda = True
fin_del_juego = True
juego_corriendo = True
while juego_corriendo:

    if fin_del_juego:
        if primera_ronda:
            pantalla_fin_del_juego()
            primera_ronda = False
        fin_del_juego = False
        vidas_jugadores = 3
        dibujo_vidas(pantalla, 690, 5, vidas_jugadores, 'images/vidas_rojas.png')
        vidas_escondidas(690, 5)
        vidas_escondidas(725, 5)
        vidas_escondidas(760, 5)
        puntaje = 0

    for evento in pygame.event.get():
        # cerra la ventana
        if evento.type == pygame.QUIT:
            juego_corriendo = False

    pantalla.blit(fondo, (0, 0))
    pantalla.blit(texto_puntaje, (0, 0))
    dibujo_vidas(pantalla, 690, 5, vidas_jugadores, 'images/vidas_rojas.png')
    vidas_escondidas(690, 5)
    vidas_escondidas(725, 5)
    vidas_escondidas(760, 5)
    for llave, valor in data.items():
        if valor['lanzar']:
            valor['x'] += valor['velocidad_x']  # movimiento de las frutas en la coordenada x
            valor['y'] += valor['velocidad_y']  # movimiento de las frutas en la coordenada y
            valor['velocidad_y'] += (1 * valor['t'])
            valor['t'] += 1

            if valor['y'] <= 800:
                pantalla.blit(valor['img'], (valor['x'], valor['y']))
            else:
                frutas_aleatorias(llave)

            posicion_actual = pygame.mouse.get_pos()

            if not valor['hit'] and valor['x'] < posicion_actual[0] < valor['x'] + 60 \
                    and valor['y'] < posicion_actual[1] < valor['y'] + 60:
                if llave == 'bomba':
                    explot.play()
                    vidas_jugadores -= 1
                    if vidas_jugadores == 0:
                        vidas_escondidas(690, 15)
                    elif vidas_jugadores == 1:
                        vidas_escondidas(725, 15)
                    elif vidas_jugadores == 2:
                        vidas_escondidas(760, 15)
                    if vidas_jugadores < 0:
                        pantalla_fin_del_juego()
                        fin_del_juego = True

                    fruta_cortada = "images/explosion.png"
                else:
                    fruta_cortada = "images/" + "media_" + llave + ".png"
                    sonido_corte.play()

                valor['img'] = pygame.image.load(fruta_cortada)
                valor['velocidad_x'] += 10
                if llave != 'bomba':
                    puntaje += 1
                texto_puntaje = fuente.render('Puntaje : ' + str(puntaje), True, (255, 255, 255))
                valor['hit'] = True
        else:
            frutas_aleatorias(llave)
    if 0 < puntaje < 10:
        FPS = 12
    elif 10 < puntaje < 20:
        FPS = 13
    elif 20 < puntaje:
        FPS = 15

    pygame.display.update()
    reloj.tick(FPS)

pygame.quit()

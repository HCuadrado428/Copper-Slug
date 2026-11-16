#!/usr/bin/env python3
"""Genera la ropa cosmética (dos juegos: vaquero y bandido): las capas de armadura, los iconos, los modelos, las recetas y los textos.

  textures/models/armor/<juego>_layer_1.png   sombrero (cabeza), chaleco/poncho (cuerpo y brazos) y botas (piernas): 64x32
  textures/models/armor/<juego>_layer_2.png   cinturón y pantalón (cuerpo bajo y piernas): 64x32
  textures/item/<pieza>.png                   los iconos (16x16)
  models/item/<pieza>.json                    modelos planos
  data/copperslug/recipes/<pieza>.json        recetas (cuero y un detalle de cobre o tinte; ninguna igual que las de vanilla)

La plantilla de una capa de armadura es la del humanoide de vanilla (64x32): cabeza en (0,0), cuerpo en (16,16), brazo en (40,16) y
pierna en (0,16); cada caja (ancho x alto x fondo) se despliega con arriba, abajo, y los cuatro lados en fila. Lo transparente deja
ver al jugador, por eso el sombrero solo cubre la mitad de arriba de la cabeza. Es idempotente. Uso: generar_ropa.py [raíz]
"""
import json
import os
import random
import sys

from PIL import Image

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
RES = os.path.join(RAIZ, 'common/src/main/resources')
ARM = os.path.join(RES, 'assets/copperslug/textures/models/armor')
ICO = os.path.join(RES, 'assets/copperslug/textures/item')
MOD = os.path.join(RES, 'assets/copperslug/models/item')
REC = os.path.join(RES, 'data/copperslug/recipe')


def c(r, g, b, a=255):
    return (r, g, b, a)


FIELTRO, FIELTRO_OSC, CUERO, CUERO_OSC, CUERO_CLARO = c(112, 78, 46), c(66, 44, 26), c(150, 102, 60), c(96, 64, 38), c(184, 134, 84)
ORO, ORO_OSC, ACERO = c(236, 192, 62), c(176, 136, 36), c(184, 186, 196)
NEGRO, NEGRO_CLARO, ROJO, ROJO_OSC = c(38, 34, 36), c(62, 58, 62), c(168, 36, 34), c(112, 22, 24)
LONA, LONA_OSC, TELA = c(150, 128, 98), c(100, 84, 64), c(70, 70, 82)


def rect(im, x, y, w, h, col):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            im.putpixel((xx, yy), col)


def moteado(im, x, y, w, h, base, tonos, seed):
    """Rellena con el color base y salpica píxeles de otros tonos (cuero, fieltro, lana: nada plano)."""
    rnd = random.Random(seed)
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            im.putpixel((xx, yy), rnd.choice(tonos) if rnd.random() < 0.28 else base)


# ================================================================ las capas de armadura, a mano (sin ruido: bisel de luz y sombra, costuras y puntadas)
# Las cajas del humanoide (64x32). Cada cara es (x, y, ancho, alto).
CABEZA = dict(arriba=(8, 0, 8, 8), der=(0, 8, 8, 8), frente=(8, 8, 8, 8), izq=(16, 8, 8, 8), atras=(24, 8, 8, 8))
CUERPO = dict(arriba=(20, 16, 8, 4), der=(16, 20, 4, 12), frente=(20, 20, 8, 12), izq=(28, 20, 4, 12), atras=(32, 20, 8, 12))
BRAZO = dict(arriba=(44, 16, 4, 4), fuera=(40, 20, 4, 12), frente=(44, 20, 4, 12), dentro=(48, 20, 4, 12), atras=(52, 20, 4, 12))
PIERNA = dict(arriba=(4, 16, 4, 4), abajo=(8, 16, 4, 4), fuera=(0, 20, 4, 12), frente=(4, 20, 4, 12), dentro=(8, 20, 4, 12), atras=(12, 20, 4, 12))

# materiales: (oscuro, medio, claro, brillo)
PIEL_CUERO = (c(70, 44, 26), c(126, 86, 50), c(166, 118, 70), c(204, 156, 100))
FIELTRO_M = (c(52, 36, 22), c(102, 70, 42), c(140, 100, 62), c(176, 134, 88))
FIELTRO_N = (c(14, 12, 16), c(34, 32, 38), c(60, 56, 66), c(92, 86, 100))
TELA_ROJA = (c(88, 18, 24), c(146, 32, 34), c(190, 54, 48), c(228, 100, 86))
LANA = (c(88, 72, 54), c(136, 114, 84), c(176, 152, 114), c(212, 190, 150))
VAQUERA = (c(28, 30, 42), c(50, 54, 72), c(74, 80, 104), c(104, 112, 140))
METAL = (c(84, 88, 100), c(140, 144, 158), c(196, 200, 214), c(240, 242, 250))
DORADO = (c(132, 94, 22), c(204, 158, 40), c(244, 202, 78), c(255, 238, 150))


def px(im, x, y, col):
    if 0 <= x < 64 and 0 <= y < 32:
        im.putpixel((x, y), col)


def relleno(im, cara, mat, bisel=True):
    """Un panel con bisel: arriba y a la izquierda se aclara, abajo y a la derecha se oscurece."""
    x, y, w, h = cara
    rect(im, x, y, w, h, mat[1])
    if bisel and w > 2 and h > 2:
        rect(im, x, y, w, 1, mat[2])
        rect(im, x, y, 1, h, mat[2])
        rect(im, x, y + h - 1, w, 1, mat[0])
        rect(im, x + w - 1, y, 1, h, mat[0])
        px(im, x, y, mat[3])


def puntadas(im, x, y, largo, col, vertical=False, paso=2):
    for i in range(0, largo, paso):
        px(im, x + (0 if vertical else i), y + (i if vertical else 0), col)


def hueco(im, x, y):
    px(im, x, y, c(0, 0, 0, 0))


def estrella(im, cx, cy):
    """La estrella de sheriff: cruz de 3x3 con las puntas y un punto de luz."""
    for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        px(im, cx + dx, cy + dy, DORADO[1])
    px(im, cx, cy, DORADO[2])
    px(im, cx - 1, cy - 1, DORADO[0]); px(im, cx + 1, cy - 1, DORADO[0])
    px(im, cx - 1, cy + 1, DORADO[0]); px(im, cx + 1, cy + 1, DORADO[0])
    px(im, cx, cy, DORADO[3])


def sombrero(im, fieltro, cinta, hebilla, pluma=None):
    """Un sombrero de ala ancha sobre la cabeza: la copa con su hendidura, la cinta y el ala (con el modelo de vanilla no hay ala de verdad)."""
    x, y, w, h = CABEZA['arriba']
    rect(im, x, y, w, h, fieltro[0])                       # el ala, vista desde arriba
    rect(im, x + 1, y + 1, 6, 6, fieltro[1])
    rect(im, x + 2, y + 2, 4, 4, fieltro[2])               # la copa
    rect(im, x + 3, y + 2, 2, 4, fieltro[1])               # la hendidura central
    rect(im, x + 3, y + 3, 2, 2, fieltro[0])
    px(im, x + 2, y + 2, fieltro[3]); px(im, x + 1, y + 1, fieltro[2])
    for nombre in ('der', 'frente', 'izq', 'atras'):
        fx, fy, fw, fh = CABEZA[nombre]
        rect(im, fx, fy, fw, 1, fieltro[2])                 # fila 0: la copa por arriba, con la hendidura
        rect(im, fx + 3, fy, 2, 1, fieltro[1])
        rect(im, fx, fy + 1, fw, 1, fieltro[1])             # fila 1: el cuerpo de la copa
        px(im, fx, fy + 1, fieltro[2]); px(im, fx + fw - 1, fy + 1, fieltro[0])
        rect(im, fx, fy + 2, fw, 1, cinta[1])               # fila 2: la cinta
        rect(im, fx, fy + 2, fw, 1, cinta[1]); px(im, fx, fy + 2, cinta[2])
        rect(im, fx, fy + 3, fw, 1, fieltro[0])             # fila 3: el ala, que da sombra
        px(im, fx, fy + 3, fieltro[1]); px(im, fx + fw - 1, fy + 3, fieltro[1])
    hx, hy, hw, hh = CABEZA['frente']
    rect(im, hx + 3, hy + 2, 2, 1, hebilla[2])             # la hebilla
    px(im, hx + 3, hy + 2, hebilla[3]); px(im, hx + 4, hy + 2, hebilla[1])
    if pluma:
        fx, fy, fw, fh = CABEZA['izq']
        for i, (dx, dy) in enumerate(((1, 2), (2, 1), (3, 0), (2, 2), (3, 1))):
            px(im, fx + dx, fy + dy, pluma[1 if i < 3 else 2])
        px(im, fx + 3, fy, pluma[3])


def pantalon_cintura(im, correa, hebilla, balas=False):
    """El cinturón en la parte baja del cuerpo (capa 2): delante, detrás y a los lados."""
    for nombre, (fx, fy, fw, fh) in (('frente', CUERPO['frente']), ('atras', CUERPO['atras']), ('der', CUERPO['der']), ('izq', CUERPO['izq'])):
        rect(im, fx, fy + 8, fw, 2, correa[1])
        rect(im, fx, fy + 8, fw, 1, correa[2])
        rect(im, fx, fy + 9, fw, 1, correa[0])
        rect(im, fx, fy + 10, fw, 2, correa[1])              # lo que asoma del pantalón bajo la correa
    fx, fy, fw, fh = CUERPO['frente']
    rect(im, fx + 3, fy + 7, 2, 4, hebilla[1])               # la hebilla
    rect(im, fx + 3, fy + 7, 2, 1, hebilla[3]); rect(im, fx + 3, fy + 10, 2, 1, hebilla[0])
    px(im, fx + 3, fy + 8, correa[0]); px(im, fx + 4, fy + 9, correa[0])
    if balas:
        for x in (1, 6):
            rect(im, fx + x, fy + 8, 1, 2, DORADO[2])
            px(im, fx + x, fy + 8, DORADO[3])


def botas_capa(im, cuero, puno, espuela):
    """Las botas (capa 1, piernas): puño doblado de dos filas, caña lisa con la luz de un lado, puntera y suela; atrás, la espuela."""
    for nombre in ('fuera', 'frente', 'dentro', 'atras'):
        fx, fy, fw, fh = PIERNA[nombre]
        rect(im, fx, fy + 7, fw, 5, cuero[1])
        rect(im, fx, fy + 7, fw, 1, puno[3]); rect(im, fx, fy + 8, fw, 1, puno[2])     # el puño, claro
        rect(im, fx, fy + 9, 1, 2, cuero[2]); rect(im, fx + fw - 1, fy + 9, 1, 2, cuero[0])   # luz a un lado, sombra al otro
        rect(im, fx, fy + 11, fw, 1, c(22, 16, 12))                                  # la suela
    fx, fy, fw, fh = PIERNA['frente']
    rect(im, fx + 1, fy + 10, 2, 1, cuero[2])                                        # la puntera, con un poco de brillo
    rect(im, *PIERNA['abajo'], c(22, 16, 12))
    if espuela:
        fx, fy, fw, fh = PIERNA['atras']
        rect(im, fx + 1, fy + 10, 2, 1, METAL[2]); px(im, fx + 1, fy + 10, METAL[3])   # la espuela, atrás en el talón
        px(im, fx + 1, fy + 9, METAL[1]); px(im, fx + 2, fy + 9, METAL[0])


def chaleco_vaquero(im):
    cu = PIEL_CUERO
    for nombre in ('arriba', 'der', 'izq', 'atras', 'frente'):
        relleno(im, CUERPO[nombre], cu)
    fx, fy, fw, fh = CUERPO['frente']
    for dx in (2, 3, 4, 5):
        hueco(im, fx + dx, fy)                                # el cuello en V, abierto
    hueco(im, fx + 3, fy + 1); hueco(im, fx + 4, fy + 1)
    rect(im, fx + 3, fy + 2, 1, 9, cu[0]); rect(im, fx + 4, fy + 2, 1, 9, cu[2])    # la costura del centro, con relieve
    for dy in (3, 6, 9):                                      # los botones
        px(im, fx + 4, fy + dy, DORADO[2]); px(im, fx + 4, fy + dy + 1 - 1, DORADO[3]); px(im, fx + 3, fy + dy, DORADO[0])
    rect(im, fx + 1, fy + 6, 2, 3, cu[0]); rect(im, fx + 1, fy + 6, 2, 1, cu[2])      # un bolsillo con puntadas
    puntadas(im, fx + 1, fy + 8, 2, cu[3], paso=1)
    rect(im, fx, fy + 10, fw, 2, cu[0]); puntadas(im, fx + 1, fy + 10, 6, cu[2])       # el dobladillo
    fx, fy, fw, fh = CUERPO['atras']
    rect(im, fx + 3, fy, 2, 12, cu[0])                        # la costura de la espalda
    rect(im, fx, fy + 4, fw, 1, cu[0]); puntadas(im, fx + 1, fy + 5, 6, cu[3])        # la yugo
    rect(im, fx + 1, fy + 8, 6, 1, cu[0]); rect(im, fx + 3, fy + 8, 2, 1, DORADO[2])  # la correa de ajuste con su hebilla
    rect(im, fx, fy + 10, fw, 2, cu[0]); puntadas(im, fx + 1, fy + 10, 6, cu[2])
    for nombre in ('der', 'izq'):
        fx, fy, fw, fh = CUERPO[nombre]
        rect(im, fx, fy + 10, fw, 2, cu[0])
        rect(im, fx + 1, fy, 2, 4, c(0, 0, 0, 0)) if False else None


def chaparreras(im):
    cu = PIEL_CUERO
    for nombre in ('fuera', 'frente', 'atras'):
        relleno(im, PIERNA[nombre], cu)
    fx, fy, fw, fh = PIERNA['fuera']
    for dy in (2, 5, 8):
        px(im, fx + 2, fy + dy, DORADO[2]); px(im, fx + 2, fy + dy - 0, DORADO[3])      # los remaches dorados
    for dy in range(1, 11, 2):
        hueco(im, fx, fy + dy)                                # el fleco del borde de fuera
    fx, fy, fw, fh = PIERNA['frente']
    rect(im, fx + 1, fy + 3, 2, 2, cu[0]); rect(im, fx + 1, fy + 3, 2, 1, cu[2])     # la rodillera
    puntadas(im, fx, fy + 10, 4, cu[3], paso=1)
    fx, fy, fw, fh = PIERNA['atras']
    puntadas(im, fx + 1, fy + 1, 9, cu[0], vertical=True)
    # el interior de la pierna se deja abierto: se ve el pantalón de debajo
    pantalon_cintura(im, c(60, 38, 22), None) if False else None
    corr = (c(48, 30, 18), c(86, 56, 32), c(128, 90, 52), c(160, 120, 76))
    pantalon_cintura(im, corr, DORADO)


def pantalon_bandido(im):
    v = VAQUERA
    for nombre in ('fuera', 'frente', 'atras', 'dentro'):
        relleno(im, PIERNA[nombre], v)
    fx, fy, fw, fh = PIERNA['frente']
    rect(im, fx + 1, fy + 5, 2, 2, v[2]); puntadas(im, fx + 1, fy + 7, 2, v[0], paso=1)     # un parche en la rodilla
    px(im, fx + 1, fy + 5, v[3])
    fx, fy, fw, fh = PIERNA['fuera']
    rect(im, fx + 3, fy, 1, 12, v[0])                          # la costura del lado
    puntadas(im, fx + 2, fy + 1, 10, v[3], vertical=True, paso=2)
    corr = (c(10, 10, 12), c(32, 30, 36), c(58, 56, 64), c(88, 84, 96))
    pantalon_cintura(im, corr, METAL, balas=True)


def poncho_bandido(im):
    la = LANA
    caras = [CUERPO[n] for n in ('arriba', 'der', 'izq', 'atras', 'frente')]
    for cara in caras:
        relleno(im, cara, la, bisel=False)
    for nombre in ('der', 'frente', 'izq', 'atras'):
        x, y, w, h = CUERPO[nombre]
        rect(im, x, y + 3, w, 2, TELA_ROJA[1]); rect(im, x, y + 3, w, 1, TELA_ROJA[2])   # la franja roja de arriba
        rect(im, x, y + 6, w, 1, FIELTRO_N[1])                                            # la raya negra
        rect(im, x, y + 8, w, 2, TELA_ROJA[1]); rect(im, x, y + 9, w, 1, TELA_ROJA[0])    # la franja roja de abajo
        if w == 8:
            for i in range(0, w, 2):
                px(im, x + i, y + 4, TELA_ROJA[0]); px(im, x + i + 1, y + 7, la[3])      # el zigzag del tejido
        for i in range(w):
            if i % 2 == 1:
                hueco(im, x + i, y + 11)                                                  # el fleco de abajo
            else:
                px(im, x + i, y + 11, la[0])
    x, y, w, h = CUERPO['frente']
    for dx in (2, 3, 4, 5):
        hueco(im, x + dx, y)
    hueco(im, x + 3, y + 1); hueco(im, x + 4, y + 1)
    # la bandolera de balas, en diagonal sobre el pecho
    for i in range(8):
        px(im, x + i, y + 1 + i, PIEL_CUERO[0]); px(im, x + i, y + 2 + i, PIEL_CUERO[1]) if y + 2 + i < y + 11 else None
        if i % 2 == 1 and i < 7:
            px(im, x + i, y + 1 + i, DORADO[2]); px(im, x + i, y + i, DORADO[3])
    # los hombros del poncho: la parte de arriba de los dos brazos
    for nombre in ('fuera', 'frente', 'dentro', 'atras'):
        x, y, w, h = BRAZO[nombre]
        rect(im, x, y, w, 6, la[1]); rect(im, x, y, w, 1, la[2]); rect(im, x, y + 2, w, 1, TELA_ROJA[1]); rect(im, x, y + 3, w, 1, TELA_ROJA[0])
        for i in range(w):
            if i % 2 == 1:
                hueco(im, x + i, y + 5)
            else:
                px(im, x + i, y + 5, la[0])
    rect(im, *BRAZO['arriba'], la[2])


def sombrero_vaquero(im):
    pass   # el sombrero es un modelo 3D (RopaCapa): la capa de armadura de la cabeza queda vacía


def sombrero_bandido(im):
    # el sombrero es un modelo 3D (RopaCapa); aquí solo el pañuelo
    # el pañuelo sobre la boca y la nariz (no sobre los ojos): delante y de lado; atrás, el nudo
    fx, fy, fw, fh = CABEZA['frente']
    rect(im, fx, fy + 6, fw, 2, TELA_ROJA[1]); rect(im, fx, fy + 6, fw, 1, TELA_ROJA[2])
    hueco(im, fx, fy + 7); hueco(im, fx + fw - 1, fy + 7)
    for i in (1, 3, 5):
        px(im, fx + i, fy + 6, c(236, 232, 226)); px(im, fx + i + 1, fy + 7, TELA_ROJA[0])
    for nombre in ('der', 'izq'):
        sx, sy, sw, sh = CABEZA[nombre]
        rect(im, sx, sy + 5, sw, 3, TELA_ROJA[1]); rect(im, sx, sy + 5, sw, 1, TELA_ROJA[2])
        rect(im, sx, sy + 7, sw, 1, TELA_ROJA[0])
    sx, sy, sw, sh = CABEZA['atras']
    rect(im, sx, sy + 5, sw, 3, TELA_ROJA[1]); rect(im, sx + 3, sy + 4, 2, 4, TELA_ROJA[0])     # el nudo
    px(im, sx + 3, sy + 4, TELA_ROJA[2])
    for i in range(0, sw, 2):
        px(im, sx + i, sy + 7, TELA_ROJA[0])


def botas(im, cuero, cuero_osc, cuero_claro, espuela):
    mat = PIEL_CUERO if espuela else FIELTRO_N
    puno = PIEL_CUERO if espuela else TELA_ROJA
    botas_capa(im, mat, puno, espuela)


# ---------------------------------------------------------------- iconos 16x16
def pinta(filas, paleta):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y, fila in enumerate(filas):
        for x, ch in enumerate(fila):
            if ch != '.':
                im.putpixel((x, y), paleta[ch])
    return im


# los iconos están en iconos_ropa.py (contorno, luz arriba a la izquierda, cuatro tonos por material)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iconos_ropa import ICONOS  # noqa: E402

PIEZAS = {'vaquero': ('sombrero_vaquero', 'chaleco_vaquero', 'chaparreras_vaquero', 'botas_vaquero'),
          'bandido': ('sombrero_bandido', 'poncho_bandido', 'pantalon_bandido', 'botas_bandido')}


def capas():
    for juego in ('vaquero', 'bandido'):
        l1 = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
        l2 = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
        if juego == 'vaquero':
            sombrero_vaquero(l1)
            chaleco_vaquero(l1)
            botas(l1, CUERO, CUERO_OSC, CUERO_CLARO, True)
            chaparreras(l2)
        else:
            sombrero_bandido(l1)
            poncho_bandido(l1)
            botas(l1, NEGRO, c(24, 22, 24), ROJO, False)
            pantalon_bandido(l2)
        os.makedirs(ARM, exist_ok=True)
        l1.save(os.path.join(ARM, juego + '_layer_1.png'))
        l2.save(os.path.join(ARM, juego + '_layer_2.png'))


def iconos_y_datos():
    ing = {'sombrero_vaquero': (['LLL', 'WWW'], {'L': 'minecraft:leather', 'W': 'minecraft:wheat'}),
           'chaleco_vaquero': (['L L', 'LCL', 'LLL'], {'L': 'minecraft:leather', 'C': 'minecraft:copper_ingot'}),
           'chaparreras_vaquero': (['LLL', 'LCL', 'L L'], {'L': 'minecraft:leather', 'C': 'minecraft:copper_ingot'}),
           'botas_vaquero': (['L L', 'C C'], {'L': 'minecraft:leather', 'C': 'minecraft:copper_ingot'}),
           'sombrero_bandido': (['LLL', 'DDD'], {'L': 'minecraft:leather', 'D': 'minecraft:black_dye'}),
           'poncho_bandido': (['R R', 'LLL', 'LLL'], {'L': 'minecraft:leather', 'R': 'minecraft:red_wool'}),
           'pantalon_bandido': (['LLL', 'LDL', 'L L'], {'L': 'minecraft:leather', 'D': 'minecraft:black_dye'}),
           'botas_bandido': (['L L', 'D D'], {'L': 'minecraft:leather', 'D': 'minecraft:black_dye'})}
    os.makedirs(REC, exist_ok=True)
    for nombre, (filas, pal) in ICONOS.items():
        pinta(filas, pal).save(os.path.join(ICO, nombre + '.png'))
        with open(os.path.join(MOD, nombre + '.json'), 'w', encoding='utf-8') as f:
            json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': 'copperslug:item/' + nombre}}, f, indent=1)
        patron, claves = ing[nombre]
        receta = {'type': 'minecraft:crafting_shaped', 'category': 'equipment', 'pattern': patron,
                  'key': {k: {'item': v} for k, v in claves.items()}, 'result': {'id': 'copperslug:' + nombre, 'count': 1}}
        with open(os.path.join(REC, nombre + '.json'), 'w', encoding='utf-8') as f:
            json.dump(receta, f, indent=2)
            f.write('\n')


if __name__ == '__main__':
    capas()
    iconos_y_datos()
    print('ropa: capas, iconos, modelos y recetas generados')

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
REC = os.path.join(RES, 'data/copperslug/recipes')


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


# ---------------------------------------------------------------- cabeza: (0,0). Cara delante en (8,8), lados en (0,8) y (16,8), atrás en (24,8), arriba en (8,0)
def sombrero_vaquero(im):
    cu = [FIELTRO_OSC, c(126, 90, 54)]
    moteado(im, 8, 0, 8, 8, FIELTRO, cu, 1)                 # la copa, de arriba
    rect(im, 11, 1, 2, 6, FIELTRO_OSC)                        # la hendidura de la copa
    for x0 in (0, 8, 16, 24):
        moteado(im, x0, 8, 8, 3, FIELTRO, cu, x0)            # la copa (tres filas)
        rect(im, x0, 10, 8, 1, c(52, 36, 22))                # la cinta
        rect(im, x0, 11, 8, 1, FIELTRO_OSC)                  # el ala, en sombra
    rect(im, 11, 10, 2, 1, ORO)                               # la hebilla
    rect(im, 11, 8, 2, 0, ORO)


def sombrero_bandido(im):
    ne = [NEGRO_CLARO, c(48, 44, 48)]
    moteado(im, 8, 0, 8, 8, NEGRO, ne, 2)
    rect(im, 11, 1, 2, 6, NEGRO_CLARO)
    for x0 in (0, 8, 16, 24):
        moteado(im, x0, 8, 8, 3, NEGRO, ne, x0 + 5)
        rect(im, x0, 10, 8, 1, ROJO)                         # la cinta roja
        rect(im, x0, 11, 8, 1, c(24, 22, 24))
    # el pañuelo sobre la nariz y la boca: delante, de lado y el nudo atrás
    rect(im, 8, 13, 8, 3, ROJO)
    for x in range(8, 16, 2):
        im.putpixel((x, 14), c(236, 232, 226))              # lunares
    rect(im, 8, 13, 8, 1, ROJO_OSC)
    rect(im, 0, 13, 8, 3, ROJO)
    rect(im, 16, 13, 8, 3, ROJO)
    rect(im, 24, 13, 8, 3, ROJO)
    rect(im, 28, 12, 2, 4, ROJO_OSC)                          # el nudo


# ---------------------------------------------------------------- cuerpo: (16,16). Delante (20,20), atrás (32,20), lados (16,20) y (28,20), arriba (20,16)
def chaleco_vaquero(im):
    cu = [CUERO_OSC, CUERO_CLARO]
    moteado(im, 20, 16, 8, 4, CUERO, cu, 3)                  # hombros (arriba)
    moteado(im, 20, 20, 8, 12, CUERO, cu, 4)                 # delante
    moteado(im, 32, 20, 8, 12, CUERO, cu, 5)                 # atrás
    moteado(im, 16, 20, 4, 12, CUERO, cu, 6)
    moteado(im, 28, 20, 4, 12, CUERO, cu, 7)
    rect(im, 23, 20, 2, 12, CUERO_OSC)                        # la abertura del centro
    for y in (22, 25, 28):
        rect(im, 22, y, 1, 1, ORO)                            # botones
    rect(im, 26, 22, 1, 1, ORO)                               # la estrella de sheriff, en el pecho
    rect(im, 25, 23, 3, 1, ORO)
    rect(im, 26, 24, 1, 1, ORO)
    rect(im, 25, 22, 1, 1, ORO_OSC)
    rect(im, 27, 22, 1, 1, ORO_OSC)
    rect(im, 20, 31, 8, 1, CUERO_OSC)                         # el borde de abajo


def poncho_bandido(im):
    for (x, y, w, h, seed) in ((20, 16, 8, 4, 8), (20, 20, 8, 12, 9), (32, 20, 8, 12, 10), (16, 20, 4, 12, 11), (28, 20, 4, 12, 12)):
        moteado(im, x, y, w, h, LONA, [LONA_OSC, c(170, 146, 112)], seed)
    for (x, y, w, h) in ((20, 20, 8, 12), (32, 20, 8, 12), (16, 20, 4, 12), (28, 20, 4, 12)):
        for yy, col in ((y + 3, ROJO), (y + 4, ROJO), (y + 7, NEGRO_CLARO), (y + 10, ROJO), (y + 11, ROJO_OSC)):
            rect(im, x, yy, w, 1, col)                        # las rayas del poncho
    for x in range(20, 28, 2):
        im.putpixel((x + 1, 31), c(0, 0, 0, 0))               # el flequillo del borde
    for x in range(32, 40, 2):
        im.putpixel((x + 1, 31), c(0, 0, 0, 0))
    # los hombros: la parte de arriba de los dos brazos
    for x0 in (40, 48, 44, 52):
        pass
    for (x, y, w) in ((40, 20, 4), (44, 20, 4), (48, 20, 4), (52, 20, 4)):
        moteado(im, x, y, w, 5, LONA, [LONA_OSC], x)
        rect(im, x, y + 3, w, 1, ROJO)
    rect(im, 44, 16, 4, 4, LONA)
    # la bandolera de balas, en diagonal sobre el pecho
    for i in range(8):
        im.putpixel((20 + i, 20 + i), c(70, 46, 28))
        if i % 2 == 0:
            im.putpixel((20 + i, 21 + i), ORO)


# ---------------------------------------------------------------- piernas: (0,16). Delante (4,20), atrás (12,20), lados (0,20) y (8,20), abajo (8,16)
def botas(im, cuero, cuero_osc, cuero_claro, espuela):
    for (x, y, w) in ((4, 20, 4), (12, 20, 4), (0, 20, 4), (8, 20, 4)):
        rect(im, x, y + 7, w, 5, cuero)                       # la caña
        rect(im, x, y + 7, w, 1, cuero_claro)                 # el borde de arriba
        rect(im, x, y + 11, w, 1, cuero_osc)                  # la suela
    rect(im, 8, 16, 4, 4, cuero_osc)                           # la planta
    if espuela:
        rect(im, 13, y_espuela := 30, 2, 1, ACERO)            # la espuela, atrás en el talón
        im.putpixel((15, 30), ACERO)
        im.putpixel((13, 29), c(120, 122, 132))


def chaparreras(im):
    cu = [CUERO_OSC, CUERO_CLARO]
    for (x, y, w) in ((4, 20, 4), (12, 20, 4), (0, 20, 4), (8, 20, 4)):
        moteado(im, x, y, w, 8, CUERO, cu, x + 20)
    for y in range(20, 28, 2):                                 # el flequillo del lado de fuera
        im.putpixel((0, y), c(0, 0, 0, 0))
    rect(im, 0, 27, 4, 1, CUERO_OSC)
    # el cinturón y la hebilla, en la parte de abajo del cuerpo
    rect(im, 20, 28, 8, 2, c(70, 46, 28))
    rect(im, 32, 28, 8, 2, c(70, 46, 28))
    rect(im, 16, 28, 4, 2, c(70, 46, 28))
    rect(im, 28, 28, 4, 2, c(70, 46, 28))
    rect(im, 23, 28, 2, 2, ORO)


def pantalon_bandido(im):
    for (x, y, w) in ((4, 20, 4), (12, 20, 4), (0, 20, 4), (8, 20, 4)):
        moteado(im, x, y, w, 8, TELA, [c(56, 56, 66)], x + 30)
    rect(im, 0, 27, 4, 1, c(48, 48, 56))
    rect(im, 20, 28, 8, 2, NEGRO)
    rect(im, 32, 28, 8, 2, NEGRO)
    rect(im, 16, 28, 4, 2, NEGRO)
    rect(im, 28, 28, 4, 2, NEGRO)
    rect(im, 23, 28, 2, 2, ACERO)
    for x in (21, 26):
        im.putpixel((x, 29), ORO)                               # dos balas en el cinturón


# ---------------------------------------------------------------- iconos 16x16
def pinta(filas, paleta):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y, fila in enumerate(filas):
        for x, ch in enumerate(fila):
            if ch != '.':
                im.putpixel((x, y), paleta[ch])
    return im


ICONOS = {
    'sombrero_vaquero': (['................', '................', '.....bbbbb......', '....bBBBBBb.....', '....bBBBBBb.....', '....bBBBBBb.....', '....bcgcccb.....', '...bbBBBBBbb....',
                          '.bbBBBBBBBBBbb..', 'bBBBBBBBBBBBBBb.', 'bbBBBBBBBBBBbb..', '.bbbbbbbbbbbb...', '................', '................', '................', '................'],
                         {'b': FIELTRO_OSC, 'B': FIELTRO, 'c': c(52, 36, 22), 'g': ORO}),
    'chaleco_vaquero': (['................', '..bbb......bbb..', '.bCCCb....bCCCb.', '.bCCCCb..bCCCCb.', '.bCCCCCbbCCCCCb.', '..bCCCCoCCCCCb..', '..bCCgCoCCEECb..', '..bCCCCoCEEEEb..',
                         '..bCCgCoCCEECb..', '..bCCCCoCCCCCb..', '..bCCgCoCCCCCb..', '..bCCCCoCCCCCb..', '..bbbbbbbbbbbb..', '................', '................', '................'],
                        {'b': CUERO_OSC, 'C': CUERO, 'o': c(72, 48, 30), 'g': ORO, 'E': ORO_OSC}),
    'chaparreras_vaquero': (['................', '..bbbbbbbbbbbb..', '..bgggBBBBgggb..', '..bBBBBBBBBBBb..', '..bBBBBbbBBBBb..', '..bBBBBb.bBBBb..', '..bBBBb...bBBb..', '..bBBBb...bBBb..',
                             '..bBBBb...bBBb..', '..bBBBb...bBBb..', '..bBBBb...bBBb..', '..bBbBb...bBbBb.', '..b.b.b...b.b.b.', '................', '................', '................'],
                            {'b': CUERO_OSC, 'B': CUERO, 'g': ORO}),
    'botas_vaquero': (['................', '................', '................', '..bbbb....bbbb..', '..bBBb....bBBb..', '..bBBb....bBBb..', '..bBBb....bBBb..', '..bBBb....bBBb..',
                       '..bBBbb...bBBbb.', '.bBBBBBb.bBBBBBb', '.bbbbbbb.bbbbbbb', '..s.......s.....', '................', '................', '................', '................'],
                      {'b': CUERO_OSC, 'B': CUERO, 's': ACERO}),
    'sombrero_bandido': (['................', '................', '.....kkkkk......', '....kNNNNNk.....', '....kNNNNNk.....', '....kNNNNNk.....', '....krrrrrk.....', '...kkNNNNNkk....',
                          '.kkNNNNNNNNNkk..', 'kNNNNNNNNNNNNNk.', 'kkNNNNNNNNNNkk..', '.kkkkkkkkkkkk...', '................', '................', '................', '................'],
                         {'k': c(24, 22, 24), 'N': NEGRO, 'r': ROJO}),
    'poncho_bandido': (['................', '....bbbbbbbb....', '..bbLLLLLLLLbb..', '.bLLLLLbbLLLLLb.', '.bLLLLb..bLLLLb.', '.bRRRRRRRRRRRRb.', '.bLLLLLLLLLLLLb.', '.bNNNNNNNNNNNNb.',
                        '.bLLLLLLLLLLLLb.', '.bRRRRRRRRRRRRb.', '.bLLLLLLLLLLLLb.', '.bRrRrRrRrRrRrb.', '..b.b.b.b.b.b...', '................', '................', '................'],
                       {'b': LONA_OSC, 'L': LONA, 'R': ROJO, 'r': ROJO_OSC, 'N': NEGRO_CLARO}),
    'pantalon_bandido': (['................', '..bbbbbbbbbbbb..', '..bgbgBBBBbgbb..', '..bTTTTTTTTTTb..', '..bTTTTbbTTTTb..', '..bTTTTb.bTTTb..', '..bTTTb...bTTb..', '..bTTTb...bTTb..',
                          '..bTTTb...bTTb..', '..bTTTb...bTTb..', '..bTTTb...bTTb..', '..bTTTb...bTTb..', '..bbbbb...bbbb..', '................', '................', '................'],
                         {'b': NEGRO, 'T': TELA, 'g': ORO, 'B': ACERO}),
    'botas_bandido': (['................', '................', '................', '..bbbb....bbbb..', '..bRRb....bRRb..', '..bNNb....bNNb..', '..bNNb....bNNb..', '..bNNb....bNNb..',
                       '..bNNbb...bNNbb.', '.bNNNNNb.bNNNNNb', '.bbbbbbb.bbbbbbb', '................', '................', '................', '................', '................'],
                      {'b': c(24, 22, 24), 'N': NEGRO, 'R': ROJO}),
}

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
                  'key': {k: {'item': v} for k, v in claves.items()}, 'result': {'item': 'copperslug:' + nombre, 'count': 1}}
        with open(os.path.join(REC, nombre + '.json'), 'w', encoding='utf-8') as f:
            json.dump(receta, f, indent=2)
            f.write('\n')


if __name__ == '__main__':
    capas()
    iconos_y_datos()
    print('ropa: capas, iconos, modelos y recetas generados')

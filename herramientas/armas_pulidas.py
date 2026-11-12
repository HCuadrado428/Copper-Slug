#!/usr/bin/env python3
"""Las armas rediseñadas con estilo vanilla pulido.

Dos partes:

1. **Texturas de piezas** (`p_<material>.png`, 16x16). En vez de un ruido que se repite, cada hoja tiene bandas de 1, 2, 3,
   4 y 5 píxeles de alto, pintadas como las caras de los modelos de vanilla (tridente, catalejo, ballesta): fila de luz
   arriba, sombra abajo y algún detalle suelto en medio (vetas en la madera, cepillado en el metal). Cada cara del modelo
   usa la banda de su alto, así que todas las piezas tienen el canto marcado y la textura nunca se estira.
2. **Modelos**: cada arma a mano, con piezas de medio píxel o de píxel entero, centradas en x = 8 y con la boca hacia z
   pequeña. Se conservan las medidas que usa el código (el tambor del revólver: centro y = 8,9, de z = 8,4 a 11) y el
   `display` de cada modelo se copia del JSON actual.

Uso: herramientas/armas_pulidas.py [--salida DIR] [--texturas DIR] [arma ...]
"""
import argparse
import json
import os
import random
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texturas_estilo_mc import COBRE, HIERRO, ACERO, LATON, MADERA, CUERO  # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'common', 'src', 'main', 'resources', 'assets',
                    'copperslug')
DIR_MOD = os.path.join(RAIZ, 'models', 'item', 'armas3d')
DIR_TEX = os.path.join(RAIZ, 'textures', 'item', 'armas3d')

ECO = [(5, 52, 62), (10, 86, 96), (22, 128, 138), (60, 190, 196), (150, 240, 236)]
CUERDA = [(96, 74, 44), (134, 104, 64), (170, 140, 92), (198, 172, 122), (226, 206, 160)]
NEGRO = [(14, 12, 12), (22, 20, 20), (30, 27, 27), (40, 36, 36), (54, 50, 50)]
BRASA = [(150, 40, 10), (214, 80, 20), (245, 140, 30), (255, 200, 70), (255, 245, 170)]
NACAR = [(168, 160, 150), (200, 194, 184), (226, 222, 212), (242, 240, 232), (255, 255, 250)]

# bandas: alto -> fila donde empieza
BANDAS = {1: 0, 2: 1, 3: 3, 4: 6, 5: 10}


# ------------------------------------------------------------------------------------------------ texturas de piezas

def hoja(r, tipo, semilla):
    rng = random.Random(semilla)
    px = [[r[2]] * 16 for _ in range(16)]
    for alto, y0 in BANDAS.items():
        filas = list(range(y0, y0 + alto))
        for i, y in enumerate(filas):
            if alto == 1:
                base = r[2]
            elif i == 0:
                base = r[3]           # canto de luz
            elif i == alto - 1 and alto >= 3:
                base = r[1]           # sombra
            else:
                base = r[2]
            for x in range(16):
                px[y][x] = base
            # detalles sueltos en las filas de en medio (nunca en el canto)
            if 0 < i < alto - 1 or alto <= 2:
                if tipo == 'madera':
                    x = rng.randrange(16)
                    for k in range(rng.randint(3, 6)):
                        px[y][(x + k) % 16] = r[1] if (y + k) % 3 else r[3]
                else:
                    for _ in range(2 if tipo == 'metal' else 1):
                        x = rng.randrange(16)
                        px[y][x] = r[3] if rng.random() < 0.5 else r[1]
        # un brillo en la esquina de luz y un poro en la sombra, como los objetos de vanilla
        if alto >= 2:
            px[y0][0] = r[4]
            px[y0][1] = r[4] if tipo == 'metal' else px[y0][1]
    for x in range(16):
        px[15][x] = r[0]
    im = Image.new('RGBA', (16, 16))
    for y in range(16):
        for x in range(16):
            im.putpixel((x, y), tuple(px[y][x]) + (255,))
    return im


MATERIALES = {
    'p_cobre_0': (COBRE[0], 'metal'), 'p_cobre_1': (COBRE[1], 'metal'), 'p_cobre_2': (COBRE[2], 'metal'),
    'p_cobre_3': (COBRE[3], 'metal'), 'p_hierro': (HIERRO, 'metal'), 'p_acero': (ACERO, 'metal'),
    'p_laton': (LATON, 'metal'), 'p_madera': (MADERA, 'madera'), 'p_cuero': (CUERO, 'cuero'),
    'p_eco': (ECO, 'metal'), 'p_nacar': (NACAR, 'metal'), 'p_cuerda': (CUERDA, 'madera'), 'p_negro': (NEGRO, 'cuero'), 'p_brasa': (BRASA, 'metal'),
}


def generar_texturas(dir_tex):
    os.makedirs(dir_tex, exist_ok=True)
    for i, (n, (r, tipo)) in enumerate(MATERIALES.items()):
        hoja(r, tipo, 500 + i).save(os.path.join(dir_tex, n + '.png'))


TEXTURAS = {k: 'copperslug:item/armas3d/p_' + v for k, v in {
    'cobre': 'cobre_0', 'hierro': 'hierro', 'acero': 'acero', 'laton': 'laton', 'madera': 'madera', 'cuero': 'cuero',
    'eco': 'eco', 'cuerda': 'cuerda', 'negro': 'negro', 'brasa': 'brasa', 'nacar': 'nacar', 'nogal': 'madera',
    'mecha': 'cuerda', 'boca': 'negro'}.items()}
# texturas que no son de material (se conservan las del JSON y se pegan enteras: manómetro, lente, tambor, bayoneta…)
ESPECIALES = ('tambor', 'tambor_lado', 'esfera', 'tolva', 'lente', 'bayoneta', 'particle')
UV_COMPLETA = ('tambor', 'esfera', 'tolva', 'lente')


# ------------------------------------------------------------------------------------------------ cajas

def _banda(alto):
    a = max(0.5, min(5.0, alto))
    h = min(5, max(1, int(round(a + 0.01))))
    return BANDAS[h], a


def _uv_cara(largo, alto):
    """UV de una cara de largo x alto: el largo va a lo ancho de la hoja (como mucho 16) y el alto elige la banda."""
    y0, a = _banda(alto)
    return [0.0, float(y0), round(min(16.0, largo), 3), round(y0 + min(a, 5.0), 3)]


def C(nombre, f, t, tex, caras=('north', 'south', 'east', 'west', 'up', 'down'), rot=None):
    dx, dy, dz = (t[k] - f[k] for k in range(3))
    e = {'name': nombre, 'from': [round(v, 3) for v in f], 'to': [round(v, 3) for v in t], 'faces': {}}
    for c in caras:
        if tex in UV_COMPLETA:
            d = {'uv': [0.0, 0.0, 16.0, 16.0]}
        else:
            # (a lo largo de u, a lo largo de v) de la cara; el lado largo va siempre a lo ancho de la hoja
            a, b = {'east': (dz, dy), 'west': (dz, dy), 'north': (dx, dy), 'south': (dx, dy)}.get(c, (dx, dz))
            if c in ('up', 'down'):
                a, b = (dz, dx) if dz >= dx else (dx, dz)
                d = {'uv': _uv_cara(a, b)}
                if dz >= dx:
                    d['rotation'] = 90
            elif b > a and b > 5:
                d = {'uv': _uv_cara(b, a), 'rotation': 90}
            else:
                d = {'uv': _uv_cara(a, b)}
        d['texture'] = '#' + tex
        e['faces'][c] = d
    if rot:
        e['rotation'] = {'origin': list(rot[0]), 'axis': rot[1], 'angle': rot[2]}
    return e


def P(nombre, z1, z2, y1, y2, ancho, tex, x=8.0, rot=None):
    """Una pieza vista de lado (de z1 a z2 y de y1 a y2) con su ancho, centrada en x."""
    return C(nombre, (x - ancho / 2, y1, z1), (x + ancho / 2, y2, z2), tex, rot=rot)


def boca(z, y1, y2, ancho, tex='negro'):
    return C('boca', (8 - ancho / 2, y1, z - 0.02), (8 + ancho / 2, y2, z), tex, caras=('north',))


# ------------------------------------------------------------------------------------------------ revólver

def revolver(abierto=False):
    el = [
        P('canon', 1, 8.4, 9, 11, 2, 'cobre'),
        boca(1, 9.5, 10.5, 1),
        P('funda_eyector', 2.5, 8.4, 8, 9, 1, 'cobre'),
        P('punto_de_mira', 1.5, 2.5, 11, 11.5, 0.5, 'hierro'),
        P('puente', 8.4, 12, 10.5, 11.5, 2, 'cobre'),
        P('base', 7.5, 11, 6, 7.25, 2, 'cobre'),
        P('frente', 7.5, 8.4, 6, 9, 2, 'cobre'),
        # el escudo de atrás con la ventana de carga a la derecha (por ella se ven los culotes)
        C('escudo_izq', (7, 6, 11), (8, 11.5, 12.5), 'cobre'),
        C('escudo_der_alto', (8, 10, 11), (9, 11.5, 12.5), 'cobre'),
        C('escudo_der_bajo', (8, 6, 11), (9, 8, 12.5), 'cobre'),
        P('martillo', 12, 13, 11, 12, 1, 'hierro'),
        P('espolon', 12.5, 13.75, 12, 12.5, 1, 'hierro'),
        # guardamonte de latón y gatillo
        P('guarda_frente', 8.5, 9, 4, 6, 1, 'laton'),
        P('guarda_bajo', 8.5, 11.5, 4, 4.5, 1, 'laton'),
        P('gatillo', 10, 10.5, 4.5, 6, 0.5, 'hierro'),
        # empuñadura en cabeza de pájaro: tres escalones hacia atrás y el culo de cobre
        P('empunadura_1', 11, 13.5, 4, 6, 2, 'madera'),
        P('empunadura_2', 11.5, 14, 2, 4, 2, 'madera'),
        P('empunadura_3', 12, 14.5, 0.5, 2, 2, 'madera'),
        P('culo', 12, 14.5, 0, 0.5, 2.5, 'cobre'),
        P('lomo', 13.5, 14, 4, 6.5, 2, 'cobre'),
    ]
    if abierto:
        el.append(C('brazo', (5, 7, 7.5), (7, 8, 8.4), 'cobre'))
    return el


# ------------------------------------------------------------------------------------------------ Winchester

def winchester(palanca=False):
    el = [
        P('canon', -14, 3.5, 9.5, 10.5, 1, 'cobre'),
        boca(-14, 9.75, 10.25, 0.5),
        P('punto_de_mira', -13.5, -13, 10.5, 11, 0.5, 'hierro'),
        P('abrazadera', -11.5, -11, 8.25, 10.75, 1.5, 'hierro'),
        P('deposito', -12, 3.5, 8.5, 9.5, 1, 'cobre'),
        P('tapon_deposito', -12.5, -12, 8.5, 9.5, 1, 'hierro'),
        P('tapa_guardamano', -4.5, -4, 8, 10, 2, 'cobre'),
        P('guardamano', -4, 3.5, 8, 10, 2, 'madera'),
        P('alza', 0, 1, 10.5, 11, 1, 'hierro'),
        P('cajon', 3.5, 10.5, 7, 11, 2, 'cobre'),
        C('ventana_carga', (9, 8, 5), (9.02, 9, 8), 'negro', caras=('east',)),
        P('martillo', 9.5, 10.5, 11, 12, 1, 'hierro'),
        P('gatillo', 7.5, 8, 6, 7, 0.5, 'hierro'),
        P('cuello', 10.5, 13, 6.5, 9.5, 2, 'madera'),
        P('culata_1', 13, 16.5, 5.5, 9.5, 2, 'madera'),
        P('culata_2', 16.5, 20, 4.5, 9.5, 2, 'madera'),
        P('cantonera', 20, 20.5, 4.5, 9.5, 2, 'cobre'),
    ]
    rot = ((8, 6.75, 5.25), 'x', 45) if palanca else None   # el eje va delante: baja la parte de atrás
    el += [
        P('palanca_frente', 5, 5.5, 4.5, 7, 1, 'hierro', rot=rot),
        P('palanca_bajo', 5, 9.5, 4.5, 5, 1, 'hierro', rot=rot),
        P('palanca_atras', 9, 9.5, 5, 7, 1, 'hierro', rot=rot),
    ]
    return el


# ------------------------------------------------------------------------------------------------ lanzallamas (tipo fusil)

def lanzallamas():
    return [
        P('boquilla', 0, 1.5, 8.5, 11.5, 3, 'hierro'),
        boca(0, 9, 11, 2),
        P('cuello_boquilla', 1.5, 2.5, 9, 11, 2, 'hierro'),
        P('encendedor', 0.5, 2.5, 7.5, 8.5, 1, 'laton'),
        P('chispa', 0.25, 0.75, 7.5, 8, 0.5, 'brasa'),
        P('canon', 2.5, 8, 9, 11, 2, 'cobre'),
        P('escudo_calor', 3, 7.5, 11, 11.5, 2.5, 'hierro'),
        P('empunadura_delantera', 3.5, 5, 5.5, 9, 1.5, 'madera'),
        P('cajon', 8, 12, 8, 11.5, 2.5, 'cobre'),
        C('manometro', (9.25, 9.5, 9.5), (9.75, 10.5, 10.5), 'laton'),
        # el depósito bajo el cajón, con dos abrazaderas y la manguera hacia la boquilla
        P('deposito', 6.5, 11.5, 5, 8, 3, 'acero'),
        P('abrazadera_1', 7.25, 7.75, 4.75, 8.25, 3.5, 'laton'),
        P('abrazadera_2', 10.25, 10.75, 4.75, 8.25, 3.5, 'laton'),
        P('manguera', 5.5, 6.5, 7, 8, 1, 'cuero'),
        P('gatillo', 12, 12.5, 6.5, 8, 0.5, 'hierro'),
        P('guarda', 11.5, 13, 6, 6.5, 1, 'hierro'),
        P('empunadura', 12.5, 14, 3.5, 8, 2, 'madera'),
        P('empunadura_baja', 13, 14.5, 2.5, 3.5, 2, 'madera'),
        # culata de tubo
        P('culata_alta', 12, 15.5, 10, 11, 1.5, 'cobre'),
        P('culata_baja', 14, 15.5, 7.5, 8.5, 1.5, 'cobre'),
        P('cantonera', 15.5, 16, 7, 11, 2, 'madera'),
    ]


# ------------------------------------------------------------------------------------------------ pistola de resonancia

def resonancia():
    return [
        # el emisor: una bocina de cobre con la cara de eco
        P('bocina', 0.5, 1.5, 8, 12.5, 4, 'cobre'),
        C('membrana', (6.5, 8.5, 0.48), (9.5, 12, 0.5), 'eco', caras=('north',)),
        P('bocina_cuello', 1.5, 2.5, 8.75, 11.75, 2.5, 'eco'),
        P('canon', 2.5, 4.5, 9.25, 11.25, 1.5, 'cobre'),
        P('corredera', 4.5, 13, 9, 11.5, 2, 'cobre'),
        P('armazon', 5, 12, 8, 9, 2, 'hierro'),
        # las bobinas de eco encima
        P('bobina_1', 5.5, 6.5, 11.5, 12, 1.5, 'eco'),
        P('bobina_2', 7.5, 8.5, 11.5, 12, 1.5, 'eco'),
        P('bobina_3', 9.5, 10.5, 11.5, 12, 1.5, 'eco'),
        P('martillo', 12.5, 13.5, 10.5, 12, 1, 'hierro'),
        # guardamonte, gatillo y empuñadura inclinada
        P('guarda_frente', 7, 7.5, 6, 8, 1, 'hierro'),
        P('guarda_bajo', 7, 10, 6, 6.5, 1, 'hierro'),
        P('gatillo', 8.5, 9, 6.5, 8, 0.5, 'hierro'),
        P('empunadura_1', 9.5, 12.5, 5, 8, 2, 'madera'),
        P('empunadura_2', 10, 13, 2.5, 5, 2, 'madera'),
        P('culo', 10, 13, 2, 2.5, 2.5, 'cobre'),
    ]


# ------------------------------------------------------------------------------------------------ arponera (fusil submarino)

def arponera():
    return [
        # el arpón encima del cañón, con la punta y las aletas
        P('arpon', -5, 14, 10.5, 11, 0.5, 'acero'),
        P('punta', -6.5, -5, 10.25, 11.25, 1, 'acero'),
        P('aletas', -5, -4.5, 9.75, 11.75, 0.5, 'acero'),
        # cabeza del cañón (donde van las gomas) y el cañón
        P('cabeza', 0.5, 2, 8, 11, 2.5, 'cobre'),
        P('goma', 1, 1.5, 7.75, 11.25, 3, 'cuero'),
        P('canon', 2, 15, 8.75, 10.5, 1.5, 'cobre'),
        # el carrete del sedal
        P('carrete_tapa_1', 6, 6.5, 5.5, 8.5, 3, 'hierro'),
        P('carrete', 6.5, 7.5, 6, 8, 2.5, 'cuerda'),
        P('carrete_tapa_2', 7.5, 8, 5.5, 8.5, 3, 'hierro'),
        P('soporte_carrete', 6.5, 7.5, 8, 8.75, 1, 'hierro'),
        # guardamonte, gatillo, empuñadura y culata
        P('guarda_frente', 10, 10.5, 7, 8.75, 1, 'hierro'),
        P('guarda_bajo', 10, 12.5, 6.5, 7, 1, 'hierro'),
        P('gatillo', 11, 11.5, 7, 8.75, 0.5, 'hierro'),
        P('empunadura', 12, 13.5, 4, 8.75, 2, 'madera'),
        P('empunadura_baja', 12.5, 14, 3, 4, 2, 'madera'),
        P('culata', 15, 16.5, 7.5, 11, 2, 'madera'),
    ]


# ------------------------------------------------------------------------------------------------ cerbatana (carabina de dardos)

def cerbatana():
    return [
        P('canon', 0.5, 9, 10, 11, 1, 'cobre'),
        boca(0.5, 10.25, 10.75, 0.5),
        P('anillo_boca', 0.5, 1, 9.75, 11.25, 1.5, 'laton'),
        P('anillo_medio', 5, 5.5, 9.75, 11.25, 1.5, 'laton'),
        P('guardamano', 4, 9, 9, 10.5, 1.5, 'madera'),
        # la cámara de aire y la pera de cuero que la carga
        P('camara', 9, 11.5, 8.5, 11.5, 2, 'cobre'),
        P('pera', 8.5, 11, 7, 8.5, 1.5, 'cuero'),
        P('alza', 10, 11, 11.5, 12, 1, 'hierro'),
        # el carcaj de dardos en el costado, con dos plumas
        C('carcaj', (9, 8.75, 5.5), (10, 10.25, 8.5), 'cuero'),
        C('pluma_1', (9.25, 10.25, 7.5), (9.75, 10.75, 8), 'laton'),
        C('pluma_2', (9.25, 10.25, 6.5), (9.75, 10.75, 7), 'eco'),
        P('gatillo', 11.5, 12, 7, 8.5, 0.5, 'hierro'),
        P('guarda', 11, 12.5, 6.5, 7, 1, 'hierro'),
        # culata
        P('cuello', 11.5, 13, 7.5, 10.5, 2, 'madera'),
        P('culata', 13, 15, 6.5, 10.5, 2, 'madera'),
        P('cantonera', 15, 15.5, 6.5, 10.5, 2, 'cobre'),
    ]


ARMAS = {}
ARMAS_7 = {
    'revolver_3d': revolver,
    'revolver_3d_abierto': lambda: revolver(True),
    'winchester_3d': winchester,
    'winchester_3d_palanca': lambda: winchester(True),
    'lanzallamas_3d': lanzallamas,
    'resonancia_3d': resonancia,
    'arponera_3d': arponera,
    'cerbatana_3d': cerbatana,
}
ARMAS.update(ARMAS_7)



# ------------------------------------------------------------------------------------------------ rifle de catalejo

def rifle(cerrojo=False):
    el = [
        P('corona', -10.5, -9.5, 8.75, 10.25, 1.5, 'cobre'),
        boca(-10.5, 9.25, 9.75, 0.5),
        P('canon', -9.5, 4, 9, 10, 1, 'cobre'),
        P('guardamano', -3, 4, 7.5, 9, 2, 'madera'),
        P('cajon', 4, 10.5, 8, 10.5, 2, 'cobre'),
        # el catalejo: monturas, tubo, objetivo con lente y ocular
        P('montura_1', 4.5, 5.5, 10.5, 11.25, 1, 'hierro'),
        P('montura_2', 9, 10, 10.5, 11.25, 1, 'hierro'),
        P('catalejo', 3, 11.5, 11.25, 12.75, 1.5, 'cobre'),
        P('objetivo', 1, 3, 11, 13, 2.5, 'cobre'),
        C('lente', (7, 11.25, 0.98), (9, 12.75, 1), 'lente', caras=('north',)),
        P('ocular', 11.5, 13, 11.25, 12.75, 2, 'negro'),
        # guardamonte, gatillo y culata
        P('guarda_frente', 6.5, 7, 6.5, 8, 1, 'hierro'),
        P('guarda_bajo', 6.5, 10, 6.25, 6.75, 1, 'cobre'),
        P('gatillo', 8.25, 8.75, 6.75, 8, 0.5, 'hierro'),
        P('muneca', 10.5, 13, 6, 10, 2, 'madera'),
        P('culata', 13, 20, 6.5, 10, 2, 'madera'),
        P('culata_baja', 15, 20, 5, 6.5, 2, 'madera'),
        P('cantonera', 20, 20.5, 5, 10, 2, 'negro'),
    ]
    if cerrojo:
        # cerrojo abierto: la manilla arriba y atrás, y el cuerpo del cerrojo fuera del cajón
        el += [P('cerrojo', 10.5, 12, 9.25, 10.25, 1.5, 'cobre'),
               C('manilla', (9, 9.5, 10.5), (10.5, 10, 11), 'hierro', rot=((9, 9.75, 10.75), 'z', 45)),
               C('bola', (10, 10.25, 10.25), (11, 11.25, 11.25), 'hierro', rot=((9, 9.75, 10.75), 'z', 45))]
    else:
        el += [C('manilla', (9, 9.25, 9), (11, 9.75, 9.5), 'hierro', rot=((9, 9.5, 9.25), 'z', -22.5)),
               C('bola', (10.75, 9, 8.75), (11.75, 10, 9.75), 'hierro', rot=((9, 9.5, 9.25), 'z', -22.5))]
    return el


# ------------------------------------------------------------------------------------------------ escopeta de presión

def escopeta():
    return [
        P('canon', -10, 5, 9, 11, 2, 'cobre'),
        C('boca_tolva', (7, 9, -10.02), (9, 11, -10), 'tolva', caras=('north',)),
        P('aro_boca', -10, -9, 8.75, 11.25, 2.5, 'hierro'),
        # el depósito de presión bajo el cañón y el corredor de bombeo
        P('deposito', -7, 5, 6.5, 8.5, 1.5, 'cobre'),
        P('tapon', -7.5, -7, 6.75, 8.25, 1, 'laton'),
        P('corredera', -5, 0, 6, 9, 2.5, 'madera'),
        P('banda_1', -4, -3.5, 5.75, 9.25, 2.75, 'hierro'),
        P('banda_2', -1.5, -1, 5.75, 9.25, 2.75, 'hierro'),
        P('cajon', 5, 10, 6, 11.5, 2.5, 'cobre'),
        # el manómetro en el costado izquierdo
        C('manometro', (5.75, 7, 6), (6.75, 10, 9), 'laton'),
        C('esfera', (5.73, 7.5, 6.5), (5.75, 9.5, 8.5), 'esfera', caras=('west',)),
        # la tolva de arriba
        P('cuello_tolva', 6.5, 7.5, 11.5, 12, 1, 'hierro'),
        P('tolva', 6, 8, 12, 13, 2, 'cobre'),
        P('guarda_frente', 6.5, 7, 5, 6, 1, 'hierro'),
        P('guarda_bajo', 6.5, 10, 4.5, 5, 1, 'cobre'),
        P('gatillo', 8, 8.5, 5, 6, 0.5, 'hierro'),
        P('muneca', 10, 12, 5, 10.5, 2, 'madera'),
        P('culata', 12, 19, 6.5, 10.5, 2, 'madera'),
        P('culata_baja', 14, 19, 5, 6.5, 2, 'madera'),
        P('cantonera', 19, 19.5, 5, 10.5, 2, 'negro'),
    ]


# ------------------------------------------------------------------------------------------------ Derringer

def derringer(abierta=False):
    rot = ((8, 8.3, 8.4), 'x', 22.5) if abierta else None
    canones = [
        P('canon_sup', 1, 8, 9.75, 11, 1.5, 'cobre', rot=rot),
        P('canon_inf', 1, 8, 8.5, 9.75, 1.5, 'cobre', rot=rot),
        P('costilla', 1.25, 7.75, 11, 11.5, 0.5, 'cobre', rot=rot),
        C('boca_sup', (7.75, 10.125, 0.98), (8.25, 10.625, 1), 'negro', caras=('north',), rot=rot),
        C('boca_inf', (7.75, 8.875, 0.98), (8.25, 9.375, 1), 'negro', caras=('north',), rot=rot),
    ]
    return canones + [
        C('pasador', (6.75, 8, 8.1), (9.25, 8.6, 8.7), 'hierro'),
        P('armazon', 8, 11, 7, 11.25, 2, 'cobre'),
        P('martillo', 10.25, 11, 11.25, 12.25, 0.75, 'hierro'),
        P('espolon', 10.75, 11.5, 12, 12.5, 0.75, 'hierro'),
        P('gatillo', 8.5, 9, 5.75, 7, 0.5, 'laton'),
        P('cachas_1', 9.5, 12, 4.5, 7, 1.75, 'nacar'),
        P('cachas_2', 10, 12.5, 3, 4.5, 1.75, 'nacar'),
        P('culo', 10, 12.5, 2.5, 3, 2, 'cobre'),
    ]


# ------------------------------------------------------------------------------------------------ Thompson

def thompson(con_tambor=True):
    el = [
        P('compensador', -12.5, -9.5, 8.75, 10.25, 1.5, 'hierro'),
        boca(-12.5, 9.25, 9.75, 0.5),
        P('punto_de_mira', -11.5, -10.5, 10.25, 10.75, 0.5, 'hierro'),
        P('canon', -9.5, 2, 9, 10, 1, 'cobre'),
    ]
    for i, z in enumerate((-8, -6.5, -5, -3.5, -2)):
        el.append(P('aleta_%d' % i, z, z + 0.5, 8.75, 10.25, 1.5, 'cobre'))
    el += [
        P('soporte_delantero', -1, 0.5, 8, 9, 1, 'cobre'),
        P('empunadura_delantera', -1.5, 1, 4.5, 8, 1.5, 'nogal'),
        P('cajon', 2, 11, 8, 11.25, 2, 'cobre'),
        P('palanca_cerrojo', 3.5, 4.5, 11.25, 11.75, 0.5, 'cobre'),
        P('alza', 9, 10, 11.25, 12, 1, 'hierro'),
        P('guarda', 7.5, 10, 6.25, 6.75, 1, 'cobre'),
        P('gatillo', 8, 8.5, 6.75, 8, 0.5, 'hierro'),
        P('empunadura', 9, 11, 3.5, 8, 1.5, 'nogal'),
        P('culata', 11, 20, 6.5, 10.5, 2, 'nogal'),
        P('culata_baja', 15, 20, 5, 6.5, 2, 'nogal'),
        P('cantonera', 20, 20.5, 5, 10.5, 2, 'negro'),
    ]
    if con_tambor:
        el += [
            P('cuello_tambor', 5, 7, 6.25, 8, 1.25, 'cobre'),
            P('tambor', 4, 8, 2.25, 6.25, 2, 'cobre'),
            C('tambor_izq', (6.98, 2.25, 4), (7, 6.25, 8), 'tambor', caras=('west',)),
            C('tambor_der', (9, 2.25, 4), (9.02, 6.25, 8), 'tambor', caras=('east',)),
        ]
    return el


# ------------------------------------------------------------------------------------------------ mosquete

def mosquete(bayoneta=True, etapa=0):
    el = [
        P('canon', -9, 12, 9.5, 10.5, 1, 'cobre'),
        boca(-9, 9.75, 10.25, 0.5),
        P('punto_de_mira', -8.5, -8, 10.5, 11, 0.5, 'hierro'),
        P('caja', -6, 12, 8, 9.75, 1.75, 'madera'),
        P('punta_caja', -6.5, -6, 8, 9.75, 2, 'laton'),
        P('abrazadera_1', -3, -2.5, 7.75, 10.75, 2, 'laton'),
        P('abrazadera_2', 3, 3.5, 7.75, 10.75, 2, 'laton'),
        # la llave de chispa en el lado derecho
        C('pletina', (8.875, 8.5, 9), (9.25, 9.75, 13), 'cobre'),
        C('rastrillo', (9.25, 9.5, 9.5), (9.75, 11, 10), 'acero'),
        C('pie_de_gato', (9.25, 10, 11.25), (9.75, 11.5, 12), 'hierro'),
        C('piedra', (9.25, 11.25, 10.75), (9.75, 11.75, 11.25), 'negro'),
        P('guarda', 12, 15, 6.5, 7, 0.75, 'laton'),
        P('gatillo', 13.25, 13.75, 7, 8, 0.5, 'acero'),
        P('muneca', 12, 15, 7, 9.75, 1.6, 'madera'),
        P('culata', 15, 24, 5.5, 9, 1.6, 'madera'),
        P('culata_baja', 19, 24, 4, 5.5, 2, 'madera'),
        P('cantonera', 24, 24.5, 4, 9, 1.8, 'laton'),
    ]
    # la baqueta: en su sitio (bajo la caja) o fuera, metida en la boca (etapas de la recarga)
    if etapa == 0:
        el.append(P('baqueta', -8.5, 11, 7.5, 8, 0.5, 'hierro'))
    elif etapa in (1, 2):
        el += [P('baqueta', -15.5, -9, 9.75, 10.25, 0.5, 'hierro'), P('cabeza_baqueta', -16, -15.5, 9.5, 10.5, 1, 'hierro')]
    else:
        el += [P('baqueta', -12, -9, 9.75, 10.25, 0.5, 'hierro'), P('cabeza_baqueta', -12.5, -12, 9.5, 10.5, 1, 'hierro')]
    if bayoneta:
        el += [
            P('cubo_bayoneta', -9.75, -8.5, 9.25, 11, 1.6, 'cobre'),
            C('brazo_bayoneta', (8.25, 8.5, -9.75), (8.75, 9.5, -9), 'acero'),
            C('hoja', (8.25, 8.5, -15), (8.75, 9.25, -9.75), 'bayoneta'),
            C('punta_hoja', (8.375, 8.625, -16), (8.625, 9.125, -15), 'bayoneta'),
        ]
    return el


# ------------------------------------------------------------------------------------------------ cañón de mano

def canon_mano(encendida=False):
    el = [
        P('brocal', -8, -7, 8.25, 10.75, 2.5, 'cobre'),
        boca(-8, 8.75, 10.25, 1.5),
        P('canon', -7, 2, 8.5, 10.5, 2, 'cobre'),
        P('refuerzo_1', -4.5, -4, 8.25, 10.75, 2.25, 'cobre'),
        P('refuerzo_2', -1.5, -1, 8.25, 10.75, 2.25, 'cobre'),
        P('recamara', 2, 4, 8.25, 10.75, 2.5, 'cobre'),
        P('gancho', -2, -1, 7.5, 8.25, 0.75, 'hierro'),
        P('mecha', 2.5, 3, 10.75, 12, 0.5, 'mecha'),
        P('vara', 4, 24, 9, 10, 1.25, 'madera'),
        P('anilla_1', 5, 5.5, 8.75, 10.25, 1.5, 'cobre'),
        P('anilla_2', 7, 7.5, 8.75, 10.25, 1.5, 'cobre'),
        P('regaton', 24, 24.5, 8.75, 10.25, 1.5, 'hierro'),
    ]
    if encendida:
        el.append(P('chispa', 2.5, 3, 12, 12.5, 0.5, 'brasa'))
    return el


# ------------------------------------------------------------------------------------------------ Gatling (piezas: el código las mueve)
# Ejes que usa GatlingRenderer: cañones sobre (x 8, y 17,25), cabeceo en (y 17,25, z 8), manivela en (y 17,25, z 12,5).

def _pata(i):
    rots = (((8, 15, 6.5), 'x', 22.5), ((8, 15, 10), 'z', 22.5), ((8, 15, 10), 'z', -22.5))
    o, eje, ang = rots[i]
    z1 = 5.75 if i == 0 else 9.25
    return [C('pata_%d' % i, (7.25, -1, z1), (8.75, 14, z1 + 1.5), 'nogal', rot=(o, eje, ang)),
            C('pie_%d' % i, (7, -1.5, z1 - 0.25), (9, 0.5, z1 + 1.75), 'hierro', rot=(o, eje, ang))]


def gatling_base():
    el = [C('cabeza', (6.5, 14, 6.5), (9.5, 15.5, 10.5), 'hierro')]
    for i in range(3):
        el += _pata(i)
    return el


def gatling_yugo():
    return [
        C('eje', (7.25, 15.5, 7.25), (8.75, 16.25, 8.75), 'hierro'),
        C('travesano', (4.5, 16.25, 6.5), (11.5, 16.75, 9.5), 'hierro'),
        C('brazo_izq', (4.5, 16.75, 7), (5.5, 18, 9), 'hierro'),
        C('brazo_der', (10.5, 16.75, 7), (11.5, 18, 9), 'hierro'),
    ]


def gatling_cuerpo():
    return [
        C('placa_delantera', (5.5, 14.75, -10.25), (10.5, 19.75, -9.75), 'hierro'),
        C('placa_media', (5.5, 14.75, -1), (10.5, 19.75, -0.5), 'hierro'),
        C('riel_izq', (5.75, 14.75, -9.75), (6.25, 15.25, 9), 'hierro'),
        C('riel_der', (9.75, 14.75, -9.75), (10.25, 15.25, 9), 'hierro'),
        C('cuna', (5.5, 14.75, 7), (10.5, 15.25, 9), 'hierro'),
        C('caja', (5.5, 14.5, 9), (10.5, 20, 15.5), 'cobre'),
        C('munon_izq', (5, 16.75, 7.5), (5.5, 17.75, 8.5), 'hierro'),
        C('munon_der', (10.5, 16.75, 7.5), (11, 17.75, 8.5), 'hierro'),
        C('culata', (7, 16, 15.5), (9, 18, 16.5), 'hierro'),
        C('boton', (7.5, 16.5, 16.5), (8.5, 17.5, 17.5), 'hierro'),
        C('collar_tolva', (6.75, 20, 10.25), (9.25, 20.5, 13.25), 'hierro'),
        C('tolva', (7, 20.5, 10.5), (9, 23.5, 13), 'laton'),
        C('caja_manivela', (10.5, 16, 11.5), (11.25, 18.5, 13.5), 'hierro'),
    ]


def gatling_canones():
    el = []
    for i, (cx, cy) in enumerate(((9.39, 18.05), (8, 18.85), (6.61, 18.05), (6.61, 16.45), (8, 15.65), (9.39, 16.45))):
        el.append(C('canon_%d' % i, (cx - 0.5, cy - 0.5, -14), (cx + 0.5, cy + 0.5, 9), 'acero'))
        el.append(C('boca_%d' % i, (cx - 0.25, cy - 0.25, -14.02), (cx + 0.25, cy + 0.25, -14), 'negro', caras=('north',)))
    el += [
        C('eje', (7.625, 16.875, -12.5), (8.375, 17.625, 9), 'hierro'),
        C('aro_1', (5.75, 15, -13), (10.25, 19.5, -12.5), 'laton'),
        C('aro_2', (6, 15.25, -4), (10, 19.25, -3.5), 'laton'),
    ]
    return el


def gatling_manivela():
    return [
        C('cubo', (11.25, 16.875, 12.125), (12, 17.625, 12.875), 'hierro'),
        C('brazo', (12, 14, 12.125), (12.5, 17.625, 12.875), 'hierro'),
        C('puno', (12.5, 13.75, 12), (14.5, 14.75, 13), 'nogal'),
    ]


def gatling_3d():
    return gatling_cuerpo() + gatling_canones() + gatling_manivela()


# ------------------------------------------------------------------------------------------------ accesorios (encantamientos que se ven)

def _silenciador(z1, z2, cy, lado):
    return [P('silenciador', z1, z2, cy - lado / 2, cy + lado / 2, lado, 'cobre'),
            P('aro_1', z1, z1 + 0.5, cy - lado / 2 - 0.25, cy + lado / 2 + 0.25, lado + 0.5, 'hierro'),
            P('aro_2', z2 - 0.5, z2, cy - lado / 2 - 0.25, cy + lado / 2 + 0.25, lado + 0.5, 'hierro'),
            boca(z1, cy - 0.25, cy + 0.25, 0.5)]


ACCESORIOS = {
    'acc_silenciador_rifle': lambda: _silenciador(-14.5, -10, 9.5, 2),
    'acc_silenciador_winchester': lambda: _silenciador(-15.95, -12, 10, 1.5),   # Minecraft no deja pasar de -16
    'acc_silenciador_thompson': lambda: _silenciador(-15.95, -11.5, 9.5, 2),
    'acc_silenciador_derringer': lambda: _silenciador(-3, 1, 10.375, 1.5),
    'acc_compensador_thompson': lambda: [P('compensador', -14, -12.5, 8.5, 10.5, 2, 'cobre'),
                                         P('ranura', -13.5, -13, 10.5, 10.75, 0.5, 'negro'), boca(-14, 9.25, 9.75, 0.5)],
    'acc_canon_largo_revolver': lambda: [P('canon_largo', -2, 1, 9, 11, 2, 'cobre'),
                                         P('punto_de_mira', -1.5, -0.5, 11, 11.5, 0.5, 'hierro'),
                                         boca(-2, 9.5, 10.5, 1)],
    'acc_deposito_winchester': lambda: [P('deposito_largo', -13.5, -12, 8.5, 9.5, 1, 'cobre'),
                                        P('collar_1', -10, -9.5, 8.25, 9.75, 1.5, 'hierro'),
                                        P('collar_2', -6.5, -6, 8.25, 9.75, 1.5, 'hierro'),
                                        P('tapon', -14, -13.5, 8.5, 9.5, 1, 'hierro')],
    'acc_estrangulador_escopeta': lambda: [P('estrangulador', -13, -10, 8.75, 11.25, 2.5, 'cobre'),
                                           P('cono', -14, -13, 9.25, 10.75, 1.5, 'cobre'),
                                           boca(-14, 9.75, 10.25, 0.5)],
    'acc_mira_mosquete': lambda: [P('base_mira', -7.5, -6.5, 10.5, 11, 1, 'cobre'),
                                  P('mira', -7.25, -6.75, 11, 11.75, 0.5, 'cobre')],
    # el ánima rayada: tres estrías de cobre dentro de la boca del cañón de mano
    'acc_anima_canon': lambda: [C('estria_%d' % i, (7.25, 8.875 + 0.5 * i, -8.04), (8.75, 9.125 + 0.5 * i, -8.02), 'cobre',
                                  caras=('north',)) for i in range(3)],
}

ARMAS.update({
    'rifle_3d': rifle,
    'rifle_3d_cerrojo': lambda: rifle(True),
    'escopeta_3d': escopeta,
    'derringer_3d': derringer,
    'derringer_3d_oculta': derringer,
    'derringer_3d_abierta': lambda: derringer(True),
    'derringer_3d_abierta_oculta': lambda: derringer(True),
    'thompson_3d': thompson,
    'thompson_3d_sin_tambor': lambda: thompson(False),
    'mosquete_3d': lambda: mosquete(True, 0),
    'mosquete_3d_sin': lambda: mosquete(False, 0),
    'mosquete_3d_1': lambda: mosquete(True, 1),
    'mosquete_3d_1_sin': lambda: mosquete(False, 1),
    'mosquete_3d_2': lambda: mosquete(True, 2),
    'mosquete_3d_2_sin': lambda: mosquete(False, 2),
    'mosquete_3d_3': lambda: mosquete(True, 3),
    'mosquete_3d_3_sin': lambda: mosquete(False, 3),
    'canon_mano_3d': canon_mano,
    'canon_mano_3d_encendida': lambda: canon_mano(True),
    'gatling_base': gatling_base,
    'gatling_yugo': gatling_yugo,
    'gatling_cuerpo': gatling_cuerpo,
    'gatling_cuerpo_1': gatling_cuerpo,
    'gatling_cuerpo_2': gatling_cuerpo,
    'gatling_cuerpo_3': gatling_cuerpo,
    'gatling_canones': gatling_canones,
    'gatling_manivela': gatling_manivela,
    'gatling_3d': gatling_3d,
})
for _n, _f in ACCESORIOS.items():
    for _ox in range(4):
        ARMAS['%s_%d' % (_n, _ox)] = _f


# ------------------------------------------------------------------------------------------------ el cinturón (se ve puesto en el cuerpo)
# Centrado en (8, 8, 8): el cuerpo del jugador mide 8 x 12 x 4. La capa del jugador lo pone a la altura de la cintura;
# x pequeña es el lado derecho del jugador y z grande el frente.

def cinturon_cartuchera():
    el = [
        C('cinto_frente', (3.5, 7.25, 10), (12.5, 8.75, 10.5), 'cuero'),
        C('cinto_atras', (3.5, 7.25, 5.5), (12.5, 8.75, 6), 'cuero'),
        C('cinto_izq', (12, 7.25, 6), (12.5, 8.75, 10), 'cuero'),
        C('cinto_der', (3.5, 7.25, 6), (4, 8.75, 10), 'cuero'),
        C('hebilla', (7.25, 7, 10.25), (8.75, 9, 10.75), 'laton'),
    ]
    # los cartuchos en sus presillas, por los lados y detrás
    for i, x in enumerate((5, 6, 9.5, 10.5)):
        el.append(C('bala_%d' % i, (x, 8.75, 5.25), (x + 0.5, 9.5, 5.75), 'laton'))
    for i, z in enumerate((7, 8.5)):
        el.append(C('bala_izq_%d' % i, (12.25, 8.75, z), (12.75, 9.5, z + 0.5), 'laton'))
    el.append(C('bolsa', (9.5, 6.5, 10.25), (11.5, 8.5, 11.25), 'cuero'))
    return el


def cinturon_funda(llena=False):
    el = [
        C('funda', (2.5, 3, 7), (3.5, 7.5, 9.5), 'cuero'),
        C('boca_funda', (2.25, 7, 6.75), (3.75, 7.75, 9.75), 'cuero'),
        C('remache', (2.24, 5, 8), (2.26, 5.5, 8.5), 'laton'),
        C('correa', (3, 7.25, 7.5), (4, 8.75, 8.5), 'cuero'),
    ]
    if llena:
        # la culata del arma asoma por arriba, hacia atrás
        el += [C('culata', (2.5, 7.75, 6.5), (3.5, 9.75, 8), 'madera'),
               C('culo', (2.5, 9.75, 6), (3.5, 10.25, 8), 'cobre'),
               C('martillo', (2.75, 7.75, 8), (3.25, 8.75, 8.75), 'hierro')]
    return el


CINTURON = {'cinturon_cartuchera': cinturon_cartuchera, 'cinturon_funda': cinturon_funda,
            'cinturon_funda_llena': lambda: cinturon_funda(True)}


def generar_cinturon(salida):
    os.makedirs(salida, exist_ok=True)
    for n, f in CINTURON.items():
        m = {'credit': 'copperslug', 'ambientocclusion': False, 'textures': dict(TEXTURAS), 'elements': f()}
        m['textures']['particle'] = 'copperslug:item/armas3d/p_cuero'
        with open(os.path.join(salida, n + '.json'), 'w', encoding='utf-8') as fh:
            json.dump(m, fh, ensure_ascii=False, separators=(',', ':'))

def generar(salida, nombres=None):
    os.makedirs(salida, exist_ok=True)
    for n in nombres or ARMAS:
        with open(os.path.join(DIR_MOD, n + '.json'), encoding='utf-8') as fh:
            m = json.load(fh)
        tex = dict(TEXTURAS)
        for k in ESPECIALES:
            if k in m.get('textures', {}):
                tex[k] = m['textures'][k]
        # las fases del óxido (gatling_cuerpo_2, acc_..._3): su cobre
        fase = n.rsplit('_', 1)[-1]
        if fase in ('1', '2', '3') and (n.startswith('gatling_cuerpo') or n.startswith('acc_')):
            tex['cobre'] = 'copperslug:item/armas3d/p_cobre_' + fase
        m['textures'] = tex
        m['elements'] = ARMAS[n]()
        with open(os.path.join(salida, n + '.json'), 'w', encoding='utf-8') as fh:
            json.dump(m, fh, ensure_ascii=False, separators=(',', ':'))
        print('%-24s %3d cajas' % (n, len(m['elements'])))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--salida', default=DIR_MOD)
    ap.add_argument('--texturas', default=DIR_TEX)
    ap.add_argument('armas', nargs='*')
    a = ap.parse_args()
    generar_texturas(a.texturas)
    generar(a.salida, a.armas)
    if not a.armas:
        generar_cinturon(a.salida)

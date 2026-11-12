#!/usr/bin/env python3
"""Las armas rediseñadas desde cero con estilo vanilla puro: piezas de píxeles enteros (o medio píxel donde hace falta
centrar en x = 8) y muy pocas cajas, como la ballesta o el tridente.

Cada arma es una lista de cajas `C(nombre, desde, hasta, textura)`. La UV de cada cara se alinea a texeles enteros, así
que cada píxel del modelo enseña un píxel entero de la textura. Se conservan las medidas que usa el código: el tambor
del revólver (centro y = 8,9, de z = 8,4 a 11, dibujado aparte), la boca hacia z pequeña y el `display` de cada modelo
(se copia del JSON actual), así que la mano en primera persona y el apuntado siguen en su sitio.

Uso: herramientas/armas_vanilla.py [--salida DIR] [arma ...]   (sin armas: todas las que hay aquí)
"""
import argparse
import json
import math
import os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'common', 'src', 'main', 'resources', 'assets',
                   'copperslug', 'models', 'item', 'armas3d')
CARAS = ('north', 'south', 'east', 'west', 'up', 'down')


def _tramo(a, b):
    """UV de a..b alineada a texel entero y dentro de 0..16."""
    w = b - a
    if w >= 16:
        return 0.0, 16.0
    u = math.floor(a) % 16 + (a - math.floor(a))
    if u + w > 16:
        u = 16 - w
    return round(u, 3), round(u + w, 3)


def uv(cara, f, t):
    if cara in ('north', 'south'):
        (u1, u2), (v1, v2) = _tramo(f[0], t[0]), _tramo(16 - t[1], 16 - f[1])
    elif cara in ('east', 'west'):
        (u1, u2), (v1, v2) = _tramo(f[2], t[2]), _tramo(16 - t[1], 16 - f[1])
    else:
        (u1, u2), (v1, v2) = _tramo(f[0], t[0]), _tramo(f[2], t[2])
    return [u1, v1, u2, v2]


def C(nombre, f, t, tex, caras=CARAS, rot=None):
    e = {'name': nombre, 'from': list(f), 'to': list(t),
         'faces': {c: {'uv': uv(c, f, t), 'texture': '#' + tex} for c in caras}}
    if rot:
        e['rotation'] = {'origin': list(rot[0]), 'axis': rot[1], 'angle': rot[2]}
    return e


def boca(x1, y1, x2, y2, z):
    """El agujero negro de la boca: una cara hacia delante, pegada a la boca."""
    return C('boca', (x1, y1, z - 0.02), (x2, y2, z), 'negro', caras=('north',))


# ---------------------------------------------------------------------------------------------------- revólver

def revolver(abierto=False):
    el = [
        C('canon', (7, 9, 1), (9, 11, 8.4), 'cobre'),
        boca(7.5, 9.5, 8.5, 10.5, 1),
        C('punto_de_mira', (7.5, 11, 1.5), (8.5, 12, 2.5), 'hierro'),
        C('varilla', (7.5, 8, 2.5), (8.5, 9, 8.4), 'hierro'),
        # el armazón alrededor del tambor (el tambor lo dibuja el código: centro y = 8,9, de z = 8,4 a 11)
        C('puente', (7, 11, 8.4), (9, 12, 12.5), 'cobre'),
        C('base', (7, 6, 7.5), (9, 7, 11), 'cobre'),
        C('frente', (7, 6, 7.5), (9, 9, 8.4), 'cobre'),
        # el escudo de atrás, con la ventana de carga a la derecha (por ella se ven los culotes)
        C('escudo_izq', (7, 7, 11), (8, 11, 12.5), 'cobre'),
        C('escudo_der_alto', (8, 10, 11), (9, 11, 12.5), 'cobre'),
        C('escudo_der_bajo', (8, 7, 11), (9, 8, 12.5), 'cobre'),
        C('martillo', (7.5, 12, 12), (8.5, 13, 13.5), 'hierro'),
        C('guarda_bajo', (7.5, 4, 8.5), (8.5, 5, 12), 'hierro'),
        C('guarda_frente', (7.5, 5, 8.5), (8.5, 6, 9.5), 'hierro'),
        C('gatillo', (7.5, 5, 10), (8.5, 6, 10.5), 'hierro'),
        # la empuñadura en escalera, con el culo de cobre
        C('empunadura_alta', (7, 3.5, 11.5), (9, 7, 14), 'madera'),
        C('empunadura_baja', (7, 0.5, 13), (9, 3.5, 15.5), 'madera'),
        C('culo', (7, -0.5, 13.5), (9, 0.5, 16), 'cobre'),
    ]
    if abierto:
        # el brazo del tambor, abierto hacia la izquierda (el código desplaza el tambor)
        el.append(C('brazo', (5, 7, 7.5), (7, 8, 8.5), 'cobre'))
    return el


# ---------------------------------------------------------------------------------------------------- Winchester

def winchester(palanca=False):
    el = [
        C('canon', (7.5, 9.5, -14), (8.5, 10.5, 3.5), 'cobre'),
        boca(7.5, 9.5, 8.5, 10.5, -14),
        C('deposito', (7.5, 8.5, -12), (8.5, 9.5, 3.5), 'cobre'),
        C('abrazadera', (7, 8, -12), (9, 10.5, -11), 'hierro'),
        C('punto_de_mira', (7.5, 10.5, -13.5), (8.5, 11.5, -12.5), 'hierro'),
        C('alza', (7.5, 10.5, 0), (8.5, 11, 1), 'hierro'),
        C('guardamano', (7, 8, -4), (9, 10, 3.5), 'madera'),
        C('cajon', (7, 7, 3.5), (9, 11, 10.5), 'cobre'),
        C('martillo', (7.5, 11, 9.5), (8.5, 12, 10.5), 'hierro'),
        C('gatillo', (7.5, 6, 7.5), (8.5, 7, 8), 'hierro'),
        C('cuello', (7, 6, 10.5), (9, 10, 13), 'madera'),
        C('culata', (7, 5, 13), (9, 9.5, 17), 'madera'),
        C('culata_baja', (7, 4.5, 17), (9, 9.5, 20), 'madera'),
        C('cantonera', (7, 4.5, 20), (9, 9.5, 20.5), 'cobre'),
    ]
    # la palanca bajo el cajón; abierta, gira hacia abajo desde su eje (detrás del gatillo)
    rot = ((8, 7, 9.5), 'x', 45) if palanca else None
    el += [
        C('palanca_frente', (7.5, 5, 5), (8.5, 7, 6), 'hierro', rot=rot),
        C('palanca_bajo', (7.5, 4, 5), (8.5, 5, 10), 'hierro', rot=rot),
        C('palanca_atras', (7.5, 5, 9), (8.5, 7, 10), 'hierro', rot=rot),
    ]
    return el


# ---------------------------------------------------------------------------------------------------- lanzallamas

def lanzallamas():
    return [
        C('boquilla', (6.5, 8, 0), (9.5, 11, 2), 'hierro'),
        boca(7, 8.5, 9, 10.5, 0),
        C('piloto', (7.5, 7, 0.5), (8.5, 8, 1.5), 'brasa'),
        C('canon', (7, 8.5, 2), (9, 10.5, 8), 'cobre'),
        C('banda_1', (6.5, 8, 3.5), (9.5, 11, 4.5), 'hierro'),
        C('banda_2', (6.5, 8, 6), (9.5, 11, 7), 'hierro'),
        C('cuerpo', (6.5, 8, 8), (9.5, 11.5, 14), 'cobre'),
        C('tapa', (7, 11.5, 9), (9, 12, 11), 'hierro'),
        # el depósito bajo el cañón, de acero con bandas de latón
        C('deposito', (6, 3.5, 3), (10, 7.5, 9.5), 'acero'),
        C('banda_dep_1', (5.75, 3.25, 4), (10.25, 7.75, 5), 'laton'),
        C('banda_dep_2', (5.75, 3.25, 7.5), (10.25, 7.75, 8.5), 'laton'),
        C('conector', (7.5, 7.5, 6), (8.5, 8, 7), 'hierro'),
        C('gatillo', (7.5, 7, 10.5), (8.5, 8, 11), 'hierro'),
        C('guarda', (7.5, 6, 10), (8.5, 7, 12), 'hierro'),
        C('empunadura_alta', (7, 3, 12), (9, 8, 14), 'madera'),
        C('empunadura_baja', (7, 1, 13), (9, 3, 15), 'madera'),
    ]


ARMAS = {
    'revolver_3d': revolver,
    'revolver_3d_abierto': lambda: revolver(abierto=True),
    'winchester_3d': winchester,
    'winchester_3d_palanca': lambda: winchester(palanca=True),
    'lanzallamas_3d': lanzallamas,
}


def generar(salida, nombres=None):
    os.makedirs(salida, exist_ok=True)
    for n in nombres or ARMAS:
        with open(os.path.join(DIR, n + '.json'), encoding='utf-8') as fh:
            m = json.load(fh)   # se conservan las texturas y el display
        m['elements'] = ARMAS[n]()
        with open(os.path.join(salida, n + '.json'), 'w', encoding='utf-8') as fh:
            json.dump(m, fh, ensure_ascii=False, separators=(',', ':'))
        print('%-28s %3d cajas' % (n, len(m['elements'])))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--salida', default=DIR)
    ap.add_argument('armas', nargs='*')
    a = ap.parse_args()
    generar(a.salida, a.armas)

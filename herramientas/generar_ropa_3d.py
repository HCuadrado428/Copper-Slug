#!/usr/bin/env python3
"""Genera los modelos 3D de la ropa cosmética: los dos sombreros (con ala), la estrella de sheriff, las espuelas y la esclavina del poncho.

El modelo de armadura de vanilla solo deja una caja alrededor de la cabeza, así que un sombrero con ala no cabe en la textura de la armadura:
se dibuja aparte, como un modelo 3D, con la capa de render RopaCapa (que va por el mismo mixin que la cartuchera y la funda).

Las coordenadas del modelo son píxeles, con la parte del cuerpo a la que va pegado como origen:
  cabeza    x 4..12, z 4..12, y 0..8 (y = 0 es la base de la cabeza, el frente está en z grande)
  cuerpo    y 0 es el hombro, hacia abajo y negativa (el pecho está en z = 10, +1 de la armadura)
  pierna    y 0 es la cadera, el talón está en y = -12 y z = 6 (atrás)
Es idempotente. Uso: generar_ropa_3d.py [raíz del repositorio]
"""
import json
import math
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_tambor import caja  # noqa: E402

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
TEX = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/textures/item/armas3d')
MOD = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item/armas3d')


def c(r, g, b):
    return (r, g, b, 255)


# ---------------------------------------------------------------- texturas 16x16 (sin ruido: fibras y bisel)
def tela(base, claro, oscuro, trama='fibra'):
    im = Image.new('RGBA', (16, 16), base)
    for y in range(16):
        for x in range(16):
            if trama == 'fibra':
                if x % 4 == 1:
                    im.putpixel((x, y), claro)
                elif x % 4 == 3 and y % 4 != 0:
                    im.putpixel((x, y), oscuro)
            elif trama == 'cuero':
                if y % 5 == 0:
                    im.putpixel((x, y), oscuro)
                elif y % 5 == 2 and x % 3 != 0:
                    im.putpixel((x, y), claro)
            elif trama == 'tejido':
                im.putpixel((x, y), claro if (x + y) % 2 == 0 else base)
                if y % 4 == 0:
                    im.putpixel((x, y), oscuro)
    return im


def oro():
    im = Image.new('RGBA', (16, 16), c(214, 168, 44))
    for y in range(16):
        for x in range(16):
            d = (x + y) % 8
            im.putpixel((x, y), c(255, 232, 130) if d == 0 else c(244, 202, 78) if d < 3 else c(214, 168, 44) if d < 6 else c(160, 118, 30))
    return im


def metal():
    im = Image.new('RGBA', (16, 16), c(150, 152, 164))
    for y in range(16):
        for x in range(16):
            d = (x + y) % 8
            im.putpixel((x, y), c(232, 234, 244) if d == 0 else c(180, 182, 196) if d < 3 else c(140, 142, 156) if d < 6 else c(96, 98, 110))
    return im


TEXTURAS = {
    'ropa_fieltro_m': tela(c(112, 78, 46), c(136, 98, 60), c(86, 58, 34)),
    'ropa_fieltro_n': tela(c(32, 30, 36), c(52, 48, 58), c(18, 16, 20)),
    'ropa_cuero': tela(c(96, 62, 36), c(124, 84, 50), c(66, 40, 22), 'cuero'),
    'ropa_tela_roja': tela(c(166, 38, 36), c(198, 62, 54), c(110, 22, 26), 'tejido'),
    'ropa_lana': tela(c(150, 128, 98), c(176, 154, 118), c(112, 94, 70), 'tejido'),
    'ropa_oro': oro(),
    'ropa_metal': metal(),
}
MAT = {k: k for k in TEXTURAS}


# ---------------------------------------------------------------- geometría
def octogono_y(cx, cz, a, y1, y2, tex, nombre):
    """Un prisma octogonal vertical de apotema a: dos cajas rectas y dos giradas 45° sobre el eje Y."""
    s = 2 * a * math.tan(math.radians(22.5))
    out = []
    for i, (ang, dx, dz) in enumerate(((0, a, s / 2), (0, s / 2, a), (45, a, s / 2), (-45, a, s / 2))):
        out.append(caja(cx - dx, y1 + 0.004 * i, cz - dz, cx + dx, y2 - 0.004 * i, cz + dz, tex, '%s_%d' % (nombre, i),
                        rot=((cx, y1, cz), 'y', ang) if ang else None))
    return out


def redondo(cx, cz, ra, y1, y2, tex, nombre, esquina=1.6):
    """Un prisma de esquinas cortadas hecho con tres cajas rectas solapadas (cruz y centro); ra = semiancho. Sin giros de 45 grados."""
    e = esquina
    return [caja(cx - ra, y1, cz - ra + e, cx + ra, y2, cz + ra - e, tex, nombre + '_a'),
            caja(cx - ra + e, y1 + 0.003, cz - ra, cx + ra - e, y2 + 0.003, cz + ra, tex, nombre + '_b'),
            caja(cx - ra + e / 2, y1 + 0.006, cz - ra + e / 2, cx + ra - e / 2, y2 + 0.006, cz + ra - e / 2, tex, nombre + '_c')]


def caja_rot(x1, y1, z1, x2, y2, z2, tex, nombre, eje, ang, origen):
    return caja(x1, y1, z1, x2, y2, z2, tex, nombre, rot=(origen, eje, ang))


def sombrero_vaquero():
    el = []
    # el ala: un disco octogonal con los dos lados levantados (como un sombrero de verdad)
    el += redondo(8, 8, 7.4, 6.0, 6.8, MAT['ropa_fieltro_m'], 'ala', 2.4)
    el.append(caja_rot(0.2, 6.5, 2.6, 2.8, 7.3, 13.4, MAT['ropa_fieltro_m'], 'ala_izq', 'z', 22.5, (2.8, 6.7, 8)))
    el.append(caja_rot(13.2, 6.5, 2.6, 15.8, 7.3, 13.4, MAT['ropa_fieltro_m'], 'ala_der', 'z', -22.5, (13.2, 6.7, 8)))
    # la copa: octógono más estrecho arriba, con la hendidura del centro
    el += redondo(8, 8, 5.0, 6.7, 10.8, MAT['ropa_fieltro_m'], 'copa', 1.0)
    el += redondo(8, 8, 4.3, 10.8, 11.7, MAT['ropa_fieltro_m'], 'copa_arriba', 1.0)
    el.append(caja(6.9, 11.3, 4.4, 9.1, 11.9, 11.6, MAT['ropa_fieltro_n'], 'hendidura'))
    # la cinta de cuero con su hebilla dorada
    el += redondo(8, 8, 5.12, 6.8, 8.1, MAT['ropa_cuero'], 'cinta', 1.0)
    el.append(caja(6.6, 6.7, 13.0, 9.4, 8.2, 13.5, MAT['ropa_oro'], 'hebilla'))
    el.append(caja(7.3, 7.1, 13.45, 8.7, 7.8, 13.8, MAT['ropa_cuero'], 'hebilla_hueco'))
    return el


def sombrero_bandido():
    el = []
    el += redondo(8, 8, 7.9, 6.0, 6.8, MAT['ropa_fieltro_n'], 'ala', 2.6)
    # el ala se dobla hacia abajo por delante y hacia arriba por detrás: un sombrero de cara tapada
    el.append(caja_rot(2.4, 5.6, 13.0, 13.6, 6.4, 15.6, MAT['ropa_fieltro_n'], 'ala_frente', 'x', -22.5, (8, 6.0, 13.0)))
    el += redondo(8, 8, 5.0, 6.7, 11.6, MAT['ropa_fieltro_n'], 'copa', 1.0)
    el += redondo(8, 8, 4.6, 11.6, 12.4, MAT['ropa_fieltro_n'], 'copa_arriba', 1.0)
    el += redondo(8, 8, 5.12, 6.8, 8.3, MAT['ropa_tela_roja'], 'cinta', 1.0)
    el.append(caja(6.9, 6.8, 13.0, 9.1, 7.7, 13.4, MAT['ropa_metal'], 'hebilla'))
    # la pluma roja, clavada en el lado izquierdo de la cinta y echada hacia atrás
    el.append(caja_rot(12.7, 7.6, 7.2, 13.3, 13.4, 8.4, MAT['ropa_tela_roja'], 'pluma', 'z', -22.5, (13.0, 7.6, 7.8)))
    el.append(caja_rot(13.0, 7.8, 7.55, 13.18, 13.2, 8.05, MAT['ropa_fieltro_n'], 'pluma_astil', 'z', -22.5, (13.0, 7.6, 7.8)))
    el.append(caja_rot(12.4, 7.6, 7.6, 12.8, 11.6, 8.2, MAT['ropa_tela_roja'], 'pluma_b', 'z', -22.5, (13.0, 7.6, 7.8)))
    return el


def estrella():
    """La estrella de sheriff en relieve (cuerpo, pecho a la izquierda del jugador)."""
    el = []
    cx, cy, z = 10.6, -3.4, 11.1
    g = MAT['ropa_oro']
    el.append(caja(cx - 1.7, cy - 0.5, z, cx + 1.7, cy + 0.5, z + 0.7, g, 'brazo_h'))
    el.append(caja(cx - 0.5, cy - 1.7, z, cx + 0.5, cy + 1.7, z + 0.7, g, 'brazo_v'))
    el.append(caja_rot(cx - 1.5, cy - 0.45, z, cx + 1.5, cy + 0.45, z + 0.7, g, 'brazo_d1', 'z', 45, (cx, cy, z)))
    el.append(caja_rot(cx - 1.5, cy - 0.45, z, cx + 1.5, cy + 0.45, z + 0.7, g, 'brazo_d2', 'z', -45, (cx, cy, z)))
    el.append(caja(cx - 0.6, cy - 0.6, z + 0.7, cx + 0.6, cy + 0.6, z + 0.95, MAT['ropa_cuero'], 'centro'))
    return el


def espuela():
    """Una espuela en el talón (pierna; se pinta en las dos). El modelo va centrado en la pierna (x = 8)."""
    el = []
    m = MAT['ropa_metal']
    el.append(caja(7.2, -11.9, 5.2, 8.8, -11.0, 6.1, m, 'banda'))                 # la banda alrededor del talón
    el.append(caja(7.7, -11.7, 4.2, 8.3, -11.3, 5.4, m, 'vastago'))               # el vástago, hacia atrás
    el.append(caja(7.55, -12.5, 3.5, 8.45, -10.6, 4.5, m, 'rodaja_v'))            # la rodaja: dos pletinas en cruz
    el.append(caja(7.55, -11.95, 3.5, 8.45, -11.25, 4.5, MAT['ropa_oro'], 'rodaja_centro'))
    el.append(caja_rot(7.55, -12.5, 3.5, 8.45, -10.6, 4.5, m, 'rodaja_d', 'x', 45, (8, -11.6, 4)))
    return el


def esclavina():
    """La esclavina del poncho: un cuello alto y los dos hombros inclinados hacia fuera, con la franja roja y el fleco en el borde."""
    el = []
    w, r, n = MAT['ropa_lana'], MAT['ropa_tela_roja'], MAT['ropa_fieltro_n']
    el.append(caja(3.3, -0.6, 3.0, 12.7, 1.9, 13.0, w, 'cuello'))                           # el cuello, alto
    el.append(caja(3.9, 1.7, 3.6, 12.1, 2.3, 12.4, r, 'cuello_borde'))
    for lado, x0, ang, sg in (('izq', 12.0, -22.5, 1), ('der', 4.0, 22.5, -1)):
        xa, xb = (x0, x0 + 6.6) if sg > 0 else (x0 - 6.6, x0)
        el.append(caja_rot(xa, -0.9, 2.5, xb, 0.9, 13.5, w, 'hombro_' + lado, 'z', ang, (x0, 0.0, 8)))
        xr1, xr2 = (x0 + 4.6, x0 + 6.9) if sg > 0 else (x0 - 6.9, x0 - 4.6)
        el.append(caja_rot(xr1, -1.2, 2.4, xr2, 0.4, 13.6, r, 'franja_' + lado, 'z', ang, (x0, 0.0, 8)))
        for i in range(5):                                                                 # el fleco del borde, colgando
            z = 2.9 + i * 2.2
            xf1, xf2 = (x0 + 6.2, x0 + 7.0) if sg > 0 else (x0 - 7.0, x0 - 6.2)
            el.append(caja_rot(xf1, -3.2, z, xf2, -1.0, z + 1.2, n if i % 2 else w, 'fleco_%s%d' % (lado, i), 'z', ang, (x0, 0.0, 8)))
    return el


MODELOS = {'ropa_sombrero_vaquero': sombrero_vaquero, 'ropa_sombrero_bandido': sombrero_bandido, 'ropa_estrella': estrella,
           'ropa_espuela': espuela, 'ropa_esclavina': esclavina}


def main():
    os.makedirs(TEX, exist_ok=True)
    for n, im in TEXTURAS.items():
        im.save(os.path.join(TEX, n + '.png'))
    texturas = {n: 'copperslug:item/armas3d/' + n for n in TEXTURAS}
    texturas['particle'] = 'copperslug:item/armas3d/ropa_fieltro_m'
    for nombre, f in MODELOS.items():
        m = {'credit': 'copperslug', 'ambientocclusion': False, 'textures': texturas, 'elements': f()}
        with open(os.path.join(MOD, nombre + '.json'), 'w', encoding='utf-8') as fh:
            json.dump(m, fh, separators=(',', ':'), ensure_ascii=False)
            fh.write('\n')
    print('ropa 3D: %d modelos y %d texturas generados' % (len(MODELOS), len(TEXTURAS)))


if __name__ == '__main__':
    main()

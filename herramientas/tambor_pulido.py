#!/usr/bin/env python3
"""El tambor del revólver con el estilo pulido de las demás armas, sin tocar su geometría.

El tambor lo dibuja el código aparte (gira de 60 en 60 grados y pone los culotes de las balas en sus recámaras), así
que su forma no cambia: solo los materiales. Los modelos revolver_cilindro_0..3 pasan a las texturas por pieza
(p_cobre_N, p_hierro, p_madera, p_negro, con la UV de banda de armas_pulidas.py) y las dos texturas propias del tambor
(la cara de las recámaras y las estrías del lateral) se recolorean con las rampas de cinco tonos del cobre, respetando
el negro de las recámaras y el latón de los pistones.

Uso: herramientas/tambor_pulido.py
"""
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import armas_pulidas as A  # noqa: E402
from texturas_estilo_mc import COBRE  # noqa: E402

TEX = A.DIR_TEX
MAT = {'cobre': None, 'hierro': 'p_hierro', 'madera': 'p_madera', 'negro': 'p_negro'}


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def es_cobre(c):
    """Los tonos del cobre (no el negro de las recámaras ni el amarillo de los pistones)."""
    r, g, b = c[:3]
    if lum(c) < 45:
        return False
    if r > 180 and g > 130 and b < 60:   # el latón de los pistones
        return False
    return True


def recolorear(nombre, rampa):
    p = os.path.join(TEX, nombre + '.png')
    im = Image.open(p).convert('RGBA')
    cols = sorted({im.getpixel((x, y)) for y in range(im.height) for x in range(im.width)
                   if im.getpixel((x, y))[3] > 0 and es_cobre(im.getpixel((x, y)))}, key=lum)
    # el más oscuro a la sombra, el más claro al brillo, los demás repartidos entre oscuro, base y claro
    destino = {}
    for i, c in enumerate(cols):
        if len(cols) == 1:
            k = 2
        else:
            k = 1 + round(3 * i / (len(cols) - 1))
        destino[c] = rampa[min(4, k)]
    for y in range(im.height):
        for x in range(im.width):
            c = im.getpixel((x, y))
            if c in destino:
                im.putpixel((x, y), tuple(destino[c]) + (255,))
    im.save(p)


def modelo(ox):
    p = os.path.join(A.DIR_MOD, 'revolver_cilindro_%d.json' % ox)
    m = json.load(open(p, encoding='utf-8'))
    t = m['textures']
    t['cobre'] = 'copperslug:item/armas3d/p_cobre_%d' % ox
    for k, v in MAT.items():
        if v:
            t[k] = 'copperslug:item/armas3d/' + v
    for e in m['elements']:
        f, to = e['from'], e['to']
        dx, dy, dz = (to[i] - f[i] for i in range(3))
        for cara, d in e.get('faces', {}).items():
            if d.get('texture', '').lstrip('#') not in MAT:
                continue
            # la UV de banda (como en armas_pulidas.C): el lado largo a lo ancho de la hoja, el alto elige la banda
            a, b = {'east': (dz, dy), 'west': (dz, dy), 'north': (dx, dy), 'south': (dx, dy)}.get(cara, (dx, dz))
            d.pop('rotation', None)
            if cara in ('up', 'down'):
                a, b = (dz, dx) if dz >= dx else (dx, dz)
                d['uv'] = A._uv_cara(a, b)
                if dz >= dx:
                    d['rotation'] = 90
            elif b > a and b > 5:
                d['uv'] = A._uv_cara(b, a)
                d['rotation'] = 90
            else:
                d['uv'] = A._uv_cara(a, b)
    json.dump(m, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))


if __name__ == '__main__':
    for ox in range(4):
        modelo(ox)
        recolorear('tambor_frente_%d' % ox, COBRE[ox])
        recolorear('tambor_lado_%d' % ox, COBRE[ox])

#!/usr/bin/env python3
"""Genera las texturas y los modelos de la arponera de cobre (la de los océanos) y su arpón.

  textures/item/arponera.png (+ _ox1.._ox3)       el icono (16x16), con el cobre en sus cuatro fases de óxido
  textures/item/arpon_cobre.png                   el arpón (la munición)
  models/item/armas3d/arponera_3d.json            cañón de cobre, la punta del arpón asomando, el carrete con cuerda y la culata
  models/item/arponera.json (+ _ox1.._ox3)        el modelo del objeto (3D en la mano, plano en el inventario)
  models/item/arpon_cobre.json

El cobre sale de la Derringer (lo que cambia entre sus texturas de óxido). Es idempotente.
Uso: generar_arponera.py [raíz del repositorio]
"""
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_tambor import caja  # noqa: E402
from modelos_armas_nuevas import MODELOS  # noqa: E402
from generar_cerbatana import cobres  # noqa: E402

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
TEX = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/textures/item')
MOD = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item')
A3D = os.path.join(MOD, 'armas3d')

HIERRO = (113, 119, 126, 255)
HIERRO_CLARO = (175, 181, 187, 255)
NEGRO = (60, 64, 70, 255)
MADERA = (121, 85, 52, 255)
MADERA_OSC = (84, 58, 36, 255)
CUERDA = (214, 188, 132, 255)
CUERDA_OSC = (160, 134, 86, 255)


def icono(tonos):
    oscuro, medio, claro = tonos
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    # el cañón ancho
    for i in range(8):
        x, y = 4 + i, 11 - i
        im.putpixel((x, y), claro)
        im.putpixel((x + 1, y), medio)
        im.putpixel((x, y + 1), medio)
        im.putpixel((x + 1, y + 1), oscuro)
    # la punta del arpón asoma por la boca (con un dentado)
    for (x, y), c in (((12, 3), HIERRO_CLARO), ((13, 2), HIERRO_CLARO), ((14, 1), HIERRO), ((12, 2), HIERRO), ((13, 3), HIERRO), ((14, 2), NEGRO)):
        im.putpixel((x, y), c)
    # el carrete a un lado, con la cuerda
    for (x, y) in ((7, 11), (8, 11), (7, 12), (8, 12), (6, 12)):
        im.putpixel((x, y), CUERDA if (x + y) % 2 else CUERDA_OSC)
    im.putpixel((7, 10), HIERRO)
    # la culata y el agarre
    for (x, y) in ((3, 12), (3, 13), (4, 13), (2, 13)):
        im.putpixel((x, y), MADERA)
    im.putpixel((2, 14), MADERA_OSC)
    im.putpixel((3, 14), MADERA_OSC)
    return im


def arpon():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for i in range(10):
        im.putpixel((3 + i, 12 - i), MADERA)
        im.putpixel((4 + i, 12 - i), MADERA_OSC)
    for (x, y), c in (((12, 3), HIERRO_CLARO), ((13, 2), HIERRO_CLARO), ((14, 1), HIERRO_CLARO), ((12, 2), HIERRO), ((13, 1), HIERRO),
                      ((11, 4), HIERRO), ((11, 3), HIERRO), ((13, 3), HIERRO), ((14, 2), HIERRO)):
        im.putpixel((x, y), c)
    for (x, y) in ((2, 13), (3, 13), (2, 12), (2, 14)):
        im.putpixel((x, y), CUERDA)
    return im


def textura_cuerda():
    im = Image.new('RGBA', (16, 16), CUERDA)
    for y in range(16):
        for x in range(16):
            if (x + y) % 4 == 0:
                im.putpixel((x, y), CUERDA_OSC)
            elif (x * 2 + y) % 7 == 0:
                im.putpixel((x, y), (236, 214, 164, 255))
    return im


def modelo_3d():
    base = json.load(open(os.path.join(A3D, 'winchester_3d.json'), encoding='utf-8'))
    # el juego completo de materiales (el de la Derringer) más el brillo de eco y la cuerda
    base['textures'] = dict(json.load(open(os.path.join(A3D, 'derringer_3d_oculta.json'), encoding='utf-8'))['textures'])
    base['textures']['eco'] = 'copperslug:item/armas3d/eco'
    base['textures']['cuerda'] = 'copperslug:item/armas3d/cuerda'
    base['elements'] = MODELOS['arponera']()
    base['textures']['particle'] = 'copperslug:item/arponera'
    with open(os.path.join(A3D, 'arponera_3d.json'), 'w', encoding='utf-8') as f:
        json.dump(base, f, separators=(',', ':'), ensure_ascii=False)
        f.write('\n')

def modelos_objeto():
    for n, suf, cobre in ((0, '', 'cobre_0'), (1, '_ox1', 'cobre_1'), (2, '_ox2', 'cobre_2'), (3, '_ox3', 'cobre_3')):
        m = {'loader': 'forge:separate_transforms', 'gui_light': 'front',
             'textures': {'particle': 'copperslug:item/arponera' + suf},
             'base': {'parent': 'copperslug:item/armas3d/arponera_3d', 'textures': {'cobre': 'copperslug:item/armas3d/' + cobre}},
             'perspectives': {'gui': {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'copperslug:item/arponera' + suf}}}}
        if n == 0:
            m['overrides'] = [{'predicate': {'copperslug:oxido': v}, 'model': 'copperslug:item/arponera_ox%d' % k}
                              for k, v in ((1, 0.25), (2, 0.5), (3, 0.75))]
        with open(os.path.join(MOD, 'arponera%s.json' % suf), 'w', encoding='utf-8') as f:
            json.dump(m, f, indent=1)
    with open(os.path.join(MOD, 'arpon_cobre.json'), 'w', encoding='utf-8') as f:
        json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': 'copperslug:item/arpon_cobre'}}, f, indent=1)


if __name__ == '__main__':
    for n, tonos in enumerate(cobres()):
        icono(tonos).save(os.path.join(TEX, 'arponera' + ('' if n == 0 else '_ox%d' % n) + '.png'))
    arpon().save(os.path.join(TEX, 'arpon_cobre.png'))
    textura_cuerda().save(os.path.join(TEX, 'armas3d', 'cuerda.png'))
    modelo_3d()
    modelos_objeto()
    print('arponera: texturas y modelos generados')

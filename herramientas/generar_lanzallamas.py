#!/usr/bin/env python3
"""Genera las texturas y los modelos del lanzallamas de cobre y su bidón de combustible.

  textures/item/lanzallamas.png (+ _ox1.._ox3)   el icono (16x16), con el cobre en sus cuatro fases de óxido
  textures/item/bidon_combustible.png
  models/item/armas3d/lanzallamas_3d.json         el cañón ancho de cobre, la boquilla con la llama piloto, el bidón de debajo y el agarre
  models/item/lanzallamas.json (+ _ox1.._ox3)     el modelo del objeto (3D en la mano, plano en el inventario)
  models/item/bidon_combustible.json

El cobre sale de la Derringer (lo que cambia entre sus texturas de óxido), así que se oxida como el resto. Es idempotente.
Uso: generar_lanzallamas.py [raíz del repositorio]
"""
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_tambor import caja  # noqa: E402
from generar_cerbatana import cobres  # noqa: E402

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
TEX = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/textures/item')
MOD = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item')
A3D = os.path.join(MOD, 'armas3d')

HIERRO = (113, 119, 126, 255)
HIERRO_CLARO = (175, 181, 187, 255)
NEGRO = (60, 64, 70, 255)
CUERO = (121, 85, 52, 255)
CUERO_OSC = (84, 58, 36, 255)
LLAMA = (255, 170, 40, 255)
LLAMA_CLARA = (255, 230, 120, 255)
ROJO = (176, 52, 40, 255)
ROJO_OSC = (118, 32, 26, 255)


def icono(tonos):
    oscuro, medio, claro = tonos
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    # el cañón, ancho (tres píxeles) en diagonal
    for i in range(10):
        x, y = 3 + i, 12 - i
        im.putpixel((x, y), claro)
        im.putpixel((x + 1, y), medio)
        im.putpixel((x + 1, y + 1), oscuro)
        im.putpixel((x, y + 1), medio)
    # el depósito debajo del cañón (rojo, con un aro de hierro)
    for (x, y) in ((4, 13), (5, 13), (4, 14), (5, 14), (6, 13), (6, 14)):
        im.putpixel((x, y), ROJO)
    for (x, y) in ((4, 14), (5, 14), (6, 14)):
        im.putpixel((x, y), ROJO_OSC)
    im.putpixel((5, 13), HIERRO_CLARO)
    # el agarre de cuero
    for (x, y) in ((3, 13), (2, 14)):
        im.putpixel((x, y), CUERO)
    # un anillo y la boca
    im.putpixel((8, 7), HIERRO_CLARO)
    im.putpixel((9, 7), HIERRO)
    im.putpixel((12, 3), NEGRO)
    # la llama del final
    for (x, y), c in (((13, 2), LLAMA), ((14, 1), LLAMA_CLARA), ((13, 1), LLAMA), ((14, 2), LLAMA)):
        im.putpixel((x, y), c)
    return im


def bidon():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y in range(3, 14):
        for x in range(5, 11):
            im.putpixel((x, y), ROJO if x < 9 else ROJO_OSC)
    for x in range(5, 11):
        im.putpixel((x, 3), HIERRO_CLARO)
        im.putpixel((x, 13), HIERRO)
        im.putpixel((x, 8), HIERRO)
    im.putpixel((7, 2), HIERRO)
    im.putpixel((8, 2), HIERRO)
    for (x, y) in ((7, 5), (8, 5), (7, 6), (8, 10), (7, 11)):
        im.putpixel((x, y), LLAMA)
    im.putpixel((7, 5), LLAMA_CLARA)
    return im


def modelo_3d():
    base = json.load(open(os.path.join(A3D, 'winchester_3d.json'), encoding='utf-8'))
    el = []
    cx, cy = 8.0, 9.6
    el.append(caja(cx - 1.0, cy - 1.0, 2.0, cx + 1.0, cy + 1.0, 12.5, 'cobre', 'lan_canon'))
    for z, n in ((4.5, 'a'), (9.0, 'b')):
        el.append(caja(cx - 1.2, cy - 1.2, z, cx + 1.2, cy + 1.2, z + 0.8, 'hierro', 'lan_anillo_' + n))
    # la boquilla y la llama piloto
    el.append(caja(cx - 0.7, cy - 0.7, 0.6, cx + 0.7, cy + 0.7, 2.0, 'hierro', 'lan_boquilla'))
    el.append(caja(cx - 0.35, cy - 0.35, 0.0, cx + 0.35, cy + 0.35, 0.6, 'brasa', 'lan_piloto'))
    # el bidón de debajo y su correa
    el.append(caja(cx - 1.1, 5.4, 6.0, cx + 1.1, 8.4, 11.5, 'tambor', 'lan_bidon'))
    el.append(caja(cx - 1.25, 5.25, 7.0, cx + 1.25, 8.55, 7.6, 'cuero', 'lan_correa_a'))
    el.append(caja(cx - 1.25, 5.25, 10.0, cx + 1.25, 8.55, 10.6, 'cuero', 'lan_correa_b'))
    # el agarre y la culata corta
    el.append(caja(cx - 0.6, 5.2, 12.0, cx + 0.6, 8.6, 13.4, 'cuero', 'lan_agarre'))
    el.append(caja(cx - 0.9, cy - 0.9, 12.5, cx + 0.9, cy + 0.9, 14.5, 'cuero', 'lan_culata'))
    base['elements'] = el
    base['textures']['particle'] = 'copperslug:item/lanzallamas'
    with open(os.path.join(A3D, 'lanzallamas_3d.json'), 'w', encoding='utf-8') as f:
        json.dump(base, f, separators=(',', ':'), ensure_ascii=False)
        f.write('\n')


def modelos_objeto():
    for n, suf, cobre in ((0, '', 'cobre_0'), (1, '_ox1', 'cobre_1'), (2, '_ox2', 'cobre_2'), (3, '_ox3', 'cobre_3')):
        m = {'loader': 'forge:separate_transforms', 'gui_light': 'front',
             'textures': {'particle': 'copperslug:item/lanzallamas' + suf},
             'base': {'parent': 'copperslug:item/armas3d/lanzallamas_3d', 'textures': {'cobre': 'copperslug:item/armas3d/' + cobre}},
             'perspectives': {'gui': {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'copperslug:item/lanzallamas' + suf}}}}
        if n == 0:
            m['overrides'] = [{'predicate': {'copperslug:oxido': v}, 'model': 'copperslug:item/lanzallamas_ox%d' % k}
                              for k, v in ((1, 0.25), (2, 0.5), (3, 0.75))]
        with open(os.path.join(MOD, 'lanzallamas%s.json' % suf), 'w', encoding='utf-8') as f:
            json.dump(m, f, indent=1)
    with open(os.path.join(MOD, 'bidon_combustible.json'), 'w', encoding='utf-8') as f:
        json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': 'copperslug:item/bidon_combustible'}}, f, indent=1)


if __name__ == '__main__':
    for n, tonos in enumerate(cobres()):
        icono(tonos).save(os.path.join(TEX, 'lanzallamas' + ('' if n == 0 else '_ox%d' % n) + '.png'))
    bidon().save(os.path.join(TEX, 'bidon_combustible.png'))
    modelo_3d()
    modelos_objeto()
    print('lanzallamas: texturas y modelos generados')

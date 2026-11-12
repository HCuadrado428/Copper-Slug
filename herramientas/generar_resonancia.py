#!/usr/bin/env python3
"""Genera las texturas y los modelos de la pistola de resonancia (la de la ciudad antigua).

  textures/item/resonancia.png (+ _ox1.._ox3)      el icono (16x16), con el cobre en sus cuatro fases de óxido
  textures/item/armas3d/eco.png                    el brillo turquesa de las bobinas y el cristal (16x16)
  models/item/armas3d/resonancia_3d.json           cañón corto de cobre con tres bobinas, el cristal de eco y la culata
  models/item/resonancia.json (+ _ox1.._ox3)       el modelo del objeto (3D en la mano, plano en el inventario)

El cobre sale de la Derringer (lo que cambia entre sus texturas de óxido), así que se oxida como el resto. Es idempotente.
Uso: generar_resonancia.py [raíz del repositorio]
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
NEGRO = (60, 64, 70, 255)
MADERA = (121, 85, 52, 255)
MADERA_OSC = (84, 58, 36, 255)
ECO = (60, 200, 200, 255)
ECO_CLARO = (170, 255, 245, 255)
ECO_OSC = (20, 90, 100, 255)


def icono(tonos):
    oscuro, medio, claro = tonos
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    # el cañón corto, en diagonal
    for i in range(7):
        x, y = 6 + i, 9 - i
        im.putpixel((x, y), claro)
        im.putpixel((x + 1, y), medio)
        im.putpixel((x, y + 1), medio)
        im.putpixel((x + 1, y + 1), oscuro)
    # tres bobinas turquesa
    for i in (1, 3, 5):
        x, y = 6 + i, 9 - i
        im.putpixel((x, y), ECO)
        im.putpixel((x + 1, y), ECO_CLARO)
        im.putpixel((x, y + 1), ECO_OSC)
    # el cuerpo y el cristal de eco
    for (x, y) in ((4, 10), (5, 10), (5, 11), (4, 11), (3, 11)):
        im.putpixel((x, y), medio)
    im.putpixel((5, 9), ECO_CLARO)
    im.putpixel((4, 9), ECO)
    im.putpixel((5, 8), ECO)
    # la empuñadura
    for (x, y) in ((3, 12), (3, 13), (2, 13), (4, 12)):
        im.putpixel((x, y), MADERA)
    im.putpixel((2, 14), MADERA_OSC)
    im.putpixel((3, 14), MADERA_OSC)
    im.putpixel((13, 2), NEGRO)
    return im


def textura_eco():
    im = Image.new('RGBA', (16, 16), ECO)
    for y in range(16):
        for x in range(16):
            if (x + y) % 5 == 0:
                im.putpixel((x, y), ECO_CLARO)
            elif (x * 3 + y) % 7 == 0:
                im.putpixel((x, y), ECO_OSC)
    return im


def modelo_3d():
    base = json.load(open(os.path.join(A3D, 'revolver_3d.json'), encoding='utf-8'))
    tex = json.load(open(os.path.join(A3D, 'derringer_3d_oculta.json'), encoding='utf-8'))['textures']
    tex['eco'] = 'copperslug:item/armas3d/eco'
    base['textures'] = tex
    el = []
    cx, cy = 8.0, 9.6
    el.append(caja(cx - 0.9, cy - 0.9, 1.5, cx + 0.9, cy + 0.9, 8.5, 'cobre', 'res_canon'))
    for z, n in ((2.5, 'a'), (4.6, 'b'), (6.7, 'c')):
        el.append(caja(cx - 1.2, cy - 1.2, z, cx + 1.2, cy + 1.2, z + 1.0, 'eco', 'res_bobina_' + n))
    el.append({'name': 'res_boca', 'from': [cx - 0.4, cy - 0.4, 1.46], 'to': [cx + 0.4, cy + 0.4, 1.5],
               'faces': {'north': {'uv': [15.0, 5.95, 15.5, 6.45], 'texture': '#negro'}}})
    el.append(caja(cx - 1.1, 7.0, 8.5, cx + 1.1, 10.8, 11.8, 'cobre', 'res_cuerpo'))
    el.append(caja(cx - 0.5, 10.8, 9.0, cx + 0.5, 12.0, 11.0, 'eco', 'res_cristal'))
    el.append(caja(cx - 0.6, 3.8, 10.0, cx + 0.6, 7.0, 11.8, 'madera', 'res_agarre'))
    el.append(caja(cx - 0.3, 6.6, 8.6, cx + 0.3, 7.0, 9.4, 'hierro', 'res_gatillo'))
    base['elements'] = el
    base['textures']['particle'] = 'copperslug:item/resonancia'
    with open(os.path.join(A3D, 'resonancia_3d.json'), 'w', encoding='utf-8') as f:
        json.dump(base, f, separators=(',', ':'), ensure_ascii=False)
        f.write('\n')


def modelos_objeto():
    for n, suf, cobre in ((0, '', 'cobre_0'), (1, '_ox1', 'cobre_1'), (2, '_ox2', 'cobre_2'), (3, '_ox3', 'cobre_3')):
        m = {'loader': 'forge:separate_transforms', 'gui_light': 'front',
             'textures': {'particle': 'copperslug:item/resonancia' + suf},
             'base': {'parent': 'copperslug:item/armas3d/resonancia_3d', 'textures': {'cobre': 'copperslug:item/armas3d/' + cobre}},
             'perspectives': {'gui': {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'copperslug:item/resonancia' + suf}}}}
        if n == 0:
            m['overrides'] = [{'predicate': {'copperslug:oxido': v}, 'model': 'copperslug:item/resonancia_ox%d' % k}
                              for k, v in ((1, 0.25), (2, 0.5), (3, 0.75))]
        with open(os.path.join(MOD, 'resonancia%s.json' % suf), 'w', encoding='utf-8') as f:
            json.dump(m, f, indent=1)


if __name__ == '__main__':
    for n, tonos in enumerate(cobres()):
        icono(tonos).save(os.path.join(TEX, 'resonancia' + ('' if n == 0 else '_ox%d' % n) + '.png'))
    textura_eco().save(os.path.join(TEX, 'armas3d', 'eco.png'))
    modelo_3d()
    modelos_objeto()
    print('resonancia: texturas y modelos generados')

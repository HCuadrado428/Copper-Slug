#!/usr/bin/env python3
"""Genera las texturas y los modelos de la cerbatana de cobre y sus tres dardos.

  textures/item/cerbatana.png (+ _ox1.._ox3)      el icono (16x16), con el cobre en sus cuatro fases de óxido
  textures/item/dardo_cerbatana.png, dardo_veneno.png, dardo_somnifero.png
  models/item/armas3d/cerbatana_3d.json           el tubo en 3D (cobre, dos anillos de hierro, el cuero del agarre y la boquilla)
  models/item/cerbatana.json (+ _ox1.._ox3)       el modelo del objeto (3D en la mano, plano en el inventario)
  models/item/dardo_*.json                        los modelos planos de los dardos

Los colores del cobre se sacan de la Derringer (lo que cambia entre sus texturas de óxido), así que la cerbatana
se oxida exactamente igual que el resto. Es idempotente. Uso: generar_cerbatana.py [raíz del repositorio]
"""
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_tambor import caja  # noqa: E402
from modelos_armas_nuevas import MODELOS, con_mano  # noqa: E402

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
TEX = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/textures/item')
MOD = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item')
A3D = os.path.join(MOD, 'armas3d')


def cobres():
    """Los tres tonos del cobre de la Derringer en cada fase: [fase][0 oscuro, 1 medio, 2 claro]."""
    base = Image.open(os.path.join(TEX, 'derringer.png')).convert('RGBA')
    fases = [base] + [Image.open(os.path.join(TEX, 'derringer_ox%d.png' % n)).convert('RGBA') for n in (1, 2, 3)]
    cambian = []
    for p in range(16 * 16):
        x, y = p % 16, p // 16
        if any(f.getpixel((x, y)) != base.getpixel((x, y)) for f in fases[1:]):
            c = base.getpixel((x, y))
            if c not in cambian:
                cambian.append(c)
    cambian.sort(key=lambda c: sum(c[:3]))
    # tres tonos: el más oscuro, uno medio y el más claro
    tonos = [cambian[0], cambian[len(cambian) // 2], cambian[-1]]
    out = []
    for f in fases:
        fila = []
        for t in tonos:
            for p in range(16 * 16):
                x, y = p % 16, p // 16
                if base.getpixel((x, y)) == t:
                    fila.append(f.getpixel((x, y)))
                    break
        out.append(fila)
    return out


HIERRO = (113, 119, 126, 255)
HIERRO_CLARO = (175, 181, 187, 255)
NEGRO = (60, 64, 70, 255)
CUERO = (121, 85, 52, 255)
CUERO_OSC = (84, 58, 36, 255)


def icono(tonos):
    oscuro, medio, claro = tonos
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    n = 12
    for i in range(n):
        x, y = 2 + i, 13 - i
        im.putpixel((x, y), claro)             # el lomo, arriba a la izquierda de la diagonal
        im.putpixel((x + 1, y), medio)
        if y + 1 < 16:
            im.putpixel((x, y + 1), oscuro if i % 2 else medio)   # la sombra de abajo
    # la boquilla (abajo a la izquierda): cuero oscuro
    for i in (0, 1):
        x, y = 2 + i, 13 - i
        im.putpixel((x, y), CUERO)
        im.putpixel((x + 1, y), CUERO_OSC)
        im.putpixel((x, y + 1), CUERO_OSC)
    # el agarre de cuero
    for i in (4, 5):
        x, y = 2 + i, 13 - i
        im.putpixel((x, y), CUERO)
        im.putpixel((x + 1, y), CUERO_OSC)
        im.putpixel((x, y + 1), CUERO_OSC)
    # dos anillos de hierro
    for i in (3, 8):
        x, y = 2 + i, 13 - i
        im.putpixel((x, y), HIERRO_CLARO)
        im.putpixel((x + 1, y), HIERRO)
        im.putpixel((x, y + 1), HIERRO)
    # la boca del tubo, oscura
    x, y = 2 + n - 1, 13 - (n - 1)
    im.putpixel((x + 1, y), NEGRO)
    return im


def dardo(punta, plumas, plumas2):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for i in range(9):
        im.putpixel((3 + i, 12 - i), CUERO)
        im.putpixel((4 + i, 12 - i), CUERO_OSC)
    im.putpixel((12, 3), punta[0])
    im.putpixel((13, 2), punta[1])
    im.putpixel((12, 2), punta[1])
    im.putpixel((13, 3), punta[0])
    # las plumas del final
    for (x, y), c in (((2, 13), plumas), ((3, 13), plumas2), ((2, 12), plumas2), ((4, 13), plumas), ((2, 11), plumas)):
        im.putpixel((x, y), c)
    return im


def modelo_plano(nombre, tex):
    with open(os.path.join(MOD, nombre + '.json'), 'w', encoding='utf-8') as f:
        json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': 'copperslug:item/' + tex}}, f, indent=1)


def tubo_3d():
    base = json.load(open(os.path.join(A3D, 'winchester_3d.json'), encoding='utf-8'))
    # el juego completo de materiales (el de la Derringer) más el brillo de eco y la cuerda
    base['textures'] = dict(json.load(open(os.path.join(A3D, 'derringer_3d_oculta.json'), encoding='utf-8'))['textures'])
    base['textures']['eco'] = 'copperslug:item/armas3d/eco'
    base['textures']['cuerda'] = 'copperslug:item/armas3d/cuerda'
    base['elements'] = MODELOS['cerbatana']()
    con_mano(base, 'cerbatana', json.load(open(os.path.join(A3D, 'revolver_3d.json'), encoding='utf-8')))
    base['textures']['particle'] = 'copperslug:item/cerbatana'
    with open(os.path.join(A3D, 'cerbatana_3d.json'), 'w', encoding='utf-8') as f:
        json.dump(base, f, separators=(',', ':'), ensure_ascii=False)
        f.write('\n')

def modelos_objeto():
    for n, suf, cobre in ((0, '', 'cobre_0'), (1, '_ox1', 'cobre_1'), (2, '_ox2', 'cobre_2'), (3, '_ox3', 'cobre_3')):
        m = {'loader': 'forge:separate_transforms', 'gui_light': 'front',
             'textures': {'particle': 'copperslug:item/cerbatana' + suf},
             'base': {'parent': 'copperslug:item/armas3d/cerbatana_3d', 'textures': {'cobre': 'copperslug:item/armas3d/' + cobre}},
             'perspectives': {'gui': {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'copperslug:item/cerbatana' + suf}}}}
        if n == 0:
            m['overrides'] = [{'predicate': {'copperslug:oxido': v}, 'model': 'copperslug:item/cerbatana_ox%d' % k}
                              for k, v in ((1, 0.25), (2, 0.5), (3, 0.75))]
        with open(os.path.join(MOD, 'cerbatana%s.json' % suf), 'w', encoding='utf-8') as f:
            json.dump(m, f, indent=1)


if __name__ == '__main__':
    fases = cobres()
    for n, tonos in enumerate(fases):
        icono(tonos).save(os.path.join(TEX, 'cerbatana' + ('' if n == 0 else '_ox%d' % n) + '.png'))
    dardo(((150, 154, 160, 255), (200, 204, 210, 255)), (225, 225, 225, 255), (180, 180, 180, 255)).save(os.path.join(TEX, 'dardo_cerbatana.png'))
    dardo(((70, 170, 70, 255), (120, 220, 90, 255)), (90, 170, 80, 255), (60, 120, 55, 255)).save(os.path.join(TEX, 'dardo_veneno.png'))
    dardo(((120, 90, 190, 255), (170, 140, 230, 255)), (150, 120, 210, 255), (100, 75, 160, 255)).save(os.path.join(TEX, 'dardo_somnifero.png'))
    for d in ('dardo_cerbatana', 'dardo_veneno', 'dardo_somnifero'):
        modelo_plano(d, d)
    tubo_3d()
    modelos_objeto()
    print('cerbatana: texturas y modelos generados')

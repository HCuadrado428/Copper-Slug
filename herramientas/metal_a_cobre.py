#!/usr/bin/env python3
"""Pasa a cobre las piezas grandes de metal gris de los modelos 3D de las armas (la gracia del mod es que todo es de
cobre y se oxida: el acero y el hierro grises no se oxidaban). Las piezas pequeñas (pasadores, gatillos, miras) se
quedan en hierro como detalle. La hoja de la bayoneta (textura «bayoneta») no se toca: es la de la espada.

Una pieza cuenta como grande si su volumen pasa de UMBRAL (píxeles cúbicos) y su textura dominante es hierro o acero.
Es idempotente. Uso: metal_a_cobre.py [raíz del repositorio]
"""
import collections
import glob
import json
import os
import sys

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
A3D = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item/armas3d')
ARMAS = ['winchester_3d*.json', 'thompson_3d*.json', 'escopeta_3d*.json', 'rifle_3d*.json', 'mosquete_3d*.json', 'canon_mano_3d*.json']
UMBRAL = 1.5
GRISES = {'#hierro', '#acero'}


def main():
    total = 0
    for patron in ARMAS:
        for ruta in sorted(glob.glob(os.path.join(A3D, patron))):
            m = json.load(open(ruta, encoding='utf-8'))
            cambiadas = 0
            for e in m['elements']:
                vol = (e['to'][0] - e['from'][0]) * (e['to'][1] - e['from'][1]) * (e['to'][2] - e['from'][2])
                dom = collections.Counter(f['texture'] for f in e['faces'].values()).most_common(1)[0][0]
                # las aletas del cañón de la Thompson son de acero y muy pequeñas: todas a cobre
                aleta = 'thompson' in os.path.basename(ruta) and dom == '#acero'
                if dom in GRISES and (vol >= UMBRAL or aleta):
                    for f in e['faces'].values():
                        if f['texture'] in GRISES:
                            f['texture'] = '#cobre'
                    cambiadas += 1
            if cambiadas:
                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump(m, f, indent=1, ensure_ascii=False)
                    f.write('\n')
                print(os.path.basename(ruta), cambiadas, 'piezas a cobre')
                total += cambiadas
    print('total', total)


def tambor_de_cobre():
    """El cargador de tambor de la Thompson tiene una textura gris (g_tambor): se tiñe de cobre conservando sus huecos."""
    from PIL import Image
    base = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/textures/item/armas3d')
    origen, destino = os.path.join(base, 'g_tambor.png'), os.path.join(base, 'g_tambor_cobre.png')
    im = Image.open(origen).convert('RGBA')
    out = Image.new('RGBA', im.size)
    oscuro, claro = (58, 30, 22), (236, 132, 96)
    for x in range(im.width):
        for y in range(im.height):
            r, g, b, a = im.getpixel((x, y))
            k = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            out.putpixel((x, y), tuple(int(oscuro[i] + (claro[i] - oscuro[i]) * k) for i in range(3)) + (a,))
    out.save(destino)
    n = 0
    for ruta in sorted(glob.glob(os.path.join(A3D, 'thompson_3d*.json'))):
        m = json.load(open(ruta, encoding='utf-8'))
        if m['textures'].get('tambor', '').endswith('g_tambor'):
            m['textures']['tambor'] = 'copperslug:item/armas3d/g_tambor_cobre'
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(m, f, separators=(',', ':'), ensure_ascii=False)
                f.write('\n')
            n += 1
    print('cargador de la Thompson en cobre:', n, 'modelos')


main()
tambor_de_cobre()

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


main()

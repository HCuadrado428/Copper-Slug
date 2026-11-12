#!/usr/bin/env python3
"""Redondea los cañones y tubos cuadrados de los modelos 3D de las armas largas: cada pieza larga y fina de cobre pasa de
una caja a un prisma octogonal (cuatro cajas, dos giradas 45°, como el cañón del revólver), con la boca marcada.

Una pieza se redondea si no está girada, mide al menos 5 de largo (eje z), su sección no pasa de 2 y es casi cuadrada
(proporción entre 0,6 y 1,7), y su textura dominante es de cobre. La altura de arriba no cambia (el octógono tiene el
mismo ancho entre caras que la caja), así que no se mueven las miras. Es idempotente: lo generado lleva el nombre
«redondo_» y no se vuelve a tocar. Uso: redondear_canones.py [raíz del repositorio]
"""
import collections
import glob
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_tambor import caja  # noqa: E402

# OBSOLETO: desde el estilo Minecraft los cañones son cuadrados (herramientas/canones_cuadrados.py deshace esto).
if '--forzar' not in sys.argv:
    sys.exit('redondear_canones.py está obsoleto: los cañones son cuadrados (estilo Minecraft). Usa --forzar si de verdad lo quieres.')
sys.argv = [a for a in sys.argv if a != '--forzar']
RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
A3D = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item/armas3d')
ARMAS = ['winchester_3d*.json', 'thompson_3d*.json', 'escopeta_3d*.json', 'rifle_3d*.json', 'mosquete_3d*.json', 'canon_mano_3d*.json']


def candidato(e):
    if 'rotation' in e or str(e.get('name', '')).startswith('redondo_'):
        return False
    w, h, l = e['to'][0] - e['from'][0], e['to'][1] - e['from'][1], e['to'][2] - e['from'][2]
    # solo piezas casi cuadradas: si no, el octógono las dejaba más finas por un lado (palancas, bandas)
    if l < 5 or max(w, h) > 2.0 or min(w, h) < 0.6 or not 0.85 <= w / h <= 1.18:
        return False
    tex = collections.Counter(f['texture'] for f in e['faces'].values()).most_common(1)[0][0]
    return tex == '#cobre'


def octogono(e, n):
    x1, y1, z1 = e['from']
    x2, y2, z2 = e['to']
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    a = min(x2 - x1, y2 - y1) / 2
    s = 2 * a * math.tan(math.radians(22.5))
    out = []
    for i, (ang, dx, dy) in enumerate(((0, a, s / 2), (0, s / 2, a), (45, a, s / 2), (-45, a, s / 2))):
        out.append(caja(cx - dx, cy - dy, z1 + 0.004 * i, cx + dx, cy + dy, z2 - 0.004 * i, 'cobre', 'redondo_%d_%d' % (n, i),
                        rot=((cx, cy, 0), 'z', ang) if ang else None))
    # la boca: lo que tenía la cara de delante, en pequeño
    norte = e['faces'].get('north')
    if norte and norte['texture'] != '#cobre':
        out.append({'name': 'redondo_%d_boca' % n, 'from': [round(cx - a * 0.55, 3), round(cy - a * 0.55, 3), round(z1 - 0.03, 3)],
                    'to': [round(cx + a * 0.55, 3), round(cy + a * 0.55, 3), round(z1 - 0.01, 3)],
                    'faces': {'north': dict(norte)}})
    return out


def main():
    total = 0
    for patron in ARMAS:
        for ruta in sorted(glob.glob(os.path.join(A3D, patron))):
            m = json.load(open(ruta, encoding='utf-8'))
            nuevos, n = [], 0
            for e in m['elements']:
                if candidato(e):
                    nuevos += octogono(e, n)
                    n += 1
                else:
                    nuevos.append(e)
            if n:
                m['elements'] = nuevos
                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump(m, f, separators=(',', ':'), ensure_ascii=False)
                    f.write('\n')
                print(os.path.basename(ruta), n, 'piezas redondeadas')
                total += n
    print('total', total)


main()

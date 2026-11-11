#!/usr/bin/env python3
"""Rehace el cañón de la Derringer en sus cuatro modelos base (cerrada/abierta, a la vista/oculta).

Antes era un bloque gris de acero (que además no se oxidaba con el resto del arma): ahora son DOS cañones de cobre
apilados (como una Derringer sobre-bajo de verdad), cada uno de cantos achaflanados (dos cajas cruzadas), con una
costilla entre ellos, las dos bocas y los pasadores de la bisagra en los costados del armazón. Como son de cobre, se
oxidan con el arma (los modelos «_ox1..3» cambian la textura «cobre»).

En el modelo «abierta» el conjunto de los cañones gira 45° sobre el eje de la bisagra, como el original.
Es idempotente. Uso: generar_derringer.py [raíz del repositorio]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_tambor import caja  # noqa: E402

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
A3D = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item/armas3d')
MODELOS = ['derringer_3d', 'derringer_3d_oculta', 'derringer_3d_abierta', 'derringer_3d_abierta_oculta']
CX = 8.0
Z1, Z2 = 1.0, 8.0
SUP, INF = 10.35, 9.0      # el centro de cada cañón (altura)
UV_NEGRO = [15.0, 5.95, 15.5, 6.45]


def canon(cy, nombre, rot):
    """Un cañón de cantos achaflanados: una caja ancha y otra alta (la unión es un cuadrado con las esquinas cortadas)."""
    return [caja(CX - 0.62, cy - 0.46, Z1, CX + 0.62, cy + 0.46, Z2, 'cobre', nombre + '_a', rot=rot),
            caja(CX - 0.46, cy - 0.62, Z1 + 0.004, CX + 0.46, cy + 0.62, Z2 - 0.004, 'cobre', nombre + '_b', rot=rot)]


def nuevos(rot):
    el = []
    el += canon(SUP, 'der_canon_sup', rot)
    el += canon(INF, 'der_canon_inf', rot)
    # la costilla entre los dos cañones
    el.append(caja(CX - 0.55, INF + 0.55, Z1 + 0.3, CX + 0.55, SUP - 0.55, Z2 - 0.1, 'cobre', 'der_costilla', rot=rot))
    # las bocas: un agujero oscuro en cada cañón, y un aro de hierro alrededor del de arriba y del de abajo
    for cy, n in ((SUP, 'sup'), (INF, 'inf')):
        el.append({'name': 'der_aro_' + n, 'from': [CX - 0.5, cy - 0.5, Z1 - 0.02], 'to': [CX + 0.5, cy + 0.5, Z1],
                   'faces': {'north': {'uv': [2, 2, 3.5, 3.5], 'texture': '#hierro'}}})
        el.append({'name': 'der_boca_' + n, 'from': [CX - 0.32, cy - 0.32, Z1 - 0.04], 'to': [CX + 0.32, cy + 0.32, Z1 - 0.02],
                   'faces': {'north': {'uv': list(UV_NEGRO), 'texture': '#negro'}}})
        if rot:
            for e in el[-2:]:
                e['rotation'] = {'origin': list(rot[0]), 'axis': rot[1], 'angle': rot[2]}
    # los pasadores de la bisagra, a los dos lados del armazón (no giran)
    for x1, x2 in ((6.96, 7.0), (9.0, 9.04)):
        el.append(caja(x1, 8.05, 8.15, x2, 8.6, 8.7, 'hierro', 'der_pasador', caras=('east', 'west')))
    return el


def procesar(nombre):
    ruta = os.path.join(A3D, nombre + '.json')
    m = json.load(open(ruta, encoding='utf-8'))
    el = m['elements']
    # la rotación (solo en «abierta»): la del cañón original o la de lo generado antes
    rot = None
    for e in el:
        if (e['from'] == [7.25, 8.0, 1.0] or str(e.get('name', '')).startswith('der_canon_sup_a')) and 'rotation' in e:
            r = e['rotation']
            rot = (tuple(r['origin']), r['axis'], r['angle'])
    # fuera el bloque de acero original (y lo generado antes)
    el = [e for e in el if not (e['from'] == [7.25, 8.0, 1.0] and e['to'] == [8.75, 11.0, 8.0]) and not str(e.get('name', '')).startswith('der_')]
    # la costilla de mira de arriba, que era de acero gris, también de cobre
    for e in el:
        if e['from'] == [7.75, 11.0, 1.2]:
            for c in e['faces'].values():
                c['texture'] = '#cobre'
    m['elements'] = nuevos(rot) + el
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(m, f, separators=(',', ':'), ensure_ascii=False)
        f.write('\n')
    return len(m['elements'])


if __name__ == '__main__':
    for n in MODELOS:
        print(n, procesar(n), 'elementos')

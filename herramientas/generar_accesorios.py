#!/usr/bin/env python3
"""Genera las piezas de cobre que se ven en las armas con ciertos encantamientos (el accesorio ES el encantamiento).

Cada pieza es un modelo con la geometría ya colocada en las coordenadas del modelo del arma; el cliente la dibuja encima del arma
(client/armasfuego/comun/AccesoriosVisibles.java, enganchado en ItemRenderer.render). Hay una por nivel de óxido (cobre_0..3).
Piezas: silenciador (rifle, Derringer, Winchester, Thompson), compensador (Thompson), cañón largo (revólver), estrangulador
(escopeta), mira de cobre (mosquete), ánima rayada (cañón de mano) y depósito largo (Winchester).
Uso: generar_accesorios.py [raíz del repositorio]   (idempotente)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_tambor import caja, octogono  # noqa: E402

RAIZ = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else '.'
A3D = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item/armas3d')
CX = 8.0


def boca(cy, z, r=0.35, nombre='boca'):
    """El agujero oscuro de la boca (cara norte, mirando al frente)."""
    return {'name': nombre, 'from': [CX - r, cy - r, z - 0.02], 'to': [CX + r, cy + r, z],
            'faces': {'north': {'uv': [15.0, 5.95, 15.5, 6.45], 'texture': '#negro'}}}


def silenciador(cy, a, z1, z2):
    el = octogono(cy, a, z1, z2, 'cobre', 'sil')
    el += octogono(cy, a + 0.05, z1, z1 + 0.5, 'cobre', 'sil_tapa')
    el += octogono(cy, a + 0.05, z2 - 0.8, z2 - 0.4, 'cobre', 'sil_aro')
    el.append(boca(cy, z1 - 0.0, 0.35, 'sil_boca'))
    return el


def compensador_thompson():
    cy = 9.5
    el = octogono(cy, 0.78, -13.9, -11.7, 'cobre', 'comp')
    for z in (-13.4, -12.8, -12.2):                    # las ranuras: arriba y a los lados
        el.append(caja(CX - 0.28, cy + 0.74, z, CX + 0.28, cy + 0.8, z + 0.35, 'negro', 'comp_ranura_s', caras=('up',)))
        el.append(caja(CX + 0.74, cy - 0.28, z, CX + 0.8, cy + 0.28, z + 0.35, 'negro', 'comp_ranura_d', caras=('east',)))
        el.append(caja(CX - 0.8, cy - 0.28, z, CX - 0.74, cy + 0.28, z + 0.35, 'negro', 'comp_ranura_i', caras=('west',)))
    el.append(boca(cy, -13.9, 0.3, 'comp_boca'))
    return el


def canon_largo():
    cy = 9.9
    el = octogono(cy, 0.72, -1.4, 1.6, 'cobre', 'cl')
    el += octogono(cy, 0.8, -1.4, -0.9, 'cobre', 'cl_aro')
    el.append(boca(cy, -1.4, 0.32, 'cl_boca'))
    return el


def estrangulador():
    cy = 10.0
    el = octogono(cy, 1.18, -12.4, -9.8, 'cobre', 'est')
    el += octogono(cy, 0.95, -13.4, -12.4, 'cobre', 'est_cono')
    el.append(boca(cy, -13.4, 0.6, 'est_boca'))
    return el


def mira_mosquete():
    el = octogono(10.2, 0.5, -9.6, -9.1, 'cobre', 'mira_base')
    el.append(caja(7.88, 10.55, -9.55, 8.12, 11.4, -9.2, 'cobre', 'mira_punto'))
    el.append(caja(7.8, 11.3, -9.6, 8.2, 11.5, -9.15, 'cobre', 'mira_cima'))
    return el


def anima_canon():
    el = []
    for z in (-7.5, -4.5, -1.5):
        el += octogono(9.5, 1.2, z, z + 0.5, 'cobre', 'anima_%d' % int(-z * 10))
    return el


def deposito_winchester():
    cy = 8.625
    el = octogono(cy, 0.62, -13.4, -12.0, 'cobre', 'dep_punta')
    el.append(boca(cy, -13.4, 0.3, 'dep_boca'))
    for z in (-8.2, -4.6, -1.0):
        el += octogono(cy, 0.78, z, z + 0.5, 'cobre', 'dep_collar_%d' % int(-z * 10))
    return el


PIEZAS = {
    'silenciador_rifle': lambda: silenciador(9.5, 0.95, -14.6, -9.4),
    'silenciador_derringer': lambda: silenciador(10.35, 0.95, -3.4, 1.5),
    'silenciador_winchester': lambda: silenciador(10.0, 0.9, -15.9, -11.5),
    'silenciador_thompson': lambda: silenciador(9.5, 0.9, -15.9, -11.2),
    'compensador_thompson': compensador_thompson,
    'canon_largo_revolver': canon_largo,
    'estrangulador_escopeta': estrangulador,
    'mira_mosquete': mira_mosquete,
    'anima_canon': anima_canon,
    'deposito_winchester': deposito_winchester,
}

for nombre, f in PIEZAS.items():
    for ox in range(4):
        m = {'textures': {'cobre': 'copperslug:item/armas3d/cobre_%d' % ox, 'negro': 'copperslug:item/armas3d/negro',
                          'particle': 'copperslug:item/armas3d/cobre_%d' % ox},
             'elements': f()}
        with open(os.path.join(A3D, 'acc_%s_%d.json' % (nombre, ox)), 'w', encoding='utf-8') as fh:
            json.dump(m, fh, separators=(',', ':'), ensure_ascii=False)
            fh.write('\n')
print(len(PIEZAS), 'piezas x 4 óxidos')

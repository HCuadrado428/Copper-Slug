#!/usr/bin/env python3
"""Genera los modelos del tambor del revólver con sus recámaras en 3D.

El cubo del tambor (3x3x3 px) enseña por detrás seis agujeros (un borde de hierro y el fondo negro) y, en las
recámaras cargadas, el culote de latón de la bala con su pistón. La pieza trasera del armazón se parte en dos tiras
(arriba y abajo) para que la cara de atrás del tambor se vea (en primera persona apuntando y desde atrás).

Un modelo no puede girar con el tambor, así que enseña CUÁNTAS balas hay (las primeras recámaras, en orden), no en
qué recámara están. El número lo da la propiedad de objeto «copperslug:cargadas» (0 a 6), que elige entre:
  armas3d/revolver_3d.json (0 balas) y armas3d/revolver_3d_n1..n6.json  (los modelos del arma),
  revolver_cargado_<óxido 0..3>_<n 1..6>.json                          (los de cada nivel de óxido con n balas).
El modelo del tambor abierto (recarga) no se toca. Todas las texturas siguen siendo de 16x16.

Es idempotente: se puede volver a ejecutar (quita lo que generó antes). Uso: generar_tambor.py [raíz del repositorio]
"""
import copy
import json
import math
import os
import sys

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
M = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item')
A3D = os.path.join(M, 'armas3d')
GEN = 'tambor_gen'

# (óxido, modelo del objeto sin balas): el cobre nuevo, expuesto, erosionado y oxidado
NIVELES = [(0, 'revolver', None), (1, 'revolver_expuesto', 0.25), (2, 'revolver_erosionado', 0.5), (3, 'revolver_oxidado', 0.75)]

CENTRO = (8.0, 9.0)   # el centro de la cara trasera del tambor (x 6.5..9.5, y 7.5..10.5)
RADIO = 0.95
Z = 11.0              # la cara de atrás del tambor
UV_HIERRO = [2, 2, 3.5, 3.5]
UV_NEGRO = [15.0, 5.95, 15.5, 6.45]
UV_LATON = [4.2, 1.2, 4.8, 1.8]    # el píxel dorado de tambor_frente_*
UV_PISTON = [2.2, 2.2, 2.8, 2.8]   # el gris del centro de tambor_frente_*


def cargar(ruta):
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)


def guardar(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=1, ensure_ascii=False)
        f.write('\n')


def recamara(k, cargada):
    """Los elementos de la recámara k (0 arriba, en el sentido del reloj visto desde atrás)."""
    a = math.radians(60 * k)
    cx, cy = CENTRO[0] + RADIO * math.sin(a), CENTRO[1] + RADIO * math.cos(a)
    cx, cy = round(cx, 3), round(cy, 3)
    e = [{'name': GEN + '_borde', 'from': [round(cx - 0.45, 3), round(cy - 0.45, 3), Z], 'to': [round(cx + 0.45, 3), round(cy + 0.45, 3), Z + 0.02],
          'faces': {'south': {'uv': UV_HIERRO, 'texture': '#hierro'}}}]
    if not cargada:
        e.append({'name': GEN + '_agujero', 'from': [round(cx - 0.35, 3), round(cy - 0.35, 3), Z + 0.02], 'to': [round(cx + 0.35, 3), round(cy + 0.35, 3), Z + 0.04],
                  'faces': {'south': {'uv': UV_NEGRO, 'texture': '#negro'}}})
        return e
    lado = {'uv': UV_LATON, 'texture': '#tambor'}
    e.append({'name': GEN + '_culote', 'from': [round(cx - 0.3, 3), round(cy - 0.3, 3), Z], 'to': [round(cx + 0.3, 3), round(cy + 0.3, 3), Z + 0.3],
              'faces': {'south': dict(lado), 'east': dict(lado), 'west': dict(lado), 'up': dict(lado), 'down': dict(lado)}})
    e.append({'name': GEN + '_piston', 'from': [round(cx - 0.12, 3), round(cy - 0.12, 3), Z + 0.3], 'to': [round(cx + 0.12, 3), round(cy + 0.12, 3), Z + 0.32],
              'faces': {'south': {'uv': UV_PISTON, 'texture': '#tambor'}}})
    return e


def modelo(base, balas):
    m = copy.deepcopy(base)
    elementos = []
    placa = None
    for e in m['elements']:
        if str(e.get('name', '')).startswith(GEN):
            continue
        if e['from'] == [6.9, 7, 11] and e['to'] == [9.1, 11.1, 12.5]:
            placa = e
            continue
        elementos.append(e)
    if placa is None:
        raise SystemExit('no encuentro la pieza trasera original: el modelo base tiene que ser el original (git checkout)')
    # la pieza trasera, partida en dos tiras: la cara de atrás del tambor (y 7.5..10.5) queda a la vista
    for nombre, y0, y1 in (('arriba', 10.5, 11.1), ('abajo', 7.0, 7.5)):
        t = copy.deepcopy(placa)
        t['name'] = GEN + '_placa_' + nombre
        t['from'] = [6.9, y0, 11]
        t['to'] = [9.1, y1, 12.5]
        elementos.append(t)
    for k in range(6):
        elementos.extend(recamara(k, k < balas))
    m['elements'] = elementos
    return m


def main():
    ruta_base = os.path.join(A3D, 'revolver_3d.json')
    base = cargar(ruta_base)
    # el modelo base tiene que ser el original (con la pieza trasera entera) o uno generado antes: si ya está generado,
    # se reconstruye la pieza entera para partirla de nuevo
    if not any(e['from'] == [6.9, 7, 11] and e['to'] == [9.1, 11.1, 12.5] for e in base['elements']):
        arriba = next(e for e in base['elements'] if e.get('name') == GEN + '_placa_arriba')
        entera = copy.deepcopy(arriba)
        entera.pop('name')
        entera['from'] = [6.9, 7, 11]
        entera['to'] = [9.1, 11.1, 12.5]
        base['elements'] = [e for e in base['elements'] if not str(e.get('name', '')).startswith(GEN)] + [entera]
    for n in range(0, 7):
        nombre = 'revolver_3d.json' if n == 0 else 'revolver_3d_n%d.json' % n
        guardar(os.path.join(A3D, nombre), modelo(base, n))
    # los modelos del objeto con n balas, uno por nivel de óxido
    for ox, nombre, _ in NIVELES:
        obj = cargar(os.path.join(M, nombre + '.json'))
        obj.pop('overrides', None)
        for n in range(1, 7):
            o = copy.deepcopy(obj)
            o['base']['parent'] = 'copperslug:item/armas3d/revolver_3d_n%d' % n
            guardar(os.path.join(M, 'revolver_cargado_%d_%d.json' % (ox, n)), o)
    # los overrides del revólver: más abajo = más prioridad (cargadas, luego óxido, luego el tambor abierto)
    principal = cargar(os.path.join(M, 'revolver.json'))
    abiertos = [o for o in principal.get('overrides', []) if 'copperslug:abierto' in o['predicate']]
    nuevos = []
    for ox, nombre, umbral in NIVELES:
        if umbral is not None:
            nuevos.append({'predicate': {'copperslug:oxido': umbral}, 'model': 'copperslug:item/' + nombre})
        for n in range(1, 7):
            p = {'copperslug:cargadas': n}
            if umbral is not None:
                p = {'copperslug:oxido': umbral, 'copperslug:cargadas': n}
            nuevos.append({'predicate': p, 'model': 'copperslug:item/revolver_cargado_%d_%d' % (ox, n)})
    principal['overrides'] = nuevos + abiertos
    guardar(os.path.join(M, 'revolver.json'), principal)
    print('modelos: revolver_3d + 6, revolver_cargado_*: 24, overrides:', len(principal['overrides']))


main()

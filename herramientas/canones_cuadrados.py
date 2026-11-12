#!/usr/bin/env python3
"""Cambia los prismas octogonales de los modelos (cuatro cajas: dos rectas y dos giradas 45°) por una sola caja cuadrada.

Los octógonos hacían que los cañones parecieran tubos redondeados de otro juego; en Minecraft los cañones, mangos y
varillas son cuadrados (el tridente, el catalejo, la ballesta). Además son tres elementos menos por cañón y desaparecen
las caras que se pisaban.

Busca en cada modelo los grupos <nombre>_0.._3 en los que _0 y _1 no están girados y _2 y _3 lo están ±45° (lo que dejan
generar_tambor.octogono y modelos_armas_nuevas.octogono_x). La caja nueva es la unión de _0 y _1. Las caras conservan su
textura; si su UV era la proyección de la caja (lo normal), se recalcula para la caja nueva, y si no (las UV fijas de
tex_lado) se deja como estaba. De paso, las piezas de menos de 0,25 px de grueso se ensanchan hasta 0,25.

Uso: herramientas/canones_cuadrados.py [modelos.json ...]   (sin argumentos: todos los de assets/copperslug/models/item)
"""
import glob
import json
import os
import re
import sys

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'common', 'src', 'main', 'resources', 'assets',
                   'copperslug', 'models', 'item')


def proyeccion(cara, f, t):
    x1, y1, z1 = f
    x2, y2, z2 = t
    if cara in ('north', 'south'):
        return [x1, 16 - y2, x2, 16 - y1]
    if cara in ('east', 'west'):
        return [z1, 16 - y2, z2, 16 - y1]
    return [x1, z1, x2, z2]


def r3(v):
    return round(v, 3)


def igual(a, b, tol=0.02):
    return a is not None and len(a) == 4 and all(abs(p - q) <= tol for p, q in zip(a, b))


def cuadrar(elementos):
    por_nombre = {}
    for i, e in enumerate(elementos):
        n = e.get('name')
        if n:
            por_nombre.setdefault(n, i)
    quitar = set()
    nuevos = {}
    for n, i in por_nombre.items():
        m = re.match(r'^(.*)_0$', n)
        if not m:
            continue
        base = m.group(1)
        idx = [por_nombre.get('%s_%d' % (base, k)) for k in range(4)]
        if None in idx or len(set(idx)) != 4:
            continue
        e0, e1, e2, e3 = (elementos[k] for k in idx)
        if 'rotation' in e0 or 'rotation' in e1:
            continue
        if not all('rotation' in e and abs(e['rotation'].get('angle', 0)) == 45 for e in (e2, e3)):
            continue
        f = [r3(min(e0['from'][k], e1['from'][k])) for k in range(3)]
        t = [r3(max(e0['to'][k], e1['to'][k])) for k in range(3)]
        caras = {}
        for cara, d in e0.get('faces', {}).items():
            d = dict(d)
            if igual(d.get('uv'), proyeccion(cara, e0['from'], e0['to'])):
                d['uv'] = [r3(v) for v in proyeccion(cara, f, t)]
            caras[cara] = d
        nuevo = {'name': base, 'from': f, 'to': t, 'faces': caras}
        nuevos[idx[0]] = nuevo
        quitar.update(idx[1:])
    out = []
    for i, e in enumerate(elementos):
        if i in quitar:
            continue
        out.append(nuevos.get(i, e))
    return out, len(nuevos)


MINIMO = 0.25


def engrosar(elementos):
    """Las piezas de menos de 0,25 px de grueso (de lejos parpadean) se ensanchan hasta 0,25 desde su centro."""
    n = 0
    for e in elementos:
        if len(e.get('faces', {})) < 2:
            continue
        f, t = list(e['from']), list(e['to'])
        cambio = False
        for k in range(3):
            if t[k] - f[k] < MINIMO:
                c = (f[k] + t[k]) / 2
                # sin salirse de -16..32 (Minecraft no carga el modelo si una coordenada se pasa)
                c = min(max(c, -16 + MINIMO / 2), 32 - MINIMO / 2)
                f[k], t[k] = r3(c - MINIMO / 2), r3(c + MINIMO / 2)
                cambio = True
        if not cambio:
            continue
        for cara, d in e['faces'].items():
            if igual(d.get('uv'), proyeccion(cara, e['from'], e['to'])):
                d['uv'] = [r3(v) for v in proyeccion(cara, f, t)]
        e['from'], e['to'] = f, t
        n += 1
    return n


def procesar(ruta):
    with open(ruta) as fh:
        texto = fh.read()
    m = json.loads(texto)
    if 'elements' not in m:
        return 0
    n = 0
    # el tambor del revólver sigue octogonal: gira de 60 en 60 grados y una caja cuadrada se vería torcida
    if not re.search(r'revolver_cilindro_\d\.json$', ruta):
        m['elements'], n = cuadrar(m['elements'])
    n += engrosar(m['elements'])
    if n:
        with open(ruta, 'w') as fh:
            json.dump(m, fh, ensure_ascii=False, separators=(',', ':'))
    return n


def main(args):
    rutas = args or sorted(glob.glob(os.path.join(DIR, '**', '*.json'), recursive=True))
    total = 0
    for r in rutas:
        n = procesar(r)
        if n:
            print('%s: %d piezas cuadradas o engrosadas' % (os.path.relpath(r), n))
        total += n
    print('total: %d' % total)


if __name__ == '__main__':
    main(sys.argv[1:])

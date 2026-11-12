#!/usr/bin/env python3
"""Versiones «más Minecraft» de los modelos 3D de las armas: menos polígonos y piezas de píxeles enteros.

Pasa cada modelo a una rejilla (1 px o 0,5 px), pinta cada celda con el material de la pieza que la ocupa (las piezas
pequeñas, como miras y bandas, encima de las grandes) y junta las celdas iguales en cajas lo más grandes posible. Las
caras que quedan tapadas por otra celda no se dibujan. La posición y el tamaño del arma no cambian, así que los
`display`, la mano en primera persona y los pivotes del código (tambor del revólver, Gatling) siguen valiendo.

Las piezas finas se redondean a una celda entera (un cañón de 0,6 px pasa a 1 px) y las giradas se muestrean por el
centro de cada celda. Las calcomanías de una sola cara (la boca negra, el percutor) se pintan sobre la celda que tocan.

Uso: herramientas/voxelizar_armas.py --rejilla 1 --salida DIR [modelos.json ...]
     (sin modelos: todos los de models/item/armas3d)
"""
import argparse
import collections
import glob
import json
import math
import os

import numpy as np

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'common', 'src', 'main', 'resources', 'assets',
                   'copperslug', 'models', 'item', 'armas3d')
CARAS = ('north', 'south', 'east', 'west', 'up', 'down')
NORMAL = {'north': (2, -1), 'south': (2, 1), 'west': (0, -1), 'east': (0, 1), 'down': (1, -1), 'up': (1, 1)}


def rot(eje, ang):
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    return {'x': np.array([[1, 0, 0], [0, c, -s], [0, s, c]]),
            'y': np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]),
            'z': np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])}[eje]


def textura_principal(e):
    c = collections.Counter(f['texture'] for f in e.get('faces', {}).values())
    return c.most_common(1)[0][0] if c else None


def voxelizar(m, g):
    els = m.get('elements', [])
    if not els:
        return None
    O = -16.0
    N = int(round(48 / g))
    grid = np.full((N, N, N), -1, dtype=np.int32)  # índice de material
    mats = []

    def mi(t):
        if t not in mats:
            mats.append(t)
        return mats.index(t)

    def idx(v):
        return int(math.floor((v - O) / g + 1e-6))

    calcos = []
    orden = []
    for e in els:
        d = [e['to'][k] - e['from'][k] for k in range(3)]
        if len(e.get('faces', {})) <= 1:
            calcos.append(e)
            continue
        orden.append((-(max(d[0], 1e-3) * max(d[1], 1e-3) * max(d[2], 1e-3)), e))
    orden.sort(key=lambda p: p[0])  # de la más grande a la más pequeña: lo pequeño se pinta encima
    for _, e in orden:
        d = [e['to'][q] - e['from'][q] for q in range(3)]
        t = textura_principal(e)
        if t is None:
            continue
        k = mi(t)
        f, to = np.array(e['from'], float), np.array(e['to'], float)
        r = e.get('rotation')
        if not r or r.get('angle', 0) == 0:
            lo, hi = [], []
            for a in range(3):
                l, h = round((f[a] - O) / g), round((to[a] - O) / g)
                if h <= l:
                    l = int(math.floor(((f[a] + to[a]) / 2 - O) / g))
                    h = l + 1
                lo.append(max(0, l))
                hi.append(min(N, h))
            caja_v = (hi[0] - lo[0]) * (hi[1] - lo[1]) * (hi[2] - lo[2]) * g ** 3
            real = max(d[0], 1e-3) * max(d[1], 1e-3) * max(d[2], 1e-3)
            zona = grid[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
            if caja_v > 0 and real / caja_v < 0.25:
                # pieza mucho más fina que la celda (aros, bandas): solo rellena lo vacío, no tapa la pieza de debajo
                zona[zona < 0] = k
            else:
                zona[...] = k
        else:
            org = np.array(r['origin'], float)
            R = rot(r['axis'], r['angle'])
            esq = np.array([[x, y, z] for x in (f[0], to[0]) for y in (f[1], to[1]) for z in (f[2], to[2])])
            w = (esq - org) @ R.T + org
            a0 = [max(0, idx(w[:, a].min())) for a in range(3)]
            a1 = [min(N, idx(w[:, a].max()) + 1) for a in range(3)]
            xs, ys, zs = [O + (np.arange(a0[a], a1[a]) + 0.5) * g for a in range(3)]
            if not (len(xs) and len(ys) and len(zs)):
                continue
            P = np.stack(np.meshgrid(xs, ys, zs, indexing='ij'), -1).reshape(-1, 3)
            L = (P - org) @ R + org  # a coordenadas de la pieza (inversa de la rotación)
            # margen de media celda para que las piezas finas giradas no desaparezcan
            mg = np.minimum(g / 2, np.maximum(0, (g - (to - f)) / 2))
            dentro = np.all((L >= f - mg - 1e-6) & (L <= to + mg + 1e-6), axis=1)
            if not dentro.any():
                c = ((f + to) / 2 - org) @ R.T + org
                ii = [min(N - 1, max(0, idx(c[a]))) for a in range(3)]
                grid[ii[0], ii[1], ii[2]] = k
                continue
            sel = np.argwhere(dentro.reshape(len(xs), len(ys), len(zs)))
            grid[sel[:, 0] + a0[0], sel[:, 1] + a0[1], sel[:, 2] + a0[2]] = k
    # calcomanías: pintan la celda llena que tienen detrás
    for e in calcos:
        if not e.get('faces'):
            continue
        cara, fc = next(iter(e['faces'].items()))
        k = mi(fc['texture'])
        c = (np.array(e['from'], float) + np.array(e['to'], float)) / 2
        a, s = NORMAL[cara]
        c[a] -= s * g / 2
        ii = [min(N - 1, max(0, idx(c[b]))) for b in range(3)]
        if grid[ii[0], ii[1], ii[2]] >= 0:
            grid[ii[0], ii[1], ii[2]] = k
    return grid, mats, O, N


def uv_de(a, b, c, d):
    """UV de 1 texel por píxel de modelo, dentro de 0..16."""
    def tramo(p, q):
        w = q - p
        if w >= 16:
            return 0.0, 16.0
        u = p % 16
        if u + w > 16:
            u = 16 - w
        return round(u, 3), round(u + w, 3)
    u1, u2 = tramo(a, b)
    v1, v2 = tramo(c, d)
    return [u1, v1, u2, v2]


def cajas(grid, mats, O, N, g):
    lleno = grid >= 0
    hecho = np.zeros_like(lleno)
    out = []
    for x, y, z in np.argwhere(lleno):
        if hecho[x, y, z]:
            continue
        k = grid[x, y, z]
        x2 = x + 1
        while x2 < N and grid[x2, y, z] == k and not hecho[x2, y, z]:
            x2 += 1
        y2 = y + 1
        while y2 < N and np.all(grid[x:x2, y2, z] == k) and not hecho[x:x2, y2, z].any():
            y2 += 1
        z2 = z + 1
        while z2 < N and np.all(grid[x:x2, y:y2, z2] == k) and not hecho[x:x2, y:y2, z2].any():
            z2 += 1
        hecho[x:x2, y:y2, z:z2] = True
        f = [O + x * g, O + y * g, O + z * g]
        t = [O + x2 * g, O + y2 * g, O + z2 * g]
        caras = {}
        for cara in CARAS:
            a, s = NORMAL[cara]
            # ¿la tapa entera otra celda llena?
            sl = [slice(x, x2), slice(y, y2), slice(z, z2)]
            vec = (x2 if a == 0 else y2 if a == 1 else z2) if s > 0 else (x if a == 0 else y if a == 1 else z) - 1
            if 0 <= vec < N:
                sl[a] = slice(vec, vec + 1)
                if lleno[tuple(sl)].all():
                    continue
            if cara in ('north', 'south'):
                uv = uv_de(f[0], t[0], 16 - t[1], 16 - f[1])
            elif cara in ('east', 'west'):
                uv = uv_de(f[2], t[2], 16 - t[1], 16 - f[1])
            else:
                uv = uv_de(f[0], t[0], f[2], t[2])
            caras[cara] = {'uv': uv, 'texture': mats[k]}
        if caras:
            out.append({'from': [round(v, 3) for v in f], 'to': [round(v, 3) for v in t], 'faces': caras})
    return out


def convertir(ruta, g, salida):
    m = json.load(open(ruta, encoding='utf-8'))
    r = voxelizar(m, g)
    if r is None:
        return None
    els = cajas(*r, g)
    antes = (len(m['elements']), sum(len(e.get('faces', {})) for e in m['elements']))
    m['elements'] = els
    os.makedirs(salida, exist_ok=True)
    with open(os.path.join(salida, os.path.basename(ruta)), 'w', encoding='utf-8') as fh:
        json.dump(m, fh, ensure_ascii=False, separators=(',', ':'))
    return antes, (len(els), sum(len(e['faces']) for e in els))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--rejilla', type=float, default=1.0)
    ap.add_argument('--salida', required=True)
    ap.add_argument('modelos', nargs='*')
    a = ap.parse_args()
    tot = [0, 0, 0, 0]
    for p in a.modelos or sorted(glob.glob(os.path.join(DIR, '*.json'))):
        r = convertir(p, a.rejilla, a.salida)
        if r:
            (e0, c0), (e1, c1) = r
            tot = [tot[0] + e0, tot[1] + c0, tot[2] + e1, tot[3] + c1]
            print('%-40s %4d cajas %5d caras  ->  %4d cajas %5d caras' % (os.path.basename(p), e0, c0, e1, c1))
    print('TOTAL %d cajas %d caras -> %d cajas %d caras' % tuple(tot))

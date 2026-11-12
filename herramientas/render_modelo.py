#!/usr/bin/env python3
"""Renderiza un modelo de objeto de Minecraft (JSON de elementos) a PNG, para revisar las armas sin abrir el juego.

Uso: herramientas/render_modelo.py modelo.json salida.png [--vista lado|tres_cuartos|arriba] [--tam 512]

Rasterizador por software (numpy + Pillow): rotaciones de elemento, UV de cara (con rotación de cara), muestreo al
vecino más cercano y el sombreado plano de Minecraft (arriba 1.0, abajo 0.5, norte/sur 0.8, este/oeste 0.6).
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'common', 'src', 'main', 'resources', 'assets')
LUZ = {'up': 1.0, 'down': 0.5, 'north': 0.8, 'south': 0.8, 'east': 0.6, 'west': 0.6}


def ruta_textura(ref):
    ns, _, p = ref.partition(':')
    if not p:
        ns, p = 'minecraft', ns
    return os.path.join(RAIZ, ns, 'textures', p + '.png')


def resolver(texs, ref, prof=0):
    while ref.startswith('#') and prof < 10:
        ref = texs.get(ref[1:], '')
        prof += 1
    return ref


def esquinas(cara, f, t):
    """Las cuatro esquinas (sup-izq, sup-der, inf-der, inf-izq) de la cara, en el orden de la textura."""
    x1, y1, z1 = f
    x2, y2, z2 = t
    return {
        'north': [(x2, y2, z1), (x1, y2, z1), (x1, y1, z1), (x2, y1, z1)],
        'south': [(x1, y2, z2), (x2, y2, z2), (x2, y1, z2), (x1, y1, z2)],
        'east': [(x2, y2, z2), (x2, y2, z1), (x2, y1, z1), (x2, y1, z2)],
        'west': [(x1, y2, z1), (x1, y2, z2), (x1, y1, z2), (x1, y1, z1)],
        'up': [(x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2)],
        'down': [(x1, y1, z2), (x2, y1, z2), (x2, y1, z1), (x1, y1, z1)],
    }[cara]


def rot_eje(eje, ang):
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    if eje == 'x':
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if eje == 'y':
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def vista(nombre):
    if nombre == 'lado':  # mirando desde +x: la boca (z pequeña) a la izquierda... a la derecha
        return rot_eje('y', -90)
    if nombre == 'arriba':
        return rot_eje('x', 90) @ rot_eje('y', -90)
    return rot_eje('x', 25) @ rot_eje('y', -60)


def render(modelo, tam=512, vista_nombre='tres_cuartos', fondo=(48, 50, 58, 255)):
    texs = modelo.get('textures', {})
    cache = {}
    tris = []
    for el in modelo.get('elements', []):
        f, t = el['from'], el['to']
        R = None
        if 'rotation' in el:
            r = el['rotation']
            R = (np.array(r['origin'], float), rot_eje(r['axis'], r['angle']))
        for cara, d in el.get('faces', {}).items():
            ref = resolver(texs, d.get('texture', ''))
            if ref not in cache:
                p = ruta_textura(ref)
                cache[ref] = np.asarray(Image.open(p).convert('RGBA'), float) if os.path.exists(p) else None
            tex = cache[ref]
            if tex is None:
                continue
            uv = d.get('uv')
            if uv is None:
                uv = [0, 0, 16, 16]
            u1, v1, u2, v2 = uv
            uvs = [(u1, v1), (u2, v1), (u2, v2), (u1, v2)]
            k = (d.get('rotation', 0) // 90) % 4
            uvs = uvs[k:] + uvs[:k]
            pts = np.array(esquinas(cara, f, t), float)
            if R is not None:
                pts = (pts - R[0]) @ R[1].T + R[0]
            tris.append((pts, uvs, tex, LUZ[cara]))
    M = vista(vista_nombre)
    todos = np.concatenate([p for p, *_ in tris]) if tris else np.zeros((1, 3))
    c = (todos - 8) @ M.T
    ext = max(np.abs(c[:, 0]).max(), np.abs(c[:, 1]).max(), 1e-3) * 1.08
    esc = tam / 2 / ext
    img = np.zeros((tam, tam, 4))
    img[:] = fondo
    zb = np.full((tam, tam), -1e9)
    for pts, uvs, tex, luz in tris:
        q = (pts - 8) @ M.T
        sx = q[:, 0] * esc + tam / 2
        sy = -q[:, 1] * esc + tam / 2
        sz = q[:, 2]
        th, tw = tex.shape[:2]
        for a, b, cc in ((0, 1, 2), (0, 2, 3)):
            xs = np.array([sx[a], sx[b], sx[cc]])
            ys = np.array([sy[a], sy[b], sy[cc]])
            x0, x1 = int(max(0, math.floor(xs.min()))), int(min(tam - 1, math.ceil(xs.max())))
            y0, y1 = int(max(0, math.floor(ys.min()))), int(min(tam - 1, math.ceil(ys.max())))
            if x1 < x0 or y1 < y0:
                continue
            den = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
            if abs(den) < 1e-9:
                continue
            gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            w0 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / den
            w1 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / den
            w2 = 1 - w0 - w1
            m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            if not m.any():
                continue
            z = w0 * sz[a] + w1 * sz[b] + w2 * sz[cc]
            u = w0 * uvs[a][0] + w1 * uvs[b][0] + w2 * uvs[cc][0]
            v = w0 * uvs[a][1] + w1 * uvs[b][1] + w2 * uvs[cc][1]
            tu = np.clip((u / 16 * tw).astype(int), 0, tw - 1)
            tv = np.clip((v / 16 * th).astype(int), 0, th - 1)
            col = tex[tv, tu]
            m &= col[..., 3] > 8
            sub = zb[y0:y1 + 1, x0:x1 + 1]
            m &= z > sub
            if not m.any():
                continue
            sub[m] = z[m]
            dst = img[y0:y1 + 1, x0:x1 + 1]
            rgb = col[..., :3] * luz
            dst[m, :3] = rgb[m]
            dst[m, 3] = 255
    return Image.fromarray(img.clip(0, 255).astype(np.uint8))


def cargar(ruta):
    with open(ruta) as fh:
        m = json.load(fh)
    padre = m.get('parent')
    if padre and 'elements' not in m:
        ns, _, p = padre.partition(':')
        if not p:
            ns, p = 'minecraft', ns
        pr = os.path.join(RAIZ, ns, 'models', p + '.json')
        if os.path.exists(pr):
            base = cargar(pr)
            base.setdefault('textures', {}).update(m.get('textures', {}))
            return base
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('modelo')
    ap.add_argument('salida')
    ap.add_argument('--vista', default='tres_cuartos')
    ap.add_argument('--tam', type=int, default=512)
    a = ap.parse_args()
    render(cargar(a.modelo), a.tam, a.vista).save(a.salida)


if __name__ == '__main__':
    sys.exit(main())

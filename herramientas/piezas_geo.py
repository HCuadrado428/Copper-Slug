#!/usr/bin/env python3
"""Las piezas que se mueven del Winchester (la palanca) y del rifle (el cerrojo), como modelos de Bloomberto
(.geo.json + atlas + animación), igual que el tambor del revólver (herramientas/tambor_geo.py).

Las piezas salen de herramientas/armas_pulidas.py (palanca_winchester, cerrojo_rifle) y ya no están en el modelo de
objeto del arma: el juego dibuja el arma y encima la pieza, posada con la animación según el ciclo del arma
(client/armasfuego/comun/PiezasAnimadas.java). La animación va en tiempo normalizado: 1 segundo = el ciclo entero.

Genera, para cada pieza:
- assets/copperslug/geo/<pieza>.geo.json
- assets/copperslug/textures/geo/<pieza>_N.png (N = fase de óxido)
- assets/copperslug/animations/<pieza>.animation.json

--comprobar dibuja cada pieza cerrada y a media animación con el port de ModelGeometry de Bloomberto, al lado de la
misma pieza como modelo de objeto (girada a mano), y dice cuánto se parecen.

Uso: herramientas/piezas_geo.py [--comprobar salida.png]
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_modelo as rm  # noqa: E402
import armas_pulidas as ap  # noqa: E402
from tambor_geo import caras_geo, uv_mc, NOMBRE_BEDROCK, rot_zyx, ASSETS, K  # noqa: E402

TEX = os.path.join(ASSETS, 'textures', 'geo')


def texturas(ox):
    t = dict(ap.TEXTURAS)
    t['cobre'] = 'copperslug:item/armas3d/p_cobre_%d' % ox
    return t


def construir(ident, huesos, texs):
    """huesos: [(nombre, padre, pivote MC, elementos)] -> (geo, atlas)."""
    cache = {}

    def textura(ref):
        r = rm.resolver(texs, ref)
        if r not in cache:
            cache[r] = np.asarray(Image.open(rm.ruta_textura(r)).convert('RGBA'))
        return cache[r]

    caras = []
    for _, _, _, els in huesos:
        for el in els:
            for cara, d in el['faces'].items():
                c = caras_geo(el['from'], el['to'])[cara]
                ancho = np.linalg.norm(np.subtract(c[1], c[0]))
                alto = np.linalg.norm(np.subtract(c[3], c[0]))
                caras.append((el, cara, d, max(1, math.ceil(ancho * K)), max(1, math.ceil(alto * K))))
    W = 128
    x = y = fila = 0
    sitio = []
    for el, cara, d, w, h in caras:
        if x + w > W:
            x, y, fila = 0, y + fila + 1, 0
        sitio.append((x, y))
        x += w + 1
        fila = max(fila, h)
    H = 1 << math.ceil(math.log2(y + fila + 1))
    atlas = np.zeros((H, W, 4), np.uint8)
    uvs = {}
    for (el, cara, d, w, h), (ax, ay) in zip(caras, sitio):
        f, t = el['from'], el['to']
        bl, br, tr, tl = [np.array(v, float) for v in caras_geo(f, t)[cara]]
        tex = textura(d['texture'])
        th, tw = tex.shape[:2]
        for j in range(h):
            for i in range(w):
                s, r = (i + 0.5) / w, (j + 0.5) / h
                if cara == 'down':
                    r = 1 - r
                p = tl + s * (tr - tl) + r * (bl - tl)
                u, v = uv_mc(cara, d, f, t, p)
                atlas[ay + j, ax + i] = tex[min(th - 1, max(0, int(v / 16 * th))), min(tw - 1, max(0, int(u / 16 * tw)))]
        uvs.setdefault(id(el), {})[NOMBRE_BEDROCK[cara]] = {'uv': [ax, ay], 'uv_size': [w, h]}

    bones = []
    for nombre, padre, piv, els in huesos:
        cubos = []
        for el in els:
            f, t = el['from'], el['to']
            cubo = {'origin': [round(-t[0], 4), f[1], f[2]],
                    'size': [round(t[0] - f[0], 4), round(t[1] - f[1], 4), round(t[2] - f[2], 4)],
                    'uv': uvs[id(el)]}
            r = el.get('rotation')
            if r:
                o = r['origin']
                ang = {'x': [r['angle'], 0, 0], 'y': [0, r['angle'], 0], 'z': [0, 0, r['angle']]}[r['axis']]
                cubo['pivot'] = [-o[0], o[1], o[2]]
                cubo['rotation'] = [-ang[0], -ang[1], ang[2]]
            cubos.append(cubo)
        b = {'name': nombre, 'pivot': [-piv[0], piv[1], piv[2]], 'cubes': cubos}
        if padre:
            b['parent'] = padre
        bones.append(b)
    geo = {'format_version': '1.12.0', 'minecraft:geometry': [{
        'description': {'identifier': 'geometry.copperslug.' + ident, 'texture_width': W, 'texture_height': H},
        'bones': bones}]}
    return geo, Image.fromarray(atlas)


def k(t, v, cat=False):
    """Un fotograma: {tiempo: valor} (catmull-rom si se pide)."""
    return ('%.2f' % t, {'post': v, 'lerp_mode': 'catmullrom'} if cat else v)


def clip(nombre, huesos):
    return {'format_version': '1.8.0', 'animations': {
        'animation.' + nombre: {'animation_length': 1.0, 'loop': 'hold_on_last_frame', 'bones': {
            h: {canal: dict(fs) for canal, fs in canales.items()} for h, canales in huesos.items()}}}}


# Bloomberto lee la x y la y de las rotaciones con el signo cambiado (como GeckoLib): abrir la palanca 45° sobre x en
# Minecraft es -45 en el archivo. La z y las posiciones en z van igual.
PIEZAS = {
    'winchester_palanca': dict(
        huesos=lambda: [('palanca', None, ap.EJE_PALANCA, ap.palanca_winchester())],
        anim=lambda: clip('winchester_palanca', {'palanca': {'rotation': [
            k(0, [0, 0, 0]), k(0.06, [0, 0, 0]), k(0.3, [-50, 0, 0]), k(0.4, [-45, 0, 0]),
            k(0.55, [-45, 0, 0]), k(0.8, [3, 0, 0]), k(1.0, [0, 0, 0])]}})),
    'rifle_cerrojo': dict(
        huesos=lambda: [('cerrojo', None, ap.EJE_MANILLA, ap.cerrojo_rifle()[0]),
                        ('manilla', 'cerrojo', ap.EJE_MANILLA, ap.cerrojo_rifle()[1])],
        anim=lambda: clip('rifle_cerrojo', {
            'manilla': {'rotation': [k(0, [0, 0, 0]), k(0.16, [0, 0, 71]), k(0.22, [0, 0, 67.5]),
                                     k(0.78, [0, 0, 67.5]), k(0.92, [0, 0, -4]), k(1.0, [0, 0, 0])]},
            'cerrojo': {'position': [k(0, [0, 0, 0]), k(0.22, [0, 0, 0]), k(0.42, [0, 0, 1.6]),
                                     k(0.58, [0, 0, 1.6]), k(0.78, [0, 0, 0]), k(1.0, [0, 0, 0])]}})),
}


# ---------------------------------------------------------------- comprobación
def interpolar(fs, t):
    """Lineal entre fotogramas (basta para comprobar los signos)."""
    claves = sorted((float(a), (b['post'] if isinstance(b, dict) else b)) for a, b in fs.items())
    for (t0, v0), (t1, v1) in zip(claves, claves[1:]):
        if t0 <= t <= t1:
            a = (t - t0) / (t1 - t0) if t1 > t0 else 0
            return [x0 + (x1 - x0) * a for x0, x1 in zip(v0, v1)]
    return claves[-1][1]


def quads(geo, atlas_np, anim, t):
    g = geo['minecraft:geometry'][0]
    W, H = g['description']['texture_width'], g['description']['texture_height']
    huesos = list(anim['animations'].values())[0]['bones']
    mats = {}
    out = []
    for b in g['bones']:
        piv = np.array([-b['pivot'][0], b['pivot'][1], b['pivot'][2]])
        canales = huesos.get(b['name'], {})
        rot = interpolar(canales['rotation'], t) if 'rotation' in canales else [0, 0, 0]
        pos = interpolar(canales['position'], t) if 'position' in canales else [0, 0, 0]
        R = rot_zyx(math.radians(-rot[0]), math.radians(-rot[1]), math.radians(rot[2]))
        P = np.array([-pos[0], pos[1], pos[2]])
        Rl, tl = R, piv + P - R @ piv
        Rp, tp = mats.get(b.get('parent'), (np.eye(3), np.zeros(3)))
        mats[b['name']] = (Rp @ Rl, Rp @ tl + tp)
        Rb, tb = mats[b['name']]
        for c in b['cubes']:
            ox, oy, oz = c['origin']
            w, h, d = c['size']
            f, tt = (-(ox + w), oy, oz), (-ox, oy + h, oz + d)
            Rc, tc = np.eye(3), np.zeros(3)
            if 'pivot' in c:
                cp = np.array([-c['pivot'][0], c['pivot'][1], c['pivot'][2]])
                Rc = rot_zyx(math.radians(-c['rotation'][0]), math.radians(-c['rotation'][1]), math.radians(c['rotation'][2]))
                tc = cp - Rc @ cp
            for cara, nombre in NOMBRE_BEDROCK.items():
                reg = c['uv'].get(nombre)
                if not reg:
                    continue
                u0, v0 = reg['uv'][0] / W, reg['uv'][1] / H
                u1, v1 = u0 + reg['uv_size'][0] / W, v0 + reg['uv_size'][1] / H
                uv = [(u0, v1), (u1, v1), (u1, v0), (u0, v0)]
                if cara == 'down':
                    uv = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
                pts = np.array(caras_geo(f, tt)[cara], float)
                pts = (pts @ Rc.T + tc) @ Rb.T + tb
                orden = [3, 2, 1, 0]
                out.append((pts[orden], [(uv[i][0] * 16, uv[i][1] * 16) for i in orden], atlas_np, rm.LUZ[cara]))
    return out


def vista(tris, centro):
    def a_vista(p):
        q = p - np.array(centro)
        R = rm.rot_eje('y', 60) @ rm.rot_eje('x', 15)
        return q @ R.T + np.array([0, 0, -0.35])
    return Image.fromarray(np.asarray(rm.render_vista([(tris, a_vista)], W=300, H=260, fov=40, fondo=(40, 42, 50, 255))).astype(np.uint8))


def comprobar(salida):
    filas = []
    for nombre, pz in PIEZAS.items():
        geo, atlas = construir(nombre, pz['huesos'](), texturas(0))
        a = np.asarray(atlas.convert('RGBA'), float)
        anim = pz['anim']()
        els = [e for _, _, _, es in pz['huesos']() for e in es]
        m = {'textures': texturas(0), 'elements': els}
        cent = np.mean([e['from'] for e in els], axis=0) / 16
        ims = [vista(rm.triangulos(m), cent), vista(quads(geo, a, anim, 0.0), cent), vista(quads(geo, a, anim, 0.5), cent)]
        d = np.abs(np.asarray(ims[0], float) - np.asarray(ims[1], float))[..., :3].mean()
        print('%-20s cerrada: diferencia con el modelo de objeto %.2f' % (nombre, d))
        filas.append(ims)
    o = Image.new('RGBA', (sum(i.width for i in filas[0]), sum(f[0].height for f in filas)))
    y = 0
    for f in filas:
        x = 0
        for i in f:
            o.paste(i, (x, y))
            x += i.width
        y += f[0].height
    o.save(salida)


def main():
    a_ = argparse.ArgumentParser()
    a_.add_argument('--comprobar')
    a = a_.parse_args()
    if a.comprobar:
        comprobar(a.comprobar)
        return
    os.makedirs(TEX, exist_ok=True)
    for nombre, pz in PIEZAS.items():
        for ox in range(4):
            geo, atlas = construir(nombre, pz['huesos'](), texturas(ox))
            atlas.save(os.path.join(TEX, '%s_%d.png' % (nombre, ox)))
        json.dump(geo, open(os.path.join(ASSETS, 'geo', nombre + '.geo.json'), 'w'), indent=1)
        json.dump(pz['anim'](), open(os.path.join(ASSETS, 'animations', nombre + '.animation.json'), 'w'), indent=1)
        print(nombre, 'escrita')


if __name__ == '__main__':
    main()

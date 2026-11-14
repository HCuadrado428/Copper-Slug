#!/usr/bin/env python3
"""El tambor del revólver como modelo de Bloomberto (geometría Bedrock .geo.json + animación), a partir del modelo de
objeto revolver_cilindro_0.json, para que la grúa del tambor se abra y se cierre con una animación de verdad.

Genera:
- assets/copperslug/geo/revolver_tambor.geo.json: los mismos cubos que el modelo de objeto, en dos huesos: «grua» (el
  brazo que saca el tambor hacia la izquierda, pivota bajo el tambor) y «tambor» (gira sobre su eje).
- textures/geo/revolver_tambor_N.png (N = fase de óxido): cada cara del modelo copiada a su propio rectángulo,
  porque la geometría Bedrock lleva una sola textura y sin rotación de cara.
- assets/copperslug/animations/revolver_tambor.animation.json: abrir y cerrar la grúa.

Bloomberto espeja la X (como GeckoLib): aquí se escribe ya espejada para que en el juego salgan las mismas coordenadas
que el modelo de objeto. --comprobar dibuja el modelo de objeto y el .geo.json (con un port en Python de
ModelGeometry de Bloomberto) y dice cuánto se parecen.

Uso: herramientas/tambor_geo.py [--comprobar salida.png]
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

ASSETS = os.path.join(rm.RAIZ, 'copperslug')
MODELOS = os.path.join(ASSETS, 'models', 'item', 'armas3d')
TEX = os.path.join(ASSETS, 'textures', 'geo')
K = 4                     # texels del atlas por píxel de modelo
CX, CY = 8.0, 8.9         # el eje del tambor (RevolverTambor.CX/CY)
GRUA = (8.0, 5.4)         # el eje de la grúa: debajo del tambor, paralelo al cañón
ABIERTA = -55.0           # grados que gira la grúa al abrir (sale hacia el centro de la pantalla y un poco abajo)


def caras_geo(f, t):
    """Las esquinas (abajo-izq, abajo-der, arriba-der, arriba-izq) de cada cara como las pone ModelGeometry."""
    x0, y0, z0 = f
    x1, y1, z1 = t
    return {
        'south': [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
        'north': [(x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0)],
        'east': [(x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, y1, z1)],   # +x: la región «west» de Bedrock
        'west': [(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)],   # -x: la región «east»
        'up': [(x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0)],
        'down': [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
    }


# en Bedrock la X está espejada: la cara +x de Minecraft es la región «west» del archivo y la -x la «east»
NOMBRE_BEDROCK = {'south': 'south', 'north': 'north', 'east': 'west', 'west': 'east', 'up': 'up', 'down': 'down'}


def uv_mc(cara, d, f, t, p):
    """El UV (en 16) que Minecraft pone en el punto p de esa cara."""
    esq = np.array(rm.esquinas(cara, f, t), float)          # sup-izq, sup-der, inf-der, inf-izq
    u1, v1, u2, v2 = d.get('uv') or [0, 0, 16, 16]
    uvs = [(u1, v1), (u2, v1), (u2, v2), (u1, v2)]
    k = (d.get('rotation', 0) // 90) % 4
    uvs = np.array(uvs[k:] + uvs[:k], float)
    a_ = esq[1] - esq[0]
    b_ = esq[3] - esq[0]
    q = np.asarray(p, float) - esq[0]
    sa = q @ a_ / max(a_ @ a_, 1e-9)
    sb = q @ b_ / max(b_ @ b_, 1e-9)
    return uvs[0] + sa * (uvs[1] - uvs[0]) + sb * (uvs[3] - uvs[0])


def generar(ox):
    modelo = json.load(open(os.path.join(MODELOS, 'revolver_cilindro_%d.json' % ox)))
    texs = modelo['textures']
    cache = {}

    def textura(ref):
        r = rm.resolver(texs, ref)
        if r not in cache:
            cache[r] = np.asarray(Image.open(rm.ruta_textura(r)).convert('RGBA'))
        return cache[r]

    # primero el sitio de cada cara en el atlas (filas por orden)
    caras = []
    for el in modelo['elements']:
        f, t = el['from'], el['to']
        for cara, d in el['faces'].items():
            c = caras_geo(f, t)[cara]
            ancho = np.linalg.norm(np.subtract(c[1], c[0]))
            alto = np.linalg.norm(np.subtract(c[3], c[0]))
            caras.append((el, cara, d, max(1, math.ceil(ancho * K)), max(1, math.ceil(alto * K))))
    W = 256
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

    huesos = {'grua': [], 'tambor': []}
    por_el = {}
    for (el, cara, d, w, h), (ax, ay) in zip(caras, sitio):
        f, t = el['from'], el['to']
        bl, br, tr, tl = [np.array(v, float) for v in caras_geo(f, t)[cara]]
        tex = textura(d['texture'])
        th, tw = tex.shape[:2]
        for j in range(h):
            for i in range(w):
                s, r = (i + 0.5) / w, (j + 0.5) / h
                if cara == 'down':   # la de abajo va con la V dada la vuelta en Bedrock
                    r = 1 - r
                p = tl + s * (tr - tl) + r * (bl - tl)
                u, v = uv_mc(cara, d, f, t, p)
                atlas[ay + j, ax + i] = tex[min(th - 1, max(0, int(v / 16 * th))), min(tw - 1, max(0, int(u / 16 * tw)))]
        por_el.setdefault(id(el), (el, {}))[1][NOMBRE_BEDROCK[cara]] = {'uv': [ax, ay], 'uv_size': [w, h]}

    for el, uv in por_el.values():
        f, t = el['from'], el['to']
        cubo = {'origin': [round(-t[0], 4), f[1], f[2]],
                'size': [round(t[0] - f[0], 4), round(t[1] - f[1], 4), round(t[2] - f[2], 4)],
                'uv': uv}
        r = el.get('rotation')
        if r:
            o = r['origin']
            ang = {'x': [r['angle'], 0, 0], 'y': [0, r['angle'], 0], 'z': [0, 0, r['angle']]}[r['axis']]
            # Bloomberto: x espejada y rotaciones con signos (-x, -y, +z)
            cubo['pivot'] = [-o[0], o[1], o[2]]
            cubo['rotation'] = [-ang[0], -ang[1], ang[2]]
        huesos['tambor'].append(cubo)
    geo = {
        'format_version': '1.12.0',
        'minecraft:geometry': [{
            'description': {'identifier': 'geometry.copperslug.revolver_tambor', 'texture_width': W, 'texture_height': H},
            'bones': [
                {'name': 'grua', 'pivot': [-GRUA[0], GRUA[1], 9.7], 'cubes': []},
                {'name': 'tambor', 'parent': 'grua', 'pivot': [-CX, CY, 9.7], 'cubes': huesos['tambor']},
            ]}]}
    return geo, Image.fromarray(atlas)


def animacion():
    # rotación z del archivo = la misma en el juego (Bloomberto solo cambia el signo de x e y)
    return {
        'format_version': '1.8.0',
        'animations': {
            'animation.revolver_tambor.abrir': {
                'animation_length': 0.3, 'loop': 'hold_on_last_frame',
                'bones': {'grua': {'rotation': {
                    '0.0': [0, 0, 0],
                    '0.15': {'post': [0, 0, ABIERTA - 6], 'lerp_mode': 'catmullrom'},
                    '0.3': {'post': [0, 0, ABIERTA], 'lerp_mode': 'catmullrom'}}}}},
            'animation.revolver_tambor.cerrar': {
                'animation_length': 0.25, 'loop': 'hold_on_last_frame',
                'bones': {'grua': {'rotation': {
                    '0.0': [0, 0, ABIERTA],
                    '0.12': [0, 0, 1.5],
                    '0.25': {'post': [0, 0, 0], 'lerp_mode': 'catmullrom'}}}}},
        }}


# ---------------------------------------------------------------- comprobación: un port de ModelGeometry de Bloomberto
def rot_zyx(rx, ry, rz):
    """JOML rotateZYX(z, y, x): primero z, luego y, luego x (intrínsecas), en radianes."""
    return rm.rot_eje('z', math.degrees(rz)) @ rm.rot_eje('y', math.degrees(ry)) @ rm.rot_eje('x', math.degrees(rx))


def quads_geo(geo, atlas_np, grua=0.0, tambor=0.0):
    g = geo['minecraft:geometry'][0]
    W, H = g['description']['texture_width'], g['description']['texture_height']
    out = []
    mats = {}
    for b in g['bones']:
        piv = np.array([-b['pivot'][0], b['pivot'][1], b['pivot'][2]])
        anim = {'grua': grua, 'tambor': tambor}.get(b['name'], 0.0)
        R = rot_zyx(0, 0, math.radians(anim))
        padre = mats.get(b.get('parent'), (np.eye(3), np.zeros(3)))
        # local = padre · T(piv) · R · T(-piv)
        Rl, tl = R, piv - R @ piv
        mats[b['name']] = (padre[0] @ Rl, padre[0] @ tl + padre[1])
        Rb, tb = mats[b['name']]
        for c in b['cubes']:
            ox, oy, oz = c['origin']
            w, h, d = c['size']
            x0, x1 = -(ox + w), -ox
            f, t = (x0, oy, oz), (x1, oy + h, oz + d)
            Rc, tc = np.eye(3), np.zeros(3)
            if 'pivot' in c:
                cp = np.array([-c['pivot'][0], c['pivot'][1], c['pivot'][2]])
                cr = [math.radians(-c['rotation'][0]), math.radians(-c['rotation'][1]), math.radians(c['rotation'][2])]
                Rc = rot_zyx(*cr)
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
                pts = np.array(caras_geo(f, t)[cara], float)
                pts = (pts @ Rc.T + tc) @ Rb.T + tb
                orden = [3, 2, 1, 0]   # a sup-izq, sup-der, inf-der, inf-izq como render_modelo
                out.append((pts[orden], [(uv[i][0] * 16, uv[i][1] * 16) for i in orden], atlas_np, rm.LUZ[cara]))
    return out


def comprobar(salida):
    geo, atlas = generar(0)
    a = np.asarray(atlas.convert('RGBA'), float)
    original = rm.triangulos(json.load(open(os.path.join(MODELOS, 'revolver_cilindro_0.json'))))
    vistas = []
    for grua in (0.0, ABIERTA):
        nuevo = quads_geo(geo, a, grua=grua)
        for tris in ((original,) if grua == 0 else ()) + (nuevo,):
            def a_vista(p):
                q = p - np.array([0.5, 0.56, 0.6])
                R = rm.rot_eje('y', 35) @ rm.rot_eje('x', 25)
                return q @ R.T + np.array([0, 0, -0.5])
            vistas.append(rm.render_vista([(tris, a_vista)], W=360, H=300, fov=40, fondo=(40, 42, 50, 255)))
    ims = [Image.fromarray(v.astype(np.uint8)) if not isinstance(v, Image.Image) else v for v in vistas]
    o = Image.new('RGBA', (sum(i.width for i in ims), ims[0].height))
    xx = 0
    for i in ims:
        o.paste(i, (xx, 0))
        xx += i.width
    o.save(salida)
    d = np.abs(np.asarray(ims[0], float) - np.asarray(ims[1], float))[..., :3].mean()
    print('diferencia media modelo de objeto / geo: %.2f (0 = igual)' % d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--comprobar')
    a = ap.parse_args()
    if a.comprobar:
        comprobar(a.comprobar)
        return
    os.makedirs(os.path.join(ASSETS, 'geo'), exist_ok=True)
    os.makedirs(os.path.join(ASSETS, 'animations'), exist_ok=True)
    for ox in range(4):
        geo, atlas = generar(ox)
        atlas.save(os.path.join(TEX, 'revolver_tambor_%d.png' % ox))
        if ox == 0:
            json.dump(geo, open(os.path.join(ASSETS, 'geo', 'revolver_tambor.geo.json'), 'w'), indent=1)
    json.dump(animacion(), open(os.path.join(ASSETS, 'animations', 'revolver_tambor.animation.json'), 'w'), indent=1)
    print('geo, atlas y animación del tambor escritos')


if __name__ == '__main__':
    main()

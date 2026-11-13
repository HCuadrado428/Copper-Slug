#!/usr/bin/env python3
"""Simula la primera persona de las armas (en la cadera y apuntando) sin abrir el juego.

Hace las mismas cuentas que el juego: el arma va al brazo (0,56, -0,52, -0,72), luego su display firstperson_righthand
(traslado, giro XYZ y escala) y, apuntando, lo de Apuntado.alinear: el alza al eje de la vista, a «prof» bloques del
ojo, y el arma enderezada. La mano se dibuja con un campo de visión fijo de 70° (el zoom no le afecta). Los datos de cada
arma se leen de Apuntado.java, así que se simula lo que hay en el código.

Uso: herramientas/simular_apuntado.py [arma ...] [--salida DIR]
"""
import argparse
import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_modelo as R  # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
JAVA = os.path.join(RAIZ, 'common/src/main/java/com/copperslug/client/armasfuego/comun/Apuntado.java')
MOD = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item/armas3d')
MODELOS = {'REVOLVER': 'revolver_3d', 'WINCHESTER': 'winchester_3d', 'THOMPSON': 'thompson_3d', 'MOSQUETE': 'mosquete_3d',
           'CERBATANA': 'cerbatana_3d', 'RESONANCIA': 'resonancia_3d', 'ARPONERA': 'arponera_3d'}


def miras(java=JAVA):
    t = open(java, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'Mira (\w+) = new Mira\(([^)]*)\)', t):
        out[m.group(1)] = [float(x.strip().rstrip('F')) for x in m.group(2).split(',')]
    return out


def T(x, y, z):
    m = np.eye(4)
    m[:3, 3] = (x, y, z)
    return m


def Rm(r3):
    m = np.eye(4)
    m[:3, :3] = r3
    return m


def S(s):
    m = np.eye(4)
    m[0, 0] = m[1, 1] = m[2, 2] = s
    return m


def transformaciones(mi, k):
    """La matriz que lleva el modelo (en bloques, 0..1) a la vista, con el apuntado k (0 = cadera, 1 = apuntando)."""
    rx, ry, tx, ty, tz, s, yr, zr, yf, zf, prof = mi[:11]
    baja = mi[11] if len(mi) > 11 else 0.0
    rot = R.rot_xyz(rx, ry, 0)
    display = T(tx / 16, ty / 16, tz / 16) @ Rm(rot) @ S(s)
    brazo = T(0.56, -0.52, -0.72)
    modelo = T(-0.5, -0.5, -0.5)
    base = brazo @ display @ modelo
    if k <= 0:
        return base
    alza = rot @ np.array([0, (yr / 16 - 0.5) * s, (zr / 16 - 0.5) * s])
    c = np.array([0.56 + tx / 16, -0.52 + ty / 16, -0.72 + tz / 16]) + alza
    sube = math.atan2(yr - yf, zr - zf)
    # el alza «baja» bloques por debajo de la cruz y el arma inclinada lo justo para que el punto de mira quede en ella
    largo = (zr - zf) / 16 * s
    inclina = math.atan2(baja, largo) if largo > 0 else 0
    q = R.rot_eje('x', math.degrees(sube + inclina)) @ rot.T
    destino = np.array([0, -0.004 - baja, -prof])
    # (k = 1) traslado al destino y giro alrededor del alza
    A = T(*destino) @ Rm(q) @ T(*(-c))
    return A @ base


def a_vista(M):
    return lambda p: (np.c_[p, np.ones(len(p))] @ M.T)[:, :3]


def simular(nombre, mi, W=640, H=360):
    m = R.cargar(os.path.join(MOD, MODELOS[nombre] + '.json'))
    if nombre == 'REVOLVER':
        cil = json.load(open(os.path.join(MOD, 'revolver_cilindro_0.json')))
        m['elements'] = m['elements'] + cil['elements']
        m['textures'] = {**cil['textures'], **m['textures']}
    tris = R.triangulos(m)
    caderas = R.render_vista([(tris, a_vista(transformaciones(mi, 0)))], W, H)
    apunta = R.render_vista([(tris, a_vista(transformaciones(mi, 1)))], W, H)
    # lo que queda detrás de la cámara (se corta en el juego)
    pts = np.concatenate([t[0] for t in tris]) / 16
    q = a_vista(transformaciones(mi, 1))(pts)
    return caderas, apunta, float(q[:, 2].max())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('armas', nargs='*')
    ap.add_argument('--salida', default='/tmp/apuntado.png')
    ap.add_argument('--prueba', action='append', default=[], help='ARMA=prof,baja: probar otros valores')
    a = ap.parse_args()
    mis = miras()
    for x in a.prueba:
        n, v = x.split('=')
        prof, baja = (float(t) for t in v.split(','))
        mi = mis[n.upper()][:11]
        mi[10] = prof
        mis[n.upper()] = mi + [baja]
    nombres = [n.upper() for n in a.armas] or list(MODELOS)
    W, H = 480, 270
    hoja = Image.new('RGB', (W * 2 + 6, (H + 4) * len(nombres)), (20, 20, 24))
    d = ImageDraw.Draw(hoja)
    for i, n in enumerate(nombres):
        c, p, zmax = simular(n, mis[n], W, H)
        hoja.paste(c.convert('RGB'), (0, i * (H + 4)))
        hoja.paste(p.convert('RGB'), (W + 6, i * (H + 4)))
        d.text((6, i * (H + 4) + 4), '%s  cadera' % n, fill='white')
        d.text((W + 12, i * (H + 4) + 4), 'apuntando   (lo más cercano: z = %.2f)' % zmax, fill='white')
    hoja.save(a.salida)
    print(a.salida)

#!/usr/bin/env python3
"""Test de estilo Minecraft de las armas: comprueba lo que hace que un arma «no parezca de Minecraft» y da recomendaciones.

No sustituye a probar en el juego (eso lo hace el workflow «Probar en el juego»); mira los recursos y avisa de:

  1. Texturas de material (armas3d) planas: menos de 4 tonos o casi sin contraste. Vanilla usa rampas de 4-6 tonos.
  2. Cañones octogonales (cajas giradas 45° en grupos _0.._3). Minecraft usa cajas cuadradas; solo el tambor del revólver
     puede ser octogonal porque gira de 60 en 60 grados.
  3. Iconos de arma que son palitos: muy pocos píxeles opacos o casi todo de un píxel de grueso (no se leen en la barra).
  4. Iconos sin contorno oscuro: vanilla bordea cada objeto con el tono más oscuro de su material.
  5. Piezas de modelo más finas de 0,25 px (de lejos parpadean y no se ven píxeles enteros).
  6. Caras con la textura estirada: la UV no tiene la misma densidad que la caja (1 texel por píxel de modelo).

Errores (1-3) hacen fallar el test; lo demás son avisos con recomendaciones. Uso: test_estilo_minecraft.py [raíz]
"""
import collections
import glob
import json
import os
import re
import sys

from PIL import Image

RAIZ = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
A = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug')
ARMAS = ['revolver', 'rifle', 'escopeta_presion_0', 'gatling', 'winchester', 'derringer', 'thompson', 'mosquete',
         'canon_mano', 'cerbatana', 'lanzallamas', 'resonancia', 'arponera']
MATERIALES = ['cobre_0', 'cobre_1', 'cobre_2', 'cobre_3', 'hierro', 'g_acero', 'laton', 'madera', 'g_madera', 'g_cuero']
OCTOGONO_PERMITIDO = re.compile(r'revolver_cilindro_\d\.json$')

errores, avisos = [], []


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def opacos(im):
    return [(x, y) for y in range(im.height) for x in range(im.width) if im.getpixel((x, y))[3] > 0]


# 1. materiales
for n in MATERIALES:
    p = os.path.join(A, 'textures/item/armas3d', n + '.png')
    im = Image.open(p).convert('RGBA')
    cols = {im.getpixel(q)[:3] for q in opacos(im)}
    ls = sorted(lum(c) for c in cols)
    if len(cols) < 4:
        errores.append(f'material {n}: solo {len(cols)} tonos (vanilla usa 4-6). Recomendación: herramientas/texturas_estilo_mc.py')
    elif ls[-1] - ls[0] < 45:
        avisos.append(f'material {n}: poco contraste ({ls[-1] - ls[0]:.0f} de luminancia); se verá plano')

# 2 y 5 y 6: modelos
finas = collections.Counter()
estiradas = collections.Counter()
for ruta in sorted(glob.glob(os.path.join(A, 'models/item/**/*.json'), recursive=True)):
    m = json.load(open(ruta, encoding='utf-8'))
    els = m.get('elements', [])
    nombres = {e.get('name') for e in els}
    if not OCTOGONO_PERMITIDO.search(ruta):
        for e in els:
            n = e.get('name') or ''
            r = e.get('rotation')
            if r and abs(r.get('angle', 0)) == 45 and re.search(r'_[23]$', n) and n[:-2] + '_0' in nombres:
                errores.append(f'{os.path.relpath(ruta, A)}: «{n[:-2]}» es un octógono. Recomendación: herramientas/canones_cuadrados.py')
                break
    for e in els:
        d = [e['to'][k] - e['from'][k] for k in range(3)]
        caras = e.get('faces', {})
        if len(caras) > 1 and min(d) < 0.25:
            finas[os.path.basename(ruta)] += 1
        for cara, f in caras.items():
            if OCTOGONO_PERMITIDO.search(ruta):
                break  # el tambor usa a propósito una UV fija para el lateral (tambor_lado)
            uv = f.get('uv')
            if not uv:
                continue
            w, h = ((d[0], d[1]) if cara in ('north', 'south') else (d[2], d[1]) if cara in ('east', 'west') else (d[0], d[2]))
            du, dv = abs(uv[2] - uv[0]), abs(uv[3] - uv[1])
            if f.get('rotation', 0) in (90, 270):
                du, dv = dv, du
            for a, b in ((w, du), (h, dv)):
                if a >= 1 and b > 0 and not 0.5 <= b / a <= 2:
                    estiradas[os.path.basename(ruta)] += 1
                    break
for n, k in finas.most_common(5):
    avisos.append(f'{n}: {k} piezas de menos de 0,25 px de grueso (parpadean de lejos; en Minecraft, ≥0,5 px)')
for n, k in estiradas.most_common(5):
    avisos.append(f'{n}: {k} caras con la textura estirada o encogida más del doble (la densidad de píxeles cambia de una pieza a otra)')

# 3 y 4: iconos
for n in ARMAS:
    im = Image.open(os.path.join(A, 'textures/item', n + '.png')).convert('RGBA')
    op = set(opacos(im))
    # «grosor»: píxeles opacos con algún vecino opaco en las dos direcciones (horizontal y vertical)
    gruesos = sum(1 for (x, y) in op if ((x - 1, y) in op or (x + 1, y) in op) and ((x, y - 1) in op or (x, y + 1) in op)
                  and ((x - 1, y - 1) in op or (x + 1, y + 1) in op or (x + 1, y - 1) in op or (x - 1, y + 1) in op)
                  and len({(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)} & op) >= 6)
    if len(op) < 40 or gruesos < 12:
        errores.append(f'icono {n}: es un palito ({len(op)} píxeles, {gruesos} con cuerpo). Recomendación: herramientas/iconos_armas_nuevas.py')
    borde = [(x, y) for (x, y) in op if any((x + dx, y + dy) not in op for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    if borde:
        lum_borde = sum(lum(im.getpixel(q)) for q in borde) / len(borde)
        interior = [q for q in op if q not in set(borde)]
        if interior:
            lum_int = sum(lum(im.getpixel(q)) for q in interior) / len(interior)
            if lum_borde > lum_int - 8:
                avisos.append(f'icono {n}: el contorno no es más oscuro que el interior (vanilla bordea con el tono más oscuro)')

# 7. apuntado: cada arma que apunta tiene su Mira y su colocación coincide con el firstperson_righthand del modelo
#    (si no, al apuntar el arma no queda en el centro de la pantalla)
JAVA = os.path.join(RAIZ, 'common/src/main/java/com/copperslug/client/armasfuego/comun/Apuntado.java')
MIRAS = {'REVOLVER': 'revolver', 'WINCHESTER': 'winchester', 'DERRINGER': 'derringer', 'THOMPSON': 'thompson',
         'MOSQUETE': 'mosquete', 'CANON': 'canon_mano', 'CERBATANA': 'cerbatana', 'LANZALLAMAS': 'lanzallamas',
         'RESONANCIA': 'resonancia', 'ARPONERA': 'arponera'}
if os.path.exists(JAVA):
    java = open(JAVA, encoding='utf-8').read()
    for const, item in MIRAS.items():
        mm = re.search(r'Mira %s = new Mira\(([^)]*)\)' % const, java)
        if not mm:
            errores.append(f'apuntado: {item} no tiene Mira en Apuntado.java (al apuntar se queda en la cadera)')
            continue
        v = [float(x.strip().rstrip('F')) for x in mm.group(1).split(',')]
        if 'return %s;' % const not in java:
            errores.append(f'apuntado: la Mira {const} no se usa en mira(Item)')
        mod = json.load(open(os.path.join(A, 'models/item', item + '.json'), encoding='utf-8'))
        base = mod.get('base', mod)
        par = base.get('parent', '').split(':')[-1]
        disp = base.get('display') or json.load(open(os.path.join(A, 'models', par + '.json'), encoding='utf-8')).get('display', {})
        fp = disp.get('firstperson_righthand', {})
        esperado = fp.get('rotation', [0, 0, 0])[:2] + fp.get('translation', [0, 0, 0]) + fp.get('scale', [1])[:1]
        if any(abs(a - b) > 1e-3 for a, b in zip(v[:6], esperado)):
            errores.append(f'apuntado: la Mira de {item} ({v[:6]}) no coincide con su firstperson_righthand ({esperado})')

print('== Test de estilo Minecraft ==')
for e in errores:
    print('ERROR  ', e)
for a in avisos:
    print('AVISO  ', a)
print(f'{len(errores)} errores, {len(avisos)} avisos')
sys.exit(1 if errores else 0)

#!/usr/bin/env python3
"""Valida los modelos JSON de los objetos con las reglas de Minecraft que se incumplen sin avisar (el modelo falla al
cargar en el juego y se ve el cubo morado, pero el JSON es válido y compila): los ángulos de rotación de un elemento
solo pueden ser -45, -22.5, 0, 22.5 o 45; from/to entre -16 y 32; cada cara con una textura que exista en el mapa de
texturas (propio o del padre) y el eje x, y o z. Sale con error si algo falla. Uso: validar_modelos.py [raíz]
"""
import glob
import json
import os
import sys

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
M = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models')
ANGULOS = {-45, -22.5, 0, 22.5, 45}
errores = []


def padre_texturas(m):
    t = dict(m.get('textures', {}))
    p = m.get('parent')
    if p and p.startswith('copperslug:'):
        ruta = os.path.join(M, p.split(':', 1)[1] + '.json')
        if os.path.exists(ruta):
            t = {**padre_texturas(json.load(open(ruta, encoding='utf-8'))), **t}
    return t


for ruta in sorted(glob.glob(os.path.join(M, '**/*.json'), recursive=True)):
    nombre = os.path.relpath(ruta, M)
    try:
        m = json.load(open(ruta, encoding='utf-8'))
    except Exception as e:
        errores.append(f'{nombre}: no es JSON ({e})')
        continue
    if 'elements' not in m:
        continue
    tex = padre_texturas(m)
    for i, e in enumerate(m['elements']):
        r = e.get('rotation')
        if r:
            if r.get('angle') not in ANGULOS:
                errores.append(f'{nombre}: elemento {i} ({e.get("name", "")}): ángulo {r.get("angle")} no vale (solo -45, -22.5, 0, 22.5, 45)')
            if r.get('axis') not in ('x', 'y', 'z'):
                errores.append(f'{nombre}: elemento {i}: eje {r.get("axis")} no vale')
        for v in list(e['from']) + list(e['to']):
            if not -16 <= v <= 32:
                errores.append(f'{nombre}: elemento {i}: coordenada {v} fuera de -16..32')
        for d, c in e.get('faces', {}).items():
            k = c.get('texture', '')
            if k.startswith('#') and k[1:] not in tex:
                errores.append(f'{nombre}: elemento {i} cara {d}: textura {k} no está en el mapa de texturas')

for e in errores[:60]:
    print(e)
if errores:
    print(f'{len(errores)} errores en los modelos')
    sys.exit(1)
print('modelos válidos')

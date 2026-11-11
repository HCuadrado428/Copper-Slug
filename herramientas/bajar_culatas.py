#!/usr/bin/env python3
"""Baja y estrecha la parte de atrás de las culatas del mosquete y de la Winchester.

Apuntando, el ojo queda justo detrás de la mira, y una culata más alta que la línea de mira se veía como una rampa
marrón enorme (y la placa de latón del final, como una columna amarilla suelta). Con el peine más bajo y más estrecho
hacia atrás, como en una culata de verdad, esa parte queda por debajo de lo que se ve. Es idempotente y solo toca las
piezas que busca por sus medidas originales. Uso: bajar_culatas.py [raíz del repositorio]
"""
import glob
import json
import os
import sys

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
A3D = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item/armas3d')

# (patrón de archivo, (from, to) original) -> (from, to) nuevos
CAMBIOS = [
    ('mosquete_3d*.json', ([7.0, 5.5, 15], [9.0, 10, 24]), ([7.25, 5.5, 15], [8.75, 8.8, 24])),
    ('mosquete_3d*.json', ([6.9, 3.9, 24], [9.1, 10.1, 24.5]), ([7.15, 3.9, 24], [8.85, 8.9, 24.5])),
    ('winchester_3d*.json', ([7.0, 6.5, 13.5], [9.0, 10.25, 20]), ([7.2, 6.5, 13.5], [8.8, 9.1, 20])),
    ('winchester_3d*.json', ([6.9, 4.65, 20], [9.1, 10.35, 20.5]), ([7.1, 4.65, 20], [8.9, 9.2, 20.5])),
    ('winchester_3d*.json', ([7.25, 6.0, 10.5], [8.75, 10.5, 13.5]), ([7.4, 6.0, 10.5], [8.6, 9.6, 13.5])),
    # la tapa del armazón por debajo de la línea de mira (si no, tapa las miras con el ojo detrás)
    ('winchester_3d*.json', ([6.75, 7.0, 3.5], [9.25, 11.25, 10.5]), ([6.75, 7.0, 3.5], [9.25, 10.75, 10.5])),
]


def igual(a, b):
    return all(abs(x - y) < 1e-6 for x, y in zip(a, b))


# las chapas laterales de latón del armazón de la Winchester, casi planas, se veían desde atrás como una raya amarilla suelta
CHAPAS = [([9.25, 8.0, 5.0], [9.4, 9.5, 7.5]), ([6.6, 8.2, 8.0], [6.75, 9.2, 9.0])]


def chapas_a_cobre():
    n = 0
    for ruta in sorted(glob.glob(os.path.join(A3D, 'winchester_3d*.json'))):
        m = json.load(open(ruta, encoding='utf-8'))
        tocado = False
        for e in m['elements']:
            if any(igual(e['from'], f) and igual(e['to'], t) for f, t in CHAPAS):
                for c in e['faces'].values():
                    if c['texture'] != '#cobre':
                        c['texture'] = '#cobre'
                        tocado = True
        if tocado:
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(m, f, indent=1, ensure_ascii=False)
                f.write('\n')
            n += 1
    return n


def martillo_y_chapas():
    """El martillo de la Winchester pasaba de la línea de mira (tapaba lo de delante) y las chapas laterales, de 0,15 de grueso,
    se veían como una raya diagonal: martillo 1,6 más abajo y chapas casi planas."""
    n = 0
    for ruta in sorted(glob.glob(os.path.join(A3D, 'winchester_3d*.json'))):
        m = json.load(open(ruta, encoding='utf-8'))
        tocado = False
        for e in m['elements']:
            if igual(e['from'], [7.6, 10.5, 10]) and igual(e['to'], [8.4, 12.5, 11]):
                e['from'][1] -= 1.6
                e['to'][1] -= 1.6
                if 'rotation' in e:
                    e['rotation']['origin'][1] -= 1.6
                tocado = True
            elif igual(e['from'], [9.25, 8.0, 5.0]) and igual(e['to'], [9.4, 9.5, 7.5]):
                e['to'][0] = 9.28
                tocado = True
            elif igual(e['from'], [6.6, 8.2, 8.0]) and igual(e['to'], [6.75, 9.2, 9.0]):
                e['from'][0] = 6.72
                tocado = True
        if tocado:
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(m, f, indent=1, ensure_ascii=False)
                f.write('\n')
            n += 1
    return n


def main():
    martillo_y_chapas()
    total = chapas_a_cobre()
    for patron, (f0, t0), (f1, t1) in CAMBIOS:
        for ruta in sorted(glob.glob(os.path.join(A3D, patron))):
            m = json.load(open(ruta, encoding='utf-8'))
            tocado = False
            for e in m['elements']:
                if igual(e['from'], f0) and igual(e['to'], t0):
                    e['from'], e['to'] = list(f1), list(t1)
                    tocado = True
                    total += 1
            if tocado:
                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump(m, f, indent=1, ensure_ascii=False)
                    f.write('\n')
    print('piezas ajustadas:', total)


main()

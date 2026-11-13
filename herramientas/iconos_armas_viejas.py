#!/usr/bin/env python3
"""Los iconos de inventario de la escopeta de presión, la Thompson y el Winchester, redibujados para que se parezcan a
sus modelos 3D actuales.

Tras rehacer los modelos los iconos viejos ya no cuadraban: la escopeta no tenía depósito ni bomba, la Thompson no
tenía su tambor redondo de la mafia y el Winchester y la Thompson se confundían (los dos en diagonal y del mismo
color). Ahora:
- escopeta de presión: horizontal; culata, cajón de cobre con el manómetro encima, cañón de hierro, depósito de cobre
  con aros de latón y el mango de la bomba debajo. La aguja del manómetro cambia de color con la presión (fases 0 a 4)
  y la reventada lleva el manómetro roto, el cañón abierto y una nube de vapor.
- Thompson: horizontal, con el tambor redondo bajo el cajón, la empuñadura delantera y las aletas del cañón.
- Winchester: en diagonal como el resto de armas largas, cajón de cobre con placa de latón, cañón de acero, tubo
  cargador debajo y la palanca.
Cada uno con la rampa de cobre de su fase de óxido (texturas_estilo_mc.COBRE).

Uso: herramientas/iconos_armas_viejas.py [--salida DIR]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texturas_estilo_mc import COBRE, HIERRO, ACERO, LATON, MADERA  # noqa: E402
from iconos_armas_nuevas import Lienzo, empunadura, DIR  # noqa: E402

# color de la aguja del manómetro por fase de presión (los mismos que los iconos de antes)
AGUJA = [(244, 240, 220), (91, 208, 58), (216, 224, 64), (240, 160, 32), (212, 42, 27)]
CREMA = (244, 240, 220)
VAPOR = [(200, 204, 210), (232, 234, 238)]
OXIDO = ['', 'expuesta', 'erosionada', 'oxidada']


def disco(l, x0, y0, filas, tonos):
    for j, fila in enumerate(filas):
        for i, ch in enumerate(fila):
            if ch != '.':
                l.px(x0 + i, y0 + j, tonos[ch])


def escopeta(c, fase):
    """fase: 0..4 o 'reventada'."""
    l = Lienzo()
    rev = fase == 'reventada'
    # culata, más alta en la cantonera
    l.caja(0, 6, 2, 11, MADERA)
    l.caja(2, 6, 5, 9, MADERA)
    l.px(1, 7, MADERA[4])
    # cañón de hierro encima y depósito de cobre debajo, con aros de latón
    l.caja(8, 4, 15, 6, HIERRO)
    l.caja(8, 7, 14, 10, c)
    l.col(10, 7, 10, LATON)
    l.col(13, 7, 10, LATON)
    l.px(15, 8, HIERRO[0])
    l.px(15, 9, HIERRO[1])
    # mango de la bomba
    l.caja(9, 11, 12, 12, MADERA)
    # cajón de cobre
    l.caja(4, 5, 8, 10, c)
    # guardamonte
    for (x, y) in ((5, 11), (5, 12), (6, 13), (7, 12), (7, 11)):
        l.px(x, y, HIERRO[0])
    # manómetro redondo encima del cajón: aro de latón y esfera crema con la aguja
    aguja = (47, 47, 51) if rev else AGUJA[fase]
    disco(l, 4, 1, ['.##.', '#ab#', '#cd#', '.##.'],
          {'#': LATON[0], 'a': CREMA, 'b': aguja, 'c': (214, 208, 184), 'd': (47, 47, 51) if rev else CREMA})
    l.px(5, 1, LATON[3])
    if rev:
        # cañón abierto y vapor
        l.px(13, 4, (30, 30, 34))
        l.px(13, 5, HIERRO[3])
        l.px(14, 3, HIERRO[1])
        for (x, y, k) in ((9, 2, 0), (10, 1, 1), (11, 2, 1), (12, 1, 0), (2, 3, 0), (1, 4, 1), (14, 1, 1), (13, 0, 0)):
            l.px(x, y, VAPOR[k])
    return l.imagen()


def thompson(c):
    l = Lienzo()
    # culata
    l.caja(0, 4, 3, 8, MADERA)
    l.px(1, 5, MADERA[4])
    # cañón con aletas de refrigeración y compensador
    l.caja(9, 4, 14, 6, HIERRO)
    for x in (10, 12):
        l.px(x, 3, c[1])
        l.px(x, 7, c[1])
    l.caja(14, 3, 15, 7, HIERRO)
    # cajón de cobre
    l.caja(3, 3, 10, 7, c)
    l.px(7, 2, HIERRO[0])
    l.px(8, 2, HIERRO[2])
    # empuñadura delantera
    l.caja(11, 7, 13, 10, MADERA)
    # empuñadura de pistola
    empunadura(l, 3, 8, 12)
    # cuello del cargador
    l.px(7, 8, HIERRO[0])
    l.px(8, 8, HIERRO[2])
    l.px(9, 8, HIERRO[0])
    # tambor redondo de la mafia: disco de cobre con buje de latón
    disco(l, 5, 9, ['.####.', '#hhhm#', '#mbbm#', '#mbds#', '#msss#', '.####.'],
          {'#': c[0], 'h': c[3], 'm': c[2], 's': c[1], 'b': LATON[3], 'd': LATON[1]})
    return l.imagen()


def winchester(c):
    l = Lienzo()
    # culata abajo a la izquierda
    l.caja(0, 11, 3, 15, MADERA)
    l.caja(3, 10, 6, 13, MADERA)
    l.col(0, 11, 15, LATON)
    # cañón de acero en diagonal y tubo cargador de latón debajo (bandas de x + y)
    banda = {14: ACERO[0], 15: ACERO[3], 16: ACERO[2], 17: LATON[3], 18: LATON[1], 19: LATON[0]}
    for y in range(16):
        for x in range(9, 16):
            s = x + y
            if s in banda and (s <= 16 or x <= 13) and y <= 8:
                l.px(x, y, banda[s])
    l.px(14, 5, ACERO[0])
    l.px(15, 4, ACERO[0])
    l.px(15, 0, ACERO[4])
    # cajón de cobre con su placa de latón
    l.caja(5, 7, 10, 11, c)
    l.px(7, 9, LATON[3])
    l.px(8, 9, LATON[2])
    # palanca
    for (x, y) in ((6, 12), (6, 13), (7, 14), (8, 14), (9, 13), (9, 12)):
        l.px(x, y, HIERRO[0])
    l.px(7, 12, HIERRO[2])
    l.px(8, 12, HIERRO[2])
    return l.imagen()


def generar(salida):
    for ox, rampa in enumerate(COBRE):
        suf = '' if ox == 0 else '_ox%d' % ox
        thompson(rampa).save(os.path.join(salida, 'thompson' + suf + '.png'))
        winchester(rampa).save(os.path.join(salida, 'winchester' + suf + '.png'))
        pre = 'escopeta_presion_' + (OXIDO[ox] + '_' if ox else '')
        for fase in list(range(5)) + ['reventada']:
            escopeta(rampa, fase).save(os.path.join(salida, pre + str(fase) + '.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--salida', default=DIR)
    generar(ap.parse_args().salida)

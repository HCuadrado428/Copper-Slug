#!/usr/bin/env python3
"""Los iconos de la cartuchera y la funda de cadera (16x16, estilo vanilla: contorno oscuro y luz de arriba a la izquierda).

Uso: herramientas/iconos_cinturon.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iconos_armas_nuevas import Lienzo, DIR  # noqa: E402
from texturas_estilo_mc import CUERO, LATON, MADERA, COBRE, HIERRO  # noqa: E402


def cartuchera():
    """Un cinturón enrollado en óvalo, con hebilla de latón y una fila de cartuchos."""
    l = Lienzo()
    # el cinto: un anillo de cuero
    for y in range(3, 13):
        for x in range(1, 15):
            dx, dy = (x - 7.5) / 6.6, (y - 7.5) / 4.6
            r = dx * dx + dy * dy
            if 0.45 <= r <= 1.0:
                borde = r > 0.86 or r < 0.55
                l.px(x, y, CUERO[0] if borde else (CUERO[3] if y < 7 else CUERO[2]))
    # cartuchos en la parte de arriba del anillo
    for x in (3, 5, 7, 9, 11):
        y = 2 if x in (5, 7, 9) else 3
        l.px(x, y, LATON[4])
        l.px(x, y + 1, LATON[2])
        l.px(x + 1, y, LATON[1])
        l.px(x + 1, y + 1, LATON[0])
    # hebilla
    l.caja(6, 10, 9, 13, LATON)
    l.px(7, 11, CUERO[1])
    l.px(8, 11, CUERO[1])
    return l.imagen()


def funda():
    """La funda de cuero vista de lado, con la culata de un revólver asomando."""
    l = Lienzo()
    # culata y martillo
    l.caja(8, 1, 11, 5, MADERA)
    l.px(9, 2, MADERA[4])
    l.px(7, 4, HIERRO[2])
    l.px(7, 5, HIERRO[0])
    l.caja(8, 0, 11, 1, COBRE[0])
    # la funda: ancha arriba y estrecha abajo
    for y in range(5, 15):
        x1 = 4 + (y - 5) // 3
        x2 = 11 - (y - 5) // 4
        for x in range(x1, x2 + 1):
            if x in (x1, x2) or y == 14:
                c = CUERO[0]
            elif x == x1 + 1:
                c = CUERO[3]
            else:
                c = CUERO[2]
            l.px(x, y, c)
    # costura y remache
    for y in range(7, 13, 2):
        l.px(9, y, CUERO[4])
    l.px(6, 7, LATON[3])
    # la correa del cinto
    for x in range(1, 15):
        l.px(x, 5, CUERO[1] if x in (1, 14) else CUERO[3])
        l.px(x, 6, CUERO[0] if x in (1, 14) else CUERO[1])
    return l.imagen()


if __name__ == '__main__':
    cartuchera().save(os.path.join(DIR, 'cartuchera.png'))
    funda().save(os.path.join(DIR, 'funda.png'))


def granada(color):
    """Una granada de cobre en forma de piña, con la anilla de hierro y una banda del color de su tipo."""
    from texturas_estilo_mc import COBRE as CB
    l = Lienzo()
    c = CB[0]
    for y in range(4, 15):
        for x in range(3, 13):
            dx, dy = (x - 7.5) / 4.6, (y - 9.3) / 5.4
            if dx * dx + dy * dy <= 1.0:
                borde = dx * dx + dy * dy > 0.72
                cuad = (x + y) % 3 == 0
                l.px(x, y, c[0] if borde else (c[4] if x < 6 and y < 8 else c[1] if cuad else c[3] if x < 8 else c[2]))
    # la banda del tipo
    for x in range(4, 12):
        for y in (9, 10):
            if l.p[y][x] and l.p[y][x] != c[0]:
                l.px(x, y, color[3] if y == 9 else color[1])
    # espoleta y anilla
    l.caja(6, 2, 9, 4, HIERRO)
    for (x, y) in ((10, 1), (11, 1), (12, 2), (12, 3), (11, 4), (10, 3)):
        l.px(x, y, HIERRO[3] if y < 3 else HIERRO[1])
    l.px(9, 1, HIERRO[0])
    return l.imagen()


if __name__ == '__main__':
    GRIS = [(70, 70, 74), (110, 110, 116), (150, 150, 156), (196, 196, 200), (230, 230, 234)]
    ROJO = [(90, 20, 14), (150, 36, 24), (196, 56, 36), (230, 90, 60), (250, 150, 120)]
    MIEL = [(130, 80, 10), (190, 120, 20), (230, 160, 30), (250, 200, 60), (255, 230, 140)]
    for n, col in (('granada_humo', GRIS), ('granada_metralla', ROJO), ('granada_miel', MIEL)):
        granada(col).save(os.path.join(DIR, n + '.png'))

#!/usr/bin/env python3
"""Los iconos de inventario de las cuatro armas nuevas (cerbatana, lanzallamas, pistola de resonancia y arponera), con
estilo Minecraft.

Los de antes eran palitos de un píxel: no se parecían a su modelo 3D y desentonaban al lado del revólver, la escopeta o la
Gatling. Estos se dibujan como los objetos de vanilla: piezas enteras con contorno oscuro, luz desde arriba a la izquierda
(fila clara arriba, fila de sombra abajo) y las mismas rampas de cobre de cinco tonos que los materiales de los modelos
(texturas_estilo_mc.py), un icono por fase de óxido: <arma>.png, <arma>_ox1.png, _ox2.png y _ox3.png.

Uso: herramientas/iconos_armas_nuevas.py [--salida DIR]
"""
import argparse
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texturas_estilo_mc import COBRE, HIERRO, ACERO, LATON, MADERA, CUERO  # noqa: E402

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'common', 'src', 'main', 'resources', 'assets',
                   'copperslug', 'textures', 'item')
ECO = [(6, 58, 68), (14, 94, 104), (30, 140, 150), (70, 205, 210), (170, 250, 245)]
FUEGO = [(120, 30, 10), (200, 60, 20), (240, 120, 30), (252, 190, 60), (255, 240, 150)]
CUERDA = [(92, 70, 40), (130, 100, 60), (170, 140, 90), (200, 175, 120), (230, 210, 160)]


class Lienzo:
    def __init__(self):
        self.p = [[None] * 16 for _ in range(16)]

    def px(self, x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            self.p[y][x] = c

    def caja(self, x1, y1, x2, y2, r, borde=True):
        """Una pieza maciza: contorno oscuro, fila clara arriba, fila de sombra abajo y un brillo en la esquina."""
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if borde and (x in (x1, x2) or y in (y1, y2)):
                    c = r[0]
                else:
                    iy1, iy2 = (y1 + 1, y2 - 1) if borde else (y1, y2)
                    if iy1 == iy2:
                        c = r[3]
                    elif y == iy1:
                        c = r[3]
                    elif y == iy2:
                        c = r[1]
                    else:
                        c = r[2]
                self.px(x, y, c)
        if borde and x2 - x1 >= 3 and y2 - y1 >= 3:
            self.px(x1 + 1, y1 + 1, r[4])

    def col(self, x, y1, y2, r):
        """Una banda vertical (aros, bobinas): oscura en los extremos y clara en medio."""
        for y in range(y1, y2 + 1):
            self.px(x, y, r[0] if y in (y1, y2) else (r[3] if y == y1 + 1 else r[2]))

    def imagen(self):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        for y in range(16):
            for x in range(16):
                if self.p[y][x]:
                    im.putpixel((x, y), tuple(self.p[y][x]) + (255,))
        return im


def empunadura(l, x, y1, y2, r=MADERA):
    """Una empuñadura de pistola inclinada hacia atrás (un píxel cada dos filas), de madera con contorno."""
    for i, y in enumerate(range(y1, y2 + 1)):
        dx = -(i // 2)
        l.px(x + dx, y, r[0])
        l.px(x + dx + 1, y, r[3] if i % 2 == 0 else r[2])
        l.px(x + dx + 2, y, r[1])
        l.px(x + dx + 3, y, r[0])
    # el culo de la empuñadura
    dx = -((y2 - y1) // 2)
    for k in range(4):
        l.px(x + dx + k, y2 + 1, r[0])


def lanzallamas(c):
    """Tipo fusil: boquilla ancha a la derecha, escudo de calor, depósito debajo y culata de tubo a la izquierda."""
    l = Lienzo()
    # culata de tubo
    l.caja(0, 4, 1, 9, MADERA)
    for x in range(1, 5):
        l.px(x, 4, c[0])
        l.px(x, 5, c[3])
        l.px(x, 8, c[1])
        l.px(x, 9, c[0])
    empunadura(l, 4, 9, 12)
    l.caja(8, 9, 12, 12, ACERO)
    l.col(9, 9, 12, LATON)
    l.col(11, 9, 12, LATON)
    l.caja(4, 4, 9, 9, c)
    l.caja(8, 5, 13, 8, c)
    for x in range(8, 13):
        l.px(x, 4, HIERRO[0] if x in (8, 12) else HIERRO[3])
    l.caja(12, 3, 14, 9, HIERRO)
    l.px(15, 5, FUEGO[3])
    l.px(15, 6, FUEGO[2])
    l.px(15, 7, FUEGO[1])
    l.px(13, 10, LATON[3])
    l.px(13, 11, FUEGO[2])
    l.px(7, 10, HIERRO[2])
    return l.imagen()


def resonancia(c):
    """Pistola: corredera de cobre, bobinas de eco encima y la bocina emisora en la boca."""
    l = Lienzo()
    empunadura(l, 4, 9, 13)
    l.caja(2, 5, 11, 9, c)
    for x in (5, 7, 9):
        l.px(x, 4, ECO[3])
        l.px(x + 1, 4, ECO[1])
    l.caja(10, 6, 12, 8, ECO)
    # la bocina, más ancha que el cañón
    l.caja(12, 3, 14, 11, c)
    for y in range(5, 10):
        l.px(15, y, ECO[3] if y in (6, 7) else ECO[1])
    l.px(13, 7, ECO[4])
    l.px(1, 5, HIERRO[2])
    l.px(1, 6, HIERRO[0])
    # guardamonte
    l.px(7, 10, HIERRO[1])
    l.px(8, 11, HIERRO[0])
    l.px(9, 11, HIERRO[0])
    l.px(8, 10, HIERRO[3])
    return l.imagen()


def arponera(c):
    """Fusil submarino: el arpón encima del cañón, con la punta a la derecha, el carrete debajo y la culata."""
    l = Lienzo()
    # arpón
    for x in range(2, 14):
        l.px(x, 5, ACERO[4] if x % 4 else ACERO[3])
        l.px(x, 6, ACERO[1])
    for (x, y) in ((13, 4), (14, 5), (15, 6), (14, 6), (13, 7), (12, 3), (12, 8)):
        l.px(x, y, ACERO[3] if y <= 5 else ACERO[1])
    l.px(15, 5, ACERO[0])
    # cañón y cabeza
    l.caja(1, 7, 11, 9, c)
    l.caja(10, 6, 12, 10, c)
    l.px(11, 8, CUERO[2])
    # culata
    l.caja(0, 6, 1, 10, MADERA)
    empunadura(l, 3, 10, 13)
    # carrete
    l.caja(6, 9, 9, 12, HIERRO)
    l.px(7, 10, CUERDA[3])
    l.px(8, 10, CUERDA[2])
    l.px(7, 11, CUERDA[2])
    l.px(8, 11, CUERDA[3])
    return l.imagen()


def cerbatana(c):
    """Carabina de dardos en diagonal, como las armas largas: culata abajo a la izquierda y boca arriba a la derecha."""
    l = Lienzo()
    # culata y cámara de aire
    l.caja(0, 11, 4, 14, MADERA)
    l.caja(3, 9, 6, 12, c)
    l.caja(4, 12, 6, 14, CUERO)
    # el cañón en diagonal (dos píxeles, contorno oscuro debajo)
    for i in range(10):
        x, y = 5 + i, 9 - i
        l.px(x, y, c[3])
        l.px(x + 1, y, c[2])
        l.px(x + 1, y + 1, c[0])
        l.px(x, y - 1, c[0])
    for i in (3, 7):
        x, y = 5 + i, 9 - i
        l.px(x, y, LATON[3])
        l.px(x + 1, y, LATON[2])
    l.px(15, 0, HIERRO[0])
    l.px(14, 0, HIERRO[2])
    # dos plumas de dardo asomando del carcaj
    l.px(8, 9, (90, 200, 90))
    l.px(9, 9, (200, 200, 210))
    l.px(8, 10, CUERO[1])
    l.px(9, 10, CUERO[2])
    return l.imagen()


ARMAS = {'lanzallamas': lanzallamas, 'resonancia': resonancia, 'arponera': arponera, 'cerbatana': cerbatana}


def generar(salida):
    for nombre, f in ARMAS.items():
        for ox, rampa in enumerate(COBRE):
            f(rampa).save(os.path.join(salida, nombre + ('' if ox == 0 else '_ox%d' % ox) + '.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--salida', default=DIR)
    generar(ap.parse_args().salida)

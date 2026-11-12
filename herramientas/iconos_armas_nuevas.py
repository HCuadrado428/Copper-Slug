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
    l = Lienzo()
    # el depósito bajo el cañón (acero, con bandas de latón)
    l.caja(6, 8, 12, 12, ACERO)
    l.col(8, 8, 12, LATON)
    l.col(11, 8, 12, LATON)
    empunadura(l, 2, 8, 12)
    # cuerpo y cañón
    l.caja(1, 3, 6, 8, c)
    l.caja(5, 4, 13, 7, c)
    for x in (8, 10):
        l.col(x, 4, 7, HIERRO)
    # boquilla ancha y llama piloto
    l.caja(12, 3, 14, 8, HIERRO)
    l.px(15, 5, FUEGO[3])
    l.px(15, 6, FUEGO[2])
    l.px(15, 4, FUEGO[1])
    l.px(14, 2, FUEGO[2])
    l.px(14, 1, FUEGO[3])
    # gatillo
    l.px(6, 9, HIERRO[2])
    l.px(5, 10, HIERRO[1])
    return l.imagen()


def resonancia(c):
    l = Lienzo()
    empunadura(l, 3, 8, 13)
    l.caja(2, 4, 8, 9, c)
    l.caja(7, 5, 14, 8, c)
    # las bobinas de eco a lo largo del cañón
    for x in (9, 11, 13):
        l.col(x, 4, 9, ECO)
    l.caja(14, 4, 15, 9, c)
    l.px(15, 6, ECO[3])
    l.px(15, 7, ECO[2])
    # el fragmento de eco encima
    l.caja(3, 1, 6, 4, ECO)
    l.px(4, 2, ECO[4])
    # emblema de latón
    l.px(5, 6, LATON[3])
    l.px(5, 7, LATON[1])
    l.px(7, 10, HIERRO[2])
    return l.imagen()


def arponera(c):
    l = Lienzo()
    empunadura(l, 2, 8, 13)
    l.caja(1, 4, 9, 8, c)
    # el carrete de cuerda bajo el cuerpo
    l.caja(5, 8, 9, 12, HIERRO)
    for y in (9, 10, 11):
        for x in (6, 7, 8):
            l.px(x, y, CUERDA[3] if (x + y) % 2 else CUERDA[2])
    # aro delantero
    l.caja(9, 3, 10, 9, c)
    # varilla y punta del arpón
    for x in range(11, 14):
        l.px(x, 5, ACERO[4])
        l.px(x, 6, ACERO[1])
    for y, (x1, x2) in {3: (12, 12), 4: (12, 13), 5: (13, 14), 6: (13, 15), 7: (12, 14), 8: (12, 12)}.items():
        for x in range(x1, x2 + 1):
            l.px(x, y, ACERO[3] if y <= 5 else ACERO[1])
    l.px(15, 6, ACERO[0])
    l.px(14, 5, ACERO[4])
    return l.imagen()


def cerbatana(c):
    l = Lienzo()
    # un tubo de cobre de dos píxeles en diagonal, como el arco y la caña de vanilla: contorno oscuro bajo el tubo
    for i in range(13):
        x, y = 2 + i, 13 - i
        l.px(x, y, c[3])
        l.px(x + 1, y, c[2])
        l.px(x + 1, y + 1, c[0])
        l.px(x, y + 1, c[1])
        l.px(x - 1, y, c[0])
        l.px(x, y - 1, c[0])
    # bandas de latón
    for i in (4, 8):
        x, y = 2 + i, 13 - i
        for (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1)):
            l.px(x + dx, y + dy, LATON[3] if dy == 0 else LATON[1])
    # boquilla de madera
    for (x, y) in ((1, 14), (2, 14), (1, 13), (2, 13), (0, 14), (1, 15)):
        l.px(x, y, MADERA[0])
    l.px(2, 13, MADERA[3])
    l.px(1, 14, MADERA[2])
    # boca de hierro
    l.px(14, 1, HIERRO[3])
    l.px(15, 1, HIERRO[0])
    l.px(14, 0, HIERRO[0])
    l.px(15, 2, HIERRO[0])
    # el carcaj de dardos colgado en medio, con dos plumas
    l.caja(8, 9, 10, 13, CUERO)
    l.px(9, 8, (90, 200, 90))
    l.px(10, 8, (200, 200, 210))
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

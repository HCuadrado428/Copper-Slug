#!/usr/bin/env python3
"""Las texturas de material de los modelos 3D (armas3d/*.png) con el estilo de las de vanilla.

Antes eran tres tonos con manchas cuadradas al azar: de lejos el cobre se veía plano, como plástico. Aquí cada material
tiene una rampa de cinco tonos (como los bloques de vanilla: sombra, oscuro, base, claro y brillo) y un dibujo con
estructura: el metal lleva vetas horizontales de cepillado y algún poro, la madera vetas largas y algún nudo, el cuero
grano y el latón el brillo del oro de vanilla. El cobre expuesto y el erosionado conservan pintas de la fase anterior,
como el cobre de vanilla, y el oxidado lleva manchas de pátina más clara.

Todo es determinista (semilla fija): volver a ejecutarlo da los mismos píxeles. Las texturas siguen siendo de 16x16
(la prueba a2c_texturas_16 lo exige).

Uso: herramientas/texturas_estilo_mc.py [--salida DIR]
"""
import argparse
import os
import random

from PIL import Image

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'common', 'src', 'main', 'resources', 'assets',
                   'copperslug', 'textures', 'item', 'armas3d')

# rampas: sombra, oscuro, base, claro, brillo (los tonos de en medio son los de los bloques de cobre de vanilla)
COBRE = [
    [(125, 52, 31), (163, 72, 43), (193, 90, 54), (231, 124, 86), (252, 163, 134)],
    [(102, 70, 60), (135, 96, 82), (161, 125, 103), (186, 147, 125), (212, 176, 152)],
    [(45, 88, 62), (62, 111, 80), (90, 140, 103), (108, 164, 116), (148, 196, 148)],
    [(36, 92, 76), (52, 120, 100), (79, 158, 128), (98, 182, 148), (139, 214, 180)],
]
HIERRO = [(34, 35, 40), (52, 54, 60), (72, 74, 82), (95, 98, 107), (128, 132, 142)]
ACERO = [(78, 83, 90), (104, 110, 118), (133, 139, 147), (163, 169, 177), (205, 210, 216)]
LATON = [(140, 92, 20), (186, 130, 32), (217, 169, 43), (240, 200, 74), (252, 236, 150)]
MADERA = [(58, 34, 15), (79, 48, 21), (99, 61, 28), (122, 77, 36), (146, 95, 46)]
G_MADERA = [(86, 53, 23), (111, 69, 31), (137, 88, 41), (163, 109, 53), (189, 133, 70)]
CUERO = [(36, 19, 11), (56, 32, 19), (76, 44, 27), (100, 60, 37), (130, 82, 52)]


def lienzo(base):
    return [[base for _ in range(16)] for _ in range(16)]


def guardar(px, nombre, salida):
    im = Image.new('RGBA', (16, 16))
    for y in range(16):
        for x in range(16):
            im.putpixel((x, y), tuple(px[y][x]) + (255,))
    im.save(os.path.join(salida, nombre + '.png'))


def metal(r, rng, vetas=True, poros=6, brillos=5):
    """Metal cepillado: base, vetas horizontales claras y oscuras (que siguen el cañón en las caras de lado), poros y
    brillos sueltos. Las filas 0 y 15 algo más claras/oscuras para que las piezas grandes tengan canto."""
    px = lienzo(r[2])
    if vetas:
        for y in range(16):
            x = rng.randrange(16)
            while x < 16 + 16:
                largo = rng.randint(2, 6)
                tono = rng.choice((1, 3, 3, 3, 2))
                for k in range(largo):
                    px[y][(x + k) % 16] = r[tono]
                x += largo + rng.randint(3, 9)
    for _ in range(poros):
        x, y = rng.randrange(16), rng.randrange(16)
        px[y][x] = r[0]
        if rng.random() < 0.5:
            px[y][(x + 1) % 16] = r[1]
    for _ in range(brillos):
        x, y = rng.randrange(16), rng.randrange(16)
        px[y][x] = r[4]
    return px


def pintas(px, r, rng, n, tam=(1, 2)):
    """Manchas pequeñas de otra rampa (las pintas de la fase anterior del cobre, o la pátina)."""
    for _ in range(n):
        cx, cy = rng.randrange(16), rng.randrange(16)
        w = rng.randint(*tam)
        for dy in range(w):
            for dx in range(w + rng.randint(0, 1)):
                if rng.random() < 0.8:
                    px[(cy + dy) % 16][(cx + dx) % 16] = r[rng.choice((1, 2, 2, 3))]
    return px


def madera(r, rng):
    """Vetas largas a lo ancho (siguen la culata en las caras de lado), una línea oscura cada pocas filas y algún nudo."""
    px = lienzo(r[2])
    y = 0
    while y < 16:
        alto = rng.randint(2, 4)
        tono = rng.choice((2, 2, 3, 1))
        for yy in range(y, min(16, y + alto)):
            for x in range(16):
                px[yy][x] = r[tono]
        # una veta oscura que corta la franja
        yy = min(15, y + alto - 1)
        x = rng.randrange(16)
        for k in range(rng.randint(5, 11)):
            px[yy][(x + k) % 16] = r[1]
        # alguna veta clara
        if rng.random() < 0.7:
            yy = y
            x = rng.randrange(16)
            for k in range(rng.randint(3, 7)):
                px[yy][(x + k) % 16] = r[min(4, tono + 1)]
        y += alto
    for _ in range(2):
        x, y = rng.randrange(1, 15), rng.randrange(1, 15)
        px[y][x] = r[0]
        px[y][x + 1] = r[1]
        px[y - 1][x] = r[1]
    return px


def cuero(r, rng):
    px = lienzo(r[2])
    for y in range(16):
        for x in range(16):
            v = rng.random()
            if v < 0.18:
                px[y][x] = r[1]
            elif v < 0.30:
                px[y][x] = r[3]
            elif v < 0.33:
                px[y][x] = r[0]
            elif v < 0.35:
                px[y][x] = r[4]
    return px


def generar(salida):
    os.makedirs(salida, exist_ok=True)
    for i, r in enumerate(COBRE):
        rng = random.Random(1000 + i)
        px = metal(r, rng)
        if i in (1, 2):
            # el expuesto conserva pintas naranjas; el erosionado, pintas del expuesto (como el cobre de vanilla)
            pintas(px, COBRE[i - 1], rng, 7 if i == 1 else 9)
        if i == 3:
            # la pátina del oxidado: manchas más claras
            for _ in range(6):
                x, y = rng.randrange(16), rng.randrange(16)
                px[y][x] = r[4]
                px[y][(x + 1) % 16] = r[3]
        guardar(px, 'cobre_%d' % i, salida)
    guardar(metal(HIERRO, random.Random(2001), poros=5, brillos=3), 'hierro', salida)
    guardar(metal(ACERO, random.Random(2002), poros=4, brillos=6), 'g_acero', salida)
    guardar(metal(LATON, random.Random(2003), poros=3, brillos=7), 'laton', salida)
    guardar(madera(MADERA, random.Random(3001)), 'madera', salida)
    guardar(madera(G_MADERA, random.Random(3002)), 'g_madera', salida)
    guardar(cuero(CUERO, random.Random(4001)), 'g_cuero', salida)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--salida', default=DIR)
    generar(ap.parse_args().salida)

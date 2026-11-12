#!/usr/bin/env python3
"""Las texturas de las partículas de las armas, en píxeles de 8x8 como las de vanilla (sin degradados ni suavizado).

- armafuego_fogonazo_0..3: el fogonazo en cuatro fotogramas (estrella blanca y amarilla, llamarada naranja, rescoldo y
  una voluta), que la partícula pasa según su edad.
- armafuego_humo_0..3: el humo de pólvora, de bocanada densa a nube que se deshace.
- armafuego_chispa_0..1: la chispa del metal, de 2x2 a 1 píxel.
- armafuego_marca_0..1: el agujero de bala que se queda en el bloque (dos variantes).
- armafuego_casquillo_0..1: el casquillo de latón, de lado y de frente.

Uso: herramientas/generar_particulas.py
"""
import os

from PIL import Image

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'common', 'src', 'main', 'resources', 'assets',
                   'copperslug', 'textures', 'particle')

PAL = {
    '.': None,
    'W': (255, 255, 236, 255), 'Y': (255, 230, 110, 255), 'O': (255, 160, 40, 255), 'R': (214, 76, 24, 255),
    'r': (140, 40, 14, 255),
    '1': (226, 222, 214, 235), '2': (184, 180, 174, 225), '3': (140, 136, 132, 210), '4': (104, 100, 98, 190),
    'a': (184, 180, 174, 150), 'b': (140, 136, 132, 120),
    'S': (255, 250, 200, 255), 's': (255, 200, 80, 255),
    'K': (20, 18, 18, 255), 'k': (46, 42, 40, 235), 'g': (78, 72, 68, 190), 'h': (110, 104, 98, 120),
    'L': (252, 226, 120, 255), 'l': (214, 160, 50, 255), 'd': (150, 100, 28, 255),
}

SPRITES = {
    'armafuego_fogonazo_0': [
        '...Y....',
        '.Y.OY.Y.',
        '..OWWO..',
        'YOWWWWOY',
        '.OWWWWO.',
        '..OWWO..',
        '.Y.OY.Y.',
        '...Y....'],
    'armafuego_fogonazo_1': [
        '........',
        '..R..R..',
        '...OO...',
        '.ROYYOR.',
        '..OYYO..',
        '...OO...',
        '..R..R..',
        '........'],
    'armafuego_fogonazo_2': [
        '........',
        '........',
        '...rR...',
        '..rOOr..',
        '..ROOr..',
        '...rr...',
        '........',
        '........'],
    'armafuego_fogonazo_3': [
        '........',
        '........',
        '........',
        '...ba...',
        '..ab3...',
        '...a....',
        '........',
        '........'],
    'armafuego_humo_0': [
        '........',
        '........',
        '...12...',
        '..1123..',
        '..2234..',
        '...34...',
        '........',
        '........'],
    'armafuego_humo_1': [
        '........',
        '...11...',
        '..1122..',
        '.112233.',
        '.122334.',
        '..2334..',
        '...44...',
        '........'],
    'armafuego_humo_2': [
        '..a.....',
        '.a1a2a..',
        '.12a22b.',
        'a2a2b3a.',
        '.2b2a3b.',
        '.a3b3ab.',
        '..b.a...',
        '........'],
    'armafuego_humo_3': [
        '.a......',
        '...a..a.',
        '.a..b...',
        '..b...a.',
        'a...b...',
        '..a...b.',
        '.....a..',
        '..b.....'],
    'armafuego_chispa_0': [
        '........',
        '........',
        '...s....',
        '..sSS...',
        '...SSs..',
        '....s...',
        '........',
        '........'],
    'armafuego_chispa_1': [
        '........',
        '........',
        '........',
        '...S....',
        '....s...',
        '........',
        '........',
        '........'],
    'armafuego_marca_0': [
        '........',
        '..h.g...',
        '...gk.h.',
        '.hgKKkg.',
        '..kKKg..',
        '.g.kg.h.',
        '..h..g..',
        '........'],
    'armafuego_marca_1': [
        '...h....',
        '.h.g..h.',
        '..gkkg..',
        '.gkKKk..',
        '..kKKkgh',
        '..gkk...',
        '.h..g.h.',
        '........'],
    'armafuego_casquillo_0': [
        '........',
        '........',
        '........',
        '.dlLLLd.',
        '.dlllld.',
        '........',
        '........',
        '........'],
    'armafuego_casquillo_1': [
        '........',
        '........',
        '...dd...',
        '..dLld..',
        '..dlld..',
        '...dd...',
        '........',
        '........'],
}


def generar():
    os.makedirs(DIR, exist_ok=True)
    for nombre, filas in SPRITES.items():
        assert len(filas) == 8 and all(len(f) == 8 for f in filas), nombre
        im = Image.new('RGBA', (8, 8), (0, 0, 0, 0))
        for y, f in enumerate(filas):
            for x, c in enumerate(f):
                if PAL[c]:
                    im.putpixel((x, y), PAL[c])
        im.save(os.path.join(DIR, nombre + '.png'))


if __name__ == '__main__':
    generar()

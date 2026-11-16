#!/usr/bin/env python3
"""Iconos 16x16 dibujados a mano: funda de cadera, metralla, cerbatana (con su cobre en cada fase) y los tres dardos."""
from PIL import Image

def c(r, g, b): return (r, g, b, 255)
CUERO = (c(92, 58, 32), c(140, 94, 54), c(176, 124, 74), c(210, 162, 106))
MADERA = (c(74, 46, 26), c(116, 76, 44), c(150, 104, 62), c(184, 136, 86))
ACERO = (c(70, 74, 84), c(120, 124, 136), c(176, 180, 192), c(230, 232, 240))
LONA = (c(118, 100, 74), c(160, 140, 106), c(196, 178, 140), c(226, 212, 178))
ORO = (c(150, 108, 28), c(212, 166, 44), c(246, 208, 86), c(255, 240, 160))
OSC = c(40, 24, 14)

def pinta(filas, p):
    assert len(filas) == 16 and all(len(r) == 16 for r in filas), [len(r) for r in filas]
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y, r in enumerate(filas):
        for x, ch in enumerate(r):
            if ch != '.':
                im.putpixel((x, y), p[ch])
    return im

def mat(mt, o, **k):
    d = {"o": o, "1": mt[0], "2": mt[1], "3": mt[2], "4": mt[3]}
    d.update(k)
    return d

# la funda de cuero, colgada del cinto, con la culata del revólver asomando
FUNDA = [
    '.........oooo...',
    '........oWWwmo..',
    '........oWwwmo..',
    '.......ooWwmmo..',
    '.....ooTosswmo..',
    '....o4433ssoo...',
    '...o34333322o...',
    '...o3g32222oBo..',
    '..o3332k221oBo..',
    '..o332k2211oo...',
    '.o332k2211o.....',
    '.o32k2211o......',
    'o3222211o.......',
    'o221111o........',
    '.oooooo.........',
    '................']

def funda():
    return pinta(FUNDA, mat(CUERO, OSC, W=MADERA[2], w=MADERA[1], m=MADERA[0], T=ACERO[1], s=ACERO[2],
                            B=CUERO[3], b=CUERO[2], g=ORO[2], k=CUERO[3]))

# la metralla: un saquito de lona atado, con los perdigones asomando
METRALLA = ['................',
            '.....oo..oo.....',
            '....oW4ooW4o....',
            '....oSsooSso....',
            '.....occcco.....',
            '.....o3442o.....',
            '....o334222o....',
            '...o33422221o...',
            '..o3342222211o..',
            '..o3322222211o..',
            '..o3222222111o..',
            '..o3222222111o..',
            '...o32222211o...',
            '....o111111o....',
            '.....oooooo.....',
            '................']

def metralla():
    return pinta(METRALLA, mat(LONA, c(60, 48, 34), W=ACERO[3], **{'4': LONA[3]}, S=ACERO[2], s=ACERO[0], c=CUERO[0]))

def diagonal(im, x0, x1, base, col):
    """Un tubo en diagonal (de abajo a la izquierda a arriba a la derecha): las celdas con x + y == base y base + 1."""
    for x in range(x0, x1 + 1):
        for k, ch in enumerate(col):
            y = base + k - 1 - x
            if 0 <= y < 16 and ch is not None:
                im.putpixel((x, y), ch)

def cerbatana(tonos):
    """El tubo de cobre en diagonal, de dos píxeles de grueso con contorno, anillos de hierro, el agarre de cuero y la boquilla."""
    oscuro, medio, claro = tonos
    contorno = tuple(int(v * 0.5) for v in oscuro[:3]) + (255,)
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    # x + y = 14 contorno de arriba, 15 claro, 16 medio, 17 oscuro, 18 contorno de abajo
    diagonal(im, 2, 13, 14, [contorno, claro, medio, oscuro, contorno])
    # agarre de cuero y boquilla
    for x0, x1, t in ((2, 3, (CUERO[1], CUERO[0])), (5, 6, (CUERO[2], CUERO[1]))):
        for x in range(x0, x1 + 1):
            im.putpixel((x, 15 - x), t[0])
            im.putpixel((x, 16 - x), t[1])
            im.putpixel((x, 17 - x), CUERO[0])
    # anillos de hierro
    for x in (4, 9):
        im.putpixel((x, 15 - x), ACERO[3])
        im.putpixel((x, 16 - x), ACERO[2])
        im.putpixel((x, 17 - x), ACERO[1])
    # las dos puntas, cerradas con el contorno, y la boca oscura arriba
    for (x, y) in ((1, 13), (1, 14), (2, 15), (14, 0), (14, 1), (14, 2), (15, 1)):
        if 0 <= y < 16:
            im.putpixel((x, y), contorno)
    im.putpixel((13, 2), c(24, 20, 18))
    im.putpixel((13, 3), contorno)
    return im

def dardo(punta, plumas):
    """Como la flecha de vanilla, más corto: astil fino, punta de metal y plumas grandes."""
    pc, ps = punta
    pl, po = plumas
    filas = ['................',
             '................',
             '...........oPo..',
             '..........oPpo..',
             '.........oAppo..',
             '........oAo.oo..',
             '.......oAo......',
             '......oAo.......',
             '.....oAo........',
             '..oooAo.........',
             '.oLlAo..........',
             '.oLlo...........',
             '.olLlo..........',
             '..oooo..........',
             '................',
             '................']
    return pinta(filas, {'o': c(40, 28, 20), 'A': CUERO[3], 'P': pc, 'p': ps, 'L': pl, 'l': po})

DARDOS = {'dardo_cerbatana': (((210, 214, 222, 255), (140, 144, 154, 255)), ((236, 236, 236, 255), (176, 176, 180, 255))),
          'dardo_veneno': (((120, 220, 90, 255), (60, 150, 60, 255)), ((110, 196, 90, 255), (60, 130, 56, 255))),
          'dardo_somnifero': (((176, 146, 236, 255), (110, 80, 176, 255)), ((160, 130, 220, 255), (100, 74, 160, 255)))}


if __name__ == '__main__':
    import os
    import sys
    raiz = sys.argv[1] if len(sys.argv) > 1 else '.'
    d = os.path.join(raiz, 'common/src/main/resources/assets/copperslug/textures/item')
    funda().save(os.path.join(d, 'funda.png'))
    metralla().save(os.path.join(d, 'metralla.png'))
    for n, (punta, plumas) in DARDOS.items():
        dardo(punta, plumas).save(os.path.join(d, n + '.png'))
    print('iconos: funda, metralla y dardos')

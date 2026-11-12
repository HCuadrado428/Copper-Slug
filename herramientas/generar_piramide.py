#!/usr/bin/env python3
"""Genera la «Pirámide del faraón» (estructura de desierto estilo película de aventuras) como datapack.

Una pirámide escalonada de 61 x 61 con dos plantas laberínticas por dentro:
  planta 1 (y 4..8)   laberinto de 11 x 11 celdas con bucles, trampas de TNT, husks y cofres en los callejones, y en el
                      centro la sala del sarcófago; una escalera de mano en un callejón lejano sube a la planta 2
  planta 2 (y 11..15) laberinto de 7 x 7 celdas y, en el centro, la cámara del tesoro del faraón
Delante, un pilono de entrada con obeliscos. Todo se genera con una semilla fija; el script comprueba que no hay fugas
al exterior y que desde la puerta se llega a cada cofre, cada husk y la escalera.
Es idempotente. Uso: generar_piramide.py [raíz del repositorio] [--mc 1.20.1|1.21.1]
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estruc import *  # noqa: E402,F401,F403
import estruc as E  # noqa: E402

RAIZ, V21 = E.contexto(sys.argv)
DATOS = os.path.join(RAIZ, 'common/src/main/resources/data/copperslug')
NOMBRE = 'piramide'
W, H, D = 61, 36, 73
CX = 30
rng = random.Random(20261112)
g = E.Cuadro(W, H, D)
poner, rell, blk, AIRE = g.poner, g.rell, E.blk, E.AIRE

AREN, CORT, CINC, LISA = blk('sandstone'), blk('cut_sandstone'), blk('chiseled_sandstone'), blk('smooth_sandstone')
ARENA, ORO, LAPIS, TELA = blk('sand'), blk('gold_block'), blk('lapis_block'), blk('cobweb')


def losa(t): return blk('smooth_sandstone_slab', type=t, waterlogged=False)


# ---------------------------------------------------------------- cimientos y pirámide escalonada (15 escalones)
rell(0, 0, 0, W - 1, 3, D - 1, ARENA)
rell(0, 2, 0, W - 1, 3, 63, AREN)
for t in range(15):
    ya, yb, a = 4 + 2 * t, 5 + 2 * t, 2 * t
    z2 = 60 - 2 * t
    rell(a, ya, a, 60 - a, yb, z2, AREN)
    for y in (ya, yb):
        for x in range(a, 61 - a):
            for z in (a, z2):
                poner(x, y, z, CORT)
        for z in range(a, z2 + 1):
            for x in (a, 60 - a):
                poner(x, y, z, CORT)
    if t % 2 == 1:
        for x in (a, 60 - a):
            for z in (a, z2):
                poner(x, yb, z, ORO)
    if t in (4, 8, 11):
        for c in range(29, 32):
            poner(c, yb, z2, LAPIS)
            poner(c, yb, a, LAPIS)
poner(CX, 34, CX, ORO)

# ---------------------------------------------------------------- pilono de la entrada (x 22..38, z 57..63)
rell(22, 4, 57, 38, 9, 63, AREN)
rell(22, 10, 57, 26, 11, 63, AREN)
rell(34, 10, 57, 38, 11, 63, AREN)
for x in range(22, 39):
    for y in range(4, 12):
        if y > 9 and 26 < x < 34:
            continue
        for z in (57, 63):
            poner(x, y, z, CORT)
for z in range(57, 64):
    for x in (22, 38):
        rell(x, 4, z, x, 11, z, CORT)
for x in list(range(22, 27)) + list(range(34, 39)):
    poner(x, 11, 63, CINC)
for x in list(range(23, 26)) + list(range(35, 38)):
    poner(x, 8, 63, LAPIS)
for x in (22, 38):
    for z in (57, 63):
        poner(x, 11, z, ORO)
# patio de delante (z 64..72): suelo liso, camino, obeliscos y columnas
rell(0, 3, 64, W - 1, 3, D - 1, ARENA)
rell(26, 3, 64, 34, 3, D - 1, LISA)
rell(29, 3, 64, 31, 3, D - 1, CINC)
for cx in (23, 37):
    rell(cx - 1, 4, 67, cx + 1, 4, 69, AREN)
    rell(cx - 1, 5, 67, cx + 1, 5, 69, CINC)
    rell(cx, 6, 68, cx, 12, 68, CORT)
    poner(cx, 13, 68, ORO)
for cx in (27, 33):
    rell(cx, 4, 65, cx, 8, 65, CINC)
    poner(cx, 9, 65, ORO)

# ---------------------------------------------------------------- las dos plantas
PASO = 4
X0, Z0 = 9, 9            # esquina de la celda (0,0) de la planta 1
N1 = 11
L1_Y0, L1_Y1 = 4, 8       # carvado de la planta 1
L2_Y0, L2_Y1 = 11, 15     # carvado de la planta 2
SUB = range(2, 9)         # celdas de la planta 1 que tiene la planta 2 (7 x 7)
CENTRO = range(4, 7)      # el bloque central 3 x 3 de celdas (sala del sarcófago / cámara del tesoro)
ENTRADA = (5, 10)


def cx0(i): return X0 + PASO * i
def cz0(j): return Z0 + PASO * j


def carvar(pasos, celdas, y0, y1):
    for (i, j) in celdas:
        rell(cx0(i), y0, cz0(j), cx0(i) + 2, y1, cz0(j) + 2, AIRE)
    for (a, b2) in pasos:
        if a < b2:
            (i, j), (i2, j2) = a, b2
            if i2 == i + 1:
                rell(cx0(i) + 3, y0, cz0(j), cx0(i) + 3, y1, cz0(j) + 2, AIRE)
            else:
                rell(cx0(i), y0, cz0(j) + 3, cx0(i) + 2, y1, cz0(j) + 3, AIRE)


pasos1 = E.laberinto(N1, rng, 0.14)
celdas1 = [(i, j) for i in range(N1) for j in range(N1)]
carvar(pasos1, celdas1, L1_Y0, L1_Y1)
# planta 2: laberinto de 7 x 7 sobre las celdas 2..8
pasos2_loc = E.laberinto(7, rng, 0.12)
pasos2 = {((a[0] + 2, a[1] + 2), (b2[0] + 2, b2[1] + 2)) for (a, b2) in pasos2_loc}
celdas2 = [(i, j) for i in SUB for j in SUB]
rell(cx0(2) - 1, 9, cz0(2) - 1, cx0(8) + 3, 10, cz0(8) + 3, AREN)    # el suelo de la planta 2 (ya lo es: es macizo)
carvar(pasos2, celdas2, L2_Y0, L2_Y1)


def abrir_bloque(y0, y1):
    """El bloque central 3 x 3 de celdas, todo abierto (sala)."""
    rell(cx0(4), y0, cz0(4), cx0(6) + 2, y1, cz0(6) + 2, AIRE)


abrir_bloque(L1_Y0, L1_Y1)
abrir_bloque(L2_Y0, L2_Y1)
SX1, SX2 = cx0(4), cx0(6) + 2       # 25..35
ENT_X = cx0(ENTRADA[0]) + 1         # 30

# pasillo de entrada: desde la celda de entrada, por la pared sur, hasta la puerta del pilono
rell(29, 4, 52, 31, 7, 63, AIRE)
for y in range(4, 9):
    for x in (28, 32):
        poner(x, y, 63, CINC)
rell(28, 8, 63, 32, 8, 63, CINC)
poner(30, 8, 63, ORO)
PUERTA = {(x, y, 63) for x in (29, 30, 31) for y in range(4, 8)}

# decoración de las paredes: jeroglíficos y algún destello de oro
def muros(pasos, celdas, y0, y1):
    cs = set(celdas)
    for (i, j) in celdas:
        for di, dj in ((1, 0), (0, 1)):
            n = (i + di, j + dj)
            if n in cs and ((i, j), n) not in pasos:
                wx = cx0(i) + 3 if di else cx0(i) + 1
                wz = cz0(j) + 1 if di else cz0(j) + 3
                if g.c.get((wx, y0 + 2, wz)) == AIRE:
                    continue
                if rng.random() < 0.40:
                    poner(wx, y0 + 2, wz, CINC)
                    if rng.random() < 0.25:
                        poner(wx, y0 + 3, wz, ORO)


muros(pasos1, celdas1, L1_Y0, L1_Y1)
muros(pasos2, celdas2, L2_Y0, L2_Y1)

# ---------------------------------------------------------------- qué va en cada celda
en_centro = lambda c: c[0] in CENTRO and c[1] in CENTRO
d1 = E.distancias(pasos1, ENTRADA)
d2 = E.distancias(pasos2, ENTRADA if ENTRADA in celdas2 else (5, 8))
grado = lambda p, c: len(E.vecinos(p, c))
usadas = set()


def libres(celdas, pasos, minimo=0):
    return [c for c in celdas if not en_centro(c) and c not in usadas and c != ENTRADA and d1.get(c, 99) >= minimo]


# --- la escalera de mano a la planta 2: un callejón de la planta 1 dentro del bloque 7 x 7
def lado_cerrado(p, c):
    """Lados de la celda sin paso (muro macizo): ('N'|'S'|'E'|'O')."""
    i, j = c
    r = []
    if ((i, j), (i, j - 1)) not in p: r.append('N')
    if ((i, j), (i, j + 1)) not in p: r.append('S')
    if ((i, j), (i + 1, j)) not in p: r.append('E')
    if ((i, j), (i - 1, j)) not in p: r.append('O')
    return r


cands = [c for c in celdas2 if not en_centro(c) and c != ENTRADA]
escalera = None
for c in sorted(cands, key=lambda c: (grado(pasos1, c), -d1[c])):
    comun = [lado for lado in lado_cerrado(pasos1, c) if lado in lado_cerrado(pasos2, c)]
    if comun:
        escalera = (c, comun[0])
        break
assert escalera, 'no hay callejón para la escalera'
(ec, elado) = escalera
usadas.add(ec)
ex, ez = cx0(ec[0]) + 1, cz0(ec[1]) + 1
if elado == 'N': lx, lz, fac = cx0(ec[0]) + 1, cz0(ec[1]), 'south'
elif elado == 'S': lx, lz, fac = cx0(ec[0]) + 1, cz0(ec[1]) + 2, 'north'
elif elado == 'E': lx, lz, fac = cx0(ec[0]) + 2, cz0(ec[1]) + 1, 'west'
else: lx, lz, fac = cx0(ec[0]), cz0(ec[1]) + 1, 'east'
rell(lx, 9, lz, lx, 10, lz, AIRE)
for y in range(4, 12):
    poner(lx, y, lz, blk('ladder', facing=fac, waterlogged=False))
ESCALERA_PIE = (ex if elado in 'NS' else lx + (-1 if elado == 'E' else 1), 4, ez if elado in 'EO' else lz + (1 if elado == 'N' else -1))

# --- cofres en callejones (con la boca hacia la abertura)
def cofre(c, y, lado_abierto):
    x0, z0 = cx0(c[0]), cz0(c[1])
    if lado_abierto == 'N': x, z, f = x0 + 1, z0 + 2, 'north'
    elif lado_abierto == 'S': x, z, f = x0 + 1, z0, 'south'
    elif lado_abierto == 'E': x, z, f = x0, z0 + 1, 'east'
    else: x, z, f = x0 + 2, z0 + 1, 'west'
    poner(x, y, z, blk('chest', facing=f, type='single', waterlogged=False))
    g.cofres.append((x, y, z))
    return (x + {'east': 1, 'west': -1}.get(f, 0), y, z + {'south': 1, 'north': -1}.get(f, 0))


def lado_abierto(p, c):
    i, j = c
    for nx in E.vecinos(p, c):
        return {(0, -1): 'N', (0, 1): 'S', (1, 0): 'E', (-1, 0): 'O'}[(nx[0] - i, nx[1] - j)]


FRENTES = []
for c in sorted([c for c in celdas1 if grado(pasos1, c) == 1 and not en_centro(c) and c not in usadas], key=lambda c: -d1[c])[:7]:
    FRENTES.append(cofre(c, 4, lado_abierto(pasos1, c)))
    usadas.add(c)
d2 = E.distancias(pasos2, ec)
for c in sorted([c for c in celdas2 if grado(pasos2, c) == 1 and not en_centro(c) and c not in usadas], key=lambda c: -d2.get(c, 0))[:5]:
    FRENTES.append(cofre(c, 11, lado_abierto(pasos2, c)))
    usadas.add(c)

# --- trampas: placa de presión sobre cuatro TNT, en celdas de paso
def trampa(c, suelo):
    x, z = cx0(c[0]) + 1, cz0(c[1]) + 1
    for dx in (0, 1):
        for dz in (0, 1):
            poner(x + dx, suelo - 1, z + dz, blk('tnt', unstable=False))
    poner(x, suelo, z, blk('stone_pressure_plate', powered=False))
    usadas.add(c)


for c in rng.sample([c for c in celdas1 if grado(pasos1, c) >= 2 and not en_centro(c) and c not in usadas and d1[c] >= 3], 7):
    trampa(c, 3)
for c in rng.sample([c for c in celdas2 if grado(pasos2, c) >= 2 and not en_centro(c) and c not in usadas], 4):
    trampa(c, 10)

# --- iluminación y telarañas
def decora(celdas, pasos, ytecho, ysuelo, prob_lampara):
    for c in celdas:
        if en_centro(c):
            continue
        x0, z0 = cx0(c[0]), cz0(c[1])
        if c not in usadas or True:
            if rng.random() < prob_lampara and g.c.get((x0 + 1, ytecho, z0 + 1)) == AIRE:
                poner(x0 + 1, ytecho, z0 + 1, blk('lantern', hanging=True, waterlogged=False))
        if rng.random() < 0.30:
            poner(*rng.choice([(x0, ytecho, z0), (x0 + 2, ytecho, z0), (x0, ytecho, z0 + 2), (x0 + 2, ytecho, z0 + 2)]), TELA)


decora(celdas1, pasos1, L1_Y1, 4, 0.45)
decora(celdas2, pasos2, L2_Y1, 11, 0.45)
# antorchas en los pilares del pasillo de entrada
for z in (54, 58):
    poner(29, 6, z, blk('wall_torch', facing='east')) if g.c.get((28, 6, z)) not in (None, AIRE) else None
    poner(31, 6, z, blk('wall_torch', facing='west')) if g.c.get((32, 6, z)) not in (None, AIRE) else None

# ---------------------------------------------------------------- las salas centrales
SC = 30


def sarcofago(y):
    rell(27, y, 27, 33, y, 33, CORT)                                  # tarima
    for x in range(29, 32):
        for z in range(29, 32):
            poner(x, y + 1, z, LISA)
            poner(x, y + 2, z, losa('top'))
    poner(30, y + 2, 29, ORO)
    poner(29, y + 2, 29, LAPIS)
    poner(31, y + 2, 29, LAPIS)
    poner(30, y + 2, 30, ORO)
    for x, z in ((27, 27), (33, 27), (27, 33), (33, 33)):
        poner(x, y + 1, z, blk('campfire', facing='north', lit=True, signal_fire=False, waterlogged=False))
    for x, z in ((26, 26), (34, 26), (26, 34), (34, 34), (26, 30), (34, 30)):
        rell(x, y, z, x, y + 4, z, CINC)


sarcofago(4)
for x, z in ((30, 26), (30, 34), (26, 30), (34, 30)):
    poner(x, 8, z, blk('lantern', hanging=True, waterlogged=False))
for p in ((25, 8, 25), (35, 8, 25), (25, 8, 35), (35, 8, 35)):
    poner(*p, TELA)
# cámara del tesoro del faraón (planta 2): tarima de oro con cuatro cofres
rell(27, 11, 27, 33, 11, 33, CORT)
rell(29, 11, 29, 31, 11, 31, ORO)
for (x, z, f) in ((30, 28, 'south'), (28, 30, 'east'), (32, 30, 'west'), (30, 32, 'north')):
    poner(x, 12, z, blk('chest', facing=f, type='single', waterlogged=False))
    g.cofres.append((x, 12, z))
    FRENTES.append((x + {'east': 1, 'west': -1}.get(f, 0), 12, z + {'south': 1, 'north': -1}.get(f, 0)))
for x, z in ((26, 26), (34, 26), (26, 34), (34, 34)):
    rell(x, 11, z, x, 15, z, CINC)
for x, z in ((30, 26), (30, 34), (26, 30), (34, 30), (30, 30)):
    poner(x, 15, z, blk('lantern', hanging=True, waterlogged=False))
for p in ((25, 15, 25), (35, 15, 25), (25, 15, 35), (35, 15, 35)):
    poner(*p, TELA)

# ---------------------------------------------------------------- mobs
def husk(x, y, z, armado, arma=None):
    """Un husk; con `armado`, lleva el arma de la expedición (mosquete o Derringer, al gusto del faraón)."""
    arma = arma or rng.choice(['mosquete', 'mosquete', 'derringer'])
    ex = (lambda v21: E.mano_arma(v21, arma)) if armado else {}
    g.entidades.append(('minecraft:husk', x, y, z, ex))


for (x, z) in ((28.5, 25.5), (32.5, 25.5), (25.5, 29.5), (35.5, 33.5)):
    husk(x, 5, z, True, 'mosquete')                                      # sala del sarcófago: mosquetes (en el suelo y la tarima)
for (x, z) in ((26.5, 28.5), (34.5, 28.5), (28.5, 34.5), (32.5, 34.5)):
    husk(x, 11, z, True)                                                 # cámara del faraón
celdas_mob = [c for c in celdas1 if not en_centro(c) and c not in usadas and d1[c] >= 3]
for c in rng.sample(celdas_mob, 12):
    husk(cx0(c[0]) + 1.5, 4, cz0(c[1]) + 1.5, rng.random() < 0.40)
    usadas.add(c)
celdas_mob2 = [c for c in celdas2 if not en_centro(c) and c not in usadas]
for c in rng.sample(celdas_mob2, 8):
    husk(cx0(c[0]) + 1.5, 11, cz0(c[1]) + 1.5, rng.random() < 0.50)
    usadas.add(c)

# ---------------------------------------------------------------- comprobaciones
fugas = g.fugas(permitidas=PUERTA)
assert not fugas, ('fugas', fugas[:10], len(fugas))
alc = g.alcanzables((ENT_X, 4, 53))
for fr in FRENTES:
    assert fr in alc, ('cofre inalcanzable', fr)
for (eid, x, y, z, ex) in g.entidades:
    assert (int(x), y, int(z)) in alc, ('husk inalcanzable', x, y, z)
assert (ESCALERA_PIE[0], 4, ESCALERA_PIE[2]) in alc and (lx, 11, lz) in alc, 'escalera'
total_aire = sum(1 for e in g.c.values() if e == AIRE)
print('alcanzables', len(alc), 'de', total_aire, 'celdas de aire; cofres', len(g.cofres), 'husks', len(g.entidades))
sin_llegar = [p for p, e in g.c.items() if e == AIRE and p not in alc and p[1] in (4, 11)]
assert len(sin_llegar) < 40, ('zonas sin alcance', len(sin_llegar), sin_llegar[:10])

# ---------------------------------------------------------------- escritura
nb, npal, ne = E.exportar(g, NOMBRE, V21, DATOS, 'copperslug:chests/' + NOMBRE)
E.datapack(DATOS, NOMBRE, V21, ['minecraft:desert'], 'surface_structures', 'beard_thin', -3, 40, 16, 1923481,
           exclusion=('minecraft:desert_pyramids', 6))
item = E.item
E.botin(DATOS, V21, 'chests/' + NOMBRE, [
    item('minecraft:gold_ingot', 8, 2, 6), item('minecraft:emerald', 4, 1, 3), item('minecraft:diamond', 2, 1, 2),
    item('minecraft:golden_apple', 2), item('copperslug:revolver_bala', 7, 4, 10), item('copperslug:bala_plata', 3, 2, 5),
    item('copperslug:bala_dinamita', 2, 1, 3), item('minecraft:bone', 4, 2, 6), item('minecraft:rotten_flesh', 4, 2, 6),
    item('minecraft:lapis_lazuli', 4, 3, 9)],
    [item('copperslug:winchester', 3), item('copperslug:derringer', 3), {'type': 'minecraft:empty', 'weight': 4}])
print(MC := ('1.21.1' if V21 else '1.20.1'), 'bloques', nb, 'paleta', npal, 'entidades', ne)

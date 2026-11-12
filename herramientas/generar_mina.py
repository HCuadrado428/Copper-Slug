#!/usr/bin/env python3
"""Genera la «Mina de cobre abandonada» como datapack: un laberinto subterráneo de 15 x 15 celdas (pasillos de 3 de ancho
y 4 de alto) al que se baja por un pozo con escalera de mano, con vías y vagonetas con cofre, puntales, polvorines con
TNT, derrumbes, mineros zombis con Winchester y, en una esquina, la cámara del filón con el cobre oxidado y el tesoro.
Arriba, un cabrestante de madera marca la entrada.

Sale en colinas, montañas y mesetas, bajo tierra (la plantilla solo pone la roca de las paredes y lo de dentro). Se genera
con una semilla fija; el script comprueba que no hay fugas y que desde el pie del pozo se llega a todo.
Es idempotente. Uso: generar_mina.py [raíz del repositorio] [--mc 1.20.1|1.21.1]
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estruc as E  # noqa: E402

RAIZ, V21 = E.contexto(sys.argv)
DATOS = os.path.join(RAIZ, 'common/src/main/resources/data/copperslug')
NOMBRE = 'mina'
W, H, D = 61, 32, 61
SY = 25                    # el bloque de la superficie en el centro (el cabrestante empieza en y 26)
rng = random.Random(20261113)
g = E.Cuadro(W, H, D)
poner, rell, blk, AIRE = g.poner, g.rell, E.blk, E.AIRE

# ---------------------------------------------------------------- la roca: un bloque macizo de piedra con vetas
ROCAS = [(blk('stone'), 0.60), (blk('andesite'), 0.12), (blk('tuff'), 0.08), (blk('cobblestone'), 0.06),
         (blk('copper_ore'), 0.08), (blk('exposed_copper'), 0.03), (blk('raw_copper_block'), 0.01), (blk('weathered_copper'), 0.02)]


def roca():
    r, acc = rng.random(), 0.0
    for b, p in ROCAS:
        acc += p
        if r < acc:
            return b
    return ROCAS[0][0]


for x in range(W):
    for z in range(D):
        for y in range(3, 9):
            poner(x, y, z, roca())

# ---------------------------------------------------------------- el laberinto
PASO, X0, Z0, N = 4, 1, 1, 15
Y0, Y1 = 4, 7                      # el pasillo: 4 de alto (y 4..7); suelo y=3, techo y=8
def cx0(i): return X0 + PASO * i
def cz0(j): return Z0 + PASO * j


CENTRO = (7, 7)
pasos = E.laberinto(N, rng, 0.10)
# el pozo está en la celda central y su pared norte tiene que ser maciza (ahí va la escalera): se quita ese paso
if ((7, 7), (7, 6)) in pasos and len(E.vecinos(pasos, (7, 7))) > 1:
    pasos.discard(((7, 7), (7, 6)))
    pasos.discard(((7, 6), (7, 7)))
    # y se vuelve a conectar la celda (7,6) si ha quedado aislada
    if not E.vecinos(pasos, (7, 6)):
        pasos.add(((7, 6), (6, 6))); pasos.add(((6, 6), (7, 6)))
celdas = [(i, j) for i in range(N) for j in range(N)]
assert len(E.distancias(pasos, (7, 7))) == N * N, 'laberinto roto'
for (i, j) in celdas:
    rell(cx0(i), Y0, cz0(j), cx0(i) + 2, Y1, cz0(j) + 2, AIRE)
for (a, b2) in pasos:
    if a < b2:
        (i, j), (i2, j2) = a, b2
        if i2 == i + 1:
            rell(cx0(i) + 3, Y0, cz0(j), cx0(i) + 3, Y1, cz0(j) + 2, AIRE)
        else:
            rell(cx0(i), Y0, cz0(j) + 3, cx0(i) + 2, Y1, cz0(j) + 3, AIRE)

# ---------------------------------------------------------------- la cámara del filón (celdas 11..13 x 1..3) y el pozo
CAM = [(i, j) for i in range(11, 14) for j in range(1, 4)]
en_cam = lambda c: c in CAM
rell(cx0(11), Y0, cz0(1), cx0(13) + 2, Y1, cz0(3) + 2, AIRE)
dist = E.distancias(pasos, CENTRO)
usadas = {CENTRO}
usadas.update(CAM)

COBRE = [blk('cut_copper'), blk('exposed_cut_copper'), blk('weathered_cut_copper')]
for x in range(cx0(11), cx0(13) + 3):
    for z in range(cz0(1), cz0(3) + 3):
        poner(x, 3, z, rng.choice(COBRE))
OXI = blk('oxidized_cut_copper')
for x, z in ((45, 5), (55, 5), (45, 15), (55, 15), (45, 10), (55, 10)):
    rell(x, Y0, z, x, Y1, z, OXI)
rell(49, 4, 9, 51, 5, 11, blk('raw_copper_block'))
for (x, z, f) in ((50, 12, 'south'), (48, 10, 'west'), (52, 10, 'east')):
    poner(x, 4, z, blk('chest', facing=f, type='single', waterlogged=False))
    g.cofres.append((x, 4, z))
for x, z in ((47, 7), (53, 7), (47, 13), (53, 13), (50, 7)):
    poner(x, 7, z, blk('lantern', hanging=True, waterlogged=False))
rell(49, 6, 9, 51, 6, 11, AIRE) if False else None

# ---------------------------------------------------------------- el pozo (celda central) y el cabrestante
rell(29, 4, 29, 31, SY, 31, AIRE)
for x in range(28, 33):
    for z in range(28, 33):
        if x in (28, 32) or z in (28, 32):
            for y in range(9, SY):
                poner(x, y, z, blk('oak_log', axis='y') if (x in (28, 32) and z in (28, 32)) else blk('oak_planks'))
for y in range(4, SY + 1):
    poner(30, y, 29, blk('ladder', facing='south', waterlogged=False))
# el cabrestante: cuatro postes, vigas, techo y una lámpara
for x, z in ((28, 28), (32, 28), (28, 32), (32, 32)):
    rell(x, SY + 1, z, x, SY + 5, z, blk('oak_log', axis='y'))
rell(28, SY + 6, 28, 32, SY + 6, 32, blk('oak_planks'))
for x in range(28, 33):
    for z in (28, 32):
        if (x, z) not in ((28, 28), (32, 28), (28, 32), (32, 32)):
            poner(x, SY + 1, z, blk('oak_fence', waterlogged=False))
for z in range(29, 32):
    for x in (28, 32):
        poner(x, SY + 1, z, blk('oak_fence', waterlogged=False))
poner(30, SY + 5, 30, blk('lantern', hanging=True, waterlogged=False))
poner(29, SY + 1, 32, AIRE)
poner(30, SY + 1, 32, AIRE)
poner(31, SY + 1, 32, AIRE)
poner(32, SY + 1, 28, blk('barrel', facing='up', open=False))

# ---------------------------------------------------------------- vías desde el pozo hasta la cámara
ruta = E.camino(pasos, CENTRO, (11, 3))
bloques = []
cx_, cz_ = cx0(ruta[0][0]) + 1, cz0(ruta[0][1]) + 1
bloques.append((cx_, cz_))
for a, b2 in zip(ruta, ruta[1:]):
    dx, dz = b2[0] - a[0], b2[1] - a[1]
    for k in range(1, 5):
        bloques.append((cx_ + dx * k, cz_ + dz * k))
    cx_, cz_ = cx_ + dx * 4, cz_ + dz * 4
DIRN = {(0, -1): 'north', (0, 1): 'south', (1, 0): 'east', (-1, 0): 'west'}
for k, (x, z) in enumerate(bloques):
    ds = set()
    if k > 0: ds.add(DIRN[(bloques[k - 1][0] - x, bloques[k - 1][1] - z)])
    if k < len(bloques) - 1: ds.add(DIRN[(bloques[k + 1][0] - x, bloques[k + 1][1] - z)])
    if len(ds) == 1:
        ds.add({'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}[next(iter(ds))])
    forma = {frozenset(('north', 'south')): 'north_south', frozenset(('east', 'west')): 'east_west',
             frozenset(('south', 'east')): 'south_east', frozenset(('south', 'west')): 'south_west',
             frozenset(('north', 'west')): 'north_west', frozenset(('north', 'east')): 'north_east'}[frozenset(ds)]
    if (x, z) != (30, 30) and g.c.get((x, 4, z)) == AIRE:
        poner(x, 4, z, blk('rail', shape=forma, waterlogged=False))
for k in rng.sample(range(8, len(bloques) - 8), 3):
    x, z = bloques[k]
    if g.c.get((x, 4, z))[0] == 'minecraft:rail':
        g.entidades.append(('minecraft:chest_minecart', x + 0.5, 4.0, z + 0.5, {'LootTable': E.s('copperslug:chests/mina_vagoneta')}))

# ---------------------------------------------------------------- cofres, polvorines y derrumbes en los callejones
def grado(c): return len(E.vecinos(pasos, c))
def lado_abierto(c):
    i, j = c
    nx = E.vecinos(pasos, c)[0]
    return {(0, -1): 'N', (0, 1): 'S', (1, 0): 'E', (-1, 0): 'O'}[(nx[0] - i, nx[1] - j)]


def contra_fondo(c, lado):
    """Posición y orientación de un bloque contra el fondo de un callejón cuyo paso está en `lado`."""
    x0, z0 = cx0(c[0]), cz0(c[1])
    return {'N': (x0 + 1, z0 + 2, 'north'), 'S': (x0 + 1, z0, 'south'), 'E': (x0, z0 + 1, 'east'), 'O': (x0 + 2, z0 + 1, 'west')}[lado]


callejones = sorted([c for c in celdas if grado(c) == 1 and c not in usadas], key=lambda c: -dist[c])
FRENTES = []
def frente(x, y, z, f):
    return (x + {'east': 1, 'west': -1}.get(f, 0), y, z + {'south': 1, 'north': -1}.get(f, 0))


for c in callejones[:6]:                                   # cofres de botín
    x, z, f = contra_fondo(c, lado_abierto(c))
    poner(x, 4, z, blk('chest', facing=f, type='single', waterlogged=False))
    g.cofres.append((x, 4, z))
    FRENTES.append(frente(x, 4, z, f))
    usadas.add(c)
POLVORINES = []
for c in callejones[6:9]:                                  # polvorines: TNT al fondo, un barril y un cofre de munición
    lado = lado_abierto(c)
    x0, z0 = cx0(c[0]), cz0(c[1])
    x, z, f = contra_fondo(c, lado)
    if lado in 'NS':
        zz = (z0 + 2, z0 + 1) if lado == 'N' else (z0, z0 + 1)
        for xx in range(x0, x0 + 3):
            for z2 in zz:
                for y in (4, 5):
                    poner(xx, y, z2, blk('tnt', unstable=False))
        poner(x0, 4, z0 + 1 - (1 if lado == 'N' else -1), blk('barrel', facing='up', open=False)) if False else None
    else:
        xx_ = (x0 + 2, x0 + 1) if lado == 'E' else (x0, x0 + 1)
        for z2 in range(z0, z0 + 3):
            for xx in xx_:
                for y in (4, 5):
                    poner(xx, y, z2, blk('tnt', unstable=False))
    usadas.add(c)
    POLVORINES.append(c)
# el cofre de munición del polvorín, justo delante del TNT
for c in POLVORINES:
    lado = lado_abierto(c)
    x0, z0 = cx0(c[0]), cz0(c[1])
    if lado == 'N': x, z, f = x0 + 1, z0, 'north'
    elif lado == 'S': x, z, f = x0 + 1, z0 + 2, 'south'
    elif lado == 'E': x, z, f = x0 + 2, z0 + 1, 'east'
    else: x, z, f = x0, z0 + 1, 'west'
    # (con el TNT a dos filas del fondo, queda una fila libre delante: ahí va el cofre)
    if g.c.get((x, 4, z)) == AIRE:
        poner(x, 4, z, blk('chest', facing=f, type='single', waterlogged=False))
        g.cofres.append((x, 4, z))
        FRENTES.append(frente(x, 4, z, f))

# derrumbes: grava en dos de las tres filas del pasillo, con telarañas encima
pasillos = [c for c in celdas if grado(c) == 2 and c not in usadas and not en_cam(c) and dist[c] >= 3]
for c in rng.sample(pasillos, 6):
    x0, z0 = cx0(c[0]), cz0(c[1])
    for xx in range(x0, x0 + 3):
        for z2 in (z0, z0 + 1):
            if g.c.get((xx, 4, z2)) == AIRE:
                poner(xx, 4, z2, blk('gravel'))
                if g.c.get((xx, 5, z2)) == AIRE and rng.random() < 0.5:
                    poner(xx, 5, z2, blk('cobweb'))
    usadas.add(c)

# ---------------------------------------------------------------- puntales, lámparas, telarañas y barriles
for c in celdas:
    if en_cam(c) or c == CENTRO:
        continue
    x0, z0 = cx0(c[0]), cz0(c[1])
    if rng.random() < 0.35 and g.c.get((x0, 4, z0)) == AIRE:
        rell(x0, 4, z0, x0, 7, z0, blk('oak_log', axis='y'))
    if rng.random() < 0.35 and g.c.get((x0 + 2, 4, z0 + 2)) == AIRE:
        rell(x0 + 2, 4, z0 + 2, x0 + 2, 7, z0 + 2, blk('oak_log', axis='y'))
    if rng.random() < 0.40 and g.c.get((x0 + 1, 7, z0 + 1)) == AIRE:
        poner(x0 + 1, 7, z0 + 1, blk('lantern', hanging=True, waterlogged=False))
    if rng.random() < 0.20:
        p = rng.choice([(x0 + 2, 4, z0), (x0, 4, z0 + 2)])
        if g.c.get(p) == AIRE:
            poner(*p, blk('barrel', facing='up', open=False))
    if rng.random() < 0.25:
        p = (x0 + rng.choice((0, 2)), 7, z0 + rng.choice((0, 2)))
        if g.c.get(p) == AIRE:
            poner(*p, blk('cobweb'))

# ---------------------------------------------------------------- mineros zombis con Winchester
def minero(x, z, y=4):
    g.entidades.append(('minecraft:zombie', x, y, z, E_minero))


def E_minero(v21):
    casco = E.comp(id=E.s('minecraft:iron_helmet'), **({'count': E.i(1)} if v21 else {'Count': E.b(1)}))
    d_ = E.mano_winchester(v21)
    d_['ArmorItems'] = E.lista(E.COMPOUND, [E.comp(), E.comp(), E.comp(), casco])
    d_['ArmorDropChances'] = E.lista(E.FLOAT, [E.f(0.0), E.f(0.0), E.f(0.0), E.f(0.05)])
    return d_


for (x, z) in ((47.5, 7.5), (53.5, 7.5), (47.5, 13.5), (53.5, 13.5)):
    minero(x, z)
cel_mob = [c for c in celdas if c not in usadas and not en_cam(c) and dist[c] >= 3]
for c in rng.sample(cel_mob, 14):
    minero(cx0(c[0]) + 1.5, cz0(c[1]) + 1.5)
    usadas.add(c)

# ---------------------------------------------------------------- comprobaciones
fugas = [f for f in g.fugas() if f[0][1] < SY]     # lo de arriba (el brocal) da al aire a propósito
assert not fugas, ('fugas', fugas[:10], len(fugas))
alc = g.alcanzables((30, 4, 30))
for fr in FRENTES:
    assert fr in alc, ('cofre inalcanzable', fr)
for fx in ((50, 4, 13), (47, 4, 10), (53, 4, 10)):
    assert fx in alc, ('cofre de la cámara', fx)
for (eid, x, y, z, ex) in g.entidades:
    assert (int(x), int(y), int(z)) in alc, ('inalcanzable', eid, x, y, z)
sin_llegar = [p for p, e in g.c.items() if e == AIRE and p not in alc and p[1] == 4]
assert len(sin_llegar) < 30, ('zonas sin alcance', len(sin_llegar), sin_llegar[:10])
print('alcanzables', len(alc), 'cofres', len(g.cofres), 'mobs', len(g.entidades))

# ---------------------------------------------------------------- escritura
nb, npal, ne = E.exportar(g, NOMBRE, V21, DATOS, 'copperslug:chests/mina')
E.datapack(DATOS, NOMBRE, V21,
           ['#minecraft:is_hill', '#minecraft:is_mountain', 'minecraft:badlands', 'minecraft:wooded_badlands', 'minecraft:eroded_badlands'],
           'underground_structures', 'none', -SY, 32, 12, 718293, exclusion=('minecraft:mineshafts', 3))
item = E.item
E.botin(DATOS, V21, 'chests/mina', [
    item('minecraft:copper_ingot', 9, 3, 9), item('minecraft:raw_copper', 6, 2, 8), item('minecraft:coal', 6, 3, 10),
    item('minecraft:iron_ingot', 4, 1, 4), item('minecraft:bread', 3, 1, 3), item('minecraft:rail', 5, 4, 12),
    item('copperslug:revolver_bala', 7, 4, 10), item('copperslug:bala_dinamita', 3, 1, 3), item('minecraft:torch', 4, 4, 12)],
    [item('copperslug:winchester', 3), item('copperslug:derringer', 3), item('copperslug:mosquete', 2), {'type': 'minecraft:empty', 'weight': 6}])
E.botin(DATOS, V21, 'chests/mina_vagoneta', [
    item('copperslug:revolver_bala', 8, 3, 8), item('minecraft:rail', 6, 2, 8), item('minecraft:coal', 5, 2, 6),
    item('minecraft:raw_copper', 5, 1, 4), item('minecraft:torch', 4, 3, 8)], [{'type': 'minecraft:empty', 'weight': 1}], tiradas=(2, 4))
print('1.21.1' if V21 else '1.20.1', 'bloques', nb, 'paleta', npal, 'entidades', ne)

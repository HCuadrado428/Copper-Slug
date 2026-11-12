#!/usr/bin/env python3
"""Genera el «Campamento de saqueadores» como datapack: una empalizada de troncos con cuatro torres de vigilancia, una hoguera con
troncos para sentarse, tres tiendas, la tienda roja del capitán con su cofre, una jaula con un prisionero (de adorno: no hace nada),
un corral con caballos, cajas y heno. Lo guardan saqueadores armados (revólver, Winchester y, el capitán, una Thompson) y dos
vindicadores en la puerta.

A cielo abierto. Se genera con semilla fija; el script comprueba que desde la puerta se llega a los cofres y a los guardias.
Es idempotente. Uso: generar_campamento.py [raíz del repositorio] [--mc 1.20.1|1.21.1]
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estruc as E  # noqa: E402

RAIZ, V21 = E.contexto(sys.argv)
DATOS = os.path.join(RAIZ, 'common/src/main/resources/data/copperslug')
NOMBRE = 'campamento'
W, H, D = 37, 16, 37
rng = random.Random(20261115)
g = E.Cuadro(W, H, D)
poner, rell, blk, AIRE = g.poner, g.rell, E.blk, E.AIRE

TIERRA, GRAVA, CAMINO = blk('dirt'), blk('coarse_dirt'), blk('dirt_path')
TRONCO = blk('spruce_log', axis='y')
TABLA = blk('spruce_planks')
VALLA = blk('spruce_fence', waterlogged=False)


def tronco_x(): return blk('stripped_spruce_log', axis='x')
def tronco_z(): return blk('stripped_spruce_log', axis='z')


# ---------------------------------------------------------------- el suelo (la capa de arriba es y=1) y el camino
rell(2, 0, 2, 34, 0, 36, TIERRA)
rell(2, 1, 2, 34, 1, 34, GRAVA)
rell(16, 0, 35, 20, 0, 36, TIERRA)
rell(16, 1, 35, 20, 1, 36, GRAVA)
rell(17, 1, 20, 19, 1, 36, CAMINO)                         # del portón a la hoguera
rell(14, 1, 14, 22, 1, 22, CAMINO)                         # el corro de la hoguera

# el interior despejado (limpia árboles y hierba) y el pasillo del portón: así se puede comprobar el alcance
rell(3, 2, 3, 33, 13, 33, AIRE)
rell(16, 2, 34, 20, 8, 36, AIRE)

# ---------------------------------------------------------------- la empalizada (x 2..34, z 2..34) con la puerta al sur (x 16..20)
for x in range(2, 35):
    for z in (2, 34):
        if z == 34 and 16 <= x <= 20:
            continue
        for y in range(2, 2 + rng.choice((3, 3, 4, 4, 5))):
            poner(x, y, z, TRONCO)
for z in range(3, 34):
    for x in (2, 34):
        for y in range(2, 2 + rng.choice((3, 3, 4, 4, 5))):
            poner(x, y, z, TRONCO)
for x in (15, 21):                                          # los postes del portón, más altos, con lana roja y farol
    rell(x, 2, 34, x, 7, 34, TRONCO)
    poner(x, 8, 34, blk('red_wool'))
    poner(x, 9, 34, blk('lantern', hanging=False, waterlogged=False))
rell(15, 7, 34, 21, 7, 34, TABLA)                           # el dintel con el cartel de tablas
rell(16, 8, 34, 20, 8, 34, blk('spruce_slab', type='bottom', waterlogged=False))
for x in range(16, 21):
    poner(x, 7, 34, blk('spruce_planks'))


# ---------------------------------------------------------------- las torres de vigilancia (4 x 4) en las esquinas
def torre(x0, z0):
    for x, z in ((x0, z0), (x0 + 3, z0), (x0, z0 + 3), (x0 + 3, z0 + 3)):
        rell(x, 2, z, x, 12, z, TRONCO)
    rell(x0, 9, z0, x0 + 3, 9, z0 + 3, TABLA)
    poner(x0 + 1, 9, z0 + 3, AIRE)                          # el hueco de la escalera
    for k in range(4):
        for (x, z) in ((x0 + k, z0), (x0 + k, z0 + 3), (x0, z0 + k), (x0 + 3, z0 + k)):
            if (x, z) in ((x0 + 1, z0 + 3),):
                continue
            if g.c.get((x, 10, z)) is None:
                poner(x, 10, z, VALLA)
    rell(x0, 13, z0, x0 + 3, 13, z0 + 3, blk('spruce_slab', type='bottom', waterlogged=False))
    for y in range(2, 10):
        poner(x0 + 1, y, z0 + 3, blk('ladder', facing='east', waterlogged=False))
    poner(x0 + 2, 12, z0 + 1, blk('lantern', hanging=True, waterlogged=False))


for (x0, z0) in ((3, 3), (30, 3), (3, 30), (30, 30)):
    torre(x0, z0)
TORRES = [(4.5, 10, 4.5), (31.5, 10, 4.5), (4.5, 10, 31.5), (31.5, 10, 31.5)]


# ---------------------------------------------------------------- la hoguera y sus troncos
poner(18, 2, 18, blk('campfire', facing='north', lit=True, signal_fire=False, waterlogged=False))
for (x, z, f) in ((16, 18, tronco_z()), (20, 18, tronco_z()), (18, 16, tronco_x()), (18, 20, tronco_x())):
    poner(x, 2, z, f)

# ---------------------------------------------------------------- las tiendas: una caja de lana con el techo en escalones, abierta al sur
def tienda(x0, z0, w, l, color, interior):
    lana = blk(color + '_wool')
    mitad = (w - 1) // 2
    for z in range(z0, z0 + l):
        for dx in (0, w - 1):                              # las paredes de los lados
            for y in (2, 3):
                poner(x0 + dx, y, z, lana)
        for dx in range(w):                                # el techo plano y, encima, los escalones hasta la cumbrera
            poner(x0 + dx, 4, z, lana)
        for k in range(1, mitad + 1):
            for dx in range(k, w - k):
                poner(x0 + dx, 4 + k, z, lana)
    for dx in range(1, w - 1):                             # la pared del fondo (norte); el sur queda abierto
        for y in (2, 3):
            poner(x0 + dx, y, z0, lana)
    interior(x0, z0, w, l)


def cama(x, z, color):
    poner(x, 2, z, blk(color + '_bed', part='foot', facing='south', occupied=False))
    poner(x, 2, z + 1, blk(color + '_bed', part='head', facing='south', occupied=False))


def int_pequena(x0, z0, w, l):
    cama(x0 + 1, z0 + 1, 'red')
    poner(x0 + 3, 2, z0 + 1, blk('barrel', facing='up', open=False))
    poner(x0 + 3, 2, z0 + 2, blk('hay_block', axis='y'))
    poner(x0 + 2, 4, z0 + 3, blk('lantern', hanging=True, waterlogged=False))


tienda(5, 9, 5, 6, 'white', int_pequena)
tienda(5, 20, 5, 6, 'light_gray', int_pequena)
tienda(27, 9, 5, 6, 'white', int_pequena)


def int_capitan(x0, z0, w, l):
    cx = x0 + w // 2
    poner(cx, 2, z0 + 1, blk('chest', facing='south', type='single', waterlogged=False))    # el cofre del capitán
    g.cofres.append((cx, 2, z0 + 1))
    poner(cx - 2, 2, z0 + 1, blk('cartography_table'))
    poner(cx + 2, 2, z0 + 1, blk('barrel', facing='up', open=False))
    cama(x0 + 1, z0 + 3, 'red')
    poner(x0 + w - 2, 2, z0 + 3, blk('lectern', facing='west', has_book=False, powered=False))
    for dz in (2, 5):
        poner(cx, 5, z0 + dz, blk('lantern', hanging=True, waterlogged=False))


tienda(14, 5, 9, 8, 'red', int_capitan)

# ---------------------------------------------------------------- la jaula del prisionero (de adorno)
for x in range(27, 32):
    for z in range(20, 25):
        borde = x in (27, 31) or z in (20, 24)
        for y in range(2, 6):
            if borde:
                poner(x, y, z, blk('iron_bars', waterlogged=False))
        poner(x, 6, z, blk('iron_bars', waterlogged=False))
poner(29, 2, 22, blk('hay_block', axis='y'))
for (x, z) in ((27, 20), (31, 20), (27, 24), (31, 24)):
    rell(x, 2, z, x, 6, z, TRONCO)

# ---------------------------------------------------------------- el corral (x 5..13, z 28..32) y las cajas
for x in range(5, 14):
    for z in range(28, 33):
        if x in (5, 13) or z in (28, 32):
            poner(x, 2, z, VALLA)
poner(9, 2, 28, blk('spruce_fence_gate', facing='north', open=False, in_wall=False, powered=False))
poner(7, 2, 31, blk('hay_block', axis='y'))
poner(8, 2, 31, blk('hay_block', axis='y'))
poner(11, 2, 31, blk('cauldron'))
for (x, z) in ((25, 28), (26, 28), (25, 29), (27, 30), (28, 28), (28, 29)):
    poner(x, 2, z, blk('barrel', facing='up', open=False))
poner(26, 3, 28, blk('barrel', facing='up', open=False))
for (x, z) in ((29, 31), (30, 31), (31, 31)):
    poner(x, 2, z, blk('hay_block', axis='y'))
poner(28, 2, 32, blk('chest', facing='west', type='single', waterlogged=False))
g.cofres.append((28, 2, 32))
# antorchas en la empalizada, por dentro
for x in range(5, 34, 6):
    poner(x, 3, 3, blk('wall_torch', facing='south'))
    if not (16 <= x <= 20):
        poner(x, 3, 33, blk('wall_torch', facing='north'))
for z in range(8, 31, 7):
    poner(3, 3, z, blk('wall_torch', facing='east'))
    poner(33, 3, z, blk('wall_torch', facing='west'))


# ---------------------------------------------------------------- los habitantes
def mob(eid, x, y, z, arma=None, extra=None):
    def ex(v21):
        d = {}
        if arma:
            d.update(E.mano_arma(v21, arma))
        if extra:
            d.update(extra(v21))
        d['Tags'] = E.lista(E.STRING, [E.s('copperslug_tirado')])
        return d
    g.entidades.append((eid, x, y, z, ex))


def hacha(v21):
    it = E.comp(id=E.s('minecraft:iron_axe'), **({'count': E.i(1)} if v21 else {'Count': E.b(1)}))
    return dict(HandItems=E.lista(E.COMPOUND, [it, E.comp()]), HandDropChances=E.lista(E.FLOAT, [E.f(0.05), E.f(0.0)]))


for (x, y, z) in TORRES:
    mob('minecraft:pillager', x, y, z, 'winchester')
mob('minecraft:pillager', 12.5, 2, 17.5, 'revolver')
mob('minecraft:pillager', 24.5, 2, 17.5, 'winchester')
mob('minecraft:pillager', 18.5, 2, 9.5, 'thompson')         # el capitán, con la Thompson
mob('minecraft:vindicator', 14.5, 2, 32.5, extra=hacha)
mob('minecraft:vindicator', 22.5, 2, 32.5, extra=hacha)


def prisionero(v21):
    return dict(Invulnerable=E.b(1), NoAI=E.b(1), Silent=E.b(1),
                VillagerData=E.comp(type=E.s('minecraft:plains'), profession=E.s('minecraft:none'), level=E.i(1)))


g.entidades.append(('minecraft:villager', 29.5, 2, 22.5, prisionero))
for (x, z) in ((8.5, 30.5), (10.5, 29.5)):
    g.entidades.append(('minecraft:horse', x, 2, z, lambda v21: dict(Variant=E.i(rng.randrange(0, 7)), Tame=E.b(0))))

# ---------------------------------------------------------------- comprobaciones: se llega a los cofres y a los guardias
alc = g.alcanzables((18, 2, 35))
for (x, y, z) in g.cofres:
    ok = any((x + dx, y, z + dz) in alc for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    assert ok, ('cofre inalcanzable', x, y, z)
for (eid, x, y, z, ex) in g.entidades:
    if eid in ('minecraft:villager', 'minecraft:horse'):
        continue
    assert (int(x), y, int(z)) in alc, ('mob inalcanzable', eid, x, y, z)
print('alcanzables', len(alc), 'cofres', len(g.cofres), 'mobs', len(g.entidades))

# ---------------------------------------------------------------- escritura
nb, npal, ne = E.exportar(g, NOMBRE, V21, DATOS, 'copperslug:chests/' + NOMBRE)
E.datapack(DATOS, NOMBRE, V21,
           ['minecraft:plains', 'minecraft:sunflower_plains', 'minecraft:meadow', 'minecraft:savanna', 'minecraft:taiga', 'minecraft:snowy_plains',
            'minecraft:forest'],
           'surface_structures', 'beard_thin', -1, 36, 12, 5190211, exclusion=('minecraft:pillager_outposts', 8), maxdist=48)
item = E.item
E.botin(DATOS, V21, 'chests/' + NOMBRE, [
    item('minecraft:arrow', 6, 4, 12), item('minecraft:emerald', 5, 1, 4), item('minecraft:iron_ingot', 5, 2, 6), item('minecraft:gold_ingot', 3, 1, 4),
    item('copperslug:revolver_bala', 8, 4, 10), item('copperslug:bala_dinamita', 2, 1, 3), item('minecraft:crossbow', 2),
    item('minecraft:hay_block', 3, 1, 2), item('minecraft:bread', 4, 2, 5), item('minecraft:torch', 4, 4, 10)],
    [item('copperslug:revolver', 3), item('copperslug:thompson', 2), item('copperslug:winchester', 3), {'type': 'minecraft:empty', 'weight': 4}],
    tiradas=(3, 6))
print('1.21.1' if V21 else '1.20.1', 'bloques', nb, 'paleta', npal, 'entidades', ne)

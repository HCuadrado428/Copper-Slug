#!/usr/bin/env python3
"""Genera la «Pirámide del faraón» (estructura de desierto estilo película de aventuras) como datapack.

Escribe en common/src/main/resources/data/copperslug/:
  structures/piramide.nbt (1.21.1: structure/)       la plantilla de bloques y mobs
  worldgen/template_pool, structure, structure_set    cómo sale en el mundo
  tags/worldgen/biome/has_structure/piramide.json     dónde (desiertos)
  loot_tables/chests/piramide.json (1.21.1: loot_table/)
Uso: generar_piramide.py [raíz del repositorio] [--mc 1.20.1|1.21.1]
Es idempotente. La plantilla es una pirámide escalonada de arenisca con patio y obeliscos, un pasillo con
pilares y una trampa de TNT, la cámara del sarcófago con cuatro husks que llevan Winchester, y la sala del tesoro.
"""
import gzip
import json
import os
import struct
import sys

args = [a for a in sys.argv[1:] if not a.startswith('--')]
RAIZ = args[0] if args else '.'
MC = '1.21.1' if '--mc' in sys.argv and sys.argv[sys.argv.index('--mc') + 1] == '1.21.1' else '1.20.1'
V21 = MC == '1.21.1'
DATA = os.path.join(RAIZ, 'common/src/main/resources/data/copperslug')

# ---------------------------------------------------------------- NBT mínimo (solo lo que hace falta)
END, BYTE, INT, FLOAT, DOUBLE, STRING, LIST, COMPOUND = 0, 1, 3, 5, 6, 8, 9, 10


class T:
    def __init__(self, tipo, valor, sub=None):
        self.tipo, self.valor, self.sub = tipo, valor, sub


def b(v): return T(BYTE, v)
def i(v): return T(INT, v)
def f(v): return T(FLOAT, v)
def d(v): return T(DOUBLE, v)
def s(v): return T(STRING, v)
def lista(sub, items): return T(LIST, items, sub)
def comp(**kw): return T(COMPOUND, kw)


def cadena(x):
    r = x.encode('utf-8')
    return struct.pack('>H', len(r)) + r


def carga(t):
    if t.tipo == BYTE: return struct.pack('>b', t.valor)
    if t.tipo == INT: return struct.pack('>i', t.valor)
    if t.tipo == FLOAT: return struct.pack('>f', t.valor)
    if t.tipo == DOUBLE: return struct.pack('>d', t.valor)
    if t.tipo == STRING: return cadena(t.valor)
    if t.tipo == LIST:
        r = struct.pack('>bi', t.sub, len(t.valor))
        return r + b''.join(carga(e) for e in t.valor)
    if t.tipo == COMPOUND:
        r = b''
        for k, v in t.valor.items():
            r += struct.pack('>b', v.tipo) + cadena(k) + carga(v)
        return r + b'\x00'
    raise ValueError(t.tipo)


def nbt_bytes(raiz):
    return struct.pack('>b', COMPOUND) + cadena('') + carga(raiz)


# ---------------------------------------------------------------- la cuadrícula de bloques
W, H, D = 29, 20, 41
AIRE = ('minecraft:air', ())
cuadro = {}


def blk(nombre, **props):
    return ('minecraft:' + nombre if ':' not in nombre else nombre, tuple(sorted((k, str(v).lower() if isinstance(v, bool) else str(v)) for k, v in props.items())))


def poner(x, y, z, e):
    assert 0 <= x < W and 0 <= y < H and 0 <= z < D, (x, y, z)
    cuadro[(x, y, z)] = e


def rell(x1, y1, z1, x2, y2, z2, e):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for z in range(min(z1, z2), max(z1, z2) + 1):
                poner(x, y, z, e)


AREN = blk('sandstone')
CORT = blk('cut_sandstone')
CINC = blk('chiseled_sandstone')
LISA = blk('smooth_sandstone')
ARENA = blk('sand')
ORO = blk('gold_block')
LAPIS = blk('lapis_block')
OCRE = blk('orange_terracotta')
TELA = blk('cobweb')


def losa(tipo): return blk('smooth_sandstone_slab', type=tipo, waterlogged=False)


# ---- cimientos y pirámide escalonada (siete escalones de dos de alto)
rell(0, 0, 0, W - 1, 3, D - 1, ARENA)
rell(0, 2, 0, W - 1, 3, 31, AREN)
for t in range(7):
    ya, yb, a, z2 = 4 + 2 * t, 5 + 2 * t, 2 * t, 28 - 2 * t
    rell(a, ya, a, 28 - a, yb, z2, AREN)
    for y in (ya, yb):                                  # el borde exterior de cada escalón, tallado
        for x in range(a, 29 - a):
            for z in (a, z2):
                poner(x, y, z, CORT)
        for z in range(a, z2 + 1):
            for x in (a, 28 - a):
                poner(x, y, z, CORT)
    if t % 2 == 1:                                      # esquinas de oro en los escalones impares
        for x in (a, 28 - a):
            for z in (a, z2):
                poner(x, yb, z, ORO)
    if t in (2, 4):                                     # una banda de lapislázuli en el centro de cada cara
        for c in range(13, 16):
            poner(c, yb, z2, LAPIS)
            poner(c, yb, a, LAPIS)
poner(14, 18, 14, ORO)                                  # el remate

# ---- la capilla trasera del tesoro (x 8..20, z 0..4, y 4..9): pegada a la pirámide, con cornisa y esquinas de oro
rell(8, 4, 0, 20, 9, 4, AREN)
for x in range(8, 21):
    for z in (0,):
        rell(x, 4, z, x, 9, z, CORT)
for z in range(0, 5):
    for x in (8, 20):
        rell(x, 4, z, x, 9, z, CORT)
rell(8, 9, 0, 20, 9, 0, CINC)
for x in (8, 20):
    poner(x, 9, 0, ORO)

# ---- el pilono de la entrada (x 7..21, z 25..31): dos torres macizas con el paso en medio, como un templo egipcio
rell(7, 4, 25, 21, 9, 31, AREN)
rell(7, 10, 25, 10, 11, 31, AREN)
rell(18, 10, 25, 21, 11, 31, AREN)
for x in range(7, 22):
    for y in range(4, 12):
        if y > 9 and 10 < x < 18:
            continue
        for z in (25, 31):
            poner(x, y, z, CORT)
for z in range(25, 32):
    for x in (7, 21):
        rell(x, 4, z, x, 11, z, CORT)
for x in (7, 8, 9, 10, 18, 19, 20, 21):
    poner(x, 11, 31, CINC)
    for x2 in (8, 9, 10, 18, 19, 20):
        poner(x2, 8, 31, LAPIS)
for x in (7, 21):
    for z in (25, 31):
        poner(x, 11, z, ORO)
rell(13, 4, 25, 15, 7, 31, AIRE)                        # el paso: 3 de ancho y 4 de alto
for y in range(4, 9):
    for x in (12, 16):
        poner(x, y, 31, CINC)
rell(12, 8, 31, 16, 8, 31, CINC)
poner(14, 8, 31, ORO)

# ---- el patio de delante (z 32..40): suelo liso, camino, obeliscos y dos columnas
rell(0, 3, 32, W - 1, 3, D - 1, ARENA)
rell(10, 3, 32, 18, 3, D - 1, LISA)
rell(13, 3, 32, 15, 3, D - 1, CINC)
for cx in (9, 19):
    rell(cx - 1, 4, 35, cx + 1, 4, 37, AREN)
    rell(cx - 1, 5, 35, cx + 1, 5, 37, CINC)
    rell(cx, 6, 36, cx, 11, 36, CORT)
    poner(cx, 12, 36, ORO)
for cx in (11, 17):
    rell(cx, 4, 33, cx, 8, 33, CINC)
    poner(cx, 9, 33, ORO)

# ---- el pasillo (x 11..17, z 18..24, y 4..8) con pilares, antorchas y telarañas
rell(11, 4, 18, 17, 8, 24, AIRE)
for x in (11, 17):
    for z in (19, 22):
        rell(x, 4, z, x, 8, z, CINC)
for z in (20, 24):
    poner(11, 6, z, blk('wall_torch', facing='east'))
    poner(17, 6, z, blk('wall_torch', facing='west'))
for z in (21, 22, 23):                                  # un panel de jeroglíficos en cada pared
    for y in (5, 6):
        poner(10, y, z, CINC)
        poner(18, y, z, CINC)
for p in ((11, 8, 18), (17, 8, 18), (11, 8, 24), (17, 8, 24), (14, 8, 20), (12, 7, 23), (16, 7, 21)):
    poner(*p, TELA)
# la trampa: una placa en el suelo sobre nueve TNT
rell(13, 2, 21, 15, 2, 23, blk('tnt', unstable=False))
poner(14, 3, 22, blk('stone_pressure_plate', powered=False))

# ---- la cámara del sarcófago (x 8..20, z 6..17, y 4..9)
rell(8, 4, 6, 20, 9, 17, AIRE)
rell(10, 4, 7, 18, 4, 13, CORT)                         # la tarima
for x, z in ((9, 7), (19, 7), (9, 16), (19, 16), (9, 12), (19, 12)):
    rell(x, 4, z, x, 9, z, CINC)
for x in range(13, 16):                                 # el sarcófago
    for z in range(9, 12):
        poner(x, 5, z, LISA)
        poner(x, 6, z, losa('top'))
poner(14, 6, 9, ORO)
poner(13, 6, 9, LAPIS)
poner(15, 6, 9, LAPIS)
poner(14, 6, 10, ORO)
for x, z in ((10, 7), (18, 7), (10, 13), (18, 13)):     # brasas en las esquinas de la tarima
    poner(x, 5, z, blk('campfire', facing='north', lit=True, signal_fire=False, waterlogged=False))
for x, z in ((11, 10), (17, 10), (14, 15), (11, 15), (17, 15)):
    poner(x, 9, z, blk('lantern', hanging=True, waterlogged=False))
for p in ((8, 9, 6), (20, 9, 6), (8, 9, 17), (20, 9, 17), (12, 8, 8), (16, 8, 14), (8, 8, 12)):
    poner(*p, TELA)
# el arco a la sala del tesoro (x 13..15) en la pared norte (z 5)
rell(13, 4, 5, 15, 7, 5, AIRE)
for y in range(4, 8):
    poner(12, y, 5, CINC)
    poner(16, y, 5, CINC)
rell(12, 8, 5, 16, 8, 5, CINC)

# ---- la sala del tesoro (x 10..18, z 1..4, y 4..7)
rell(10, 4, 1, 18, 7, 4, AIRE)
for x in (12, 14, 16):
    poner(x, 4, 1, blk('chest', facing='south', type='single', waterlogged=False))
rell(10, 3, 1, 18, 3, 4, CORT)
for x in (10, 18):
    poner(x, 4, 4, ORO)
poner(14, 4, 3, ORO)
poner(14, 7, 3, blk('lantern', hanging=True, waterlogged=False))
poner(11, 7, 2, TELA)
poner(17, 7, 2, TELA)

# ---------------------------------------------------------------- a NBT
paleta, indice = [], {}


def pal(e):
    if e not in indice:
        indice[e] = len(paleta)
        paleta.append(e)
    return indice[e]


cofre = comp(id=s('minecraft:chest'), LootTable=s('copperslug:chests/piramide'))
bloques = []
for (x, y, z), e in sorted(cuadro.items()):
    if e == AIRE:
        continue
    kw = dict(pos=lista(INT, [i(x), i(y), i(z)]), state=i(pal(e)))
    if e[0] == 'minecraft:chest':
        kw['nbt'] = cofre
    bloques.append(comp(**kw))
pal(AIRE)     # el aire también está en la paleta (los vanos que se excavan)
# los vanos de aire se guardan como bloques de aire para que la plantilla los excave del macizo
for (x, y, z), e in sorted(cuadro.items()):
    if e == AIRE:
        bloques.append(comp(pos=lista(INT, [i(x), i(y), i(z)]), state=i(pal(AIRE))))


def entrada_paleta(e):
    kw = dict(Name=s(e[0]))
    if e[1]:
        kw['Properties'] = comp(**{k: s(v) for k, v in e[1]})
    return comp(**kw)


def husk(x, y, z):
    arma = comp(id=s('copperslug:winchester'), **({'count': i(1)} if V21 else {'Count': b(1)}))
    nbt = comp(id=s('minecraft:husk'), PersistenceRequired=b(1),
               Pos=lista(DOUBLE, [d(x), d(y), d(z)]),
               HandItems=lista(COMPOUND, [arma, comp()]),
               HandDropChances=lista(FLOAT, [f(0.1), f(0.0)]))
    return comp(pos=lista(DOUBLE, [d(x), d(y), d(z)]), blockPos=lista(INT, [i(int(x)), i(int(y)), i(int(z))]), nbt=nbt)


entidades = [husk(*p) for p in ((10.5, 4, 15.5), (18.5, 4, 15.5), (12.5, 5, 8.5), (16.5, 5, 11.5))]
raiz = comp(DataVersion=i(3955 if V21 else 3465), size=lista(INT, [i(W), i(H), i(D)]),
            palette=lista(COMPOUND, [entrada_paleta(e) for e in paleta]),
            blocks=lista(COMPOUND, bloques), entities=lista(COMPOUND, entidades))


def escribir(ruta, contenido, binario=False):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    if binario:
        with gzip.GzipFile(ruta, 'wb', mtime=0) as g:
            g.write(contenido)
    else:
        with open(ruta, 'w', encoding='utf-8') as fh:
            json.dump(contenido, fh, indent=2, ensure_ascii=False)
            fh.write('\n')


escribir(os.path.join(DATA, 'structure' if V21 else 'structures', 'piramide.nbt'), nbt_bytes(raiz), binario=True)

WG = os.path.join(DATA, 'worldgen')
escribir(os.path.join(WG, 'template_pool/piramide/inicio.json'), {
    'fallback': 'minecraft:empty',
    'elements': [{'weight': 1, 'element': {
        'element_type': 'minecraft:single_pool_element', 'location': 'copperslug:piramide',
        'processors': 'minecraft:empty', 'projection': 'rigid'}}]})
escribir(os.path.join(WG, 'structure/piramide.json'), {
    'type': 'minecraft:jigsaw', 'biomes': '#copperslug:has_structure/piramide', 'step': 'surface_structures',
    'spawn_overrides': {}, 'terrain_adaptation': 'beard_thin', 'start_pool': 'copperslug:piramide/inicio',
    'size': 1, 'max_distance_from_center': 80, 'use_expansion_hack': False,
    'start_height': {'absolute': -3}, 'project_start_to_heightmap': 'WORLD_SURFACE_WG'})
escribir(os.path.join(WG, 'structure_set/piramide.json'), {
    'structures': [{'structure': 'copperslug:piramide', 'weight': 1}],
    'placement': {'type': 'minecraft:random_spread', 'spacing': 36, 'separation': 14, 'salt': 1923481,
                  'exclusion_zone': {'other_set': 'minecraft:desert_pyramids', 'chunk_count': 5}}})
escribir(os.path.join(DATA, 'tags/worldgen/biome/has_structure/piramide.json'), {'values': ['minecraft:desert']})


def item(n, peso, lo=None, hi=None):
    e = {'type': 'minecraft:item', 'name': n, 'weight': peso}
    if lo is not None:
        e['functions'] = [{'function': 'minecraft:set_count', 'count': {'type': 'minecraft:uniform', 'min': lo, 'max': hi}}]
    return e


escribir(os.path.join(DATA, 'loot_table' if V21 else 'loot_tables', 'chests/piramide.json'), {
    'type': 'minecraft:chest',
    'pools': [
        {'rolls': {'type': 'minecraft:uniform', 'min': 4, 'max': 7}, 'entries': [
            item('minecraft:gold_ingot', 8, 2, 6), item('minecraft:emerald', 4, 1, 3), item('minecraft:diamond', 2, 1, 2),
            item('minecraft:golden_apple', 2), item('copperslug:revolver_bala', 7, 4, 10), item('copperslug:bala_plata', 3, 2, 5),
            item('copperslug:bala_dinamita', 2, 1, 3), item('minecraft:bone', 4, 2, 6), item('minecraft:rotten_flesh', 4, 2, 6),
            item('minecraft:lapis_lazuli', 4, 3, 9)]},
        {'rolls': 1, 'entries': [item('copperslug:winchester', 3), item('copperslug:derringer', 3), {'type': 'minecraft:empty', 'weight': 4}]}]})
print(MC, 'bloques', len(bloques), 'paleta', len(paleta), 'husks', len(entidades))

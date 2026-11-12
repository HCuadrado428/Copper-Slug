"""Utilidades comunes de los generadores de estructuras (pirámide, mina): NBT mínimo, cuadrícula de bloques,
laberintos, comprobaciones (fugas y alcanzabilidad) y escritura del datapack (plantilla, pool, structure, set, tags, botín).
No se ejecuta solo: lo importan generar_piramide.py y generar_mina.py."""
import gzip
import json
import os
import random
import struct
import sys
from collections import deque

# ---------------------------------------------------------------- NBT mínimo
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


def _cad(x):
    r = x.encode('utf-8')
    return struct.pack('>H', len(r)) + r


def _carga(t):
    if t.tipo == BYTE: return struct.pack('>b', t.valor)
    if t.tipo == INT: return struct.pack('>i', t.valor)
    if t.tipo == FLOAT: return struct.pack('>f', t.valor)
    if t.tipo == DOUBLE: return struct.pack('>d', t.valor)
    if t.tipo == STRING: return _cad(t.valor)
    if t.tipo == LIST:
        return struct.pack('>bi', t.sub, len(t.valor)) + b''.join(_carga(e) for e in t.valor)
    if t.tipo == COMPOUND:
        r = b''
        for k, v in t.valor.items():
            r += struct.pack('>b', v.tipo) + _cad(k) + _carga(v)
        return r + b'\x00'
    raise ValueError(t.tipo)


def nbt_bytes(raiz):
    return struct.pack('>b', COMPOUND) + _cad('') + _carga(raiz)


# ---------------------------------------------------------------- versión y rutas
def contexto(argv, destino=None):
    """(raiz del repo, ¿1.21.1?)"""
    args = [a for a in argv[1:] if not a.startswith('--')]
    v21 = '--mc' in argv and argv[argv.index('--mc') + 1] == '1.21.1'
    return (args[0] if args else '.'), v21


def escribir(ruta, contenido, binario=False):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    if binario:
        with gzip.GzipFile(ruta, 'wb', mtime=0) as g:
            g.write(contenido)
    else:
        with open(ruta, 'w', encoding='utf-8') as fh:
            json.dump(contenido, fh, indent=2, ensure_ascii=False)
            fh.write('\n')


# ---------------------------------------------------------------- la cuadrícula
AIRE = ('minecraft:air', ())


def blk(nombre, **props):
    return ('minecraft:' + nombre if ':' not in nombre else nombre,
            tuple(sorted((k, str(v).lower() if isinstance(v, bool) else str(v)) for k, v in props.items())))


class Cuadro:
    def __init__(self, W, H, D):
        self.W, self.H, self.D = W, H, D
        self.c = {}
        self.cofres = []      # (x,y,z)
        self.entidades = []   # (id, x, y, z, nbt-extra dict)

    def poner(self, x, y, z, e):
        assert 0 <= x < self.W and 0 <= y < self.H and 0 <= z < self.D, (x, y, z)
        self.c[(x, y, z)] = e

    def rell(self, x1, y1, z1, x2, y2, z2, e):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.poner(x, y, z, e)

    def aire(self, x, y, z):
        return self.c.get((x, y, z)) == AIRE

    def solido(self, x, y, z):
        e = self.c.get((x, y, z))
        return e is not None and e[0] not in ('minecraft:air', 'minecraft:cobweb', 'minecraft:lantern', 'minecraft:wall_torch',
                                               'minecraft:campfire', 'minecraft:rail', 'minecraft:ladder', 'minecraft:stone_pressure_plate')

    # --- comprobaciones
    def fugas(self, permitidas=()):
        """Celdas de aire cuyo vecino no está definido (se ve el exterior). Devuelve la lista (sin las permitidas)."""
        r = []
        for (x, y, z), e in self.c.items():
            if e != AIRE:
                continue
            for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                n = (x + dx, y + dy, z + dz)
                if n not in self.c and (x, y, z) not in permitidas:
                    r.append(((x, y, z), n))
        return r

    def alcanzables(self, inicio):
        """Celdas de aire (y de rieles, placas, telarañas, escaleras...) a las que se llega a pie desde `inicio`
        (se anda por 4 direcciones y se sube/baja 1 bloque; las escaleras de mano suben)."""
        def libre(p):
            e = self.c.get(p)
            return e is not None and not self.solido(*p) and e[0] != 'minecraft:cobweb_bloquea'
        vis = {inicio}
        q = deque([inicio])
        while q:
            x, y, z = q.popleft()
            e = self.c.get((x, y, z))
            movs = [(1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
            if e and e[0] == 'minecraft:ladder':
                movs += [(0, 1, 0), (0, -1, 0)]
            for dx, dy, dz in movs:
                n = (x + dx, y + dy, z + dz)
                if n in vis or not libre(n):
                    continue
                vis.add(n)
                q.append(n)
            # caer o bajar un escalón: si no hay suelo debajo se cae hasta el suelo
            below = (x, y - 1, z)
            if libre(below) and below not in vis:
                vis.add(below)
                q.append(below)
        return vis


# ---------------------------------------------------------------- laberinto
def laberinto(n, rng, trenzado=0.12):
    """Laberinto perfecto de n x n celdas (backtracker iterativo) con algunos muros quitados al azar para que haya
    bucles. Devuelve un conjunto de pasos {((i,j),(i2,j2))} con la pareja en los dos sentidos."""
    visto = {(0, 0)}
    pila = [(0, 0)]
    pasos = set()
    while pila:
        ci, cj = pila[-1]
        vec = [(ci + a, cj + b2) for a, b2 in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if 0 <= ci + a < n and 0 <= cj + b2 < n and (ci + a, cj + b2) not in visto]
        if not vec:
            pila.pop()
            continue
        nx = rng.choice(vec)
        visto.add(nx)
        pasos.add(((ci, cj), nx))
        pasos.add((nx, (ci, cj)))
        pila.append(nx)
    for ci in range(n):
        for cj in range(n):
            for a, b2 in ((1, 0), (0, 1)):
                nx = (ci + a, cj + b2)
                if nx[0] < n and nx[1] < n and ((ci, cj), nx) not in pasos and rng.random() < trenzado:
                    pasos.add(((ci, cj), nx))
                    pasos.add((nx, (ci, cj)))
    return pasos


def vecinos(pasos, c):
    return [b2 for (a, b2) in pasos if a == c]


def distancias(pasos, origen):
    dist = {origen: 0}
    q = deque([origen])
    while q:
        c = q.popleft()
        for nx in vecinos(pasos, c):
            if nx not in dist:
                dist[nx] = dist[c] + 1
                q.append(nx)
    return dist


def camino(pasos, a, b2):
    ant = {a: None}
    q = deque([a])
    while q:
        c = q.popleft()
        if c == b2:
            break
        for nx in vecinos(pasos, c):
            if nx not in ant:
                ant[nx] = c
                q.append(nx)
    r, c = [], b2
    while c is not None:
        r.append(c)
        c = ant[c]
    return r[::-1]


# ---------------------------------------------------------------- escritura de la plantilla
def exportar(cuadro, nombre, v21, datos, loot, extras_bloque=None):
    """Escribe la plantilla {nombre}.nbt. `loot`: tabla de botín de los cofres (ResourceLocation)."""
    paleta, indice = [], {}

    def pal(e):
        if e not in indice:
            indice[e] = len(paleta)
            paleta.append(e)
        return indice[e]

    bloques = []
    for (x, y, z), e in sorted(cuadro.c.items()):
        kw = dict(pos=lista(INT, [i(x), i(y), i(z)]), state=i(pal(e)))
        if e[0] == 'minecraft:chest':
            kw['nbt'] = comp(id=s('minecraft:chest'), LootTable=s(loot))
        bloques.append(comp(**kw))

    def entrada(e):
        kw = dict(Name=s(e[0]))
        if e[1]:
            kw['Properties'] = comp(**{k: s(v) for k, v in e[1]})
        return comp(**kw)

    ents = []
    for (eid, x, y, z, ex) in cuadro.entidades:
        nbt = dict(id=s(eid), PersistenceRequired=b(1), Pos=lista(DOUBLE, [d(x), d(y), d(z)]))
        nbt.update(ex(v21) if callable(ex) else ex)
        ents.append(comp(pos=lista(DOUBLE, [d(x), d(y), d(z)]), blockPos=lista(INT, [i(int(x)), i(int(y)), i(int(z))]), nbt=comp(**nbt)))
    raiz = comp(DataVersion=i(3955 if v21 else 3465), size=lista(INT, [i(cuadro.W), i(cuadro.H), i(cuadro.D)]),
                palette=lista(COMPOUND, [entrada(e) for e in paleta]), blocks=lista(COMPOUND, bloques), entities=lista(COMPOUND, ents))
    escribir(os.path.join(datos, 'structure' if v21 else 'structures', nombre + '.nbt'), nbt_bytes(raiz), binario=True)
    return len(bloques), len(paleta), len(ents)


def mano_arma(v21, arma='winchester'):
    """HandItems/HandDropChances de un mob con ese arma (copperslug:<arma>) en la mano principal."""
    it = comp(id=s('copperslug:' + arma), **({'count': i(1)} if v21 else {'Count': b(1)}))
    return dict(HandItems=lista(COMPOUND, [it, comp()]), HandDropChances=lista(FLOAT, [f(0.1), f(0.0)]))


def mano_winchester(v21):
    return mano_arma(v21, 'winchester')


def datapack(datos, nombre, v21, biomas, paso, adaptacion, alto_inicio, spacing, separation, salt, exclusion=None,
             proyeccion='WORLD_SURFACE_WG', maxdist=80):
    wg = os.path.join(datos, 'worldgen')
    escribir(os.path.join(wg, 'template_pool', nombre, 'inicio.json'), {
        'fallback': 'minecraft:empty',
        'elements': [{'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': 'copperslug:' + nombre,
                                               'processors': 'minecraft:empty', 'projection': 'rigid'}}]})
    escribir(os.path.join(wg, 'structure', nombre + '.json'), {
        'type': 'minecraft:jigsaw', 'biomes': '#copperslug:has_structure/' + nombre, 'step': paso, 'spawn_overrides': {},
        'terrain_adaptation': adaptacion, 'start_pool': 'copperslug:%s/inicio' % nombre, 'size': 1, 'max_distance_from_center': maxdist,
        'use_expansion_hack': False, 'start_height': {'absolute': alto_inicio}, 'project_start_to_heightmap': proyeccion})
    colocacion = {'type': 'minecraft:random_spread', 'spacing': spacing, 'separation': separation, 'salt': salt}
    if exclusion:
        colocacion['exclusion_zone'] = {'other_set': exclusion[0], 'chunk_count': exclusion[1]}
    escribir(os.path.join(wg, 'structure_set', nombre + '.json'),
             {'structures': [{'structure': 'copperslug:' + nombre, 'weight': 1}], 'placement': colocacion})
    escribir(os.path.join(datos, 'tags/worldgen/biome/has_structure', nombre + '.json'), {'values': biomas})


def item(n, peso, lo=None, hi=None):
    e = {'type': 'minecraft:item', 'name': n, 'weight': peso}
    if lo is not None:
        e['functions'] = [{'function': 'minecraft:set_count', 'count': {'type': 'minecraft:uniform', 'min': lo, 'max': hi}}]
    return e


def botin(datos, v21, ruta, comunes, raros, tiradas=(4, 7)):
    escribir(os.path.join(datos, 'loot_table' if v21 else 'loot_tables', ruta + '.json'), {
        'type': 'minecraft:chest',
        'pools': [{'rolls': {'type': 'minecraft:uniform', 'min': tiradas[0], 'max': tiradas[1]}, 'entries': comunes},
                  {'rolls': 1, 'entries': raros}]})

#!/usr/bin/env python3
"""
Convierte el código portado de 1.20.1 (la salida de portar.py, o la rama main) a la API de 1.21.1.

Uso:
    a_1_21_1.py <carpeta>     (cambia en el sitio los .java y los datos de <carpeta>/common/src/main)

Solo hace lo mecánico, lo que se repite por todo el código:
  - new ResourceLocation(a, b) / (s)        -> ResourceLocation.fromNamespaceAndPath(a, b) / parse(s)
  - el NBT de los ItemStack (getOrCreateTag, getTag, hasTag, removeTagKey) -> com.copperslug.shim.Nbt (datos del
    componente minecraft:custom_data, con una etiqueta "viva" que se guarda en el objeto al cambiarla)
  - los niveles de los encantamientos propios (que en 1.21 son datos) -> com.copperslug.shim.Enc
  - defineSynchedData() -> defineSynchedData(SynchedEntityData.Builder)
  - hurtAndBreak con lambda -> hurtAndBreak(n, entidad, ranura)
  - carpetas y formato de los datos (recipes -> recipe, advancements -> advancement, tags/items -> tags/item...)
Lo demás (lo que cambia poco y en sitios concretos) se arregla a mano en la rama 1.21.1, y portar_cambios.py lo
respeta con la fusión a tres bandas.
"""
import json
import os
import re
import sys


def receptor(t, fin):
    """El inicio de la expresión que acaba justo antes de t[fin] (un '.metodo('): identificadores, puntos y paréntesis."""
    i = fin
    while i > 0:
        c = t[i - 1]
        if c.isalnum() or c in '_.$':
            i -= 1
        elif c in ')]':
            cierre = c
            abre = '(' if c == ')' else '['
            prof = 0
            j = i - 1
            while j >= 0:
                if t[j] == cierre:
                    prof += 1
                elif t[j] == abre:
                    prof -= 1
                    if prof == 0:
                        break
                j -= 1
            i = j
        else:
            break
    return i


def argumentos(t, abre):
    """Posición del ')' que cierra el '(' de t[abre] y los argumentos de nivel 0."""
    prof = 0
    args, ini = [], abre + 1
    i = abre
    en_cad = None
    while i < len(t):
        c = t[i]
        if en_cad:
            if c == '\\':
                i += 2
                continue
            if c == en_cad:
                en_cad = None
        elif c in '"\'':
            en_cad = c
        elif c in '([{':
            prof += 1
        elif c in ')]}':
            prof -= 1
            if prof == 0:
                args.append(t[ini:i])
                return i, [a.strip() for a in args]
        elif c == ',' and prof == 1:
            args.append(t[ini:i])
            ini = i + 1
        i += 1
    raise ValueError('paréntesis sin cerrar')


def cambiar_metodo(t, metodo, f):
    """Cada 'X.metodo(args)' -> f(X, args) (de atrás adelante para no mover posiciones)."""
    pat = re.compile(r'\.' + metodo + r'\(')
    pos = [m.start() for m in pat.finditer(t)]
    for p in reversed(pos):
        ini = receptor(t, p)
        x = t[ini:p]
        if not x:
            continue
        fin, args = argumentos(t, p + len(metodo) + 1)
        nuevo = f(x, [a for a in args if a])
        if nuevo is not None:
            t = t[:ini] + nuevo + t[fin + 1:]
    return t


def resource_location(t):
    out = []
    i = 0
    for m in re.finditer(r'new (?:net\.minecraft\.resources\.)?ResourceLocation\(', t):
        pass
    pat = re.compile(r'new (?:net\.minecraft\.resources\.)?ResourceLocation\(')
    while True:
        m = pat.search(t, i)
        if not m:
            break
        fin, args = argumentos(t, m.end() - 1)
        if len(args) == 2:
            nuevo = 'net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(' + ', '.join(args) + ')'
        else:
            nuevo = 'net.minecraft.resources.ResourceLocation.parse(' + args[0] + ')'
        t = t[:m.start()] + nuevo + t[fin + 1:]
        i = m.start() + len(nuevo)
    return t


def nbt(t):
    t = cambiar_metodo(t, 'getOrCreateTag', lambda x, a: 'com.copperslug.shim.Nbt.tag(' + x + ')' if not a else None)
    t = cambiar_metodo(t, 'getTag', lambda x, a: 'com.copperslug.shim.Nbt.leer(' + x + ')' if not a and not x.endswith('Tag') else None)
    t = cambiar_metodo(t, 'hasTag', lambda x, a: 'com.copperslug.shim.Nbt.tiene(' + x + ')' if not a else None)
    t = cambiar_metodo(t, 'removeTagKey', lambda x, a: 'com.copperslug.shim.Nbt.quitar(' + x + ', ' + a[0] + ')' if len(a) == 1 else None)
    t = cambiar_metodo(t, 'setTag', lambda x, a: 'com.copperslug.shim.Nbt.poner(' + x + ', ' + a[0] + ')' if len(a) == 1 else None)
    t = t.replace('ItemStack.isSameItemSameTags(', 'ItemStack.isSameItemSameComponents(')
    return t


def encantamientos(t):
    # EnchantmentHelper.getItemEnchantmentLevel(ModEnchantments.X.get(), s) -> Enc.nivel(ModEnchantments.X, s)
    t = re.sub(r'(?:net\.minecraft\.world\.item\.enchantment\.)?EnchantmentHelper\.getItemEnchantmentLevel\(\s*((?:com\.copperslug\.registry\.)?ModEnchantments\.[A-Z_]+)\.get\(\)\s*,',
               r'com.copperslug.shim.Enc.nivel(\1,', t)
    # s.enchant(ModEnchantments.X.get(), n) -> Enc.poner(s, ModEnchantments.X, n)
    t = cambiar_metodo(t, 'enchant', lambda x, a: ('com.copperslug.shim.Enc.poner(' + x + ', ' + a[0][:-len('.get()')] + ', ' + a[1] + ')')
                       if len(a) == 2 and re.match(r'(?:com\.copperslug\.registry\.)?ModEnchantments\.[A-Z_]+\.get\(\)$', a[0]) else None)
    return t


def entidades(t):
    m = re.search(r'protected void defineSynchedData\(\)\s*\{', t)
    if m:
        fin, _ = argumentos(t.replace('{', '(', 1) if False else t, m.end() - 1) if False else (None, None)
        # el cuerpo: de la llave de apertura a su cierre
        ab = m.end() - 1
        prof, i = 0, ab
        while i < len(t):
            if t[i] == '{':
                prof += 1
            elif t[i] == '}':
                prof -= 1
                if prof == 0:
                    break
            i += 1
        cuerpo = t[ab:i + 1]
        cuerpo = re.sub(r'(?:this\.)?entityData\.define\(', 'b.define(', cuerpo)
        cuerpo = cuerpo.replace('super.defineSynchedData()', 'super.defineSynchedData(b)')
        t = t[:m.start()] + 'protected void defineSynchedData(net.minecraft.network.syncher.SynchedEntityData.Builder b) ' + cuerpo + t[i + 1:]
    return t


def durabilidad(t):
    # s.hurtAndBreak(n, e, x -> x.broadcastBreakEvent(SLOT)) -> s.hurtAndBreak(n, e, SLOT)
    t = re.sub(r'\.hurtAndBreak\(([^,]+),\s*([^,]+),\s*\w+\s*->\s*\w+\.broadcastBreakEvent\(([^)]+)\)\)', r'.hurtAndBreak(\1, \2, \3)', t)
    return t


def java(t):
    t = resource_location(t)
    t = nbt(t)
    t = encantamientos(t)
    t = entidades(t)
    t = durabilidad(t)
    return t


# ---------------------------------------------------------------- datos
CARPETAS = {'recipes': 'recipe', 'advancements': 'advancement', 'loot_tables': 'loot_table', 'loot_modifiers': 'loot_modifiers'}
TAGS = {'items': 'item', 'blocks': 'block', 'entity_types': 'entity_type', 'damage_type': 'damage_type'}


def item_de(o):
    """{"item": x, "count": n, "nbt": ...} -> {"id": x, "count": n} (formato de 1.21)."""
    if isinstance(o, dict) and 'item' in o:
        n = {'id': o['item']}
        if 'count' in o:
            n['count'] = o['count']
        return n
    return o


def receta(j):
    if 'result' in j:
        r = j['result']
        if isinstance(r, str):
            j['result'] = {'id': r}
        else:
            j['result'] = item_de(r)
    return j


def logro(j):
    d = j.get('display')
    if d and isinstance(d.get('icon'), dict):
        d['icon'] = item_de(d['icon'])
        d['icon'].pop('nbt', None)
    for c in (j.get('criteria') or {}).values():
        cond = c.get('conditions') or {}
        if c.get('trigger') == 'minecraft:inventory_changed' and 'items' in cond:
            nuevos = []
            for it in cond['items']:
                if 'items' in it:
                    v = it['items']
                    nuevos.append({'items': v[0] if len(v) == 1 else v})
                elif 'tag' in it:
                    nuevos.append({'items': '#' + it['tag']})
                else:
                    nuevos.append(it)
            cond['items'] = nuevos
    return j


def datos(raiz):
    d = os.path.join(raiz, 'data')
    if not os.path.isdir(d):
        return
    for ns in os.listdir(d):
        for viejo, nuevo in CARPETAS.items():
            a, b = os.path.join(d, ns, viejo), os.path.join(d, ns, nuevo)
            if os.path.isdir(a) and a != b:
                os.makedirs(os.path.dirname(b), exist_ok=True)
                os.rename(a, b)
        tg = os.path.join(d, ns, 'tags')
        if os.path.isdir(tg):
            for viejo, nuevo in TAGS.items():
                a, b = os.path.join(tg, viejo), os.path.join(tg, nuevo)
                if os.path.isdir(a) and a != b:
                    os.rename(a, b)
        for sub, f in [('recipe', receta), ('advancement', logro)]:
            base = os.path.join(d, ns, sub)
            for r, _, fs in os.walk(base):
                for x in fs:
                    if x.endswith('.json'):
                        p = os.path.join(r, x)
                        j = json.load(open(p, encoding='utf-8'))
                        json.dump(f(j), open(p, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)


def convertir(carpeta):
    base = os.path.join(carpeta, 'common/src/main')
    for r, _, fs in os.walk(os.path.join(base, 'java')):
        for x in fs:
            if x.endswith('.java'):
                p = os.path.join(r, x)
                t = open(p, encoding='utf-8').read()
                n = java(t)
                if n != t:
                    open(p, 'w', encoding='utf-8').write(n)
    datos(os.path.join(base, 'resources'))


if __name__ == '__main__':
    convertir(sys.argv[1])

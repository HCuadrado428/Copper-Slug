#!/usr/bin/env python3
"""Comprueba que Suscriptores.java lista todas las clases con @Mod.EventBusSubscriber (y ninguna que no exista).

Si una clase con esa anotación falta en la lista, el bus de eventos nunca la registra y sus @SubscribeEvent no corren
(así pasó con Apuntado). Se arregla regenerando con portar.py o añadiendo la línea a mano. Uso: comprobar_suscriptores.py [raíz]
"""
import os
import re
import sys

raiz = sys.argv[1] if len(sys.argv) > 1 else '.'
java = os.path.join(raiz, 'common/src/main/java')
esperadas = set()
for d, _, fs in os.walk(java):
    for f in fs:
        if not f.endswith('.java') or f == 'Suscriptores.java':
            continue
        t = open(os.path.join(d, f), encoding='utf-8').read()
        if '@Mod.EventBusSubscriber' not in t:
            continue
        pkg = re.search(r'^package ([\w.]+);', t, re.M).group(1)
        lineas = t.split('\n')
        externa = None
        for i, l in enumerate(lineas):
            m = re.match(r'\s*public (?:static )?(?:final )?(?:abstract )?class (\w+)', l)
            if m and externa is None:
                externa = m.group(1)
            if '@Mod.EventBusSubscriber' in l:
                for l2 in lineas[i + 1:i + 4]:
                    m2 = re.match(r'(\s*)public (?:static )?(?:final )?class (\w+)', l2)
                    if m2:
                        n = m2.group(2)
                        anid = len(m2.group(1)) > 0
                        esperadas.add(pkg + '.' + (externa + '$' + n if anid and externa and externa != n else n))
                        break

lista = open(os.path.join(java, 'com/copperslug/Suscriptores.java'), encoding='utf-8').read()
listadas = set(re.findall(r'"(com\.copperslug[\w.$]+)"', lista))
faltan, sobran = sorted(esperadas - listadas), sorted(listadas - esperadas)
for c in faltan:
    print(f'FALTA en Suscriptores.java: {c}')
for c in sobran:
    print(f'SOBRA en Suscriptores.java (no tiene @Mod.EventBusSubscriber): {c}')
if faltan or sobran:
    sys.exit(1)
print(f'Suscriptores.java al día ({len(listadas)} clases)')

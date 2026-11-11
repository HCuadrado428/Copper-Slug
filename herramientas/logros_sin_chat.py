#!/usr/bin/env python3
"""Los 57 logros de las armas escribían en el chat al conseguirlos («X ha conseguido el progreso [..]»), y con tantos era
mucho ruido: se quedan con el aviso (el toast) pero sin anunciarlo en el chat (announce_to_chat: false). Cambia solo ese
valor en el texto, sin reformatear. Vale para las dos carpetas (1.20.1: advancements; 1.21.1: advancement). Idempotente.
Uso: logros_sin_chat.py [raíz del repositorio]
"""
import glob
import os
import sys

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
n = 0
for carpeta in ('advancements', 'advancement'):
    for ruta in glob.glob(os.path.join(RAIZ, 'common/src/main/resources/data/copperslug', carpeta, '**/*.json'), recursive=True):
        t = open(ruta, encoding='utf-8').read()
        nuevo = t.replace('"announce_to_chat": true', '"announce_to_chat": false').replace('"announce_to_chat":true', '"announce_to_chat":false')
        if nuevo != t:
            open(ruta, 'w', encoding='utf-8').write(nuevo)
            n += 1
print('logros sin anuncio en el chat:', n)

#!/usr/bin/env python3
"""Genera los recursos de los nueve accesorios de cobre: texturas de 16x16, modelos, recetas y textos (EN/ES).

Uso: generar_accesorios.py [raíz del repositorio] [--mc 1.20.1|1.21.1]  (idempotente; las recetas cambian de formato)
"""
import json
import os
import sys

from PIL import Image, ImageDraw

args = [a for a in sys.argv[1:] if not a.startswith('--')]
RAIZ = args[0] if args else '.'
V21 = '--mc' in sys.argv and sys.argv[sys.argv.index('--mc') + 1] == '1.21.1'
RES = os.path.join(RAIZ, 'common/src/main/resources')
TEX = os.path.join(RES, 'assets/copperslug/textures/item')
MOD = os.path.join(RES, 'assets/copperslug/models/item')
LANG = os.path.join(RES, 'assets/copperslug/lang')
REC = os.path.join(RES, 'data/copperslug', 'recipe' if V21 else 'recipes')

OSC, MED, CLA, BRI = (122, 62, 38, 255), (192, 106, 64, 255), (226, 140, 96, 255), (250, 190, 140, 255)
HIE, HIE2, NEG = (120, 124, 132, 255), (82, 86, 94, 255), (30, 30, 36, 255)
Z = (0, 0, 0, 0)


def lienzo():
    im = Image.new('RGBA', (16, 16), Z)
    return im, ImageDraw.Draw(im)


def caja(d, x1, y1, x2, y2, c):
    d.rectangle([x1, y1, x2, y2], fill=c)


def borde_cobre(d, x1, y1, x2, y2):
    """Una caja de cobre con luz arriba y sombra abajo."""
    caja(d, x1, y1, x2, y2, MED)
    d.line([x1, y1, x2, y1], fill=CLA)
    d.line([x1, y2, x2, y2], fill=OSC)


def t_canon_largo():
    im, d = lienzo()
    borde_cobre(d, 1, 6, 14, 9)                    # el cañón largo
    caja(d, 14, 5, 15, 10, HIE2)                   # la boca
    d.line([1, 6, 13, 6], fill=BRI)
    for x in (4, 8, 12): caja(d, x, 5, x, 10, OSC)
    caja(d, 0, 6, 0, 9, NEG)
    return im


def t_bipode():
    im, d = lienzo()
    borde_cobre(d, 5, 2, 10, 5)                    # la abrazadera
    d.line([6, 6, 2, 14], fill=MED, width=1); d.line([9, 6, 13, 14], fill=MED, width=1)
    d.line([7, 6, 3, 14], fill=OSC); d.line([8, 6, 12, 14], fill=OSC)
    caja(d, 1, 14, 4, 15, HIE2); caja(d, 11, 14, 14, 15, HIE2)
    caja(d, 7, 3, 8, 4, HIE)
    return im


def t_estrangulador():
    im, d = lienzo()
    for k, (x1, x2) in enumerate(((1, 5), (5, 9), (9, 12))):
        borde_cobre(d, x1, 3 + k, x2, 12 - k)       # un cono que se cierra
    caja(d, 12, 6, 15, 9, HIE2)
    caja(d, 14, 7, 15, 8, NEG)
    d.line([2, 4, 11, 6], fill=BRI)
    return im


def t_radiador():
    im, d = lienzo()
    caja(d, 1, 7, 14, 8, OSC)                       # el eje
    for x in range(2, 14, 3):
        borde_cobre(d, x, 2, x + 1, 13)             # las aletas
        d.point((x, 2), fill=BRI)
    caja(d, 0, 6, 0, 9, HIE2); caja(d, 15, 6, 15, 9, HIE2)
    return im


def t_tubo():
    im, d = lienzo()
    borde_cobre(d, 1, 5, 14, 10)                    # el tubo
    d.line([1, 6, 14, 6], fill=BRI)
    caja(d, 14, 4, 15, 11, HIE)                     # la tapa
    caja(d, 0, 4, 1, 11, HIE2)
    for x in (4, 7, 10): d.line([x, 5, x, 10], fill=OSC)
    d.point((15, 7), fill=NEG); d.point((15, 8), fill=NEG)
    return im


def t_silenciador():
    im, d = lienzo()
    caja(d, 1, 4, 14, 11, HIE2)                     # el cilindro
    d.line([1, 4, 14, 4], fill=HIE)
    d.line([1, 11, 14, 11], fill=NEG)
    for x in (3, 5, 7, 9, 11):
        d.point((x, 6), fill=NEG); d.point((x, 9), fill=NEG)
    caja(d, 0, 5, 1, 10, MED); caja(d, 14, 5, 15, 10, MED)
    d.point((15, 7), fill=NEG); d.point((15, 8), fill=NEG)
    return im


def t_empunadura():
    im, d = lienzo()
    borde_cobre(d, 4, 1, 11, 3)                     # la abrazadera de arriba
    borde_cobre(d, 6, 3, 9, 14)                     # el agarre
    for y in (5, 7, 9, 11): d.line([6, y, 9, y], fill=OSC)
    caja(d, 5, 14, 10, 15, HIE2)
    d.line([7, 3, 7, 13], fill=CLA)
    return im


def t_mira():
    im, d = lienzo()
    borde_cobre(d, 2, 5, 13, 10)                    # el cuerpo de la mira
    caja(d, 0, 4, 2, 11, HIE2); caja(d, 13, 4, 15, 11, HIE2)
    d.ellipse([5, 5, 10, 10], fill=(70, 170, 200, 255), outline=NEG)
    d.point((6, 6), fill=(230, 250, 255, 255))
    caja(d, 6, 11, 9, 14, OSC)                      # la base
    return im


def t_anima():
    im, d = lienzo()
    borde_cobre(d, 1, 3, 14, 12)
    caja(d, 4, 5, 11, 10, NEG)                      # el ánima
    for k, x in enumerate(range(4, 12)):            # el rayado en espiral
        d.point((x, 5 + (k % 4)), fill=MED)
        d.point((x, 10 - (k % 4)), fill=CLA)
    caja(d, 14, 2, 15, 13, HIE2)
    return im


ACC = [
    # id, textura, EN nombre, ES nombre, EN arma, ES arma, EN ayuda, ES ayuda, receta (ingredientes)
    ('canon_largo', t_canon_largo, 'Long Barrel', 'Cañón largo', 'Roulette Revolver', 'Revólver de ruleta',
     'Tighter groups: 40% less spread.', 'Disparos más juntos: un 40 % menos de dispersión.', ['copper_ingot'] * 3 + ['iron_nugget']),
    ('bipode', t_bipode, 'Bipod', 'Bípode', 'Spyglass Rifle', 'Rifle de catalejo',
     'Rock steady: half the spread.', 'Firme como una roca: la mitad de dispersión.', ['copper_ingot'] * 2 + ['iron_nugget'] * 2),
    ('estrangulador', t_estrangulador, 'Choke', 'Estrangulador', 'Pressure Shotgun', 'Escopeta de presión',
     'Pellets fly closer together: 40% less spread.', 'Los perdigones salen más juntos: un 40 % menos de dispersión.', ['copper_ingot'] * 2 + ['iron_nugget', 'stick']),
    ('radiador', t_radiador, 'Radiator', 'Radiador', 'Crank Gatling Gun', 'Gatling de manivela',
     'Runs cooler: 35% less heat per shot.', 'Se calienta menos: un 35 % menos de calor por disparo.', ['copper_ingot'] * 2 + ['iron_ingot', 'redstone']),
    ('tubo', t_tubo, 'Extended Tube', 'Tubo ampliado', 'Winchester 1873', 'Winchester 1873',
     'Four more rounds in the tube.', 'Cuatro balas más en el depósito.', ['copper_ingot'] * 3 + ['iron_ingot']),
    ('silenciador', t_silenciador, 'Suppressor', 'Silenciador', 'Derringer', 'Derringer',
     'Shoots almost silently: sculk does not hear it.', 'Dispara casi sin ruido: el sculk no lo oye.', ['copper_ingot'] * 2 + ['iron_ingot'] * 2),
    ('empunadura', t_empunadura, 'Foregrip', 'Empuñadura frontal', 'Thompson', 'Thompson',
     'Steadier bursts: 30% less spread.', 'Ráfagas más firmes: un 30 % menos de dispersión.', ['copper_ingot'] * 2 + ['stick'] * 2),
    ('mira', t_mira, 'Copper Sight', 'Mira de cobre', 'Bayonet Musket', 'Mosquete con bayoneta',
     'Aim true: half the spread.', 'Puntería fina: la mitad de dispersión.', ['copper_ingot'] * 2 + ['glass_pane', 'iron_nugget']),
    ('anima', t_anima, 'Rifled Bore', 'Ánima rayada', 'Hand Cannon', 'Cañón de mano',
     'The ball flies much straighter.', 'La bola sale mucho más recta.', ['copper_ingot'] * 4),
]

for (aid, tex, en, es, aen, aes, hen, hes, ing) in ACC:
    tex().save(os.path.join(TEX, 'accesorio_%s.png' % aid))
    with open(os.path.join(MOD, 'accesorio_%s.json' % aid), 'w', encoding='utf-8') as f:
        json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': 'copperslug:item/accesorio_' + aid}}, f, indent=1)
    ings = [{'item': 'minecraft:' + i} for i in ing]
    res = {'id': 'copperslug:accesorio_' + aid, 'count': 1} if V21 else {'item': 'copperslug:accesorio_' + aid, 'count': 1}
    os.makedirs(REC, exist_ok=True)
    with open(os.path.join(REC, 'accesorio_%s.json' % aid), 'w', encoding='utf-8') as f:
        json.dump({'type': 'minecraft:crafting_shapeless', 'category': 'equipment', 'ingredients': ings, 'result': res}, f, indent=2)
        f.write('\n')

TEXTOS = {
    'en_us.json': {'msg.copperslug.accesorio.montado': 'Accessory: %s', 'msg.copperslug.accesorio.para': 'Accessory for: %s',
                   'msg.copperslug.accesorio.yunque': 'Fit it in an anvil: weapon on the left, this on the right (2 levels).'},
    'es_es.json': {'msg.copperslug.accesorio.montado': 'Accesorio: %s', 'msg.copperslug.accesorio.para': 'Accesorio para: %s',
                   'msg.copperslug.accesorio.yunque': 'Se monta en el yunque: el arma a la izquierda, esto a la derecha (2 niveles).'},
}
for (aid, tex, en, es, aen, aes, hen, hes, ing) in ACC:
    TEXTOS['en_us.json'].update({'item.copperslug.accesorio_' + aid: en, 'item.copperslug.accesorio_%s.ayuda' % aid: hen,
                                 'accesorio.copperslug.' + aid: en, 'accesorio.copperslug.%s.arma' % aid: aen})
    TEXTOS['es_es.json'].update({'item.copperslug.accesorio_' + aid: es, 'item.copperslug.accesorio_%s.ayuda' % aid: hes,
                                 'accesorio.copperslug.' + aid: es, 'accesorio.copperslug.%s.arma' % aid: aes})
for fn, kv in TEXTOS.items():
    ruta = os.path.join(LANG, fn)
    d = json.load(open(ruta, encoding='utf-8'))
    d.update(kv)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write('\n')
print('accesorios:', len(ACC), 'recetas en', REC)

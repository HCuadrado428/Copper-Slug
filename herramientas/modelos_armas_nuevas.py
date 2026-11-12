#!/usr/bin/env python3
"""Los modelos 3D de las cuatro armas nuevas (cerbatana, lanzallamas, pistola de resonancia y arponera).

Cada función devuelve la lista de elementos del modelo (en píxeles de 16x16x16, la boca hacia z pequeña, igual que el revólver
y la Derringer). Se usan los cañones octogonales de generar_tambor.octogono (cuatro cajas: dos rectas y dos giradas 45°) y
anillos, bandas, miras, guardamontes, carretes y mangueras para que no sean tubos lisos. Los scripts generar_<arma>.py
las meten en armas3d/<arma>_3d.json.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_tambor import caja, octogono, CX  # noqa: E402


def oct_(cy, a, z1, z2, tex, nombre):
    return octogono(cy, a, z1, z2, tex, nombre)


def octogono_x(cx, cy, cz, a, x1, x2, tex, nombre):
    """Un prisma octogonal de apotema a con el eje a lo largo de X (el carrete de la arponera): cuatro cajas, dos rectas y dos
    giradas 45° sobre el eje X, como el octógono de los cañones."""
    import math
    s = 2 * a * math.tan(math.radians(22.5))
    out = []
    for i, (ang, dy, dz) in enumerate(((0, a, s / 2), (0, s / 2, a), (45, a, s / 2), (-45, a, s / 2))):
        out.append(caja(x1 + 0.004 * i, cy - dy, cz - dz, x2 - 0.004 * i, cy + dy, cz + dz, tex, nombre + '_%d' % i,
                        rot=((x1, cy, cz), 'x', ang) if ang else None))
    return out


def cuadrado(x1, y1, z1, x2, y2, z2, tex, nombre, rot=None, caras=None):
    return [caja(x1, y1, z1, x2, y2, z2, tex, nombre, rot=rot, caras=caras)]


def boca_negra(cy, z, r, nombre):
    """El agujero oscuro de la boca (una cara hacia delante)."""
    return [{'name': nombre, 'from': [CX - r, cy - r, z - 0.04], 'to': [CX + r, cy + r, z],
             'faces': {'north': {'uv': [15.0, 5.95, 15.5, 6.45], 'texture': '#negro'}}}]


def guardamonte(y_bajo, y_alto, z1, z2, nombre, tex='hierro'):
    """Guardamonte: tres tiras finas (delante, abajo y detrás) bajo el cuerpo."""
    g = 0.3
    el = []
    el += cuadrado(CX - 0.2, y_bajo, z1, CX + 0.2, y_alto, z1 + g, tex, nombre + '_d')
    el += cuadrado(CX - 0.2, y_bajo, z1, CX + 0.2, y_bajo + g, z2, tex, nombre + '_b')
    el += cuadrado(CX - 0.2, y_bajo, z2 - g, CX + 0.2, y_alto, z2, tex, nombre + '_t')
    return el


def cerbatana():
    cy = 9.6
    el = []
    # el tubo largo, de cobre, con la boca acampanada y la boquilla de madera
    el += oct_(cy, 0.75, 1.6, 14.0, 'cobre', 'cer_tubo')
    el += oct_(cy, 0.98, 0.9, 2.4, 'cobre', 'cer_campana')
    el += oct_(cy, 1.1, 0.7, 1.15, 'hierro', 'cer_aro_boca')
    el += boca_negra(cy, 0.7, 0.55, 'cer_boca')
    el += oct_(cy, 0.62, 14.0, 15.3, 'madera', 'cer_boquilla')
    el += oct_(cy, 0.92, 15.3, 15.75, 'madera', 'cer_boquilla_borde')
    # bandas de hierro con un filo de latón al lado
    for z, n in ((3.9, 'a'), (7.4, 'b'), (11.2, 'c')):
        el += oct_(cy, 0.9, z, z + 0.55, 'hierro', 'cer_banda_' + n)
        el += oct_(cy, 0.84, z + 0.55, z + 0.8, 'laton', 'cer_filo_' + n)
    # el agarre: tres vueltas de cuero
    for i, z in enumerate((5.1, 5.75, 6.4)):
        el += oct_(cy, 0.86, z, z + 0.45, 'cuero', 'cer_cuero_%d' % i)
    # una mira de punta y una muesca atrás
    el += cuadrado(CX - 0.15, cy + 0.72, 2.5, CX + 0.15, cy + 1.4, 2.8, 'hierro', 'cer_mira')
    el += cuadrado(CX - 0.55, cy + 0.72, 12.2, CX - 0.3, cy + 1.2, 12.5, 'hierro', 'cer_muesca_i')
    el += cuadrado(CX + 0.3, cy + 0.72, 12.2, CX + 0.55, cy + 1.2, 12.5, 'hierro', 'cer_muesca_d')
    # una correa de cuero colgando bajo el tubo
    el += cuadrado(CX - 0.18, cy - 1.45, 7.7, CX + 0.18, cy - 0.7, 8.1, 'cuero', 'cer_correa_a')
    el += cuadrado(CX - 0.18, cy - 1.45, 7.7, CX + 0.18, cy - 1.15, 9.2, 'cuero', 'cer_correa_b')
    el += cuadrado(CX - 0.18, cy - 1.45, 8.8, CX + 0.18, cy - 0.7, 9.2, 'cuero', 'cer_correa_c')
    return el


def lanzallamas():
    cy = 9.9
    el = []
    # el cañón con su camisa de refrigeración (anillos con rejillas entre medias)
    el += oct_(cy, 1.0, 2.0, 11.2, 'cobre', 'lan_canon')
    for i, z in enumerate((2.6, 3.9, 5.2, 6.5, 7.8)):
        el += oct_(cy, 1.22, z, z + 0.5, 'hierro', 'lan_aro_%d' % i)
        el += cuadrado(CX - 0.45, cy + 1.0, z + 0.55, CX + 0.45, cy + 1.08, z + 1.25, 'negro', 'lan_rejilla_%d' % i)
    # la boquilla: embudo de hierro con el fondo negro, y el piloto al lado
    el += oct_(cy, 1.35, 0.9, 2.0, 'hierro', 'lan_embudo')
    el += oct_(cy, 0.95, 0.6, 1.0, 'hierro', 'lan_embudo_borde')
    el += boca_negra(cy, 0.6, 0.6, 'lan_boca')
    el += cuadrado(CX + 1.05, cy - 0.95, 0.5, CX + 1.35, cy - 0.65, 2.4, 'hierro', 'lan_piloto_tubo')
    el += cuadrado(CX + 1.0, cy - 1.05, 0.0, CX + 1.4, cy - 0.55, 0.5, 'brasa', 'lan_piloto_llama')
    # la mira
    el += cuadrado(CX - 0.15, cy + 1.0, 3.0, CX + 0.15, cy + 1.7, 3.35, 'hierro', 'lan_mira')
    # el depósito de debajo, con tapas, correas, válvula y manómetro
    ty = 5.6
    el += oct_(ty, 1.7, 4.6, 10.8, 'tambor', 'lan_deposito')
    el += oct_(ty, 1.45, 4.3, 4.6, 'hierro', 'lan_tapa_d')
    el += oct_(ty, 1.45, 10.8, 11.1, 'hierro', 'lan_tapa_t')
    for i, z in enumerate((5.4, 9.7)):
        el += oct_(ty, 1.82, z, z + 0.55, 'cuero', 'lan_correa_%d' % i)
    el += cuadrado(CX - 0.3, ty + 1.7, 7.0, CX + 0.3, ty + 2.2, 7.6, 'laton', 'lan_valvula')
    el += cuadrado(CX - 0.6, ty + 2.2, 6.9, CX + 0.6, ty + 2.45, 7.7, 'hierro', 'lan_volante')
    el += cuadrado(CX + 1.7, ty - 0.5, 7.6, CX + 2.05, ty + 0.5, 8.6, 'laton', 'lan_manometro')
    el += cuadrado(CX + 2.05, ty - 0.3, 7.8, CX + 2.12, ty + 0.3, 8.4, 'negro', 'lan_manometro_cara', caras=('east',))
    # las tuberías que suben del depósito al cañón
    el += cuadrado(CX - 0.35, ty + 1.6, 5.2, CX + 0.35, cy - 1.0, 5.9, 'hierro', 'lan_tubo_a')
    el += cuadrado(CX - 0.35, ty + 1.6, 9.2, CX + 0.35, cy - 1.0, 9.9, 'hierro', 'lan_tubo_b')
    # el cuerpo, el guardamonte, la empuñadura y la culata
    el += cuadrado(CX - 1.15, 7.6, 11.2, CX + 1.15, 11.3, 13.4, 'cobre', 'lan_cuerpo')
    el += cuadrado(CX - 0.7, 11.3, 11.6, CX + 0.7, 11.8, 12.6, 'hierro', 'lan_encendedor')
    el += guardamonte(6.5, 7.6, 11.4, 13.1, 'lan_guarda')
    el += cuadrado(CX - 0.6, 3.9, 12.6, CX + 0.6, 7.6, 14.2, 'madera', 'lan_agarre')
    el += cuadrado(CX - 0.3, 6.9, 11.6, CX + 0.3, 7.5, 11.95, 'hierro', 'lan_gatillo')
    el += cuadrado(CX - 0.9, 8.1, 13.4, CX + 0.9, 11.0, 14.8, 'cuero', 'lan_culata')
    return el


def resonancia():
    cy = 9.6
    el = []
    # el cuerpo: receptor de cobre con las esquinas cortadas
    el += oct_(9.4, 1.25, 7.8, 12.2, 'cobre', 'res_cuerpo')
    el += oct_(cy, 0.7, 2.4, 7.8, 'cobre', 'res_canon')
    # la bocina: anillos de eco que crecen hacia la boca, separados por latón
    for i, (z, a) in enumerate(((6.7, 0.95), (5.6, 1.05), (4.5, 1.15), (3.4, 1.25), (2.3, 1.35))):
        el += oct_(cy, a, z, z + 0.75, 'eco', 'res_bobina_%d' % i)
        el += oct_(cy, a - 0.18, z + 0.75, z + 1.0, 'laton', 'res_sep_%d' % i)
    # el diapasón: dos púas al frente con la punta de eco
    for lado, n in ((-1, 'i'), (1, 'd')):
        x1, x2 = (CX + 0.95 * lado - 0.25, CX + 0.95 * lado + 0.25)
        el += cuadrado(min(x1, x2), cy - 0.55, 0.4, max(x1, x2), cy + 0.55, 2.4, 'cobre', 'res_pua_' + n)
        el += cuadrado(min(x1, x2), cy - 0.55, 0.0, max(x1, x2), cy + 0.55, 0.45, 'eco', 'res_pua_punta_' + n)
    # el cristal de eco sobre el cuerpo, en su cuna de hierro (un rombo)
    el += cuadrado(CX - 0.95, 10.65, 8.7, CX + 0.95, 11.0, 11.0, 'hierro', 'res_cuna')
    for dx, n in ((-0.8, 'i'), (0.8, 'd')):
        el += cuadrado(CX + dx - 0.12, 11.0, 8.8, CX + dx + 0.12, 12.1, 9.1, 'hierro', 'res_garra_a' + n)
        el += cuadrado(CX + dx - 0.12, 11.0, 10.6, CX + dx + 0.12, 12.1, 10.9, 'hierro', 'res_garra_b' + n)
    el += cuadrado(CX - 0.5, 11.15, 9.1, CX + 0.5, 12.6, 10.6, 'eco', 'res_cristal_a', rot=((CX, 11.9, 9.85), 'z', 45))
    el += cuadrado(CX - 0.5, 11.15, 9.1, CX + 0.5, 12.6, 10.6, 'eco', 'res_cristal_b')
    # el dial del lateral
    el += cuadrado(CX + 1.25, 8.7, 9.2, CX + 1.4, 10.1, 10.6, 'laton', 'res_dial')
    el += cuadrado(CX + 1.4, 9.1, 9.6, CX + 1.45, 9.7, 10.2, 'negro', 'res_dial_cara', caras=('east',))
    # el aleta de atrás, el guardamonte, el gatillo y la empuñadura con placas de madera
    el += cuadrado(CX - 0.3, 10.65, 11.4, CX + 0.3, 11.5, 12.6, 'cobre', 'res_aleta')
    el += guardamonte(6.6, 8.1, 8.8, 10.6, 'res_guarda')
    el += cuadrado(CX - 0.3, 7.0, 9.4, CX + 0.3, 8.1, 9.75, 'hierro', 'res_gatillo')
    el += cuadrado(CX - 0.65, 4.6, 10.4, CX + 0.65, 8.2, 12.4, 'cobre', 'res_agarre_nucleo')
    el += cuadrado(CX - 0.8, 4.7, 10.5, CX - 0.6, 8.1, 12.3, 'madera', 'res_placa_i')
    el += cuadrado(CX + 0.6, 4.7, 10.5, CX + 0.8, 8.1, 12.3, 'madera', 'res_placa_d')
    el += cuadrado(CX - 0.75, 4.3, 10.3, CX + 0.75, 4.7, 12.5, 'laton', 'res_cantonera')
    return el


def arponera():
    cy = 9.6
    el = []
    # el cañón ancho con dos abrazaderas
    el += oct_(cy, 1.0, 3.0, 10.5, 'cobre', 'arp_canon')
    for z, n in ((4.6, 'a'), (8.0, 'b')):
        el += oct_(cy, 1.22, z, z + 0.6, 'hierro', 'arp_banda_' + n)
    # el arpón asomando: asta, punta y las dos aletas en cruz
    el += oct_(cy, 0.38, 1.4, 3.0, 'hierro', 'arp_asta')
    el += cuadrado(CX - 0.18, cy - 0.18, 0.2, CX + 0.18, cy + 0.18, 1.5, 'acero', 'arp_punta')
    el += cuadrado(CX - 0.85, cy - 0.1, 1.2, CX + 0.85, cy + 0.1, 2.1, 'acero', 'arp_aleta_h')
    el += cuadrado(CX - 0.1, cy - 0.85, 1.2, CX + 0.1, cy + 0.85, 2.1, 'acero', 'arp_aleta_v')
    el += cuadrado(CX - 0.6, cy - 0.06, 1.5, CX + 0.6, cy + 0.06, 2.4, 'acero', 'arp_aleta_d1', rot=((CX, cy, 1.9), 'z', 45))
    # el carrete a la derecha: tambor de cuerda entre dos platos de hierro, y la manivela
    rx = CX + 1.9
    el += octogono_x(rx - 0.75, cy, 7.0, 1.4, rx - 0.75, rx + 0.75, 'cuerda', 'arp_tambor')
    el += octogono_x(rx - 0.75, cy, 7.0, 1.7, rx - 0.95, rx - 0.75, 'hierro', 'arp_plato_i')
    el += octogono_x(rx - 0.75, cy, 7.0, 1.7, rx + 0.75, rx + 0.95, 'hierro', 'arp_plato_d')
    el += cuadrado(rx + 0.95, cy + 0.3, 6.75, rx + 1.15, cy + 1.9, 7.25, 'hierro', 'arp_brazo')
    el += cuadrado(rx + 1.15, cy + 1.5, 6.6, rx + 2.1, cy + 2.1, 7.4, 'madera', 'arp_pomo')
    # la cuerda que sale del carrete hacia el cañón
    el += cuadrado(CX + 0.95, cy + 0.2, 3.2, CX + 1.25, cy + 0.55, 5.8, 'cuerda', 'arp_cuerda_a')
    el += cuadrado(CX + 1.0, cy - 0.35, 5.6, CX + 1.9, cy + 0.0, 6.0, 'cuerda', 'arp_cuerda_b')
    # el guardamanos de madera con cuero, el cuerpo, la empuñadura, el guardamonte y la culata
    el += cuadrado(CX - 0.95, 7.2, 5.0, CX + 0.95, 8.6, 9.2, 'madera', 'arp_guardamanos')
    el += cuadrado(CX - 1.0, 7.1, 6.4, CX + 1.0, 8.7, 6.9, 'cuero', 'arp_guardamanos_cuero')
    el += cuadrado(CX - 1.2, 7.4, 10.5, CX + 1.2, 11.0, 13.2, 'cobre', 'arp_cuerpo')
    el += cuadrado(CX - 0.6, 3.9, 11.6, CX + 0.6, 7.4, 13.2, 'madera', 'arp_agarre')
    el += guardamonte(6.4, 7.4, 10.8, 12.6, 'arp_guarda')
    el += cuadrado(CX - 0.3, 6.7, 11.0, CX + 0.3, 7.3, 11.35, 'hierro', 'arp_gatillo')
    el += cuadrado(CX - 0.15, cy + 1.0, 3.4, CX + 0.15, cy + 1.8, 3.75, 'hierro', 'arp_mira')
    el += cuadrado(CX - 0.5, 11.0, 12.0, CX + 0.5, 11.55, 12.5, 'hierro', 'arp_alza')
    el += cuadrado(CX - 0.9, 8.2, 13.2, CX + 0.9, 11.0, 14.7, 'madera', 'arp_culata')
    return el


MODELOS = {'cerbatana': cerbatana, 'lanzallamas': lanzallamas, 'resonancia': resonancia, 'arponera': arponera}

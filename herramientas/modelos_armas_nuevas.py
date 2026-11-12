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
    import generar_tambor
    if generar_tambor.CUADRADOS:
        return [caja(x1, cy - a, cz - a, x2, cy + a, cz + a, tex, nombre)]
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
    el += oct_(cy, 0.95, 1.8, 13.6, 'cobre', 'cer_tubo')
    el += oct_(cy, 1.2, 0.9, 2.6, 'cobre', 'cer_campana')
    el += oct_(cy, 1.3, 0.6, 1.1, 'hierro', 'cer_aro_boca')
    el += boca_negra(cy, 0.6, 0.7, 'cer_boca')
    el += oct_(cy, 0.8, 13.6, 14.8, 'madera', 'cer_boquilla')
    el += oct_(cy, 1.1, 14.8, 15.3, 'madera', 'cer_boquilla_borde')
    # tres bandas de hierro con un filo de latón al lado
    for z, n in ((3.9, 'a'), (7.4, 'b'), (11.0, 'c')):
        el += oct_(cy, 1.1, z, z + 0.6, 'hierro', 'cer_banda_' + n)
        el += oct_(cy, 1.02, z + 0.6, z + 0.9, 'laton', 'cer_filo_' + n)
    # el agarre: vueltas de cuero
    for i, z in enumerate((5.0, 5.7, 6.4)):
        el += oct_(cy, 1.04, z, z + 0.5, 'cuero', 'cer_cuero_%d' % i)
    # la mira de punta (delante) y las muescas (atrás)
    el += cuadrado(CX - 0.15, cy + 1.15, 2.5, CX + 0.15, cy + 1.9, 2.85, 'hierro', 'cer_mira')
    el += cuadrado(CX - 0.7, cy + 0.95, 12.1, CX - 0.4, cy + 1.6, 12.5, 'hierro', 'cer_muesca_i')
    el += cuadrado(CX + 0.4, cy + 0.95, 12.1, CX + 0.7, cy + 1.6, 12.5, 'hierro', 'cer_muesca_d')
    # el carcaj de dardos, atado al costado: un tubo de cuero con las plumas asomando
    qx = CX + 1.75
    for z, n in ((6.2, 'a'), (9.6, 'b')):
        el += cuadrado(qx - 0.55, cy - 1.15, z, qx + 0.55, cy + 0.15, z + 0.5, 'cuero', 'cer_atadura_' + n)
    el += cuadrado(qx - 0.45, cy - 1.05, 6.4, qx + 0.45, cy + 0.05, 10.0, 'cuero', 'cer_carcaj')
    for dx, tex, n in ((-0.25, 'laton', 'a'), (0.0, 'eco', 'b'), (0.25, 'madera', 'c')):
        el += cuadrado(qx + dx - 0.1, cy - 0.55, 5.6, qx + dx + 0.1, cy - 0.05, 6.4, tex, 'cer_pluma_' + n)
    # una borla de plumas atrás, colgando de la boquilla
    el += cuadrado(CX - 0.15, cy - 1.0, 15.0, CX + 0.15, cy - 0.7, 15.4, 'cuero', 'cer_cordon')
    el += cuadrado(CX - 0.4, cy - 2.4, 14.9, CX + 0.4, cy - 1.0, 15.5, 'eco', 'cer_borla')
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
    # la mira de punta sobre el último anillo
    el += cuadrado(CX - 0.12, cy + 1.3, 2.4, CX + 0.12, cy + 2.0, 2.75, 'hierro', 'res_mira')
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
    # el cañón ancho con dos abrazaderas y la boca acampanada
    el += oct_(cy, 1.0, 3.4, 10.5, 'cobre', 'arp_canon')
    el += oct_(cy, 1.25, 2.6, 3.8, 'cobre', 'arp_campana')
    for z, n in ((4.9, 'a'), (8.2, 'b')):
        el += oct_(cy, 1.22, z, z + 0.6, 'hierro', 'arp_banda_' + n)
    # el arpón cargado, asomando bien: asta larga, cabeza de punta con dos alas y las muescas del barbado
    el += oct_(cy, 0.4, -2.2, 3.4, 'madera', 'arp_asta')
    el += cuadrado(CX - 0.25, cy - 0.25, -3.6, CX + 0.25, cy + 0.25, -2.2, 'acero', 'arp_punta')
    el += cuadrado(CX - 0.55, cy - 0.45, -2.6, CX + 0.55, cy + 0.45, -0.9, 'acero', 'arp_cabeza')
    el += cuadrado(CX - 1.5, cy - 0.12, -1.6, CX + 1.5, cy + 0.12, 0.2, 'acero', 'arp_ala_h')
    el += cuadrado(CX - 0.12, cy - 1.5, -1.6, CX + 0.12, cy + 1.5, 0.2, 'acero', 'arp_ala_v')
    el += cuadrado(CX - 1.2, cy - 0.1, -0.6, CX + 1.2, cy + 0.1, 0.6, 'hierro', 'arp_pua_h')
    el += cuadrado(CX - 0.1, cy - 1.2, -0.6, CX + 0.1, cy + 1.2, 0.6, 'hierro', 'arp_pua_v')
    # la cuerda atada al asta, que baja hasta el carrete
    el += cuadrado(CX - 0.55, cy - 0.5, 0.4, CX + 0.55, cy + 0.5, 1.2, 'cuerda', 'arp_nudo')
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


# La mano en primera persona de cada arma (giro x, giro y, traslado x, y, z y escala): propia de cada una, a una escala como
# la del revólver (con la de la Winchester, que es un arma larga, salían diminutas y flotando en medio de la pantalla).
MANO = {
    'cerbatana': (2, 18, 1.0, -2.0, -6.5, 0.85),
    'lanzallamas': (2, 20, 0.8, 1.8, -5.5, 0.85),
    'resonancia': (2, 20, 0.8, 3.0, -5.0, 0.9),
    'arponera': (2, 20, 0.8, 1.5, -5.5, 0.88),
}

# Las miras de cada arma, en píxeles del modelo: (alza y, alza z, punto de mira y, punto de mira z, distancia del ojo al alza).
MIRAS = {
    'cerbatana': (10.8, 12.3, 11.5, 2.65, 0.45),
    'lanzallamas': (11.8, 12.1, 11.6, 3.2, 0.5),
    'resonancia': (11.5, 12.0, 11.6, 2.6, 0.45),
    'arponera': (11.55, 12.25, 11.4, 3.55, 0.5),
}


def con_mano(base, nombre, revolver):
    """Pone en el modelo la mano propia del arma: la del revólver para todo (tercera persona, suelo, marco) salvo la de primera persona."""
    d = dict(revolver['display'])
    rx, ry, tx, ty, tz, sc = MANO[nombre]
    for lado in ('firstperson_righthand', 'firstperson_lefthand'):
        d[lado] = {'rotation': [rx, ry, 0], 'translation': [tx, ty, tz], 'scale': [sc, sc, sc]}
    base['display'] = d
    return base


MODELOS = {'cerbatana': cerbatana, 'lanzallamas': lanzallamas, 'resonancia': resonancia, 'arponera': arponera}

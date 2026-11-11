#!/usr/bin/env python3
"""Genera los modelos 3D del revólver (un Colt de acción simple) con las recámaras del tambor.

Se parte de herramientas/revolver_3d_original.json (de ahí se conservan el armazón de abajo, el guardamonte, el gatillo y
la empuñadura) y se construye el resto: cañón y tambor octogonales (cuatro cajas, dos de ellas giradas 45°), punto de
mira, mira de muesca con alza, martillo, eje del tambor y el hueco de carga del lado derecho del armazón, por donde se
ven desde atrás los culotes de latón de las balas.

El tambor enseña las recámaras EN SU SITIO: la de arriba es la que toca (como la muesca del HUD) y el resto, en el
sentido del reloj visto desde atrás. La máscara de 6 bits (bit k = recámara k desde la que toca, cargada o no) la da la
propiedad de objeto «copperslug:recamaras» (0 a 63), que elige entre:
  armas3d/revolver_3d.json (máscara 0) y armas3d/revolver_3d_m1..m63.json (los modelos del arma),
  armas3d/revolver_3d_abierto.json (el tambor salido a un lado, al meter una bala),
  revolver_cargado_<óxido 0..3>_<máscara 1..63>.json                       (los de cada nivel de óxido).
Todas las texturas siguen siendo de 16x16. Se puede ejecutar de nuevo cuando se quiera.
Uso: generar_tambor.py [raíz del repositorio]
"""
import copy
import json
import math
import os
import sys

RAIZ = sys.argv[1] if len(sys.argv) > 1 else '.'
M = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/models/item')
A3D = os.path.join(M, 'armas3d')
ORIGINAL = os.path.join(RAIZ, 'herramientas/revolver_3d_original.json')

NIVELES = [(0, 'revolver', None), (1, 'revolver_expuesto', 0.25), (2, 'revolver_erosionado', 0.5), (3, 'revolver_oxidado', 0.75)]

# ---------------------------------------------------------------------------------------------- medidas
CX = 8.0
BARRIL = dict(cy=9.9, a=0.72, z1=1.5, z2=8.4)          # el cañón (centro, apotema, de la boca al tambor)
TAMBOR = dict(cy=8.9, a=1.62, z1=8.4, z2=11.0)         # el tambor
ANILLO = 1.0                                           # radio del anillo de recámaras
Z_ATRAS = TAMBOR['z2']                                 # la cara de atrás del tambor
UV_LATON = [4.2, 1.2, 4.8, 1.8]                        # el píxel dorado de tambor_frente_*
UV_PISTON = [2.2, 2.2, 2.8, 2.8]                       # el gris del centro de tambor_frente_*
UV_NEGRO = [15.0, 5.95, 15.5, 6.45]


def r3(v):
    return round(v, 3)


def uv_caja(d, x1, y1, z1, x2, y2, z2):
    """UV que sigue las coordenadas del mundo (igual densidad de píxel en todas las caras)."""
    if d in ('north', 'south'):
        return [r3(x1 % 16), r3(16 - y2), r3(x1 % 16 + (x2 - x1)), r3(16 - y1)]
    if d in ('east', 'west'):
        return [r3(z1), r3(16 - y2), r3(z2), r3(16 - y1)]
    return [r3(x1 % 16), r3(z1), r3(x1 % 16 + (x2 - x1)), r3(z2)]


def caja(x1, y1, z1, x2, y2, z2, tex='cobre', nombre='caja', rot=None, caras=None):
    e = {'name': nombre, 'from': [r3(x1), r3(y1), r3(z1)], 'to': [r3(x2), r3(y2), r3(z2)], 'faces': {}}
    for d in caras or ('north', 'south', 'east', 'west', 'up', 'down'):
        e['faces'][d] = {'uv': uv_caja(d, x1, y1, z1, x2, y2, z2), 'texture': '#' + tex}
    if rot:
        e['rotation'] = {'origin': [r3(v) for v in rot[0]], 'axis': rot[1], 'angle': rot[2]}
    return e


def octogono(cy, a, z1, z2, tex, nombre, tex_lado=None, uv_lado=None):
    """Un prisma octogonal de apotema a: dos cajas rectas y dos giradas 45° (la unión es el octógono)."""
    s = 2 * a * math.tan(math.radians(22.5))
    out = []
    for i, (ang, dx, dy) in enumerate(((0, a, s / 2), (0, s / 2, a), (45, a, s / 2), (-45, a, s / 2))):
        # los extremos se desplazan una pizca para que no peleen entre sí al coincidir
        e = caja(CX - dx, cy - dy, z1 + 0.004 * i, CX + dx, cy + dy, z2 - 0.004 * i, tex, nombre + '_%d' % i,
                 rot=((CX, cy, 0), 'z', ang) if ang else None)
        if tex_lado:
            for d in ('east', 'west', 'up', 'down'):
                e['faces'][d]['texture'] = '#' + tex_lado
                if uv_lado:
                    e['faces'][d]['uv'] = list(uv_lado)
        out.append(e)
    return out


def recamara_pos(k):
    ang = math.radians(60 * k)
    return CX + ANILLO * math.sin(ang), TAMBOR['cy'] + ANILLO * math.cos(ang)


def cara_trasera(cx, cy, z, tex, uv, tam, grosor, nombre, lado='south'):
    return {'name': nombre, 'from': [r3(cx - tam), r3(cy - tam), r3(z)], 'to': [r3(cx + tam), r3(cy + tam), r3(z + grosor)],
            'faces': {lado: {'uv': list(uv), 'texture': '#' + tex}}}


def recamaras(mascara):
    out = []
    cy = TAMBOR['cy']
    for k in range(6):
        x, y = recamara_pos(k)
        cargada = bool(mascara >> k & 1)
        # cara de atrás: borde de hierro y agujero oscuro (o el culote de latón de la bala, que sobresale)
        out.append(cara_trasera(x, y, Z_ATRAS, 'hierro', [2, 2, 3.5, 3.5], 0.42, 0.02, 'cil_borde_t'))
        if cargada:
            lat = {'uv': UV_LATON, 'texture': '#tambor'}
            out.append({'name': 'cil_culote', 'from': [r3(x - 0.3), r3(y - 0.3), Z_ATRAS], 'to': [r3(x + 0.3), r3(y + 0.3), Z_ATRAS + 0.4],
                        'faces': {'south': dict(lat), 'east': dict(lat), 'west': dict(lat), 'up': dict(lat), 'down': dict(lat)}})
            out.append(cara_trasera(x, y, Z_ATRAS + 0.4, 'tambor', UV_PISTON, 0.12, 0.02, 'cil_piston'))
        else:
            out.append(cara_trasera(x, y, Z_ATRAS + 0.02, 'negro', UV_NEGRO, 0.3, 0.02, 'cil_agujero_t'))
        # cara de delante: los mismos agujeros (se ven mirando al arma de frente); las cargadas, con el plomo
        front = TAMBOR['z1']
        out.append({'name': 'cil_borde_d', 'from': [r3(x - 0.42), r3(y - 0.42), front - 0.02], 'to': [r3(x + 0.42), r3(y + 0.42), front],
                    'faces': {'north': {'uv': [2, 2, 3.5, 3.5], 'texture': '#hierro'}}})
        if cargada:
            out.append({'name': 'cil_plomo_d', 'from': [r3(x - 0.28), r3(y - 0.28), front - 0.04], 'to': [r3(x + 0.28), r3(y + 0.28), front - 0.02],
                        'faces': {'north': {'uv': [3.4, 3.4, 3.9, 3.9], 'texture': '#hierro'}}})
        else:
            out.append({'name': 'cil_agujero_d', 'from': [r3(x - 0.3), r3(y - 0.3), front - 0.04], 'to': [r3(x + 0.3), r3(y + 0.3), front - 0.02],
                        'faces': {'north': {'uv': list(UV_NEGRO), 'texture': '#negro'}}})
    # el eje del tambor (un clavito de hierro en el centro, por los dos lados)
    out.append(cara_trasera(CX, cy, Z_ATRAS, 'hierro', [2, 2, 3.5, 3.5], 0.3, 0.03, 'cil_eje_t'))
    out.append({'name': 'cil_eje_d', 'from': [CX - 0.3, cy - 0.3, TAMBOR['z1'] - 0.03], 'to': [CX + 0.3, cy + 0.3, TAMBOR['z1']],
                'faces': {'north': {'uv': [2, 2, 3.5, 3.5], 'texture': '#hierro'}}})
    return out


def cilindro(mascara):
    out = octogono(TAMBOR['cy'], TAMBOR['a'], TAMBOR['z1'], TAMBOR['z2'], 'cobre', 'cil_cuerpo', tex_lado='tambor_lado', uv_lado=[6, 6, 10, 10])
    return out + recamaras(mascara)


def construir(mascara, abierto=False):
    original = cargar(ORIGINAL)
    conservar = [original['elements'][i] for i in (7, 9, 10, 11, 12, 13, 14)]
    el = []
    # ---- el cañón, con la boca, el punto de mira y la varilla del eyector debajo
    el += octogono(BARRIL['cy'], BARRIL['a'], BARRIL['z1'], BARRIL['z2'], 'cobre', 'canon')
    el.append({'name': 'boca', 'from': [CX - 0.26, BARRIL['cy'] - 0.26, BARRIL['z1'] - 0.03], 'to': [CX + 0.26, BARRIL['cy'] + 0.26, BARRIL['z1'] - 0.01],
               'faces': {'north': {'uv': list(UV_NEGRO), 'texture': '#negro'}}})
    el.append(caja(CX - 0.18, 10.55, 1.9, CX + 0.18, 11.15, 2.4, 'hierro', 'punto_de_mira'))
    el.append(caja(CX + 0.35, 8.95, 2.6, CX + 0.85, 9.4, 8.4, 'hierro', 'varilla'))
    el.append(caja(CX + 0.25, 8.85, 2.35, CX + 0.95, 9.5, 2.6, 'hierro', 'tapon_varilla'))
    # ---- la parte de atrás de un Colt de acción simple
    # la cinta de arriba, con la ranura de la mira a todo lo largo (dos raíles y el fondo más bajo)
    el.append(caja(7.0, 10.5, 8.4, 7.85, 11.05, 12.6, 'cobre', 'cinta_izq'))
    el.append(caja(8.15, 10.5, 8.4, 9.0, 11.05, 12.6, 'cobre', 'cinta_der'))
    el.append(caja(7.85, 10.5, 8.4, 8.15, 10.8, 12.6, 'cobre', 'cinta_fondo'))
    # el escudo de retroceso: una placa detrás del tambor, con el agujero del percutor y el hueco de carga SOLO a la
    # derecha (por ahí se ven los culotes de las dos recámaras de ese lado, como por la puerta de carga de uno de verdad)
    el.append(caja(6.8, 7.4, 11.0, 8.4, 10.5, 12.2, 'cobre', 'escudo_izq'))
    el.append(caja(8.4, 9.8, 11.0, 9.2, 10.5, 12.2, 'cobre', 'escudo_der_alto'))
    el.append(caja(8.4, 7.4, 11.0, 9.2, 8.0, 12.2, 'cobre', 'escudo_der_bajo'))
    el.append({'name': 'percutor', 'from': [7.8, 8.7, 12.18], 'to': [8.2, 9.1, 12.2], 'faces': {'south': {'uv': list(UV_NEGRO), 'texture': '#negro'}}})
    # el martillo: cuerpo, cuello inclinado hacia atrás y el espolón plano (por debajo de la línea de mira)
    el.append(caja(7.85, 9.3, 12.2, 8.15, 10.3, 12.7, 'hierro', 'martillo'))
    el.append(caja(7.85, 10.0, 12.55, 8.15, 10.8, 13.05, 'hierro', 'martillo_cuello', rot=((CX, 10.0, 12.8), 'x', 22.5)))
    el.append(caja(7.75, 10.55, 12.95, 8.25, 10.85, 13.55, 'hierro', 'martillo_espolon'))
    # la cola de la empuñadura: una tira que sube desde la culata hasta detrás del escudo, inclinada hacia atrás
    el.append(caja(7.55, 7.0, 12.2, 8.45, 10.2, 12.8, 'cobre', 'cola', rot=((CX, 10.2, 12.5), 'x', -22.5)))
    el += conservar
    cil = cilindro(mascara)
    if abierto:
        # el tambor salido hacia la izquierda (con su grúa) para meter la bala
        for e in cil:
            e['from'][0] = r3(e['from'][0] - 3.4)
            e['to'][0] = r3(e['to'][0] - 3.4)
            if 'rotation' in e:
                e['rotation']['origin'][0] = r3(e['rotation']['origin'][0] - 3.4)
        el.append(caja(5.6, 6.9, 8.6, 7.2, 7.45, 10.6, 'cobre', 'grua'))
    el += cil
    m = copy.deepcopy(original)
    m['elements'] = el
    return m


def cargar(ruta):
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)


def guardar(ruta, datos, compacto=False):
    with open(ruta, 'w', encoding='utf-8') as f:
        if compacto:
            json.dump(datos, f, separators=(',', ':'), ensure_ascii=False)
        else:
            json.dump(datos, f, indent=1, ensure_ascii=False)
        f.write('\n')


def main():
    for f in os.listdir(A3D):
        if f.startswith('revolver_3d_n') or f.startswith('revolver_3d_m'):
            os.remove(os.path.join(A3D, f))
    for f in os.listdir(M):
        if f.startswith('revolver_cargado_'):
            os.remove(os.path.join(M, f))
    for mascara in range(0, 64):
        nombre = 'revolver_3d.json' if mascara == 0 else 'revolver_3d_m%d.json' % mascara
        guardar(os.path.join(A3D, nombre), construir(mascara), True)
    guardar(os.path.join(A3D, 'revolver_3d_abierto.json'), construir(0, abierto=True), True)
    for ox, nombre, _ in NIVELES:
        obj = cargar(os.path.join(M, nombre + '.json'))
        obj.pop('overrides', None)
        for mascara in range(1, 64):
            o = copy.deepcopy(obj)
            o['base']['parent'] = 'copperslug:item/armas3d/revolver_3d_m%d' % mascara
            guardar(os.path.join(M, 'revolver_cargado_%d_%d.json' % (ox, mascara)), o)
    # los overrides del revólver: más abajo = más prioridad (máscara, luego óxido, luego el tambor abierto)
    principal = cargar(os.path.join(M, 'revolver.json'))
    abiertos = [o for o in principal.get('overrides', []) if 'copperslug:abierto' in o['predicate']]
    nuevos = []
    for ox, nombre, umbral in NIVELES:
        if umbral is not None:
            nuevos.append({'predicate': {'copperslug:oxido': umbral}, 'model': 'copperslug:item/' + nombre})
        # de menor a mayor máscara: gana la última que cumple (>=), o sea la máscara exacta
        for mascara in range(1, 64):
            p = {'copperslug:recamaras': mascara}
            if umbral is not None:
                p = {'copperslug:oxido': umbral, 'copperslug:recamaras': mascara}
            nuevos.append({'predicate': p, 'model': 'copperslug:item/revolver_cargado_%d_%d' % (ox, mascara)})
    principal['overrides'] = nuevos + abiertos
    guardar(os.path.join(M, 'revolver.json'), principal)
    print('modelos: revolver_3d + 63 + abierto, revolver_cargado_*: 252, overrides:', len(principal['overrides']))


if __name__ == '__main__':
    main()

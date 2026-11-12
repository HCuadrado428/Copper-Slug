#!/usr/bin/env python3
"""Sintetiza los sonidos de las armas (disparos, mecanismos, impactos y lo nuevo) con numpy y los codifica en Ogg Vorbis.

Cada arma tiene su carácter: el revólver seco y con cuerpo, el rifle un latigazo con eco largo, la escopeta de presión un soplido
con golpe, la Gatling un «tuc» metálico, la Winchester un estampido de calibre grande, la Derringer un chasquido pequeño, la
Thompson un traqueteo, el mosquete un estruendo de pólvora negra con chispazo previo y el cañón un trueno que sacude. Cada disparo
tiene además su versión «_lejos» (apagada y con eco, para los que están lejos) y hay un eco de interior y el silenciador de verdad.

Los sonidos se generan con semilla fija (salen siempre igual). Hace falta ffmpeg con libvorbis. Uso: generar_sonidos.py [raíz]
    generar_sonidos.py [raíz] --informe   # solo escribe las métricas y los espectrogramas en el directorio temporal
"""
import json
import os
import subprocess
import sys

import numpy as np

args = [a for a in sys.argv[1:] if not a.startswith('--')]
RAIZ = args[0] if args else '.'
SALIDA = os.path.join(RAIZ, 'common/src/main/resources/assets/copperslug/sounds')
SR = 44100
rng = np.random.default_rng(20261114)


# ------------------------------------------------------------------ utilidades de señal
def n_(d):
    return int(d * SR)


def tt(d):
    return np.arange(n_(d)) / SR


def ruido(d):
    return rng.standard_normal(n_(d))


def filtro(x, lo=None, hi=None, orden=2):
    """Paso alto en `lo` y/o paso bajo en `hi` (en el dominio de la frecuencia). Se rellena con ceros por los dos lados para que la
    respuesta del filtro no dé la vuelta y aparezca al otro extremo de la señal (un eco falso)."""
    pad = 8192
    xp = np.pad(x, (pad, pad))
    X = np.fft.rfft(xp)
    f = np.fft.rfftfreq(len(xp), 1 / SR)
    H = np.ones_like(f)
    if lo:
        H *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** (2 * orden))
    if hi:
        H *= 1 / (1 + (f / hi) ** (2 * orden))
    return np.fft.irfft(X * H, len(xp))[pad:pad + len(x)]


def env(d, decay, ataque=0.0005):
    t = tt(d)
    e = np.exp(-t / decay)
    if ataque > 0:
        e = e * np.minimum(1, t / ataque)
    return e


def seno(f, d):
    """Seno con frecuencia constante o una función/array de frecuencia."""
    t = tt(d)
    f = np.broadcast_to(f, t.shape) if np.isscalar(f) else f
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def barrido(f0, f1, d, tau):
    t = tt(d)
    return seno(f1 + (f0 - f1) * np.exp(-t / tau), d)


def ponder(partes, d):
    """Suma señales de distinta longitud en un lienzo de d segundos, cada una con su retraso (s) y ganancia."""
    out = np.zeros(n_(d))
    for (x, retraso, g) in partes:
        i = n_(retraso)
        m = min(len(x), len(out) - i)
        if m > 0:
            out[i:i + m] += g * x[:m]
    return out


def reverb(x, rt, lp=3000, mezcla=0.3, pre=0.0):
    """Cola de reverberación: ruido que se apaga en `rt` segundos, filtrado, convolucionado con la señal."""
    ir = ruido(rt * 1.2 + 0.05) * np.exp(-tt(rt * 1.2 + 0.05) / (rt / 6.9))
    ir = filtro(ir, hi=lp, orden=2)
    ir[:n_(pre)] = 0
    ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
    n = len(x) + len(ir)
    y = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)
    out = np.zeros(n)
    out[:len(x)] += x * (1 - mezcla)
    out += y * mezcla * 2.5
    return out


def fundido(x, frac=0.3):
    """Apaga el final de la señal seca con un coseno para que no se corte de golpe (si no, se oye un clic)."""
    k = max(1, int(len(x) * frac))
    x = x.copy()
    x[-k:] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, k)))
    return x


def saturar(x, g):
    return np.tanh(g * x) / np.tanh(g)


def normalizar(x, pico=0.9):
    x = x - np.mean(x)
    m = np.max(np.abs(x)) + 1e-9
    return x / m * pico


def recortar(x, d, fundido=0.02):
    x = x[:n_(d)].copy()
    if len(x) < n_(d):
        x = np.pad(x, (0, n_(d) - len(x)))
    k = n_(fundido)
    x[-k:] *= np.linspace(1, 0, k)
    return x


# ------------------------------------------------------------------ piezas
def modal(base, d, modos=(1, 2.4, 4.1, 6.9), caidas=(0.05, 0.035, 0.02, 0.012), amps=(1, 0.6, 0.4, 0.25)):
    """Un golpe de metal: varios modos que se apagan a distinta velocidad."""
    t = tt(d)
    return sum(a * np.exp(-t / c) * np.sin(2 * np.pi * base * m * t) for m, c, a in zip(modos, caidas, amps))


def tink(base=2400, d=0.18, brillo=1.0, ataque=0.0003):
    t = tt(d)
    golpe = filtro(ruido(d), lo=3000) * np.exp(-t / 0.0012)
    return modal(base, d) * np.minimum(1, t / ataque) + 0.7 * brillo * golpe


def clac(base=900, d=0.12):
    """Un golpe de metal grave y mate (cerrar una palanca, un cierre)."""
    t = tt(d)
    return modal(base, d, caidas=(0.03, 0.02, 0.012, 0.008)) + 0.8 * filtro(ruido(d), hi=1500) * np.exp(-t / 0.004)


def siseo(d, lo, hi, decay=None):
    x = filtro(ruido(d), lo=lo, hi=hi)
    return x * (env(d, decay, 0.01) if decay else 1)


def raspa(d, lo=1500, hi=7000, vel=40):
    """Roce de metal contra metal: ruido que se enciende y apaga al azar despacio."""
    mod = np.abs(filtro(ruido(d), hi=vel, orden=2))
    mod = mod / (np.max(mod) + 1e-9)
    return filtro(ruido(d), lo=lo, hi=hi) * (0.3 + 0.7 * mod)


# ------------------------------------------------------------------ el disparo
def disparo(d, crack_hp=4000, crack_d=0.005, crack_a=1.0, boom=(120, 60), boom_d=0.18, boom_a=1.0, cuerpo_lp=1800, cuerpo_d=0.08,
            cuerpo_a=0.7, ring=(2500, 0.04, 0.15), cola=(0.6, 1800, 0.25), drive=2.0, extra=None, retraso_crack=0.0):
    crack_a, boom_a, cuerpo_a = crack_a * 2.6, boom_a * 0.42, cuerpo_a * 1.7     # el chasquido y el cuerpo mandan; el bajo acompaña
    crack = filtro(ruido(d), lo=crack_hp) * env(d, crack_d, 0.0002)
    boomx = barrido(boom[0], boom[1], d, 0.03) * env(d, boom_d, 0.001)
    cuerpo = filtro(ruido(d), hi=cuerpo_lp) * env(d, cuerpo_d, 0.0008)
    partes = [(crack, retraso_crack, crack_a), (boomx, 0, boom_a), (cuerpo, 0, cuerpo_a)]
    if ring:
        partes.append((np.sin(2 * np.pi * ring[0] * tt(d)) * env(d, ring[1], 0.0005), 0.001, ring[2]))
    if extra:
        partes += extra
    x = ponder(partes, d)
    x = fundido(saturar(x / (np.max(np.abs(x)) + 1e-9), drive))
    if cola:
        x = reverb(x, cola[0], cola[1], cola[2])
    return x


def revolver_disparo():
    return disparo(0.45, 4200, 0.0045, 1.0, (135, 62), 0.16, 1.0, 1900, 0.075, 0.7, (2300, 0.04, 0.15), (0.7, 1800, 0.28), 2.2)


def rifle_disparo():
    # el latigazo del catalejo: un chasquido afilado, un golpe sordo y un eco largo de valle
    return disparo(0.55, 5200, 0.0035, 1.15, (95, 52), 0.20, 0.7, 1300, 0.09, 0.5, (3100, 0.06, 0.18), (1.6, 1600, 0.5), 2.0)


def presion_disparo():
    t = tt(0.6)
    sopl = filtro(ruido(0.6), lo=900, hi=6500) * env(0.6, 0.11, 0.004)
    sopl += 0.6 * filtro(ruido(0.6), lo=300, hi=2500) * env(0.6, 0.2, 0.01)
    golpe = barrido(80, 42, 0.6, 0.04) * env(0.6, 0.1, 0.001)
    x = ponder([(sopl, 0, 0.9), (golpe, 0, 1.1)], 0.6)
    return reverb(fundido(saturar(x / np.max(np.abs(x)), 1.6)), 0.5, 2200, 0.2)


def gatling_disparo():
    # un tiro suelto de la Gatling: un «tuc» corto y metálico (dispara a mucha cadencia: tiene que ser breve)
    return disparo(0.2, 3200, 0.003, 0.7, (170, 95), 0.05, 0.95, 2200, 0.04, 0.5, (1500, 0.05, 0.3), (0.2, 2500, 0.1), 2.4)


def winchester_disparo():
    return disparo(0.8, 4600, 0.0055, 1.0, (112, 56), 0.25, 1.0, 1500, 0.12, 0.8, (2650, 0.05, 0.18), (1.0, 1700, 0.38), 2.1)


def derringer_disparo():
    # pequeño y seco: un pum agudo sin cuerpo
    return disparo(0.35, 6200, 0.0028, 1.1, (230, 130), 0.07, 0.6, 3200, 0.04, 0.5, (4100, 0.03, 0.25), (0.35, 3500, 0.14), 2.0)


def thompson_disparo():
    return disparo(0.22, 3600, 0.004, 0.8, (155, 82), 0.06, 0.9, 2100, 0.05, 0.7, (1850, 0.04, 0.25), (0.25, 2200, 0.12), 2.3)


def mosquete_disparo():
    # chispazo en la cazoleta, un instante de nada y el estruendo de la pólvora negra con humo
    d = 1.9
    flash = filtro(ruido(0.09), lo=2500) * env(0.09, 0.025, 0.004)
    chispa = ponder([(flash, 0, 0.5)], d)
    rugido = filtro(ruido(d), hi=900) * env(d, 0.32, 0.004) * 1.9
    boom = barrido(80, 38, d, 0.05) * env(d, 0.5, 0.002) * 0.55
    crack = filtro(ruido(d), lo=2200, hi=9000) * env(d, 0.009, 0.0005) * 2.0
    humo = filtro(ruido(d), lo=2000, hi=6500) * env(d, 0.45, 0.05) * 0.5
    x = ponder([(chispa, 0, 1.0), (rugido, 0.09, 1.0), (boom, 0.09, 1.0), (crack, 0.09, 1.0), (humo, 0.13, 1.0)], d)
    return reverb(fundido(saturar(x / np.max(np.abs(x)), 2.0)), 1.6, 1500, 0.4)


def canon_disparo():
    d = 2.2
    boom = barrido(62, 27, d, 0.07) * env(d, 1.0, 0.002) * 0.9
    cuerpo = filtro(ruido(d), hi=800) * env(d, 0.6, 0.003) * 1.9
    crack = filtro(ruido(d), lo=1500, hi=6000) * env(d, 0.012, 0.0005) * 2.2
    escombros = filtro(ruido(d), lo=60, hi=400) * env(d, 0.9, 0.05) * 0.9
    pings = sum(np.sin(2 * np.pi * f * tt(0.5)) * env(0.5, 0.08, 0.001) * 0.1 for f in (1400, 2100, 3300))
    x = ponder([(boom, 0, 1.0), (cuerpo, 0, 1.0), (crack, 0, 1.0), (escombros, 0.05, 1.0), (pings, 0.35, 1.0), (pings, 0.62, 0.6)], d)
    return reverb(fundido(saturar(x / np.max(np.abs(x)), 2.2)), 2.0, 1200, 0.45)


def fogueo():
    # cartucho de fogueo: un chasquido de papel muy fuerte y poco más
    return disparo(0.9, 2200, 0.014, 1.2, (105, 62), 0.12, 0.7, 2400, 0.06, 0.6, None, (1.2, 2000, 0.35), 2.0)


def silenciador():
    t = tt(0.3)
    pff = filtro(ruido(0.3), lo=900, hi=5500) * env(0.3, 0.045, 0.004)
    golpe = barrido(110, 80, 0.3, 0.02) * env(0.3, 0.035, 0.001)
    mec = tink(2900, 0.16) * 0.25
    x = ponder([(pff, 0, 0.8), (golpe, 0, 0.5), (mec, 0.012, 1.0)], 0.3)
    return reverb(fundido(x), 0.15, 2500, 0.1)


# ------------------------------------------------------------------ mecanismos
def amartillar():
    # clic-clic-CLAC: el martillo al montarse
    d = 0.26
    return ponder([(tink(2100, 0.07, 0.7), 0.0, 0.6), (tink(2600, 0.07, 0.8), 0.07, 0.75), (clac(1400, 0.1), 0.15, 1.0)], d)


def revolver_cargar():
    d = 0.22
    return ponder([(raspa(0.08, 2500, 7000, 80), 0, 0.4), (tink(3300, 0.12), 0.05, 0.9), (clac(1900, 0.07), 0.09, 0.4)], d)


def revolver_vacio():
    d = 0.1
    return ponder([(tink(1900, 0.09, 1.1), 0, 1.0), (clac(700, 0.06), 0.002, 0.5)], d)


def ruleta():
    # el tambor girando: una trinquete que va frenando
    d = 1.4
    out = np.zeros(n_(d))
    tiempo, paso = 0.0, 0.025
    while tiempo < d - 0.1:
        k = tink(2000 + 400 * rng.random(), 0.05, 0.6)
        i = n_(tiempo)
        m = min(len(k), len(out) - i)
        out[i:i + m] += k[:m] * (1.0 - 0.5 * tiempo / d)
        tiempo += paso
        paso *= 1.045
    return out + 0.1 * raspa(d, 1500, 5000, 30) * env(d, 0.9, 0.01)


def winchester_cargar():
    d = 0.3
    return ponder([(tink(3000, 0.15), 0, 0.8), (clac(1500, 0.08), 0.05, 0.7), (raspa(0.07, 3000, 8000, 90), 0.0, 0.3)], d)


def winchester_palanca():
    # la palanca baja (roce), sube y cierra con un golpe
    d = 0.5
    baja = raspa(0.16, 800, 4500, 25) * env(0.16, 0.12, 0.01) * 0.8
    abre = clac(850, 0.12) * 0.8
    cierra = clac(1100, 0.13)
    cierra2 = tink(2300, 0.1) * 0.4
    return ponder([(baja, 0, 0.8), (abre, 0.16, 0.9), (cierra, 0.34, 1.0), (cierra2, 0.34, 0.8)], d)


def derringer_abrir():
    d = 0.32
    bisagra = raspa(0.12, 2200, 6000, 90) * env(0.12, 0.08, 0.005) * 0.4
    return ponder([(clac(1700, 0.1), 0, 1.0), (bisagra, 0.04, 0.8), (tink(3600, 0.12), 0.12, 0.6)], d)


def thompson_tambor():
    d = 0.6
    out = np.zeros(n_(d))
    for k, tiempo in enumerate(np.arange(0.0, 0.45, 0.07)):
        c = tink(1700 + 150 * (k % 3), 0.07, 0.8)
        i = n_(tiempo)
        out[i:i + len(c)] += c[:len(out) - i] * 0.8
    out = ponder([(out, 0, 1.0), (clac(950, 0.12), 0.46, 1.0)], d)
    return out


def baqueta():
    # la baqueta del mosquete: roce largo y golpe seco al fondo del cañón
    d = 0.7
    roce = raspa(0.4, 500, 3500, 20) * env(0.4, 0.3, 0.02) * 0.9
    golpe = clac(420, 0.18)
    return ponder([(roce, 0, 0.8), (golpe, 0.42, 1.0)], d)


def cazoleta():
    d = 0.5
    sisea = siseo(0.45, 3000, 9000, 0.12) * 0.7
    chispas = np.zeros(n_(d))
    for _ in range(16):
        i = int(rng.random() * 0.35 * SR)
        k = filtro(ruido(0.01), lo=4000) * np.exp(-tt(0.01) / 0.002)
        chispas[i:i + len(k)] += k * (0.3 + 0.7 * rng.random())
    return ponder([(sisea, 0, 1.0), (chispas, 0, 0.8)], d)


def mecha():
    # mecha chisporroteando
    d = 0.9
    base = siseo(d, 2500, 9000) * 0.25 * np.minimum(1, tt(d) / 0.1)
    pops = np.zeros(n_(d))
    for _ in range(40):
        i = int(rng.random() * (d - 0.03) * SR)
        k = filtro(ruido(0.012), lo=2500) * np.exp(-tt(0.012) / 0.003)
        pops[i:i + len(k)] += k * (0.3 + rng.random())
    return base + 0.5 * pops


def gatling_cinta():
    d = 0.7
    out = np.zeros(n_(d))
    for tiempo in np.arange(0, 0.6, 0.055):
        c = tink(1700 + 700 * rng.random(), 0.06, 0.6) * (0.5 + 0.5 * rng.random())
        i = n_(tiempo)
        out[i:i + len(c)] += c[:len(out) - i]
    return out + 0.15 * raspa(d, 1500, 6000, 60)


def gatling_manivela():
    d = 0.18
    return ponder([(tink(2100, 0.06, 0.6), 0, 0.7), (clac(1200, 0.07), 0.05, 0.9)], d)


def gatling_vapor():
    d = 1.5
    s = siseo(d, 2000, 10000) * env(d, 0.7, 0.05)
    return s + 0.2 * siseo(d, 500, 2500) * env(d, 0.5, 0.02)


def atasco():
    d = 0.35
    return ponder([(raspa(0.12, 400, 3000, 50) * 0.9, 0, 0.9), (clac(600, 0.15), 0.1, 1.0), (tink(1500, 0.12), 0.14, 0.4)], d)


# ------------------------------------------------------------------ impactos
def rebote():
    # el zumbido de una bala que rebota
    d = 0.6
    t = tt(d)
    f = 3400 * np.exp(-t / 0.18) + 700
    sil = seno(f, d) * env(d, 0.16, 0.002)
    return ponder([(sil, 0, 0.7), (filtro(ruido(0.02), lo=3000) * np.exp(-tt(0.02) / 0.004), 0, 1.0), (tink(2700, 0.1), 0, 0.4)], d)


def casquillo():
    d = 0.35
    return ponder([(tink(4200, 0.1), 0.0, 0.9), (tink(4600, 0.09), 0.11, 0.55), (tink(4900, 0.08), 0.19, 0.3), (tink(5200, 0.07), 0.24, 0.15)], d)


def goma():
    d = 0.4
    t = tt(d)
    f = 320 - 160 * (1 - np.exp(-t / 0.05))
    return ponder([(seno(f, d) * env(d, 0.08, 0.002), 0, 0.9), (filtro(ruido(d), hi=900) * env(d, 0.03, 0.001), 0, 0.5)], d)


# ------------------------------------------------------------------ nuevos
def mob_montar():
    # lo que se oye antes del disparo de un mob: el gatillo y el martillo
    d = 0.14
    return ponder([(tink(2300, 0.08, 0.8), 0, 0.7), (clac(1500, 0.08), 0.045, 1.0)], d)


def mob_chispa():
    d = 0.4
    return ponder([(siseo(0.35, 3500, 10000, 0.1) * 0.5, 0, 1.0), (cazoleta()[:n_(0.4)] * 0.4, 0, 1.0)], d)


def mob_clic_seco():
    return revolver_vacio() * 0.9


def eco_interior():
    # la respuesta de una sala cerrada o una cueva: una cola densa y oscura con un par de rebotes
    d = 2.2
    base = np.zeros(n_(d))
    base[:50] = np.hanning(50)
    ir = reverb(base, 1.8, 1400, 0.95, 0.04)
    ir = recortar(ir, d, 0.4)
    ir[:n_(0.03)] *= np.linspace(0, 1, n_(0.03))
    for ret, g in ((0.085, 0.5), (0.16, 0.35), (0.27, 0.22)):
        i = n_(ret)
        ir[i:i + 800] += g * np.hanning(800) * rng.standard_normal(800)
    return filtro(ir, lo=80, hi=1800)


def lejos(f, tau=2.2):
    """La versión lejana de un disparo: sin agudos, un poco retrasada y con mucha cola de eco."""
    x = filtro(f, hi=950, orden=3)
    x = fundido(np.pad(x, (n_(0.05), 0)), 0.2)
    x = reverb(x, tau, 900, 0.55, 0.0)
    return recortar(x, len(f) / SR + 1.5, 0.5)


# ------------------------------------------------------------------ catálogo
DISPAROS = {
    'revolver_disparo': revolver_disparo, 'rifle_catalejo_disparo': rifle_disparo, 'presion_disparo': presion_disparo,
    'gatling_disparo': gatling_disparo, 'winchester_disparo': winchester_disparo, 'derringer_disparo': derringer_disparo,
    'thompson_disparo': thompson_disparo, 'mosquete_disparo': mosquete_disparo, 'canon_disparo': canon_disparo,
}
OTROS = {
    'revolver_fogueo': (fogueo, 0.95), 'silenciador_disparo': (silenciador, 0.7),
    'revolver_amartillar': (amartillar, 0.8), 'revolver_cargar': (revolver_cargar, 0.8), 'revolver_vacio': (revolver_vacio, 0.7),
    'revolver_ruleta': (ruleta, 0.8), 'winchester_cargar': (winchester_cargar, 0.8), 'winchester_palanca': (winchester_palanca, 0.85),
    'derringer_abrir': (derringer_abrir, 0.8), 'thompson_tambor': (thompson_tambor, 0.8), 'mosquete_baqueta': (baqueta, 0.85),
    'mosquete_cazoleta': (cazoleta, 0.7), 'canon_mecha': (mecha, 0.7), 'gatling_cinta': (gatling_cinta, 0.8),
    'gatling_manivela': (gatling_manivela, 0.75), 'gatling_vapor': (gatling_vapor, 0.7), 'armafuego_atasco': (atasco, 0.85),
    'revolver_rebote': (rebote, 0.75), 'casquillo_suelo': (casquillo, 0.6), 'goma_rebote': (goma, 0.75),
    'mob_montar': (mob_montar, 0.7), 'mob_chispa': (mob_chispa, 0.7), 'mob_clic_seco': (mob_clic_seco, 0.7), 'eco_interior': (eco_interior, 0.8),
}


def construir():
    s = {}
    for nombre, f in DISPAROS.items():
        x = f()
        s[nombre] = normalizar(x, 0.95)
        s[nombre + '_lejos'] = normalizar(lejos(x), 0.85)
    for nombre, (f, pico) in OTROS.items():
        s[nombre] = normalizar(f(), pico)
    return s


def escribir_ogg(ruta, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype('<i2').tobytes()
    p = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'libvorbis', '-q:a', '4', ruta],
                       input=pcm, capture_output=True)
    if p.returncode:
        raise SystemExit(p.stderr.decode())


def informe(sonidos, carpeta):
    """Métricas por sonido y una hoja de espectrogramas (para revisarlos sin oírlos)."""
    from PIL import Image, ImageDraw
    os.makedirs(carpeta, exist_ok=True)
    filas = []
    for nombre, x in sonidos.items():
        d = len(x) / SR
        rms = float(np.sqrt(np.mean(x ** 2)))
        X = np.abs(np.fft.rfft(x))
        f = np.fft.rfftfreq(len(x), 1 / SR)
        cen = float(np.sum(f * X) / (np.sum(X) + 1e-9))
        t90 = float(np.argmax(np.cumsum(x ** 2) > 0.9 * np.sum(x ** 2)) / SR)
        filas.append((nombre, d, float(np.max(np.abs(x))), rms, cen, t90, bool(np.any(~np.isfinite(x)))))
    with open(os.path.join(carpeta, 'metricas.txt'), 'w') as fh:
        fh.write('nombre dur pico rms centroide_Hz t90\n')
        for r in filas:
            fh.write('%-26s %5.2f %5.2f %6.3f %6.0f %5.2f %s\n' % (r[0], r[1], r[2], r[3], r[4], r[5], 'NAN' if r[6] else ''))
    nombres = list(sonidos)
    W, H, cols = 300, 110, 4
    hoja = Image.new('RGB', (W * cols, (H + 18) * ((len(nombres) + cols - 1) // cols)), (14, 14, 20))
    d = ImageDraw.Draw(hoja)
    for k, nombre in enumerate(nombres):
        x = sonidos[nombre]
        nfft, hop = 512, 256
        ventana = np.hanning(nfft)
        marcos = [np.abs(np.fft.rfft(x[i:i + nfft] * ventana)) for i in range(0, max(1, len(x) - nfft), hop)]
        S = np.log10(np.array(marcos).T + 1e-4)
        S = np.clip((S + 3) / 3.5, 0, 1)
        img = Image.fromarray((S[::-1] * 255).astype('uint8')).resize((W, H))
        ox, oy = (k % cols) * W, (k // cols) * (H + 18)
        hoja.paste(Image.merge('RGB', (img, img.point(lambda v: v * 3 // 4), img.point(lambda v: v // 2))), (ox, oy + 16))
        d.text((ox + 3, oy + 2), '%s %.2fs' % (nombre, len(x) / SR), fill=(255, 210, 140))
    hoja.save(os.path.join(carpeta, 'espectrogramas.png'))


if __name__ == '__main__':
    sonidos = construir()
    if '--informe' in sys.argv:
        informe(sonidos, os.environ.get('INFORME', '/tmp'))
        print('informe escrito')
    else:
        os.makedirs(SALIDA, exist_ok=True)
        for nombre, x in sonidos.items():
            escribir_ogg(os.path.join(SALIDA, nombre + '.ogg'), x)
        print(len(sonidos), 'sonidos escritos en', SALIDA)

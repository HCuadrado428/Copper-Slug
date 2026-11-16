"""Iconos 16x16 de la ropa: contorno oscuro, luz arriba a la izquierda, cuatro tonos por material."""
def c(r, g, b): return (r, g, b, 255)
# materiales: 1 oscuro, 2 medio, 3 claro, 4 brillo
FIELTRO_M = (c(66, 44, 26), c(112, 78, 46), c(146, 104, 62), c(180, 136, 88))
FIELTRO_N = (c(22, 20, 24), c(40, 38, 44), c(62, 58, 68), c(92, 88, 102))
CUERO = (c(92, 58, 32), c(140, 94, 54), c(176, 124, 74), c(210, 162, 106))
LANA = (c(110, 92, 68), c(150, 128, 96), c(184, 162, 124), c(214, 196, 158))
VAQUERA = (c(34, 36, 50), c(54, 58, 78), c(78, 84, 110), c(108, 116, 146))
ROJO = (c(96, 20, 24), c(150, 34, 34), c(192, 56, 48), c(226, 98, 84))
ORO = (c(150, 108, 28), c(212, 166, 44), c(246, 208, 86), c(255, 240, 160))
ACERO = (c(90, 94, 104), c(146, 150, 162), c(198, 202, 214), c(240, 242, 250))
CAMISA = (c(54, 74, 120), c(82, 108, 160))

def pal(mat, contorno, **extra):
    p = {'o': contorno, '1': mat[0], '2': mat[1], '3': mat[2], '4': mat[3]}
    p.update(extra)
    return p

SOMBRERO = [
    '................',
    '................',
    '.....ooo.ooo....',
    '....o3441322o...',
    '....o3332222o...',
    '....o3322221o...',
    '....obgGbbbbo...',
    '.oo.o3222221o.oo',
    'o34oo2222221oo2o',
    'o33322222222211o',
    '.o332222222221o.',
    '..oo11111111oo..',
    '....oooooooo....',
    '................',
    '................',
    '................']

GORRO = ['................',
         '..............r.',
         '....ooooooooorR.',
         '....o3433322oR..',
         '....o3322221oR..',
         '....o3222211or..',
         '....obbgbbbbo...',
         '..ooo2222211ooo.',
         '.o3332222221111o',
         'o33222222222111o',
         '.oo1111111111oo.',
         '...oooooooooo...',
         '................',
         '................',
         '................',
         '................']

CHALECO = ['................',
           '..oooo....oooo..',
           '.o3342o..o2211o.',
           '.o32221cp22211o.',
           '.o32221cp22y21o.',
           '.o322g1cp2yYy1o.',
           '.o32221cp22y21o.',
           '.o32221oo22221o.',
           '.o322g1oo22221o.',
           '.o32221oo21111o.',
           '.o32221oo22221o.',
           '.o1111o..o1111o.',
           '..oooo....oooo..',
           '................',
           '................',
           '................']

PIERNAS = ['................',
           '................',
           '..oooooooooooo..',
           '..obbbbgGbbbbo..',
           '..o3322222211o..',
           '..o332o..o211o..',
           '.fo322o..o211of.',
           '.Fo322o..o211oF.',
           '.fo322o..o211of.',
           '.Fo322o..o211oF.',
           '.fo322o..o211of.',
           '..o222o..o111o..',
           '..ooooo..ooooo..',
           '................',
           '................',
           '................']

# como las de vanilla: dos botas en espejo, con la punta hacia fuera (y la espuela en el talón, hacia dentro)
BOTAS = [
    '................',
    '................',
    '................',
    '................',
    '..oooo....oooo..',
    '..oCCo....oCCo..',
    '..o32o....o32o..',
    '..o32o....o32o..',
    '..o32o....o32o..',
    '.o332o....o322o.',
    'o3322oS..So2221o',
    'o1111os..so1111o',
    'oooooo....oooooo',
    '................',
    '................',
    '................']

PONCHO = ['................',
          '................',
          '....oooooooo....',
          '...o33o..o21o...',
          '..o3332oo2221o..',
          '.o333222222211o.',
          '.oRRRRRRRRRRRRo.',
          'o33222222222211o',
          'orRrRrRrRrRrRrro',
          'o32222222222111o',
          'oRRRRRRRRRRRRRRo',
          'o11111111111111o',
          '.f.f.f.f.f.f.f..',
          '................',
          '................',
          '................']

def bandido_pluma(filas):
    f = [list(r) for r in filas]
    for x, y, ch in ((13, 1, 'r'), (12, 2, 'R'), (13, 2, 'r'), (12, 3, 'R'), (12, 4, 'r')):
        f[y][x] = ch
    return [''.join(r) for r in f]

OSC = c(40, 24, 14)
NEG = c(10, 8, 12)
ICONOS = {
    'sombrero_vaquero': (SOMBRERO, pal(FIELTRO_M, OSC, b=CUERO[0], g=ORO[2], G=ORO[1])),
    'chaleco_vaquero': (CHALECO, pal(CUERO, OSC, c=CAMISA[1], p=CAMISA[0], g=ORO[2], y=ORO[1], Y=ORO[3])),
    'chaparreras_vaquero': (PIERNAS, pal(CUERO, OSC, b=FIELTRO_M[0], g=ORO[2], G=ORO[1], f=CUERO[2], F=CUERO[1])),
    'botas_vaquero': (BOTAS, pal(CUERO, OSC, C=CUERO[3], s=ACERO[1], S=ACERO[3])),
    'sombrero_bandido': (GORRO, pal(FIELTRO_N, NEG, b=ROJO[1], g=ROJO[3], R=ROJO[2], r=ROJO[0])),
    'poncho_bandido': (PONCHO, pal(LANA, c(64, 50, 36), R=ROJO[1], r=ROJO[0], f=LANA[1])),
    'pantalon_bandido': ([r.replace('f', '.').replace('F', '.') for r in PIERNAS], pal(VAQUERA, NEG, b=NEG, g=ACERO[2], G=ACERO[1], f=VAQUERA[2])),
    'botas_bandido': ([r.replace('s', '.').replace('S', '.') for r in BOTAS], pal(FIELTRO_N, NEG, C=ROJO[2], s=FIELTRO_N[0])),
}
for n, (f, _) in ICONOS.items():
    assert len(f) == 16 and all(len(r) == 16 for r in f), (n, [len(r) for r in f])

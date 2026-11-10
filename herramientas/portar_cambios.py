#!/usr/bin/env python3
"""
Porta a Copper Slug lo que ha cambiado en las armas de Miscelánea entre dos commits.

Uso (desde la raíz de Copper Slug):
    herramientas/portar_cambios.py <repo de Miscelánea> <commit viejo> <commit nuevo> [--rama-mc 1.21.1]

1. Saca los dos commits de Miscelánea (git archive) y pasa los dos por herramientas/portar.py.
2. Para cada fichero portado que haya cambiado entre los dos, hace una fusión a tres bandas con git merge-file:
   base = la versión portada del commit viejo, la nuestra = la del repo (con nuestros retoques a mano), la otra = la
   portada del commit nuevo. Así entran los cambios de Miscelánea sin perder lo adaptado aquí.
3. Los ficheros nuevos se copian; los borrados en Miscelánea se listan (no se borran solos); los binarios (texturas,
   sonidos) se copian si aquí no se habían tocado.
4. Al final dice qué ha quedado con conflictos (marcas <<<<<<< ======= >>>>>>>) y apunta el commit nuevo en
   herramientas/ultimo_portado.txt.

Con --rama-mc 1.21.1 (en la rama 1.21.1), antes de fusionar aplica a las dos versiones los cambios de nombres de la API
de 1.21.1 de herramientas/a_1_21_1.py, si existe, para que la fusión compare lo mismo.
"""
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import portar  # noqa: E402


def sacar(repo, commit, dst):
    os.makedirs(dst)
    p = subprocess.Popen(['git', '-C', repo, 'archive', commit, 'src'], stdout=subprocess.PIPE)
    subprocess.check_call(['tar', 'x', '-C', dst], stdin=p.stdout)
    p.wait()


def ficheros(d):
    out = {}
    for raiz, _, fs in os.walk(d):
        for f in fs:
            p = os.path.join(raiz, f)
            out[os.path.relpath(p, d)] = p
    return out


def igual(a, b):
    return os.path.exists(a) and os.path.exists(b) and open(a, 'rb').read() == open(b, 'rb').read()


def es_texto(p):
    return p.endswith(('.java', '.json', '.mcmeta', '.txt', '.cfg', '.toml', '.md'))


def main():
    args = sys.argv[1:]
    rama = None
    if '--rama-mc' in args:
        i = args.index('--rama-mc')
        rama = args[i + 1]
        del args[i:i + 2]
    repo, viejo, nuevo = args
    tmp = tempfile.mkdtemp(prefix='portar_')
    sacar(repo, viejo, os.path.join(tmp, 'src_viejo'))
    sacar(repo, nuevo, os.path.join(tmp, 'src_nuevo'))
    portar.main(os.path.join(tmp, 'src_viejo'), os.path.join(tmp, 'viejo'))
    portar.main(os.path.join(tmp, 'src_nuevo'), os.path.join(tmp, 'nuevo'))
    if rama == '1.21.1' and os.path.exists(os.path.join(AQUI, 'a_1_21_1.py')):
        import a_1_21_1
        a_1_21_1.convertir(os.path.join(tmp, 'viejo'))
        a_1_21_1.convertir(os.path.join(tmp, 'nuevo'))
    A = ficheros(os.path.join(tmp, 'viejo'))
    B = ficheros(os.path.join(tmp, 'nuevo'))
    cambiados, nuevos, conflictos, borrados, binarios = [], [], [], [], []
    for rel in sorted(set(A) | set(B)):
        a, b = A.get(rel), B.get(rel)
        dst = os.path.join(RAIZ, rel)
        if a and b and igual(a, b):
            continue
        if b and not a:
            if os.path.exists(dst) and not igual(dst, b):
                conflictos.append(rel + ' (nuevo en Miscelánea, pero aquí ya existe distinto)')
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(b, dst)
            nuevos.append(rel)
            continue
        if a and not b:
            borrados.append(rel)
            continue
        if not os.path.exists(dst):
            conflictos.append(rel + ' (aquí no existe: ¿se quitó a propósito?)')
            continue
        if not es_texto(rel):
            if igual(dst, a):
                shutil.copyfile(b, dst)
                cambiados.append(rel)
            else:
                binarios.append(rel)
            continue
        r = subprocess.run(['git', 'merge-file', '-L', 'Copper Slug', '-L', 'Miscelánea viejo', '-L', 'Miscelánea nuevo', dst, a, b])
        (conflictos if r.returncode != 0 else cambiados).append(rel)
    open(os.path.join(AQUI, 'ultimo_portado.txt'), 'w').write(nuevo + '\n')
    print('cambiados:', len(cambiados))
    for x in cambiados:
        print('  ', x)
    print('nuevos:', len(nuevos))
    for x in nuevos:
        print('  ', x)
    if borrados:
        print('borrados en Miscelánea (bórralos a mano si toca):')
        for x in borrados:
            print('  ', x)
    if binarios:
        print('binarios cambiados en los dos lados (elige a mano):')
        for x in binarios:
            print('  ', x)
    if conflictos:
        print('CON CONFLICTOS (busca <<<<<<<):')
        for x in conflictos:
            print('  ', x)
    shutil.rmtree(tmp)
    sys.exit(1 if conflictos else 0)


if __name__ == '__main__':
    main()

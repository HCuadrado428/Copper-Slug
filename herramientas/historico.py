"""Seguro para los generadores históricos.

Estos scripts hicieron la primera versión de modelos y texturas que después se retocaron a mano o con otros scripts. Volver a
ejecutarlos pisaría los archivos actuales con la versión antigua, así que solo escriben si se les pasa --forzar.
"""
import sys


def seguro(nombre):
    if '--forzar' in sys.argv:
        sys.argv.remove('--forzar')
        return
    print('%s es un generador histórico: sus archivos se retocaron después y ejecutarlo los pisaría con la versión antigua.\n'
          'No se ha escrito nada. Si de verdad quieres rehacerlos, pásale --forzar (y revisa el diff antes de subir).' % nombre)
    sys.exit(1)

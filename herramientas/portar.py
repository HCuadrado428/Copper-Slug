#!/usr/bin/env python3
"""
Portar las armas de fuego de Miscelánea a Copper Slug.

Uso:
    portar.py <raíz de Miscelánea> <salida>

Copia de un árbol de Miscelánea (un checkout o un `git archive`) los ficheros de las armas de fuego y los transforma
para Copper Slug: paquetes (com.miscelanea -> com.copperslug, net.minecraftforge -> com.copperslug.shim), el id del
mod (miscelanea -> copperslug) y las rutas de los recursos. Los recursos se eligen solos: los modelos, texturas,
sonidos, logros, recetas y textos que usan las armas.

No escribe en el repo: deja el resultado en <salida>. Para portar cambios se compara la salida de dos commits de
Miscelánea y la diferencia se aplica como parche (ver herramientas/portar.sh y PORTAR.md). Así no se pierden los
retoques hechos a mano en Copper Slug.
"""
import json
import os
import re
import shutil
import sys

J = 'src/main/java/com/miscelanea/'
R = 'src/main/resources/'

# ---------------------------------------------------------------- código que se copia tal cual (con los cambios de nombre)
JAVA_DIRS = ['armasfuego', 'client/armasfuego']
JAVA_SUELTOS = [
    'mixin/RiflePlayerMixin.java',
    'mixin/LivingEntityGolpeAccessor.java',
    'tirolina/Polea.java',
    'tirolina/Cable.java',
    'client/tirolina/PoleaRenderer.java',
    'logros/LogroTrigger.java',
    'logros/LogrosMiscelanea.java',
]

# ---------------------------------------------------------------- registros: de los de Miscelánea, solo lo de las armas
# (cada declaración "public static final ..." que mencione armasfuego o uno de estos nombres)
REGISTROS = {
    'registry/ModItems.java': None,
    'registry/ModSounds.java': None,
    'registry/ModEntities.java': None,
    'registry/ModEnchantments.java': None,
    'registry/ModEffects.java': None,
    'registry/ModRecipes.java': None,
}
# objetos que no llevan "armasfuego" en su declaración (munición simple) pero son de las armas
ITEMS_EXTRA = {'REVOLVER_BALA', 'REVOLVER_BENGALA', 'REVOLVER_DARDO', 'REVOLVER_FOGUEO', 'REVOLVER_IMAN', 'REVOLVER_TIEMPO',
               'CASQUILLO_RIFLE', 'PALOMITAS'}
ENCANT_EXTRA = {'REVOLVER', 'RIFLE', 'ESCOPETA_PRESION', 'GATLING', 'WINCHESTER', 'DERRINGER', 'THOMPSON', 'MOSQUETE', 'CANON'}


JEI_INFO = ['revolver_botin', 'escopeta_botin', 'rifle_botin', 'gatling_botin', 'winchester_botin', 'derringer_botin', 'thompson_botin',
            'mosquete_botin', 'canon_botin', 'gatling_utilidad', 'winchester_deposito', 'derringer_manga', 'estuche_violin',
            'mosquete_bayoneta', 'canon_bloques']

FORGE_SIN_OVERRIDE = ['shouldCauseReequipAnimation', 'shouldCauseBlockBreakReset', 'canContinueUsing', 'onEntitySwing',
                      'shouldRiderSit', 'getAttributeModifiers', 'canApplyAtEnchantingTable', 'isBookEnchantable',
                      'onLeftClickEntity', 'getAddEntityPacket_no']


def transformar_java(t):
    t = t.replace('import com.miscelanea.Miscelanea;', 'import com.copperslug.CopperSlug;')
    t = re.sub(r'\bcom\.miscelanea\.Miscelanea\b', 'com.copperslug.CopperSlug', t)
    t = re.sub(r'\bMiscelanea\.MOD_ID\b', 'CopperSlug.MOD_ID', t)
    t = re.sub(r'\bMiscelanea\.LOGGER\b', 'CopperSlug.LOG', t)
    t = t.replace('com.miscelanea.', 'com.copperslug.')
    t = t.replace('package com.miscelanea', 'package com.copperslug')
    t = t.replace('net.minecraftforge.', 'com.copperslug.shim.')
    t = t.replace('import net.minecraft.client.renderer.item.ItemProperties;', 'import com.copperslug.shim.ItemProperties;')
    t = t.replace('net.minecraft.client.renderer.item.ItemProperties.register', 'com.copperslug.shim.ItemProperties.register')
    t = t.replace('EnchantmentCategory.create(', 'com.copperslug.shim.Categorias.create(')
    # métodos de las extensiones de Forge (IForgeItem, IForgeEntity...): sin @Override, porque en vanilla y en
    # Fabric no sobrescriben nada (en Forge sí, por la firma). Fabric los llama con mixins (ver ExtensionesItem).
    for m in FORGE_SIN_OVERRIDE:
        t = re.sub(r'@Override(\s*\n\s*public [\w.<>, ?]+ ' + m + r'\()', r'\1', t)
    # initializeClient choca con el de Forge (misma firma borrada): se llama de otra forma y lo lee la plataforma
    t = re.sub(r'(?:@Override\s*\n\s*)?public void initializeClient\(', 'public void extensionesCliente(', t)
    t = t.replace('super.getAttributeModifiers(slot, s)', 'super.getDefaultAttributeModifiers(slot)')
    t = re.sub(r'\b(\w+) instanceof FakePlayer\b', r'com.copperslug.plataforma.Plataforma.get().esJugadorFalso(\1)', t)
    t = t.replace('import com.copperslug.shim.common.util.FakePlayer;\n', '')
    # modelos sueltos: getModel(ResourceLocation) es de Forge; renderModel sin ModelData ni RenderType
    t = re.sub(r'Minecraft\.getInstance\(\)\.getModelManager\(\)\.getModel\(', 'com.copperslug.plataforma.ClienteComun.modelo(', t)
    t = re.sub(r',\s*ModelData\.EMPTY,\s*null\)', ')', t)
    t = t.replace('import com.copperslug.shim.client.model.data.ModelData;\n', '')
    # poses de brazo nuevas (ArmPose.create es de Forge)
    t = t.replace('HumanoidModel.ArmPose.create(', 'com.copperslug.plataforma.ClienteComun.poseBrazo(')
    t = t.replace('miscelanea$', 'copperslug$')
    t = re.sub(r'\bmiscelanea\b', 'copperslug', t)
    t = t.replace('MISCELANEA_', 'COPPERSLUG_')
    return t


def transformar_texto(t):
    """JSON y demás recursos: ids y claves de idioma."""
    t = t.replace('miscelanea:', 'copperslug:')
    t = re.sub(r'\bmiscelanea\b', 'copperslug', t)
    return t


def declaraciones(texto):
    """Trozos 'public static final ... ;' (con el comentario de antes) y static {...} de un fichero de registro."""
    out = []
    lineas = texto.split('\n')
    i = 0
    coment = []
    while i < len(lineas):
        l = lineas[i]
        s = l.strip()
        if s.startswith('/**') or s.startswith('//') or s.startswith('*'):
            coment.append(l)
            i += 1
            continue
        if re.match(r'\s*(public|private)\s+static\s+(final\s+)?', l) and '(' not in l.split('=')[0] or re.match(r'\s*(public|private)\s+static\s+final', l):
            bloque = [l]
            prof = l.count('{') - l.count('}')
            while not (bloque[-1].rstrip().endswith(';') and prof <= 0) and not (prof == 0 and bloque[-1].rstrip().endswith('}') and len(bloque) > 1):
                i += 1
                if i >= len(lineas):
                    break
                bloque.append(lineas[i])
                prof += lineas[i].count('{') - lineas[i].count('}')
            out.append((coment, bloque))
            coment = []
        elif re.match(r'\s*(public|private)\s+static\s+[\w<>?, ]+\s+\w+\(.*\)\s*\{\s*$', l):
            bloque = [l]
            prof = l.count('{') - l.count('}')
            while prof > 0:
                i += 1
                bloque.append(lineas[i])
                prof += lineas[i].count('{') - lineas[i].count('}')
            out.append((coment, bloque))
            coment = []
        elif s.startswith('static {'):
            bloque = [l]
            prof = l.count('{') - l.count('}')
            while prof > 0:
                i += 1
                bloque.append(lineas[i])
                prof += lineas[i].count('{') - lineas[i].count('}')
            out.append((coment, bloque))
            coment = []
        else:
            coment = []
        i += 1
    return out


def nombre_decl(bloque):
    m = re.search(r'(\w+)\s*=', bloque[0])
    if m:
        return m.group(1)
    m = re.search(r'\s(\w+)\s*\(', bloque[0])
    return m.group(1) if m else ''


def filtrar_registro(ruta, texto):
    cab = texto.split('public final class', 1)[0]
    nombre_clase = os.path.basename(ruta)[:-5]
    decls = declaraciones(texto)
    keep = []
    for coment, b in decls:
        cuerpo = '\n'.join(b)
        n = nombre_decl(b)
        es_reg = re.search(r'DeferredRegister<', cuerpo) is not None
        arma = ('armasfuego' in cuerpo or es_reg or
                (nombre_clase == 'ModItems' and (n in ITEMS_EXTRA or 'escopetaCartucho' in cuerpo or 'ESCOPETA_CARTUCHOS' in cuerpo)) or
                (nombre_clase == 'ModEnchantments' and n in ENCANT_EXTRA))
        if nombre_clase == 'ModSounds':
            arma = es_reg or n in SONIDOS_USADOS or 'register(String' in cuerpo or 'private static RegistryObject<SoundEvent> register' in cuerpo
        if arma:
            keep.append(coment + b)
    # imports: los de Miscelánea que no sean de otras partes
    imps = [l for l in cab.split('\n') if l.startswith('import ') and not re.match(r'import com\.miscelanea\.(?!Miscelanea;)', l)]
    pkg = [l for l in cab.split('\n') if l.startswith('package ')]
    s = '\n'.join(pkg) + '\n\n' + '\n'.join(imps) + '\n\n'
    s += '/** Generado por herramientas/portar.py a partir del ' + nombre_clase + ' de Miscelánea (solo lo de las armas). */\n'
    s += 'public final class ' + nombre_clase + ' {\n'
    for b in keep:
        s += '\n'.join(b) + '\n'
    s += '\n    private ' + nombre_clase + '() {}\n}\n'
    return s


SONIDOS_USADOS = set()


def suscriptores(ficheros):
    """Suscriptores.java: las clases con @Mod.EventBusSubscriber (las de cliente aparte, solo se cargan en el cliente)."""
    comun, cliente = [], []
    for p in sorted(ficheros):
        t = open(p, encoding='utf-8').read()
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
                        nombre = m2.group(2)
                        anid = len(m2.group(1)) > 0
                        q = pkg + '.' + (externa + '$' + nombre if anid and externa and externa != nombre else nombre)
                        (cliente if 'Dist.CLIENT' in l else comun).append(q)
                        break
    s = 'package com.copperslug;\n\n'
    s += '/** Generado por herramientas/portar.py: las clases con @Mod.EventBusSubscriber del código portado. */\n'
    s += 'public final class Suscriptores {\n    private Suscriptores() {}\n\n'
    s += '    public static final String[] COMUN = {\n' + ''.join('            "' + c + '",\n' for c in comun) + '    };\n\n'
    s += '    public static final String[] CLIENTE = {\n' + ''.join('            "' + c + '",\n' for c in cliente) + '    };\n}\n'
    return s


def main(src, dst):
    os.makedirs(dst, exist_ok=True)
    java_out = os.path.join(dst, 'common/src/main/java/com/copperslug/')
    escritos = []

    def escribir(rel, texto):
        p = os.path.join(java_out, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(texto)
        escritos.append(p)

    todo_java = ''
    for d in JAVA_DIRS:
        base = os.path.join(src, J, d)
        for raiz, _, fs in os.walk(base):
            for f in sorted(fs):
                if not f.endswith('.java'):
                    continue
                p = os.path.join(raiz, f)
                rel = os.path.relpath(p, os.path.join(src, J))
                t = open(p, encoding='utf-8').read()
                todo_java += t
                escribir(rel, transformar_java(t))
    for rel in JAVA_SUELTOS:
        p = os.path.join(src, J, rel)
        if os.path.exists(p):
            t = open(p, encoding='utf-8').read()
            todo_java += t
            escribir(rel, transformar_java(t))

    escribir('Suscriptores.java', suscriptores(list(escritos)))
    for m in re.finditer(r'ModSounds\.([A-Z0-9_]+)', todo_java):
        SONIDOS_USADOS.add(m.group(1))
    for rel in REGISTROS:
        t = open(os.path.join(src, J, rel), encoding='utf-8').read()
        escribir(rel, transformar_java(filtrar_registro(rel, t)))

    # ------------------------------------------------------------ recursos
    a_src = os.path.join(src, R, 'assets/miscelanea/')
    d_src = os.path.join(src, R, 'data/miscelanea/')
    a_dst = os.path.join(dst, 'common/src/main/resources/assets/copperslug/')
    d_dst = os.path.join(dst, 'common/src/main/resources/data/copperslug/')

    portado = ''.join(open(p, encoding='utf-8').read() for p in escritos)
    # ids registrados
    ids_items = set(re.findall(r'ITEMS\.register\("([a-z0-9_]+)"', portado))
    ids_items |= {'escopeta_cartucho_' + x for x in re.findall(r'\b[A-Z_]+\("([a-z_]+)"', open(
        os.path.join(src, J, 'armasfuego/escopeta/TipoCartucho.java'), encoding='utf-8').read())}
    ids_ench = set(re.findall(r'ENCHANTMENTS\.register\("([a-z0-9_]+)"', portado))
    ids_ent = set(re.findall(r'ENTITIES\.register\("([a-z0-9_]+)"', portado))
    ids_efe = set(re.findall(r'EFFECTS\.register\("([a-z0-9_]+)"', portado))
    ids_snd = set()
    snd_txt = open(os.path.join(src, J, 'registry/ModSounds.java'), encoding='utf-8').read()
    for n in SONIDOS_USADOS:
        m = re.search(n + r'\s*=\s*register\("([a-z0-9_.]+)"', snd_txt)
        if m:
            ids_snd.add(m.group(1))

    literales = set(re.findall(r'"([a-z0-9_/.]+)"', todo_java))
    literales |= set(re.findall(r'"([a-z0-9_/.]+)"\s*\+', todo_java))

    copiar = set()

    def ref_a_ruta(ref, carpeta, ext):
        ref = ref.split('#')[0]
        if ':' in ref:
            ns, path = ref.split(':', 1)
            if ns != 'miscelanea':
                return None
        else:
            path = ref
        return os.path.join(carpeta, path + ext)

    def modelo(path):
        """Un modelo (relativo a models/, sin .json) y lo que usa."""
        p = os.path.join('models', path + '.json')
        if p in copiar or not os.path.exists(os.path.join(a_src, p)):
            return
        copiar.add(p)
        try:
            j = json.load(open(os.path.join(a_src, p), encoding='utf-8'))
        except Exception:
            return
        if 'parent' in j:
            r = ref_a_ruta(j['parent'], '', '')
            if r is not None:
                modelo(r.lstrip('/'))
        for v in (j.get('textures') or {}).values():
            r = ref_a_ruta(v, 'textures', '.png')
            if r and os.path.exists(os.path.join(a_src, r)):
                copiar.add(r)
                if os.path.exists(os.path.join(a_src, r + '.mcmeta')):
                    copiar.add(r + '.mcmeta')
        for o in j.get('overrides') or []:
            r = ref_a_ruta(o.get('model', ''), '', '')
            if r:
                modelo(r.lstrip('/'))

    for i in ids_items:
        modelo('item/' + i)
    # modelos y texturas nombrados en el código (por su ruta o por un prefijo que se completa en tiempo de ejecución)
    todos = []
    for raiz, _, fs in os.walk(a_src):
        for f in fs:
            todos.append(os.path.relpath(os.path.join(raiz, f), a_src))
    for lit in literales:
        for t in todos:
            sin = t.rsplit('.', 1)[0]
            candidatos = [sin, sin.split('/', 1)[1] if '/' in sin else sin, t]
            if any(c == lit or (lit.endswith('_') and c.startswith(lit) and len(lit) > 6) for c in candidatos):
                if t.startswith('models/'):
                    modelo(sin[len('models/'):])
                elif t.startswith('textures/'):
                    copiar.add(t)
                    if os.path.exists(os.path.join(a_src, t + '.mcmeta')):
                        copiar.add(t + '.mcmeta')
    for i in ids_ent:
        for t in todos:
            if t.startswith('textures/entity/') and os.path.basename(t).startswith(i):
                copiar.add(t)
    for e in ids_efe:
        if os.path.exists(os.path.join(a_src, 'textures/mob_effect', e + '.png')):
            copiar.add('textures/mob_effect/' + e + '.png')
    # partículas
    for t in todos:
        if t.startswith('particles/') and 'armafuego' in t:
            copiar.add(t)
            j = json.load(open(os.path.join(a_src, t)))
            for tx in j.get('textures', []):
                r = ref_a_ruta(tx, 'textures/particle', '.png')
                if r:
                    copiar.add(r)

    # sonidos
    sj = json.load(open(os.path.join(a_src, 'sounds.json'), encoding='utf-8'))
    sj_out = {}
    for k in sorted(ids_snd):
        if k in sj:
            sj_out[k] = sj[k]
            for s in sj[k].get('sounds', []):
                n = s if isinstance(s, str) else s.get('name')
                r = ref_a_ruta(n, 'sounds', '.ogg')
                if r:
                    copiar.add(r)

    for t in sorted(copiar):
        o = os.path.join(a_src, t)
        if not os.path.exists(o):
            continue
        d = os.path.join(a_dst, t)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if t.endswith('.json') or t.endswith('.mcmeta'):
            open(d, 'w', encoding='utf-8').write(transformar_texto(open(o, encoding='utf-8').read()))
        else:
            shutil.copyfile(o, d)
    os.makedirs(a_dst, exist_ok=True)
    json.dump(json.loads(transformar_texto(json.dumps(sj_out))), open(os.path.join(a_dst, 'sounds.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

    # ------------------------------------------------------------ datos: logros de las armas de fuego, recetas, tipos de daño
    acciones = set(re.findall(r'LogrosMiscelanea\.dar\([^;]*?"([a-z0-9_/]+)"\)', todo_java))
    datos = []
    adv = os.path.join(d_src, 'advancements')
    for raiz, _, fs in os.walk(adv):
        for f in fs:
            p = os.path.join(raiz, f)
            t = open(p, encoding='utf-8').read()
            accs = set(re.findall(r'"accion"\s*:\s*"([a-z0-9_/]+)"', t))
            usa_items = any(('miscelanea:' + i + '"') in t for i in ids_items)
            if not os.path.relpath(p, adv).startswith('armas/'):
                continue
            if (accs and accs <= acciones) or (not accs and usa_items):
                datos.append(os.path.relpath(p, d_src))
    rec = os.path.join(d_src, 'recipes')
    for f in sorted(os.listdir(rec)):
        t = open(os.path.join(rec, f), encoding='utf-8').read()
        res = re.search(r'"result"\s*:\s*\{[^}]*"item"\s*:\s*"miscelanea:([a-z0-9_]+)"', t)
        tipo = re.search(r'"type"\s*:\s*"miscelanea:mosquete_bayoneta"', t)
        if (res and res.group(1) in ids_items) or tipo:
            datos.append('recipes/' + f)
    for d in ['damage_type']:
        pass  # las armas de fuego no usan los tipos de daño de DanoArma (solo su marca "extra")
    for t in datos:
        o = os.path.join(d_src, t)
        dd = os.path.join(d_dst, t)
        os.makedirs(os.path.dirname(dd), exist_ok=True)
        open(dd, 'w', encoding='utf-8').write(transformar_texto(open(o, encoding='utf-8').read()))

    # ------------------------------------------------------------ idiomas: las claves que usa lo portado
    texto_portado = portado + ''.join(open(os.path.join(d_dst, t), encoding='utf-8').read() for t in datos)
    texto_portado_orig = todo_java + ''.join(open(os.path.join(d_src, t), encoding='utf-8').read() for t in datos)
    prefijos = set(re.findall(r'"((?:[a-z_]+\.)+miscelanea\.[a-z0-9_.]*)"', texto_portado_orig))
    prefijos |= set(re.findall(r'"(miscelanea\.[a-z0-9_.]+)"', texto_portado_orig))
    # las páginas de JEI de las armas (el plugin se escribe aparte: compat/jei/CopperSlugJei.java)
    prefijos |= {'jei.miscelanea.info.' + x for x in JEI_INFO}
    for idioma in ['es_es', 'en_us']:
        lj = json.load(open(os.path.join(a_src, 'lang', idioma + '.json'), encoding='utf-8'))
        out = {}
        for k, v in lj.items():
            ok = False
            partes = k.split('.')
            if len(partes) >= 3 and partes[1] == 'miscelanea':
                tipo, ident = partes[0], partes[2]
                if tipo == 'item' and ident in ids_items: ok = True
                if tipo == 'enchantment' and ident in ids_ench: ok = True
                if tipo == 'entity' and ident in ids_ent: ok = True
                if tipo == 'effect' and ident in ids_efe: ok = True
                if tipo == 'subtitles' and '.'.join(partes[2:]) in ids_snd: ok = True
            if not ok:
                for p in prefijos:
                    if k == p or (p.endswith('.') and k.startswith(p)) or k.startswith(p + '.'):
                        ok = True
                        break
            if ok:
                out[transformar_texto(k)] = v
        # lo propio de Copper Slug (pestaña, raíz de los logros...): herramientas/lang_extra
        extra = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lang_extra', idioma + '.json')
        if os.path.exists(extra):
            out.update(json.load(open(extra, encoding='utf-8')))
        os.makedirs(os.path.join(a_dst, 'lang'), exist_ok=True)
        json.dump(out, open(os.path.join(a_dst, 'lang', idioma + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    print('java:', len(escritos), '· recursos:', len(copiar), '· datos:', len(datos), '· sonidos:', len(sj_out))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

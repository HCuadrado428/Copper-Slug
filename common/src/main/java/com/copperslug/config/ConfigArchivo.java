package com.copperslug.config;

import com.copperslug.CopperSlug;
import com.copperslug.shim.common.ForgeConfigSpec;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

/**
 * Guarda y lee una {@link ForgeConfigSpec} en un TOML sencillo: [seccion.sub], clave = valor y # comentarios. Lo que
 * falte o no valga se queda con el valor por defecto, y el archivo se reescribe entero con todo (y sus comentarios).
 */
public final class ConfigArchivo {
    private ConfigArchivo() {}

    public static void cargar(ForgeConfigSpec spec, Path p) {
        Map<String, String> leidos = new HashMap<>();
        if (Files.exists(p)) {
            try {
                String sec = "";
                for (String l : Files.readAllLines(p, StandardCharsets.UTF_8)) {
                    String s = l.trim();
                    if (s.isEmpty() || s.startsWith("#")) continue;
                    if (s.startsWith("[") && s.endsWith("]")) {
                        sec = s.substring(1, s.length() - 1).trim();
                        continue;
                    }
                    int i = s.indexOf('=');
                    if (i <= 0) continue;
                    String v = s.substring(i + 1);
                    int c = v.indexOf('#');
                    if (c >= 0) v = v.substring(0, c);
                    leidos.put((sec.isEmpty() ? "" : sec + ".") + s.substring(0, i).trim(), v.trim());
                }
            } catch (IOException e) {
                CopperSlug.LOG.warn("Copper Slug: no se pudo leer {}", p, e);
            }
        }
        for (var v : spec.valores.values()) {
            v.set(null);
            resetear(v);
            String s = leidos.get(v.ruta());
            if (s != null) v.leer(s);
        }
        spec.cargada = true;
        guardar(spec, p);
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static void resetear(ForgeConfigSpec.Value v) {
        v.set(v.getDefault());
    }

    public static void guardar(ForgeConfigSpec spec, Path p) {
        StringBuilder b = new StringBuilder("# Copper Slug: config del servidor (se lee al abrir el mundo).\n");
        String sec = null;
        for (var v : spec.valores.values()) {
            String r = v.ruta();
            int i = r.lastIndexOf('.');
            String s = i < 0 ? "" : r.substring(0, i);
            if (!s.equals(sec)) {
                sec = s;
                b.append('\n');
                String[] cs = spec.secciones.get(s);
                if (cs != null) for (String c : cs) b.append("# ").append(c).append('\n');
                if (!s.isEmpty()) b.append('[').append(s).append("]\n");
            }
            for (String c : v.comentario) b.append("\t# ").append(c).append('\n');
            b.append("\t# ").append(v.rango()).append(" (por defecto: ").append(v.getDefault()).append(")\n");
            b.append('\t').append(r.substring(i + 1)).append(" = ").append(v.texto()).append('\n');
        }
        try {
            Files.createDirectories(p.getParent());
            Files.writeString(p, b.toString(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            CopperSlug.LOG.warn("Copper Slug: no se pudo guardar {}", p, e);
        }
    }
}

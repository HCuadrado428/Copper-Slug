package com.copperslug.shim.common;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Una config sencilla con la forma de ForgeConfigSpec (Builder con comment/push/pop/defineInRange/define), para que
 * las secciones de Miscelánea se copien tal cual. Se guarda en TOML (ver {@link com.copperslug.config.ConfigArchivo}) y el servidor manda
 * sus valores a cada cliente al entrar.
 */
public final class ForgeConfigSpec {
    /** Todos los valores por su ruta ("seccion.subseccion.clave"), en orden. */
    public final Map<String, Value<?>> valores = new LinkedHashMap<>();
    /** Comentarios de las secciones (por su ruta). */
    public final Map<String, String[]> secciones = new LinkedHashMap<>();
    public volatile boolean cargada;

    public boolean isLoaded() {
        return cargada;
    }

    public Map<String, Value<?>> valores() {
        return valores;
    }

    public abstract static class Value<T> {
        final String ruta;
        public final String[] comentario;
        final T def;
        volatile T valor;

        Value(String ruta, String[] comentario, T def) {
            this.ruta = ruta;
            this.comentario = comentario;
            this.def = def;
            this.valor = def;
        }

        public T get() {
            return valor;
        }

        public T getDefault() {
            return def;
        }

        public void set(T v) {
            valor = v;
        }

        public String ruta() {
            return ruta;
        }

        /** Lee un valor de texto (del archivo o de la red); si no vale, se queda el que había. */
        public abstract void leer(String s);

        public abstract String rango();

        public String texto() {
            return String.valueOf(valor);
        }
    }

    /** Como el de Forge: cualquier valor de la config (aquí, el de las listas). */
    public abstract static class ConfigValue<T> extends Value<T> {
        ConfigValue(String ruta, String[] comentario, T def) {
            super(ruta, comentario, def);
        }
    }

    /** Una lista (en el archivo, {@code [a, b, c]}): números si lo parecen y, si no, texto; cada uno pasa el filtro. */
    public static final class ListValue<E> extends ConfigValue<List<? extends E>> {
        final java.util.function.Predicate<Object> vale;

        ListValue(String r, String[] c, List<? extends E> d, java.util.function.Predicate<Object> vale) {
            super(r, c, List.copyOf(d));
            this.vale = vale;
        }

        @Override
        @SuppressWarnings("unchecked")
        public void leer(String s) {
            s = s.trim();
            if (!s.startsWith("[") || !s.endsWith("]")) return;
            String dentro = s.substring(1, s.length() - 1).trim();
            List<Object> l = new ArrayList<>();
            if (!dentro.isEmpty()) for (String x : dentro.split(",")) {
                x = x.trim();
                Object o;
                try {
                    o = Double.parseDouble(x);
                } catch (NumberFormatException e) {
                    o = x.replaceAll("^\"|\"$", "");
                }
                if (!vale.test(o)) return;
                l.add(o);
            }
            valor = (List<? extends E>) List.copyOf(l);
        }

        @Override
        public String rango() {
            return "Lista: [a, b, ...]";
        }

        @Override
        public String texto() {
            StringBuilder b = new StringBuilder("[");
            for (Object o : valor) {
                if (b.length() > 1) b.append(", ");
                b.append(o instanceof Number ? String.valueOf(o) : "\"" + o + "\"");
            }
            return b.append(']').toString();
        }
    }

    public static final class DoubleValue extends Value<Double> {
        final double min, max;

        DoubleValue(String r, String[] c, double d, double min, double max) {
            super(r, c, d);
            this.min = min;
            this.max = max;
        }

        @Override
        public void leer(String s) {
            try {
                double v = Double.parseDouble(s.trim());
                if (v >= min && v <= max) valor = v;
            } catch (NumberFormatException ignored) {}
        }

        @Override
        public String rango() {
            return "Rango: " + min + " ~ " + max;
        }
    }

    public static final class IntValue extends Value<Integer> {
        final int min, max;

        IntValue(String r, String[] c, int d, int min, int max) {
            super(r, c, d);
            this.min = min;
            this.max = max;
        }

        @Override
        public void leer(String s) {
            try {
                int v = Integer.parseInt(s.trim());
                if (v >= min && v <= max) valor = v;
            } catch (NumberFormatException ignored) {}
        }

        @Override
        public String rango() {
            return "Rango: " + min + " ~ " + max;
        }
    }

    public static final class BooleanValue extends Value<Boolean> {
        BooleanValue(String r, String[] c, boolean d) {
            super(r, c, d);
        }

        @Override
        public void leer(String s) {
            s = s.trim();
            if (s.equals("true") || s.equals("false")) valor = Boolean.parseBoolean(s);
        }

        @Override
        public String rango() {
            return "true / false";
        }
    }

    public static final class Builder {
        private final ForgeConfigSpec spec = new ForgeConfigSpec();
        private final List<String> camino = new ArrayList<>();
        private String[] comentario = new String[0];

        public Builder comment(String... c) {
            comentario = c;
            return this;
        }

        public Builder push(String s) {
            camino.add(s);
            spec.secciones.put(String.join(".", camino), comentario);
            comentario = new String[0];
            return this;
        }

        public Builder pop() {
            camino.remove(camino.size() - 1);
            return this;
        }

        private String ruta(String k) {
            return camino.isEmpty() ? k : String.join(".", camino) + "." + k;
        }

        private <V extends Value<?>> V poner(V v) {
            spec.valores.put(v.ruta, v);
            comentario = new String[0];
            return v;
        }

        public DoubleValue defineInRange(String k, double d, double min, double max) {
            return poner(new DoubleValue(ruta(k), comentario, d, min, max));
        }

        public IntValue defineInRange(String k, int d, int min, int max) {
            return poner(new IntValue(ruta(k), comentario, d, min, max));
        }

        public <E> ConfigValue<List<? extends E>> defineList(String k, List<? extends E> d, java.util.function.Predicate<Object> vale) {
            return poner(new ListValue<E>(ruta(k), comentario, d, vale));
        }

        public BooleanValue define(String k, boolean d) {
            return poner(new BooleanValue(ruta(k), comentario, d));
        }

        public ForgeConfigSpec build() {
            return spec;
        }
    }
}

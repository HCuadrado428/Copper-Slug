package com.copperslug.fabric;

import java.lang.reflect.Method;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Los métodos de las extensiones de Forge (IForgeItem) que tienen las armas, para llamarlos desde los mixins de Fabric.
 * Solo se buscan en las clases de Copper Slug, una vez por clase y método.
 */
public final class ExtensionesItemFabric {
    private ExtensionesItemFabric() {}

    private record K(Class<?> c, String n) {}

    private static final Map<K, Optional<Method>> CACHE = new ConcurrentHashMap<>();

    public static Method metodo(Object o, String nombre, Class<?>... tipos) {
        Class<?> c = o.getClass();
        if (!c.getName().startsWith("com.copperslug.")) return null;
        return CACHE.computeIfAbsent(new K(c, nombre), k -> {
            try {
                Method m = c.getMethod(nombre, tipos);
                m.setAccessible(true);
                return Optional.of(m);
            } catch (NoSuchMethodException e) {
                return Optional.empty();
            }
        }).orElse(null);
    }

    public static Object llamar(Method m, Object o, Object... args) {
        try {
            return m.invoke(o, args);
        } catch (java.lang.reflect.InvocationTargetException e) {
            if (e.getCause() instanceof RuntimeException r) throw r;
            throw new RuntimeException(e.getCause());
        } catch (IllegalAccessException e) {
            throw new RuntimeException(e);
        }
    }
}

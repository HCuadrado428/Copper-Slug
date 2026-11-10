package com.copperslug.shim.eventbus.api;

import com.copperslug.CopperSlug;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;

/**
 * Un bus de eventos mínimo, como el de Forge: las clases de la lista ({@link com.copperslug.Suscriptores}) tienen
 * métodos estáticos con {@code @SubscribeEvent} y un parámetro (el evento). Los cargadores crean los eventos del shim
 * desde los suyos y los mandan con {@link #post}.
 */
public final class Bus {
    private Bus() {}

    private record H(Class<?> tipo, Consumer<Object> f, EventPriority pr, boolean cancelados) {}

    private static final List<H> TODOS = new ArrayList<>();
    private static final Map<Class<?>, List<H>> POR_TIPO = new HashMap<>();

    public static synchronized void suscribir(Class<?> c) {
        for (Method m : c.getDeclaredMethods()) {
            SubscribeEvent a = m.getAnnotation(SubscribeEvent.class);
            if (a == null || !Modifier.isStatic(m.getModifiers()) || m.getParameterCount() != 1) continue;
            m.setAccessible(true);
            Class<?> t = m.getParameterTypes()[0];
            TODOS.add(new H(t, e -> {
                try {
                    m.invoke(null, e);
                } catch (java.lang.reflect.InvocationTargetException x) {
                    Throwable y = x.getCause();
                    if (y instanceof RuntimeException r) throw r;
                    if (y instanceof Error er) throw er;
                    throw new RuntimeException(y);
                } catch (IllegalAccessException x) {
                    throw new RuntimeException(x);
                }
            }, a.priority(), a.receiveCanceled()));
        }
        POR_TIPO.clear();
    }

    private static synchronized List<H> de(Class<?> t) {
        return POR_TIPO.computeIfAbsent(t, k -> {
            List<H> l = new ArrayList<>();
            for (H h : TODOS) if (h.tipo.isAssignableFrom(k)) l.add(h);
            l.sort(Comparator.comparing(H::pr));
            return l;
        });
    }

    /** Manda el evento a sus manejadores; devuelve si ha quedado cancelado. */
    public static <E> E post(E e) {
        for (H h : de(e.getClass())) {
            if (e instanceof Event ev && ev.isCanceled() && !h.cancelados) continue;
            try {
                h.f.accept(e);
            } catch (RuntimeException x) {
                CopperSlug.LOG.error("Copper Slug: error en un manejador de {}", e.getClass().getSimpleName(), x);
            }
        }
        return e;
    }

    public static boolean cancelado(Object e) {
        return e instanceof Event ev && ev.isCanceled();
    }
}

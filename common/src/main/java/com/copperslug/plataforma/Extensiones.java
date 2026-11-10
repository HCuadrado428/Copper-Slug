package com.copperslug.plataforma;

import com.copperslug.shim.client.extensions.common.IClientItemExtensions;
import net.minecraft.world.item.Item;

import java.lang.reflect.Method;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Consumer;

/**
 * Las extensiones de cliente de los objetos de las armas (lo que en Forge da initializeClient): cada objeto que tenga
 * {@code extensionesCliente(Consumer)} la da ahí. Se busca una vez por clase.
 */
public final class Extensiones {
    private Extensiones() {}

    private static final Object NADA = new Object();
    private static final Map<Item, Object> CACHE = new ConcurrentHashMap<>();

    public static IClientItemExtensions de(Item item) {
        Object o = CACHE.computeIfAbsent(item, Extensiones::buscar);
        return o == NADA ? null : (IClientItemExtensions) o;
    }

    private static Object buscar(Item item) {
        try {
            Method m = item.getClass().getMethod("extensionesCliente", Consumer.class);
            IClientItemExtensions[] r = new IClientItemExtensions[1];
            Consumer<IClientItemExtensions> c = x -> r[0] = x;
            m.invoke(item, c);
            return r[0] == null ? NADA : r[0];
        } catch (NoSuchMethodException e) {
            return NADA;
        } catch (ReflectiveOperationException e) {
            throw new RuntimeException(e);
        }
    }
}

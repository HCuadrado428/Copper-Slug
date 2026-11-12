package com.copperslug.armasfuego.cinturon;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;

import java.lang.reflect.Method;
import java.util.Optional;
import java.util.function.Predicate;

/**
 * Dónde lleva el jugador la cartuchera y la funda: en el hueco de cinturón de Curios (Forge y NeoForge) o de Trinkets
 * (Fabric) si esos mods están instalados, y si no en cualquier parte del inventario. No depende de ellos: se les llama
 * por reflexión y, si no están (o cambian su API), se mira solo el inventario.
 */
public final class Cinturon {
    private Cinturon() {}

    private static Boolean hayCurios, hayTrinkets;

    /** La primera pila que cumple {@code cond}: primero en el cinturón (Curios/Trinkets), luego en la mano y el inventario. La pila es la de verdad (se puede cambiar). */
    public static ItemStack buscar(LivingEntity e, Predicate<ItemStack> cond) {
        ItemStack s = curios(e, cond);
        if (s.isEmpty()) s = trinkets(e, cond);
        if (!s.isEmpty()) return s;
        if (cond.test(e.getOffhandItem())) return e.getOffhandItem();
        if (e instanceof Player p)
            for (int i = 0; i < p.getInventory().getContainerSize(); i++) {
                ItemStack x = p.getInventory().getItem(i);
                if (!x.isEmpty() && cond.test(x)) return x;
            }
        return ItemStack.EMPTY;
    }

    @SuppressWarnings("unchecked")
    private static ItemStack curios(LivingEntity e, Predicate<ItemStack> cond) {
        if (Boolean.FALSE.equals(hayCurios)) return ItemStack.EMPTY;
        try {
            Class<?> api = Class.forName("top.theillusivec4.curios.api.CuriosApi");
            hayCurios = true;
            Object inv = api.getMethod("getCuriosInventory", LivingEntity.class).invoke(null, e);
            // 1.20.1 devuelve un LazyOptional (con resolve()); 1.21 un Optional
            Optional<Object> o = inv instanceof Optional<?> op ? (Optional<Object>) op : (Optional<Object>) inv.getClass().getMethod("resolve").invoke(inv);
            if (o.isEmpty()) return ItemStack.EMPTY;
            Object h = o.get();
            Method f = h.getClass().getMethod("findFirstCurio", Predicate.class);
            Optional<Object> r = (Optional<Object>) f.invoke(h, cond);
            if (r.isEmpty()) return ItemStack.EMPTY;
            Object sr = r.get();
            return (ItemStack) sr.getClass().getMethod("stack").invoke(sr);
        } catch (ClassNotFoundException ex) {
            hayCurios = false;
        } catch (Throwable ex) {
            // otra versión de la API: se sigue con el inventario
        }
        return ItemStack.EMPTY;
    }

    @SuppressWarnings("unchecked")
    private static ItemStack trinkets(LivingEntity e, Predicate<ItemStack> cond) {
        if (Boolean.FALSE.equals(hayTrinkets)) return ItemStack.EMPTY;
        try {
            Class<?> api = Class.forName("dev.emi.trinkets.api.TrinketsApi");
            hayTrinkets = true;
            Optional<Object> o = (Optional<Object>) api.getMethod("getTrinketComponent", LivingEntity.class).invoke(null, e);
            if (o.isEmpty()) return ItemStack.EMPTY;
            Object c = o.get();
            java.util.List<Object> l = (java.util.List<Object>) c.getClass().getMethod("getEquipped", Predicate.class).invoke(c, cond);
            if (l.isEmpty()) return ItemStack.EMPTY;
            Object par = l.get(0);
            return (ItemStack) par.getClass().getMethod("getB").invoke(par);
        } catch (ClassNotFoundException ex) {
            hayTrinkets = false;
        } catch (Throwable ex) {
            // otra versión de la API
        }
        return ItemStack.EMPTY;
    }

    // ------------------------------------------------------------------ pilas dentro de un objeto (en 1.21.1 cambia: solo aquí)

    /** Guarda una pila en una etiqueta. */
    public static CompoundTag guardar(ItemStack s) {
        return (CompoundTag) s.saveOptional(com.copperslug.shim.Enc.registros());   // (1.21.1: con los registros del mundo)
    }

    /** Lee una pila de una etiqueta. */
    public static ItemStack leer(CompoundTag t) {
        return ItemStack.parseOptional(com.copperslug.shim.Enc.registros(), t);
    }
}

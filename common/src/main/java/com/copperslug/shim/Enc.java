package com.copperslug.shim;

import com.copperslug.shim.server.ServerLifecycleHooks;
import net.minecraft.core.Holder;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.ItemEnchantments;

/**
 * Los encantamientos en 1.21: son datos, y el código los conoce por su clave (ModEnchantments). El nivel se lee de los
 * encantamientos del objeto (sin necesitar el registro); para poner uno hace falta el registro del mundo.
 */
public final class Enc {
    private Enc() {}

    public static int nivel(ResourceKey<Enchantment> k, ItemStack s) {
        if (s.isEmpty()) return 0;
        ItemEnchantments e = s.getEnchantments();
        for (var x : e.entrySet()) if (x.getKey().is(k)) return x.getIntValue();
        return 0;
    }

    /** Lo mismo con un encantamiento del registro (vanilla o propio). */
    public static int nivel(Holder<Enchantment> h, ItemStack s) {
        return s.isEmpty() ? 0 : s.getEnchantments().getLevel(h);
    }

    public static void poner(ItemStack s, ResourceKey<Enchantment> k, int nivel) {
        Holder<Enchantment> h = holder(k);
        if (h != null) s.enchant(h, nivel);
    }

    /** El registro de encantamientos del mundo que haya (el del servidor o, en el cliente, el del nivel). */
    public static RegistryAccess registros() {
        var srv = ServerLifecycleHooks.getCurrentServer();
        if (srv != null) return srv.registryAccess();
        return com.copperslug.plataforma.Plataforma.get().registrosCliente();
    }

    public static Holder<Enchantment> holder(ResourceKey<Enchantment> k) {
        RegistryAccess r = registros();
        if (r == null) return null;
        return r.registryOrThrow(Registries.ENCHANTMENT).getHolder(k).orElse(null);
    }
}

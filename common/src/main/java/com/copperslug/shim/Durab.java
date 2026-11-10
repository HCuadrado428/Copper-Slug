package com.copperslug.shim;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.ItemStack;

/** com.copperslug.shim.Durab.danar(ItemStack, n, azar, jugador) de 1.20.1 (true si se rompe), que en 1.21 ya no existe. */
public final class Durab {
    private Durab() {}

    public static boolean danar(ItemStack s, int n, RandomSource r, ServerPlayer p) {
        if (!s.isDamageableItem()) return false;
        if (p != null && p.level() instanceof ServerLevel sl) {
            boolean[] roto = {false};
            ItemStack copia = s.copy();
            copia.hurtAndBreak(n, sl, p, it -> roto[0] = true);
            if (!roto[0]) s.setDamageValue(copia.getDamageValue());
            return roto[0];
        }
        s.setDamageValue(s.getDamageValue() + n);
        return s.getDamageValue() >= s.getMaxDamage();
    }
}

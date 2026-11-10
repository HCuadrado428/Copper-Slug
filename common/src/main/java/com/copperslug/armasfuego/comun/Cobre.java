package com.copperslug.armasfuego.comun;

import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.Vec3;

/**
 * El cobre de las armas de fuego de la segunda tanda, igual que el del revólver, la escopeta y el rifle: cuatro fases
 * (normal, expuesto, erosionado, oxidado) que se pasan con el uso (más deprisa mojado), con más dispersión y más
 * encasquillados cuanto más oxidado; un panal lo encera (ya no se oxida) y un hacha quita la cera o un paso de óxido.
 * Va en el NBT del arma ({@code Oxido} 0..3, {@code Encerado}, {@code Usos}).
 */
public final class Cobre {
    private Cobre() {}

    public static final String OXIDO = "Oxido", ENCERADO = "Encerado", USOS = "Usos";
    /** Encasquillado y dispersión (radianes) que añade cada fase. */
    public static final float[] ATASCO = {0F, 0.01F, 0.03F, 0.06F};
    public static final double[] DISPERSION = {0, 0.006, 0.014, 0.026};

    public static int oxido(ItemStack s) {
        return com.copperslug.shim.Nbt.tiene(s) ? Mth.clamp(com.copperslug.shim.Nbt.leer(s).getInt(OXIDO), 0, 3) : 0;
    }

    public static void ponerOxido(ItemStack s, int o) {
        com.copperslug.shim.Nbt.tag(s).putInt(OXIDO, Mth.clamp(o, 0, 3));
    }

    public static boolean encerado(ItemStack s) {
        return com.copperslug.shim.Nbt.tiene(s) && com.copperslug.shim.Nbt.leer(s).getBoolean(ENCERADO);
    }

    /**
     * Un disparo más: cada {@code cada} disparos (mojado, el triple de rápido) pasa a la siguiente fase. Devuelve si
     * ha cambiado de fase.
     */
    public static boolean desgastar(ItemStack s, int cada, boolean mojado) {
        if (encerado(s) || oxido(s) >= 3) return false;
        CompoundTag t = com.copperslug.shim.Nbt.tag(s);
        int u = t.getInt(USOS) + (mojado ? 3 : 1);
        if (u >= cada) {
            t.putInt(OXIDO, oxido(s) + 1);
            t.putInt(USOS, 0);
            return true;
        }
        t.putInt(USOS, u);
        return false;
    }

    /** Aviso en la barra de acción al pasar de fase. */
    public static void avisar(ServerPlayer p, ItemStack s) {
        p.displayClientMessage(Component.translatable("armafuego.copperslug.oxido." + oxido(s)).withStyle(ChatFormatting.DARK_AQUA), true);
    }

    public static boolean esPanal(ItemStack s) {
        return s.is(Items.HONEYCOMB);
    }

    public static boolean esHacha(ItemStack s) {
        return s.getItem() instanceof AxeItem;
    }

    /** Panal: encera. Devuelve si ha hecho algo. Los sonidos y chispas, en {@code donde} (null = sin partículas). */
    public static boolean encerar(Player p, ItemStack s, ItemStack panal, Vec3 donde) {
        if (encerado(s)) return false;
        com.copperslug.shim.Nbt.tag(s).putBoolean(ENCERADO, true);
        if (!p.getAbilities().instabuild) panal.shrink(1);
        efecto(p, donde, true);
        return true;
    }

    /** Hacha: quita la cera o, si no tiene, un paso de óxido (como los bloques de cobre). */
    public static boolean rascar(Player p, ItemStack s, ItemStack hacha, Vec3 donde) {
        if (encerado(s)) {
            com.copperslug.shim.Nbt.tag(s).remove(ENCERADO);
            sonido(p, donde, SoundEvents.AXE_WAX_OFF);
            if (donde != null && p.level() instanceof ServerLevel l) l.sendParticles(ParticleTypes.WAX_OFF, donde.x, donde.y, donde.z, 8, 0.2, 0.2, 0.2, 0.5);
        } else if (oxido(s) > 0) {
            com.copperslug.shim.Nbt.tag(s).putInt(OXIDO, oxido(s) - 1);
            com.copperslug.shim.Nbt.tag(s).putInt(USOS, 0);
            sonido(p, donde, SoundEvents.AXE_SCRAPE);
            if (donde != null && p.level() instanceof ServerLevel l) l.sendParticles(ParticleTypes.SCRAPE, donde.x, donde.y, donde.z, 8, 0.2, 0.2, 0.2, 0.5);
        } else return false;
        if (!p.level().isClientSide && hacha.isDamageableItem() && !p.getAbilities().instabuild && com.copperslug.shim.Durab.danar(hacha, 1, p.getRandom(), p instanceof ServerPlayer sp ? sp : null))
            hacha.shrink(1);
        return true;
    }

    private static void efecto(Player p, Vec3 donde, boolean cera) {
        sonido(p, donde, SoundEvents.HONEYCOMB_WAX_ON);
        if (donde != null && p.level() instanceof ServerLevel l) l.sendParticles(ParticleTypes.WAX_ON, donde.x, donde.y, donde.z, 8, 0.2, 0.2, 0.2, 0.5);
    }

    private static void sonido(Player p, Vec3 donde, net.minecraft.sounds.SoundEvent e) {
        if (p.level().isClientSide) {
            if (donde == null) p.playSound(e, 1.0F, 1.0F);   // en el inventario solo lo oye el que lo hace
            return;
        }
        Vec3 q = donde == null ? p.position() : donde;
        p.level().playSound(donde == null ? p : null, q.x, q.y, q.z, e, SoundSource.PLAYERS, 1.0F, 1.0F);
    }

    /** El nombre con el estado del cobre: «Winchester 1873 erosionada (encerada)», como el del revólver. */
    public static MutableComponent nombre(MutableComponent n, ItemStack s, boolean femenino) {
        String g = femenino ? "armafuego.copperslug.f." : "armafuego.copperslug.m.";
        int ox = oxido(s);
        if (ox > 0) n = Component.translatable(g + "oxido_nombre." + ox, n);
        if (encerado(s)) n = Component.translatable(g + "encerado_nombre", n);
        return n;
    }

    /** La línea del tooltip: estado del cobre (y si está encerado). */
    public static Component estado(ItemStack s) {
        String[] ox = {"normal", "expuesto", "erosionado", "oxidado"};
        Component e = Component.translatable("item.copperslug.rifle.cobre." + ox[oxido(s)]);
        return Component.translatable(encerado(s) ? "item.copperslug.rifle.estado_encerado" : "item.copperslug.rifle.estado", e).withStyle(ChatFormatting.DARK_AQUA);
    }
}

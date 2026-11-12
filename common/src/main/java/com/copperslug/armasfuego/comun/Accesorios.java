package com.copperslug.armasfuego.comun;

import com.copperslug.registry.ModItems;
import com.copperslug.shim.Nbt;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;

import java.util.List;

/** Lo que lleva montado un arma (en su NBT, clave {@code Accesorio}) y lo que cambia: dispersión, calor, balas y ruido. */
public final class Accesorios {
    private Accesorios() {}

    public static final String CLAVE = "Accesorio";

    /** El accesorio montado en el arma (o null). */
    public static Accesorio de(ItemStack arma) {
        if (arma == null || arma.isEmpty() || !Nbt.tiene(arma) || !Nbt.leer(arma).contains(CLAVE)) return null;
        Accesorio a = Accesorio.de(Nbt.leer(arma).getString(CLAVE));
        return a != null && a.vale(arma.getItem()) ? a : null;
    }

    public static void poner(ItemStack arma, Accesorio a) {
        Nbt.tag(arma).putString(CLAVE, a.id);
    }

    /** Qué accesorio es este objeto (o null si no lo es). */
    public static Accesorio deObjeto(ItemStack s) {
        if (s.isEmpty()) return null;
        for (Accesorio a : Accesorio.values()) if (s.is(ModItems.accesorio(a))) return a;
        return null;
    }

    public static float dispersion(ItemStack arma) {
        Accesorio a = de(arma);
        return a == null ? 1F : a.dispersion;
    }

    public static float calor(ItemStack arma) {
        Accesorio a = de(arma);
        return a == null ? 1F : a.calor;
    }

    public static int capacidad(ItemStack arma) {
        Accesorio a = de(arma);
        return a == null ? 0 : a.capacidad;
    }

    public static boolean silencioso(ItemStack arma) {
        Accesorio a = de(arma);
        return a != null && a.silencioso;
    }

    public static void tooltip(ItemStack arma, List<Component> l) {
        Accesorio a = de(arma);
        if (a != null) l.add(Component.translatable("msg.copperslug.accesorio.montado", Component.translatable(a.claveNombre())).withStyle(ChatFormatting.AQUA));
    }
}

package com.copperslug.armasfuego.cinturon;

import net.minecraft.ChatFormatting;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.SlotAccess;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.ClickAction;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.core.registries.Registries;

import javax.annotation.Nullable;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Predicate;

/**
 * La cartuchera: un cinturón de cuero con bolsillos que guarda hasta {@link #CAPACIDAD} piezas de munición (lo que
 * lleve la etiqueta copperslug:municion). Se llena como el saco de vanilla: con la cartuchera en el cursor, clic derecho
 * sobre la munición (o al revés); clic derecho sobre un hueco vacío saca la última. Al recargar, si no queda munición
 * suelta en el inventario, la cartuchera saca la que haga falta.
 */
public class CartucheraItem extends Item {
    public static final int CAPACIDAD = 256;
    public static final TagKey<Item> MUNICION = TagKey.create(Registries.ITEM, net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("copperslug", "municion"));
    private static final String CONTENIDO = "municion";

    public CartucheraItem(Properties p) {
        super(p);
    }

    public static boolean esMunicion(ItemStack s) {
        return !s.isEmpty() && s.is(MUNICION);
    }

    public static List<ItemStack> contenido(ItemStack c) {
        List<ItemStack> out = new ArrayList<>();
        if (!com.copperslug.shim.Nbt.tiene(c)) return out;
        ListTag l = com.copperslug.shim.Nbt.leer(c).getList(CONTENIDO, Tag.TAG_COMPOUND);
        for (int i = 0; i < l.size(); i++) {
            ItemStack s = Cinturon.leer(l.getCompound(i));
            if (!s.isEmpty()) out.add(s);
        }
        return out;
    }

    private static void poner(ItemStack c, List<ItemStack> l) {
        ListTag t = new ListTag();
        for (ItemStack s : l) if (!s.isEmpty()) t.add(Cinturon.guardar(s));
        com.copperslug.shim.Nbt.tag(c).put(CONTENIDO, t);
    }

    public static int total(ItemStack c) {
        int n = 0;
        for (ItemStack s : contenido(c)) n += s.getCount();
        return n;
    }

    /** Mete todo lo que quepa de {@code s} (la pila se queda con lo que no cabe). Devuelve cuántas ha metido. */
    public static int meter(ItemStack c, ItemStack s) {
        if (!esMunicion(s)) return 0;
        int cabe = Math.min(s.getCount(), CAPACIDAD - total(c));
        if (cabe <= 0) return 0;
        List<ItemStack> l = contenido(c);
        int resto = cabe;
        for (ItemStack x : l) {
            if (resto <= 0) break;
            if (ItemStack.isSameItemSameComponents(x, s) && x.getCount() < x.getMaxStackSize()) {
                int k = Math.min(resto, x.getMaxStackSize() - x.getCount());
                x.grow(k);
                resto -= k;
            }
        }
        while (resto > 0) {
            ItemStack n = s.copy();
            n.setCount(Math.min(resto, s.getMaxStackSize()));
            resto -= n.getCount();
            l.add(n);
        }
        s.shrink(cabe);
        poner(c, l);
        return cabe;
    }

    /** Saca la última pila guardada (o vacío). */
    public static ItemStack sacarUltima(ItemStack c) {
        List<ItemStack> l = contenido(c);
        if (l.isEmpty()) return ItemStack.EMPTY;
        ItemStack s = l.remove(l.size() - 1);
        poner(c, l);
        return s;
    }

    /**
     * Para recargar: si el jugador lleva una cartuchera (en el cinturón o en el inventario) con munición que cumpla
     * {@code cond}, saca una pila al inventario (lo que no quepa vuelve a la cartuchera). Devuelve true si ha sacado algo.
     */
    public static boolean reponer(Player p, Predicate<ItemStack> cond) {
        ItemStack c = Cinturon.buscar(p, x -> x.getItem() instanceof CartucheraItem && total(x) > 0);
        if (c.isEmpty()) return false;
        List<ItemStack> l = contenido(c);
        for (int i = 0; i < l.size(); i++) {
            ItemStack s = l.get(i);
            if (!cond.test(s)) continue;
            l.remove(i);
            poner(c, l);
            int antes = s.getCount();
            p.getInventory().add(s);
            if (!s.isEmpty()) meter(c, s);
            if (s.getCount() < antes) {
                p.level().playSound(null, p.getX(), p.getY(), p.getZ(), SoundEvents.ARMOR_EQUIP_LEATHER.value(), SoundSource.PLAYERS, 0.5F, 1.4F);
                return true;
            }
            return false;
        }
        return false;
    }

    @Override
    public boolean overrideStackedOnOther(ItemStack c, Slot slot, ClickAction a, Player p) {
        if (a != ClickAction.SECONDARY) return false;
        ItemStack s = slot.getItem();
        if (s.isEmpty()) {
            ItemStack fuera = sacarUltima(c);
            if (!fuera.isEmpty()) {
                ItemStack resto = slot.safeInsert(fuera);
                if (!resto.isEmpty()) meter(c, resto);
                p.playSound(SoundEvents.BUNDLE_REMOVE_ONE, 0.8F, 0.8F);
            }
        } else if (esMunicion(s) && meter(c, s) > 0) {
            p.playSound(SoundEvents.BUNDLE_INSERT, 0.8F, 0.8F);
        }
        return true;
    }

    @Override
    public boolean overrideOtherStackedOnMe(ItemStack c, ItemStack otra, Slot slot, ClickAction a, Player p, SlotAccess cursor) {
        if (a != ClickAction.SECONDARY || !slot.allowModification(p)) return false;
        if (otra.isEmpty()) {
            ItemStack fuera = sacarUltima(c);
            if (fuera.isEmpty()) return false;
            cursor.set(fuera);
            p.playSound(SoundEvents.BUNDLE_REMOVE_ONE, 0.8F, 0.8F);
            return true;
        }
        if (esMunicion(otra) && meter(c, otra) > 0) {
            p.playSound(SoundEvents.BUNDLE_INSERT, 0.8F, 0.8F);
            return true;
        }
        return false;
    }

    @Override
    public boolean isBarVisible(ItemStack c) {
        return total(c) > 0;
    }

    @Override
    public int getBarWidth(ItemStack c) {
        return Math.min(13, 1 + 12 * total(c) / CAPACIDAD);
    }

    @Override
    public int getBarColor(ItemStack c) {
        return 0xD9A92B;
    }

    @Override
    public void appendHoverText(ItemStack c, net.minecraft.world.item.Item.TooltipContext copperslug$ctx, List<Component> t, TooltipFlag f) {
        net.minecraft.world.level.Level l = com.copperslug.shim.Mundo.cliente();
        t.add(Component.translatable("item.copperslug.cartuchera.lleva", total(c), CAPACIDAD).withStyle(ChatFormatting.GRAY));
        for (ItemStack s : contenido(c))
            t.add(Component.literal("  " + s.getCount() + " × ").append(s.getHoverName()).withStyle(ChatFormatting.DARK_GRAY));
    }
}

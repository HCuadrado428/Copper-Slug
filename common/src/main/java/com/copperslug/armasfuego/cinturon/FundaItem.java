package com.copperslug.armasfuego.cinturon;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.SlotAccess;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.ClickAction;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

import javax.annotation.Nullable;
import java.util.List;

/**
 * La funda de cadera: guarda un arma corta (revólver, Derringer, pistola de resonancia o arponera). Con la tecla de la
 * funda (H por defecto) se desenfunda a la mano o se enfunda la que se lleva. También se llena en el inventario como el
 * saco: clic derecho con el arma sobre la funda, o con la funda vacía de cursor para sacarla.
 */
public class FundaItem extends Item {
    private static final String ARMA = "arma";

    public FundaItem(Properties p) {
        super(p);
    }

    /** ¿Cabe en la funda? Solo las armas cortas. */
    public static boolean cabe(ItemStack s) {
        Item i = s.getItem();
        return i instanceof com.copperslug.armasfuego.pistola.RevolverItem || i instanceof com.copperslug.armasfuego.oeste.DerringerItem
                || i instanceof com.copperslug.armasfuego.ciudad.ResonanciaItem || i instanceof com.copperslug.armasfuego.oceano.ArponeraItem;
    }

    public static ItemStack arma(ItemStack f) {
        if (!com.copperslug.shim.Nbt.tiene(f) || !com.copperslug.shim.Nbt.leer(f).contains(ARMA)) return ItemStack.EMPTY;
        return Cinturon.leer(com.copperslug.shim.Nbt.leer(f).getCompound(ARMA));
    }

    public static void ponerArma(ItemStack f, ItemStack a) {
        if (a.isEmpty()) com.copperslug.shim.Nbt.quitar(f, ARMA);
        else com.copperslug.shim.Nbt.tag(f).put(ARMA, Cinturon.guardar(a));
    }

    /** La tecla de la funda: si la mano lleva un arma corta y hay una funda vacía, la enfunda; si no, desenfunda. */
    public static void tecla(ServerPlayer p) {
        ItemStack mano = p.getMainHandItem();
        if (cabe(mano)) {
            ItemStack f = Cinturon.buscar(p, x -> x.getItem() instanceof FundaItem && arma(x).isEmpty());
            if (f.isEmpty()) return;
            ponerArma(f, mano.copy());
            p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY);
            p.level().playSound(null, p.getX(), p.getY(), p.getZ(), SoundEvents.ARMOR_EQUIP_LEATHER.value(), SoundSource.PLAYERS, 0.8F, 1.2F);
            return;
        }
        ItemStack f = Cinturon.buscar(p, x -> x.getItem() instanceof FundaItem && !arma(x).isEmpty());
        if (f.isEmpty()) return;
        // lo que haya en la mano va al inventario; si no cabe, no se desenfunda
        if (!mano.isEmpty()) {
            if (p.getInventory().getFreeSlot() < 0) return;
            ItemStack m = mano.copy();
            p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY);
            p.getInventory().add(m);
        }
        p.setItemInHand(InteractionHand.MAIN_HAND, arma(f));
        ponerArma(f, ItemStack.EMPTY);
        p.level().playSound(null, p.getX(), p.getY(), p.getZ(), SoundEvents.ARMOR_EQUIP_LEATHER.value(), SoundSource.PLAYERS, 0.8F, 1.6F);
        p.level().playSound(null, p.getX(), p.getY(), p.getZ(), com.copperslug.registry.ModSounds.MOB_MONTAR.get(), SoundSource.PLAYERS, 0.5F, 1.3F);
    }

    @Override
    public boolean overrideStackedOnOther(ItemStack f, Slot slot, ClickAction a, Player p) {
        if (a != ClickAction.SECONDARY) return false;
        ItemStack s = slot.getItem();
        ItemStack dentro = arma(f);
        if (s.isEmpty() && !dentro.isEmpty()) {
            slot.safeInsert(dentro);
            ponerArma(f, ItemStack.EMPTY);
            p.playSound(SoundEvents.ARMOR_EQUIP_LEATHER.value(), 0.8F, 1.4F);
        } else if (dentro.isEmpty() && cabe(s)) {
            ponerArma(f, s.split(1));
            p.playSound(SoundEvents.ARMOR_EQUIP_LEATHER.value(), 0.8F, 1.2F);
        }
        return true;
    }

    @Override
    public boolean overrideOtherStackedOnMe(ItemStack f, ItemStack otra, Slot slot, ClickAction a, Player p, SlotAccess cursor) {
        if (a != ClickAction.SECONDARY || !slot.allowModification(p)) return false;
        ItemStack dentro = arma(f);
        if (otra.isEmpty() && !dentro.isEmpty()) {
            cursor.set(dentro);
            ponerArma(f, ItemStack.EMPTY);
            p.playSound(SoundEvents.ARMOR_EQUIP_LEATHER.value(), 0.8F, 1.4F);
            return true;
        }
        if (dentro.isEmpty() && cabe(otra)) {
            ponerArma(f, otra.split(1));
            p.playSound(SoundEvents.ARMOR_EQUIP_LEATHER.value(), 0.8F, 1.2F);
            return true;
        }
        return false;
    }

    @Override
    public void appendHoverText(ItemStack f, net.minecraft.world.item.Item.TooltipContext copperslug$ctx, List<Component> t, TooltipFlag fl) {
        net.minecraft.world.level.Level l = com.copperslug.shim.Mundo.cliente();
        ItemStack a = arma(f);
        t.add(a.isEmpty() ? Component.translatable("item.copperslug.funda.vacia").withStyle(ChatFormatting.GRAY)
                : Component.translatable("item.copperslug.funda.lleva", a.getHoverName()).withStyle(ChatFormatting.GRAY));
        t.add(Component.translatable("item.copperslug.funda.tecla").withStyle(ChatFormatting.DARK_GRAY));
    }
}

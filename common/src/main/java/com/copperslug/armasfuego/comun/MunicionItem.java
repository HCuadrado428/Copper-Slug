package com.copperslug.armasfuego.comun;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

import javax.annotation.Nullable;
import java.util.List;

/** Munición de las armas de fuego nuevas: solo añade su línea de ayuda ({@code <id>.ayuda}). */
public class MunicionItem extends Item {
    public MunicionItem(Properties p) {
        super(p);
    }

    @Override
    public void appendHoverText(ItemStack s, net.minecraft.world.item.Item.TooltipContext copperslug$ctx, List<Component> lista, TooltipFlag f) {
        net.minecraft.world.level.Level l = com.copperslug.shim.Mundo.cliente();
        lista.add(Component.translatable(getDescriptionId() + ".ayuda").withStyle(ChatFormatting.GRAY));
    }
}

package com.copperslug.armasfuego.comun;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

import java.util.List;

/** Un accesorio de cobre para una arma concreta: se monta en el yunque. */
public class AccesorioItem extends Item {
    public final Accesorio accesorio;

    public AccesorioItem(Accesorio a, Properties p) {
        super(p);
        this.accesorio = a;
    }

    @Override
    public void appendHoverText(ItemStack s, Item.TooltipContext ctx, List<Component> lista, TooltipFlag f) {
        lista.add(Component.translatable("msg.copperslug.accesorio.para", Component.translatable("accesorio.copperslug." + accesorio.id + ".arma")).withStyle(ChatFormatting.GOLD));
        lista.add(Component.translatable(getDescriptionId() + ".ayuda").withStyle(ChatFormatting.GRAY));
        lista.add(Component.translatable("msg.copperslug.accesorio.yunque").withStyle(ChatFormatting.DARK_GRAY));
    }
}

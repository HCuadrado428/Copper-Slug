package com.copperslug.recompensas;

import net.minecraft.ChatFormatting;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

import java.util.List;

/**
 * Cartel de «Se busca». Recién hecho está en blanco; al usarlo sale un forajido con nombre y el sitio donde lo vieron por
 * última vez (el campamento de saqueadores más cercano, o un sitio lejos si no hay ninguno). Al llegar cerca aparece con
 * su banda; muerto, el cartel queda «cazado» y cualquier aldeano paga la recompensa.
 */
public class CartelItem extends Item {
    public CartelItem(Properties p) {
        super(p);
    }

    public static CompoundTag datos(ItemStack s) {
        return s.getOrCreateTag();
    }

    public static Forajidos.Estado estado(ItemStack s) {
        if (!(s.getItem() instanceof CartelItem) || !s.hasTag()) return Forajidos.Estado.EN_BLANCO;
        return Forajidos.Estado.de(s.getTag().getString(Forajidos.ESTADO));
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level l, Player p, InteractionHand mano) {
        ItemStack s = p.getItemInHand(mano);
        if (estado(s) != Forajidos.Estado.EN_BLANCO) return InteractionResultHolder.pass(s);
        if (l instanceof ServerLevel sl && p instanceof ServerPlayer sp) Forajidos.nuevo(sl, sp, s, null);
        return InteractionResultHolder.sidedSuccess(s, l.isClientSide);
    }

    @Override
    public boolean isFoil(ItemStack s) {
        return estado(s) == Forajidos.Estado.CAZADO;
    }

    @Override
    public Component getName(ItemStack s) {
        if (estado(s) == Forajidos.Estado.EN_BLANCO) return super.getName(s);
        return Component.translatable("item.copperslug.cartel_se_busca.de", Forajidos.nombre(s.getTag()));
    }

    @Override
    public void appendHoverText(ItemStack s, Level l, List<Component> t, TooltipFlag f) {
        switch (estado(s)) {
            case EN_BLANCO -> t.add(Component.translatable("item.copperslug.cartel_se_busca.blanco").withStyle(ChatFormatting.GRAY));
            case BUSCADO -> {
                CompoundTag d = s.getTag();
                t.add(Component.translatable("item.copperslug.cartel_se_busca.visto", d.getInt(Forajidos.X), d.getInt(Forajidos.Z)).withStyle(ChatFormatting.GRAY));
                t.add(Component.translatable("item.copperslug.cartel_se_busca.recompensa", d.getInt(Forajidos.PAGO)).withStyle(ChatFormatting.GREEN));
            }
            case CAZADO -> t.add(Component.translatable("item.copperslug.cartel_se_busca.cazado", s.getTag().getInt(Forajidos.PAGO)).withStyle(ChatFormatting.GOLD));
        }
    }
}

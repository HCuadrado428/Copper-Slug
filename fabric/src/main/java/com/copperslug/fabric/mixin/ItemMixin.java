package com.copperslug.fabric.mixin;

import com.copperslug.fabric.ExtensionesItemFabric;
import com.google.common.collect.Multimap;
import net.fabricmc.fabric.api.item.v1.FabricItem;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;

/** Las extensiones de Forge de las armas (shouldCauseReequipAnimation...) a través de FabricItem. */
@Mixin(Item.class)
public abstract class ItemMixin implements FabricItem {
    @Override
    public boolean allowNbtUpdateAnimation(Player p, InteractionHand h, ItemStack viejo, ItemStack nuevo) {
        var m = ExtensionesItemFabric.metodo(this, "shouldCauseReequipAnimation", ItemStack.class, ItemStack.class, boolean.class);
        if (m == null) return true;
        return (Boolean) ExtensionesItemFabric.llamar(m, this, viejo, nuevo, false);
    }

    @Override
    public boolean allowContinuingBlockBreaking(Player p, ItemStack viejo, ItemStack nuevo) {
        var m = ExtensionesItemFabric.metodo(this, "shouldCauseBlockBreakReset", ItemStack.class, ItemStack.class);
        if (m == null) return false;
        return !(Boolean) ExtensionesItemFabric.llamar(m, this, viejo, nuevo);
    }

    @Override
    @SuppressWarnings("unchecked")
    public Multimap<Attribute, AttributeModifier> getAttributeModifiers(ItemStack s, EquipmentSlot slot) {
        var m = ExtensionesItemFabric.metodo(this, "getAttributeModifiers", EquipmentSlot.class, ItemStack.class);
        if (m == null) return ((Item) (Object) this).getDefaultAttributeModifiers(slot);
        return (Multimap<Attribute, AttributeModifier>) ExtensionesItemFabric.llamar(m, this, slot, s);
    }
}

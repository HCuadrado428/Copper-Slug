package com.copperslug.mixin;

import net.minecraft.client.gui.screens.inventory.CreativeModeInventoryScreen;
import net.minecraft.world.item.CreativeModeTab;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Invoker;

/** Para la prueba del CI: abrir el inventario creativo en la pestaña de Copper Slug. */
@Mixin(CreativeModeInventoryScreen.class)
public interface CreativeScreenAccessor {
    @Invoker("selectTab")
    void copperslug$elegir(CreativeModeTab tab);
}

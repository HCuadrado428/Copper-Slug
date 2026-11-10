package com.copperslug.forge.mixin;

import net.minecraft.world.item.Item;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

/** Las propiedades de render de Forge (lo que da initializeClient), para ponérselas a las armas desde fuera. */
@Mixin(Item.class)
public interface ItemRenderAccessor {
    @Accessor(value = "renderProperties", remap = false)
    void copperslug$ponerRender(Object o);
}

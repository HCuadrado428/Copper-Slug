package com.copperslug.shim;

import com.copperslug.mixin.ItemPropertiesAccessor;
import net.minecraft.client.renderer.item.ClampedItemPropertyFunction;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;

/** ItemProperties.register es privado en vanilla (Forge lo abre): se llama con un invoker. */
public final class ItemProperties {
    private ItemProperties() {}

    public static void register(Item item, ResourceLocation id, ClampedItemPropertyFunction f) {
        ItemPropertiesAccessor.copperslug$register(item, id, f);
    }
}

package com.copperslug.shim.common;

import com.copperslug.CopperSlug;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;

/**
 * Las etiquetas de Forge que usan las armas, como etiquetas propias (data/copperslug/tags): cada una lleva lo vanilla
 * y, si existen, las de Forge (forge:) y las comunes de Fabric (c:).
 */
public final class Tags {
    private Tags() {}

    private static ResourceLocation rl(String n) {
        return new ResourceLocation(CopperSlug.MOD_ID, n);
    }

    public static final class Blocks {
        public static final TagKey<Block> GLASS = TagKey.create(Registries.BLOCK, rl("glass"));
        public static final TagKey<Block> GLASS_PANES = TagKey.create(Registries.BLOCK, rl("glass_panes"));
    }

    public static final class Items {
        public static final TagKey<Item> SHEARS = TagKey.create(Registries.ITEM, rl("shears"));
        public static final TagKey<Item> COBBLESTONE = TagKey.create(Registries.ITEM, rl("cobblestone"));
    }

    public static final class EntityTypes {
        public static final TagKey<EntityType<?>> BOSSES = TagKey.create(Registries.ENTITY_TYPE, rl("bosses"));
    }
}

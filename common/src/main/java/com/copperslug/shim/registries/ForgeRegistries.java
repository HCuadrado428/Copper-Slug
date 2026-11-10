package com.copperslug.shim.registries;

import net.minecraft.core.Registry;
import net.minecraft.core.particles.ParticleType;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.enchantment.Enchantment;

import java.util.Map;
import java.util.Set;

/** Los registros vanilla con los nombres de Forge (y los métodos que usan las armas). */
public final class ForgeRegistries {
    private ForgeRegistries() {}

    public record R<T>(ResourceKey<? extends Registry<T>> clave, Registry<T> reg) {
        public ResourceLocation getKey(T t) {
            return reg.getKey(t);
        }

        public T getValue(ResourceLocation id) {
            return reg.containsKey(id) ? reg.get(id) : null;
        }

        public boolean containsKey(ResourceLocation id) {
            return reg.containsKey(id);
        }

        public Set<Map.Entry<ResourceKey<T>, T>> getEntries() {
            return reg.entrySet();
        }

        public Iterable<T> getValues() {
            return reg;
        }
    }

    public static final R<Item> ITEMS = new R<>(Registries.ITEM, BuiltInRegistries.ITEM);
    public static final R<Enchantment> ENCHANTMENTS = new R<>(Registries.ENCHANTMENT, BuiltInRegistries.ENCHANTMENT);
    public static final R<MobEffect> MOB_EFFECTS = new R<>(Registries.MOB_EFFECT, BuiltInRegistries.MOB_EFFECT);
    public static final R<SoundEvent> SOUND_EVENTS = new R<>(Registries.SOUND_EVENT, BuiltInRegistries.SOUND_EVENT);
    public static final R<EntityType<?>> ENTITY_TYPES = new R<>(Registries.ENTITY_TYPE, BuiltInRegistries.ENTITY_TYPE);
    public static final R<RecipeSerializer<?>> RECIPE_SERIALIZERS = new R<>(Registries.RECIPE_SERIALIZER, BuiltInRegistries.RECIPE_SERIALIZER);
    public static final R<ParticleType<?>> PARTICLE_TYPES = new R<>(Registries.PARTICLE_TYPE, BuiltInRegistries.PARTICLE_TYPE);
    public static final R<net.minecraft.world.level.block.Block> BLOCKS = new R<>(Registries.BLOCK, BuiltInRegistries.BLOCK);
}

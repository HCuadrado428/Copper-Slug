package com.copperslug.ropa;

import net.minecraft.core.Holder;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.Ingredient;

import java.util.List;
import java.util.Map;

/**
 * El material de la ropa cosmética (dos juegos: vaquero y bandido). Es ropa de cuero: protege lo mismo que una armadura de cuero
 * (1, 3, 2 y 1) y dura algo más; lo que cambia es cómo se ve. La capa de textura sale de {@code textures/models/armor/<nombre>_layer_N.png}.
 * En 1.21 el material es un Holder: aquí va directo, sin registro, para no depender del orden en que cada cargador registra las cosas.
 */
public final class Ropa {
    private Ropa() {}

    /** El factor de durabilidad (el de cuero es 5). */
    public static final int DURABILIDAD = 8;

    public static final Holder<ArmorMaterial> VAQUERO = material("vaquero");
    public static final Holder<ArmorMaterial> BANDIDO = material("bandido");

    private static Holder<ArmorMaterial> material(String nombre) {
        return Holder.direct(new ArmorMaterial(
                Map.of(ArmorItem.Type.HELMET, 1, ArmorItem.Type.CHESTPLATE, 3, ArmorItem.Type.LEGGINGS, 2, ArmorItem.Type.BOOTS, 1),
                12, SoundEvents.ARMOR_EQUIP_LEATHER, () -> Ingredient.of(Items.LEATHER),
                List.of(new ArmorMaterial.Layer(ResourceLocation.fromNamespaceAndPath(com.copperslug.CopperSlug.MOD_ID, nombre))), 0F, 0F));
    }
}

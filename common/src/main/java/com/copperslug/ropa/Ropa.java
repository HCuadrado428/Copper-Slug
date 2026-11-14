package com.copperslug.ropa;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.Ingredient;

/**
 * El material de la ropa cosmética (dos juegos: vaquero y bandido). Es ropa de cuero: protege lo mismo que una armadura de cuero
 * (1, 3, 2 y 1) y dura algo más; lo que cambia es cómo se ve. La capa de textura sale de {@code textures/models/armor/<nombre>_layer_N.png}.
 */
public enum Ropa implements ArmorMaterial {
    VAQUERO("vaquero"),
    BANDIDO("bandido");

    private static final int[] VIDA = {13, 15, 16, 11};   // casco, peto, pantalón, botas (el de cuero, por 8 en vez de por 5)
    private static final int[] DEFENSA = {1, 3, 2, 1};

    private final String nombre;

    Ropa(String nombre) {
        this.nombre = nombre;
    }

    private static int pos(ArmorItem.Type t) {
        return switch (t) {
            case HELMET -> 0;
            case CHESTPLATE -> 1;
            case LEGGINGS -> 2;
            case BOOTS -> 3;
        };
    }

    @Override
    public int getDurabilityForType(ArmorItem.Type t) {
        return VIDA[pos(t)] * 8;
    }

    @Override
    public int getDefenseForType(ArmorItem.Type t) {
        return DEFENSA[pos(t)];
    }

    @Override
    public int getEnchantmentValue() {
        return 12;
    }

    @Override
    public SoundEvent getEquipSound() {
        return SoundEvents.ARMOR_EQUIP_LEATHER;
    }

    @Override
    public Ingredient getRepairIngredient() {
        return Ingredient.of(Items.LEATHER);
    }

    @Override
    public String getName() {
        return com.copperslug.CopperSlug.MOD_ID + ":" + nombre;
    }

    @Override
    public float getToughness() {
        return 0F;
    }

    @Override
    public float getKnockbackResistance() {
        return 0F;
    }
}

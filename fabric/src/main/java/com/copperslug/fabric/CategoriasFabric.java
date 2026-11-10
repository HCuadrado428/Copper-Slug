package com.copperslug.fabric;

import net.minecraft.world.item.Item;
import net.minecraft.world.item.enchantment.EnchantmentCategory;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Predicate;

/**
 * En Fabric no se pueden crear constantes nuevas de EnchantmentCategory. Cada categoría de las armas usa una vanilla
 * distinta como "etiqueta" y, para los encantamientos de Copper Slug, los mixins de Enchantment.canEnchant y de la
 * mesa de encantamientos miran el filtro de verdad (este mapa) en vez de la categoría vanilla.
 */
public final class CategoriasFabric {
    private CategoriasFabric() {}

    private static final EnchantmentCategory[] HUECOS = {EnchantmentCategory.ARMOR_FEET, EnchantmentCategory.ARMOR_LEGS, EnchantmentCategory.ARMOR_CHEST,
            EnchantmentCategory.ARMOR_HEAD, EnchantmentCategory.WEAPON, EnchantmentCategory.DIGGER, EnchantmentCategory.FISHING_ROD,
            EnchantmentCategory.TRIDENT, EnchantmentCategory.BOW, EnchantmentCategory.WEARABLE, EnchantmentCategory.CROSSBOW,
            EnchantmentCategory.VANISHABLE, EnchantmentCategory.ARMOR, EnchantmentCategory.BREAKABLE};
    private static final Map<EnchantmentCategory, Predicate<Item>> FILTROS = new HashMap<>();
    private static int n;

    static EnchantmentCategory nueva(String nombre, Predicate<Item> filtro) {
        if (n >= HUECOS.length) throw new IllegalStateException("demasiadas categorías de encantamiento");
        EnchantmentCategory c = HUECOS[n++];
        FILTROS.put(c, filtro);
        return c;
    }

    /** El filtro de una categoría de las armas (null si es otra). */
    public static Predicate<Item> filtro(EnchantmentCategory c) {
        return FILTROS.get(c);
    }
}

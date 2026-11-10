package com.copperslug.shim;

import com.copperslug.plataforma.Plataforma;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.enchantment.EnchantmentCategory;

import java.util.function.Predicate;

/** EnchantmentCategory.create de Forge (en Fabric no se pueden crear constantes del enum: ver la plataforma). */
public final class Categorias {
    private Categorias() {}

    public static EnchantmentCategory create(String nombre, Predicate<Item> filtro) {
        return Plataforma.get().categoria(nombre, filtro);
    }
}

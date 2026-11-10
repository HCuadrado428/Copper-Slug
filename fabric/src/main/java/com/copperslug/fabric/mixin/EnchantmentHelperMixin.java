package com.copperslug.fabric.mixin;

import com.copperslug.fabric.CategoriasFabric;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentCategory;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/** La mesa de encantamientos mira la categoría a pelo: para los de las armas, su filtro de verdad. */
@Mixin(EnchantmentHelper.class)
public abstract class EnchantmentHelperMixin {
    @Unique
    private static Enchantment copperslug$ultimo;

    @Redirect(method = "getAvailableEnchantmentResults", at = @At(value = "FIELD",
            target = "Lnet/minecraft/world/item/enchantment/Enchantment;category:Lnet/minecraft/world/item/enchantment/EnchantmentCategory;"))
    private static EnchantmentCategory copperslug$categoria(Enchantment e) {
        copperslug$ultimo = e;
        return e.category;
    }

    @Redirect(method = "getAvailableEnchantmentResults", at = @At(value = "INVOKE",
            target = "Lnet/minecraft/world/item/enchantment/EnchantmentCategory;canEnchant(Lnet/minecraft/world/item/Item;)Z"))
    private static boolean copperslug$vale(EnchantmentCategory c, Item item) {
        Enchantment e = copperslug$ultimo;
        if (e != null && e.getClass().getName().startsWith("com.copperslug.")) {
            var f = CategoriasFabric.filtro(c);
            if (f != null) return f.test(item);
        }
        return c.canEnchant(item);
    }
}

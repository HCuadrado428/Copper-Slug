package com.copperslug.fabric.mixin;

import com.copperslug.fabric.CategoriasFabric;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentCategory;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Los encantamientos de las armas: qué objetos valen (ver CategoriasFabric). */
@Mixin(Enchantment.class)
public abstract class EnchantmentMixin {
    @Shadow
    @Final
    public EnchantmentCategory category;

    @Inject(method = "canEnchant", at = @At("HEAD"), cancellable = true)
    private void copperslug$vale(ItemStack s, CallbackInfoReturnable<Boolean> cir) {
        if (!getClass().getName().startsWith("com.copperslug.")) return;
        var f = CategoriasFabric.filtro(category);
        if (f != null) cir.setReturnValue(f.test(s.getItem()));
    }
}

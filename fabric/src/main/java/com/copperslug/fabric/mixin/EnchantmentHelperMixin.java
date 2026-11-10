package com.copperslug.fabric.mixin;

import com.copperslug.fabric.CategoriasFabric;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentCategory;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.Redirect;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import com.copperslug.armasfuego.oeste.MosqueteItem;
import net.minecraft.world.item.ItemStack;

/**
 * La mesa de encantamientos mira la categoría a pelo: para los de las armas, su filtro de verdad. Y los encantamientos
 * por objeto de Forge (IForgeItem.getEnchantmentLevel/getAllEnchantments): el mosquete suma los de la espada calada.
 */
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

    @Inject(method = "getItemEnchantmentLevel", at = @At("RETURN"), cancellable = true)
    private static void copperslug$nivel(Enchantment e, ItemStack s, CallbackInfoReturnable<Integer> cir) {
        if (s.getItem() instanceof MosqueteItem m) cir.setReturnValue(m.getEnchantmentLevel(s, e));
    }

    // (getEnchantments no: es lo que leen el yunque y la piedra de afilar, y en Forge tampoco cambia)

    /** El daño extra (Filo, Golpe…) y los efectos al golpear recorren los encantamientos del objeto: también los de la espada. */
    @Inject(method = "runIterationOnItem", at = @At("HEAD"), cancellable = true)
    private static void copperslug$recorrer(EnchantmentHelper.EnchantmentVisitor v, ItemStack s, CallbackInfo ci) {
        if (s.isEmpty() || !(s.getItem() instanceof MosqueteItem m)) return;
        m.getAllEnchantments(s).forEach(v::accept);
        ci.cancel();
    }
}

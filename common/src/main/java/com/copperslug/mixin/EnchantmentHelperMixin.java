package com.copperslug.mixin;

import com.copperslug.armasfuego.oeste.MosqueteItem;
import net.minecraft.core.Holder;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.EnchantedItemInUse;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * La bayoneta del mosquete con los encantamientos de su espada (Filo, Aspecto ígneo, Botín…; Barrido, Irrompibilidad y
 * Reparación no): el nivel de un encantamiento y el recorrido de los encantamientos del objeto al golpear. En 1.20.1
 * Forge lo hacía con getEnchantmentLevel/getAllEnchantments del objeto; en 1.21 se hace igual en los tres cargadores.
 */
@Mixin(EnchantmentHelper.class)
public abstract class EnchantmentHelperMixin {
    @Inject(method = "getItemEnchantmentLevel", at = @At("RETURN"), cancellable = true)
    private static void copperslug$nivel(Holder<Enchantment> e, ItemStack s, CallbackInfoReturnable<Integer> cir) {
        if (MosqueteItem.conBayoneta(s)) cir.setReturnValue(MosqueteItem.nivelConBayoneta(s, e, cir.getReturnValueI()));
    }

    @Inject(method = "runIterationOnItem(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/enchantment/EnchantmentHelper$EnchantmentVisitor;)V",
            at = @At("HEAD"), cancellable = true)
    private static void copperslug$recorrer(ItemStack s, EnchantmentHelper.EnchantmentVisitor v, CallbackInfo ci) {
        if (!MosqueteItem.conBayoneta(s)) return;
        for (var x : MosqueteItem.encantamientosConBayoneta(s).entrySet()) v.accept(x.getKey(), x.getIntValue());
        ci.cancel();
    }

    @Inject(method = "runIterationOnItem(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/enchantment/EnchantmentHelper$EnchantmentInSlotVisitor;)V",
            at = @At("HEAD"), cancellable = true)
    private static void copperslug$recorrerEnRanura(ItemStack s, EquipmentSlot ranura, LivingEntity quien, EnchantmentHelper.EnchantmentInSlotVisitor v, CallbackInfo ci) {
        if (!MosqueteItem.conBayoneta(s)) return;
        EnchantedItemInUse uso = new EnchantedItemInUse(s, ranura, quien);
        for (var x : MosqueteItem.encantamientosConBayoneta(s).entrySet())
            if (x.getKey().value().matchingSlot(ranura)) v.accept(x.getKey(), x.getIntValue(), uso);
        ci.cancel();
    }
}

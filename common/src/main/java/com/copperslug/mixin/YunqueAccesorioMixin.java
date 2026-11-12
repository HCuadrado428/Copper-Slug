package com.copperslug.mixin;

import com.copperslug.armasfuego.comun.Accesorio;
import com.copperslug.armasfuego.comun.Accesorios;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.AnvilMenu;
import net.minecraft.world.inventory.DataSlot;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Monta un accesorio en un arma en el yunque: arma a la izquierda, accesorio a la derecha, dos niveles y uno de cobre. */
@Mixin(AnvilMenu.class)
public abstract class YunqueAccesorioMixin {
    @Shadow
    private DataSlot cost;
    @Shadow
    private int repairItemCountCost;

    @Inject(method = "createResult", at = @At("TAIL"))
    private void copperslug$accesorio(CallbackInfo ci) {
        AbstractContainerMenu m = (AbstractContainerMenu) (Object) this;
        ItemStack arma = m.getSlot(0).getItem(), acc = m.getSlot(1).getItem();
        Accesorio a = Accesorios.deObjeto(acc);
        if (a == null || !a.vale(arma.getItem()) || Accesorios.de(arma) == a) return;
        ItemStack r = arma.copy();
        Accesorios.poner(r, a);
        m.getSlot(2).set(r);
        this.cost.set(2);
        this.repairItemCountCost = 1;
        m.broadcastChanges();
    }
}

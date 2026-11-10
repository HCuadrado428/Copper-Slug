package com.copperslug.fabric.mixin;

import com.copperslug.shim.event.entity.player.PlayerEvent;
import com.copperslug.shim.eventbus.api.Bus;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** El ItemPickupEvent de Forge: cuando el jugador recoge algo del suelo. */
@Mixin(ItemEntity.class)
public abstract class ItemEntityMixin {
    @Unique
    private ItemStack copperslug$antes;

    @Inject(method = "playerTouch", at = @At("HEAD"))
    private void copperslug$antes(Player p, CallbackInfo ci) {
        copperslug$antes = ((ItemEntity) (Object) this).getItem().copy();
    }

    @Inject(method = "playerTouch", at = @At("RETURN"))
    private void copperslug$despues(Player p, CallbackInfo ci) {
        ItemStack a = copperslug$antes;
        copperslug$antes = null;
        if (a == null || p.level().isClientSide) return;
        int quedan = ((ItemEntity) (Object) this).getItem().getCount();
        if (((ItemEntity) (Object) this).isRemoved()) quedan = 0;
        if (quedan < a.getCount()) {
            ItemStack cogido = a.copyWithCount(a.getCount() - quedan);
            Bus.post(new PlayerEvent.ItemPickupEvent(p, (ItemEntity) (Object) this, cogido));
        }
    }
}

package com.copperslug.fabric.mixin;

import com.copperslug.fabric.ExtensionesItemFabric;
import com.copperslug.shim.event.entity.living.LivingEvent;
import com.copperslug.shim.eventbus.api.Bus;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(LivingEntity.class)
public abstract class LivingEntityMixin {
    /** El LivingJumpEvent de Forge. */
    @Inject(method = "jumpFromGround", at = @At("TAIL"))
    private void copperslug$salto(CallbackInfo ci) {
        Bus.post(new LivingEvent.LivingJumpEvent((LivingEntity) (Object) this));
    }

    /** IForgeItem.onEntitySwing: el arma puede impedir el golpe de brazo (el rifle no lo hace al accionar el cerrojo). */
    @Inject(method = "swing(Lnet/minecraft/world/InteractionHand;Z)V", at = @At("HEAD"), cancellable = true)
    private void copperslug$balanceo(InteractionHand h, boolean enviar, CallbackInfo ci) {
        LivingEntity e = (LivingEntity) (Object) this;
        ItemStack s = e.getItemInHand(h);
        if (s.isEmpty()) return;
        var m = ExtensionesItemFabric.metodo(s.getItem(), "onEntitySwing", ItemStack.class, LivingEntity.class);
        if (m != null && (Boolean) ExtensionesItemFabric.llamar(m, s.getItem(), s, e)) ci.cancel();
    }
}

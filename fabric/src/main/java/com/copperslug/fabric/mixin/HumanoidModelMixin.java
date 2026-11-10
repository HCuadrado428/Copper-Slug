package com.copperslug.fabric.mixin;

import com.copperslug.fabric.cliente.PosesFabric;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Las poses de brazo propias de las armas (ver PosesFabric). */
@Mixin(HumanoidModel.class)
public abstract class HumanoidModelMixin<T extends LivingEntity> {
    @Inject(method = "setupAnim(Lnet/minecraft/world/entity/LivingEntity;FFFFF)V", at = @At("TAIL"))
    private void copperslug$poses(T e, float a, float b, float c, float d, float f, CallbackInfo ci) {
        PosesFabric.aplicar((HumanoidModel<?>) (Object) this, e);
    }
}

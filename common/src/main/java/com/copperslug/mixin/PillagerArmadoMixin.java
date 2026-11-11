package com.copperslug.mixin;

import com.copperslug.armasfuego.comun.MobsArmados;
import net.minecraft.world.entity.monster.AbstractIllager;
import net.minecraft.world.entity.monster.Pillager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Un saqueador con la Winchester la lleva en alto con las dos manos (la pose de la ballesta), no colgando del costado. */
@Mixin(Pillager.class)
public abstract class PillagerArmadoMixin {
    @Inject(method = "getArmPose", at = @At("RETURN"), cancellable = true)
    private void copperslug$armado(CallbackInfoReturnable<AbstractIllager.IllagerArmPose> cir) {
        if (MobsArmados.armado((Pillager) (Object) this)) cir.setReturnValue(AbstractIllager.IllagerArmPose.CROSSBOW_HOLD);
    }
}

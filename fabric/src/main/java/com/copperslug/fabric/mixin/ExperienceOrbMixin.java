package com.copperslug.fabric.mixin;

import com.copperslug.shim.event.entity.player.PlayerXpEvent;
import com.copperslug.shim.eventbus.api.Bus;
import net.minecraft.world.entity.ExperienceOrb;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** El PlayerXpEvent.PickupXp de Forge: justo antes de que el jugador recoja el orbe (y vanilla arregle con Reparación). */
@Mixin(ExperienceOrb.class)
public abstract class ExperienceOrbMixin {
    @Inject(method = "playerTouch", at = @At(value = "INVOKE", target = "Lnet/minecraft/world/entity/player/Player;take(Lnet/minecraft/world/entity/Entity;I)V"))
    private void copperslug$recoger(Player p, CallbackInfo ci) {
        Bus.post(new PlayerXpEvent.PickupXp(p, (ExperienceOrb) (Object) this));
    }
}

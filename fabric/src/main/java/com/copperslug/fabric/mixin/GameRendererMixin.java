package com.copperslug.fabric.mixin;

import com.copperslug.shim.client.event.ViewportEvent;
import com.copperslug.shim.event.TickEvent;
import com.copperslug.shim.eventbus.api.Bus;
import net.minecraft.client.Camera;
import net.minecraft.client.renderer.GameRenderer;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** El RenderTickEvent y el ComputeCameraAngles de Forge. */
@Mixin(GameRenderer.class)
public abstract class GameRendererMixin {
    @Shadow
    @Final
    private Camera mainCamera;

    @Inject(method = "render", at = @At("HEAD"))
    private void copperslug$antes(net.minecraft.client.DeltaTracker dt, boolean mundo, CallbackInfo ci) {
        Bus.post(new TickEvent.RenderTickEvent(TickEvent.Phase.START, dt.getGameTimeDeltaPartialTick(false)));
    }

    @Inject(method = "render", at = @At("RETURN"))
    private void copperslug$despues(net.minecraft.client.DeltaTracker dt, boolean mundo, CallbackInfo ci) {
        Bus.post(new TickEvent.RenderTickEvent(TickEvent.Phase.END, dt.getGameTimeDeltaPartialTick(false)));
    }

    @Inject(method = "renderLevel", at = @At(value = "INVOKE", target = "Lnet/minecraft/client/Camera;setup(Lnet/minecraft/world/level/BlockGetter;Lnet/minecraft/world/entity/Entity;ZZF)V",
            shift = At.Shift.AFTER))
    private void copperslug$camara(net.minecraft.client.DeltaTracker dt, CallbackInfo ci) {
        Camera c = mainCamera;
        var e = Bus.post(new ViewportEvent.ComputeCameraAngles(c, dt.getGameTimeDeltaPartialTick(true), c.getYRot(), c.getXRot(), 0F));
        if (e.getYaw() != c.getYRot() || e.getPitch() != c.getXRot()) ((CameraAccessor) c).copperslug$girar(e.getYaw(), e.getPitch());
        // (en 1.21 el giro sobre el eje de la vista va en una matriz que no se ve desde aquí: en Fabric el «roll» no se aplica)
    }
}

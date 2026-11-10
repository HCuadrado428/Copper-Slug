package com.copperslug.fabric.mixin;

import com.copperslug.shim.client.event.ViewportEvent;
import com.copperslug.shim.event.TickEvent;
import com.copperslug.shim.eventbus.api.Bus;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
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
    private void copperslug$antes(float pt, long t, boolean mundo, CallbackInfo ci) {
        Bus.post(new TickEvent.RenderTickEvent(TickEvent.Phase.START, pt));
    }

    @Inject(method = "render", at = @At("RETURN"))
    private void copperslug$despues(float pt, long t, boolean mundo, CallbackInfo ci) {
        Bus.post(new TickEvent.RenderTickEvent(TickEvent.Phase.END, pt));
    }

    @Inject(method = "renderLevel", at = @At(value = "INVOKE", target = "Lnet/minecraft/client/Camera;setup(Lnet/minecraft/world/level/BlockGetter;Lnet/minecraft/world/entity/Entity;ZZF)V",
            shift = At.Shift.AFTER))
    private void copperslug$camara(float pt, long t, PoseStack ps, CallbackInfo ci) {
        Camera c = mainCamera;
        var e = Bus.post(new ViewportEvent.ComputeCameraAngles(c, pt, c.getYRot(), c.getXRot(), 0F));
        if (e.getYaw() != c.getYRot() || e.getPitch() != c.getXRot()) ((CameraAccessor) c).copperslug$girar(e.getYaw(), e.getPitch());
        if (e.getRoll() != 0F) ps.mulPose(Axis.ZP.rotationDegrees(e.getRoll()));
    }
}

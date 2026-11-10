package com.copperslug.fabric.mixin;

import com.copperslug.shim.client.event.InputEvent;
import com.copperslug.shim.eventbus.api.Bus;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.MultiPlayerGameMode;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import org.jetbrains.annotations.Nullable;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** El InteractionKeyMappingTriggered de Forge: clic de atacar y de usar, con las mismas condiciones que en Forge. */
@Mixin(Minecraft.class)
public abstract class MinecraftMixin {
    @Shadow
    protected int missTime;
    @Shadow
    private int rightClickDelay;
    @Shadow
    @Nullable
    public LocalPlayer player;
    @Shadow
    @Nullable
    public HitResult hitResult;
    @Shadow
    @Nullable
    public MultiPlayerGameMode gameMode;

    @Inject(method = "startAttack", at = @At("HEAD"), cancellable = true)
    private void copperslug$ataque(CallbackInfoReturnable<Boolean> cir) {
        if (missTime > 0 || hitResult == null || player == null || player.isHandsBusy()) return;
        var e = Bus.post(InputEvent.InteractionKeyMappingTriggered.ataque(InteractionHand.MAIN_HAND));
        if (!e.isCanceled()) return;
        if (e.shouldSwingHand()) player.swing(InteractionHand.MAIN_HAND);
        cir.setReturnValue(false);
    }

    @Inject(method = "continueAttack", at = @At("HEAD"), cancellable = true)
    private void copperslug$sigueAtaque(boolean izq, CallbackInfo ci) {
        if (!izq || missTime > 0 || player == null || player.isUsingItem()) return;
        if (!(hitResult instanceof BlockHitResult b) || b.getType() != HitResult.Type.BLOCK) return;
        var e = Bus.post(InputEvent.InteractionKeyMappingTriggered.ataque(InteractionHand.MAIN_HAND));
        if (!e.isCanceled()) return;
        if (e.shouldSwingHand()) player.swing(InteractionHand.MAIN_HAND);
        ci.cancel();
    }

    @Inject(method = "startUseItem", at = @At("HEAD"), cancellable = true)
    private void copperslug$uso(CallbackInfo ci) {
        if (gameMode == null || gameMode.isDestroying() || player == null || player.isHandsBusy()) return;
        for (InteractionHand h : InteractionHand.values()) {
            var e = Bus.post(InputEvent.InteractionKeyMappingTriggered.uso(h));
            if (e.isCanceled()) {
                rightClickDelay = 4;
                if (e.shouldSwingHand()) player.swing(h);
                ci.cancel();
                return;
            }
            if (!player.getItemInHand(h).isEmpty()) return;   // vanilla usará esa mano
        }
    }
}

package com.copperslug.fabric.mixin;

import com.copperslug.fabric.cliente.PosesFabric;
import com.copperslug.plataforma.Extensiones;
import com.copperslug.shim.client.event.RenderPlayerEvent;
import com.copperslug.shim.eventbus.api.Bus;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.player.PlayerRenderer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(PlayerRenderer.class)
public abstract class PlayerRendererMixin {
    /** IClientItemExtensions.getArmPose de las armas. */
    @Inject(method = "getArmPose", at = @At("HEAD"), cancellable = true)
    private static void copperslug$pose(AbstractClientPlayer p, InteractionHand h, CallbackInfoReturnable<HumanoidModel.ArmPose> cir) {
        ItemStack s = p.getItemInHand(h);
        HumanoidArm brazo = h == InteractionHand.MAIN_HAND ? p.getMainArm() : p.getMainArm().getOpposite();
        var x = s.isEmpty() ? null : Extensiones.de(s.getItem());
        HumanoidModel.ArmPose pose = x == null ? null : x.getArmPose(p, h, s);
        PosesFabric.apuntar(p, brazo, pose);
        if (pose != null) cir.setReturnValue(pose);
    }

    /** El RenderPlayerEvent.Pre de Forge: con las poses ya puestas y antes de dibujar. */
    @Inject(method = "render(Lnet/minecraft/client/player/AbstractClientPlayer;FFLcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;I)V",
            at = @At(value = "INVOKE", target = "Lnet/minecraft/client/renderer/entity/LivingEntityRenderer;render(Lnet/minecraft/world/entity/LivingEntity;FFLcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;I)V"),
            cancellable = true)
    private void copperslug$pre(AbstractClientPlayer p, float yaw, float pt, PoseStack ps, MultiBufferSource buf, int luz, CallbackInfo ci) {
        var e = Bus.post(new RenderPlayerEvent.Pre(p, (PlayerRenderer) (Object) this, pt, ps, buf, luz));
        if (e.isCanceled()) ci.cancel();
    }
}

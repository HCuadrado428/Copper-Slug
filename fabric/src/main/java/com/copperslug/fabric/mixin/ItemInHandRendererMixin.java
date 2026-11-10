package com.copperslug.fabric.mixin;

import com.copperslug.plataforma.Extensiones;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.client.renderer.ItemInHandRenderer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** IClientItemExtensions.applyForgeHandTransform: donde lo llama Forge (recién empezada la pose de la mano). */
@Mixin(ItemInHandRenderer.class)
public abstract class ItemInHandRendererMixin {
    @Shadow
    public abstract void renderItem(net.minecraft.world.entity.LivingEntity e, ItemStack s, ItemDisplayContext ctx, boolean izq, PoseStack ps,
                                    MultiBufferSource buf, int luz);

    @Inject(method = "renderArmWithItem", at = @At(value = "INVOKE", target = "Lcom/mojang/blaze3d/vertex/PoseStack;pushPose()V", shift = At.Shift.AFTER, ordinal = 0),
            cancellable = true)
    private void copperslug$mano(AbstractClientPlayer p, float pt, float pitch, InteractionHand h, float golpe, ItemStack s, float equipar, PoseStack ps,
                                 MultiBufferSource buf, int luz, CallbackInfo ci) {
        if (s.isEmpty() || s.is(Items.FILLED_MAP) || s.is(Items.CROSSBOW)) return;
        var x = Extensiones.de(s.getItem());
        if (x == null) return;
        HumanoidArm brazo = h == InteractionHand.MAIN_HAND ? p.getMainArm() : p.getMainArm().getOpposite();
        if (!x.applyForgeHandTransform(ps, Minecraft.getInstance().player, brazo, s, pt, equipar, golpe)) return;
        boolean der = brazo == HumanoidArm.RIGHT;
        renderItem(p, s, der ? ItemDisplayContext.FIRST_PERSON_RIGHT_HAND : ItemDisplayContext.FIRST_PERSON_LEFT_HAND, !der, ps, buf, luz);
        ps.popPose();
        ci.cancel();
    }
}

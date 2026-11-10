package com.copperslug.fabric.mixin;

import com.copperslug.fabric.cliente.ModelosSeparados;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.ItemRenderer;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Los modelos forge:separate_transforms de las armas: en el inventario, el plano; en todo lo demás, el 3D. */
@Mixin(ItemRenderer.class)
public abstract class ItemRendererMixin {
    @Shadow
    public abstract void render(ItemStack s, ItemDisplayContext ctx, boolean izq, PoseStack ps, MultiBufferSource buf, int luz, int overlay, BakedModel m);

    @Inject(method = "render", at = @At("HEAD"), cancellable = true)
    private void copperslug$separado(ItemStack s, ItemDisplayContext ctx, boolean izq, PoseStack ps, MultiBufferSource buf, int luz, int overlay,
                                     BakedModel m, CallbackInfo ci) {
        if (m instanceof ModelosSeparados.Separado sep) {
            render(s, ctx, izq, ps, buf, luz, overlay, sep.para(ctx));
            ci.cancel();
        }
    }
}

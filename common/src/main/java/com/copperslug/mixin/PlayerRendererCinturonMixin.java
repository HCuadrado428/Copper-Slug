package com.copperslug.mixin;

import com.copperslug.client.armasfuego.cinturon.CinturonCapa;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.LivingEntityRenderer;
import net.minecraft.client.renderer.entity.player.PlayerRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Añade la capa del cinturón (cartuchera y funda) al jugador, en Forge y en Fabric por igual. */
@Mixin(PlayerRenderer.class)
public abstract class PlayerRendererCinturonMixin extends LivingEntityRenderer<AbstractClientPlayer, PlayerModel<AbstractClientPlayer>> {
    private PlayerRendererCinturonMixin(EntityRendererProvider.Context c, PlayerModel<AbstractClientPlayer> m, float s) {
        super(c, m, s);
    }

    @Inject(method = "<init>", at = @At("TAIL"))
    private void copperslug$cinturon(EntityRendererProvider.Context c, boolean fino, CallbackInfo ci) {
        addLayer(new CinturonCapa(this));
    }
}

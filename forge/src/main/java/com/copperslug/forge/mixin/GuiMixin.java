package com.copperslug.forge.mixin;

import com.copperslug.shim.client.gui.overlay.ForgeGui;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Gui;
import net.minecraft.client.gui.GuiGraphics;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Las capas del HUD de las armas, al final del HUD vanilla (Forge 52 no tiene evento para registrarlas). */
@Mixin(Gui.class)
public class GuiMixin {
    @Inject(method = "render", at = @At("TAIL"))
    private void copperslug$capas(GuiGraphics g, DeltaTracker dt, CallbackInfo ci) {
        if (Minecraft.getInstance().options.hideGui) return;
        float pt = dt.getGameTimeDeltaPartialTick(false);
        for (var c : com.copperslug.shim.client.event.RegisterGuiOverlaysEvent.CAPAS)
            c.capa().render(ForgeGui.I, g, pt, g.guiWidth(), g.guiHeight());
    }
}

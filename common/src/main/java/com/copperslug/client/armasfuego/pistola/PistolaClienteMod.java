package com.copperslug.client.armasfuego.pistola;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.pistola.Tambor;
import com.copperslug.registry.ModEntities;
import com.copperslug.registry.ModItems;
import com.copperslug.shim.ItemProperties;
import net.minecraft.resources.ResourceLocation;
import com.copperslug.shim.api.distmarker.Dist;
import com.copperslug.shim.client.event.EntityRenderersEvent;
import com.copperslug.shim.client.event.RegisterGuiOverlaysEvent;
import com.copperslug.shim.client.gui.overlay.VanillaGuiOverlay;
import com.copperslug.shim.eventbus.api.SubscribeEvent;
import com.copperslug.shim.fml.common.Mod;
import com.copperslug.shim.fml.event.lifecycle.FMLClientSetupEvent;

/** Registro del cliente (bus del mod) del revólver: texturas según el óxido, el tambor del HUD y la bengala. */
@Mod.EventBusSubscriber(modid = CopperSlug.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class PistolaClienteMod {
    private PistolaClienteMod() {}

    @SubscribeEvent
    public static void setup(FMLClientSetupEvent e) {
        e.enqueueWork(() -> {
            PistolaCliente.init();
            com.copperslug.client.armasfuego.comun.Apuntado.init();
            ItemProperties.register(ModItems.REVOLVER.get(), new ResourceLocation(CopperSlug.MOD_ID, "oxido"),
                    (s, l, ent, seed) -> Tambor.oxido(s) / 4F);
        });
    }

    @SubscribeEvent
    public static void overlays(RegisterGuiOverlaysEvent e) {
        e.registerAbove(VanillaGuiOverlay.CROSSHAIR.id(), "revolver_tambor", PistolaCliente::hud);
    }

    @SubscribeEvent
    public static void renderers(EntityRenderersEvent.RegisterRenderers e) {
        e.registerEntityRenderer(ModEntities.REVOLVER_BENGALA.get(), BengalaRenderer::new);
    }
}

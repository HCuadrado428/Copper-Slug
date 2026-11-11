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
            ItemProperties.register(ModItems.REVOLVER.get(), net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "oxido"),
                    (s, l, ent, seed) -> Tambor.oxido(s) / 4F);
            // las recámaras cargadas, en su sitio: máscara de 6 bits (bit k = la recámara k desde la que toca). El modelo
            // 3D enseña por detrás un agujero por recámara y el culote de latón de las cargadas (generar_tambor.py).
            // Con el tambor girado (ruleta rusa) no se gira con la que toca, para no delatarla.
            ItemProperties.register(ModItems.REVOLVER.get(), net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "recamaras"), (s, l, ent, seed) -> {
                int[] r = Tambor.recamaras(s);
                int pos = Tambor.girado(s) ? 0 : Tambor.pos(s), mascara = 0;
                for (int k = 0; k < Tambor.N; k++) if (r[(pos + k) % Tambor.N] != 0) mascara |= 1 << k;
                return (float) mascara;
            });
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

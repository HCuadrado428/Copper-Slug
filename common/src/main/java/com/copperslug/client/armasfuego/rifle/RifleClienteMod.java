package com.copperslug.client.armasfuego.rifle;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.rifle.Rifle;
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

/** Registro del cliente (bus del mod) del rifle de catalejo. */
@Mod.EventBusSubscriber(modid = CopperSlug.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class RifleClienteMod {
    private RifleClienteMod() {}

    @SubscribeEvent
    public static void setup(FMLClientSetupEvent e) {
        e.enqueueWork(() -> {
            // óxido del cobre (0, 1/3, 2/3, 1: las propiedades van de 0 a 1) y cerrojo abierto (mientras se acciona)
            ItemProperties.register(ModItems.RIFLE.get(), new ResourceLocation(CopperSlug.MOD_ID, "oxido"), (s, l, en, seed) -> Rifle.oxido(s) / 3F);
            ItemProperties.register(ModItems.RIFLE.get(), new ResourceLocation(CopperSlug.MOD_ID, "cerrojo"),
                    (s, l, en, seed) -> Rifle.cerrojo(s) > 2 ? 1F : 0F);
        });
    }

    @SubscribeEvent
    public static void renderers(EntityRenderersEvent.RegisterRenderers e) {
        e.registerEntityRenderer(ModEntities.BALA_RIFLE.get(), BalaRifleRenderer::new);
        e.registerEntityRenderer(ModEntities.GANCHO_TIROLINA.get(), GanchoTirolinaRenderer::new);
    }

    @SubscribeEvent
    public static void overlays(RegisterGuiOverlaysEvent e) {
        e.registerAbove(VanillaGuiOverlay.SPYGLASS.id(), "rifle_telemetro", RifleHud::dibujar);
    }
}

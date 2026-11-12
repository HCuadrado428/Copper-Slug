package com.copperslug.client.armasfuego.comun;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.comun.ArmaFuegoItem;
import com.copperslug.armasfuego.comun.ArmasFuegoRegistro;
import com.copperslug.armasfuego.comun.EquilibrioArmas;
import com.copperslug.armasfuego.oeste.CanonManoItem;
import com.copperslug.armasfuego.oeste.DerringerItem;
import com.copperslug.armasfuego.oeste.WinchesterItem;
import com.copperslug.armasfuego.rifle.Pintura;
import com.copperslug.registry.ModEntities;
import com.copperslug.registry.ModItems;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.entity.ThrownItemRenderer;
import com.copperslug.shim.ItemProperties;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import com.copperslug.shim.api.distmarker.Dist;
import com.copperslug.shim.client.event.EntityRenderersEvent;
import com.copperslug.shim.client.event.ModelEvent;
import com.copperslug.shim.client.event.RegisterColorHandlersEvent;
import com.copperslug.shim.client.event.RegisterGuiOverlaysEvent;
import com.copperslug.shim.client.event.RegisterParticleProvidersEvent;
import com.copperslug.shim.client.gui.overlay.VanillaGuiOverlay;
import com.copperslug.shim.eventbus.api.SubscribeEvent;
import com.copperslug.shim.fml.common.Mod;
import com.copperslug.shim.fml.event.lifecycle.FMLClientSetupEvent;

/** Registro del cliente (bus del mod) de las armas de fuego de la segunda tanda y de lo nuevo de las tres primeras. */
@Mod.EventBusSubscriber(modid = CopperSlug.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class FuegoClienteMod {
    private FuegoClienteMod() {}

    private static ResourceLocation rl(String n) {
        return new ResourceLocation(CopperSlug.MOD_ID, n);
    }

    private static Level nivel(ClientLevel l, LivingEntity e) {
        return l != null ? l : e != null ? e.level() : Minecraft.getInstance().level;
    }

    private static boolean recargando(LivingEntity e, ItemStack s) {
        return e != null && e.isUsingItem() && e.getUseItem() == s && ArmaFuegoItem.modo(s) == ArmaFuegoItem.MODO_RECARGA;
    }

    @SubscribeEvent
    public static void setup(FMLClientSetupEvent e) {
        e.enqueueWork(() -> {
            // Winchester: la palanca abierta en la primera mitad del ciclo
            ItemProperties.register(ModItems.WINCHESTER.get(), rl("palanca"), (s, l, en, seed) -> {
                Level lv = nivel(l, en);
                float d = ArmaFuegoItem.desdeDisparo(s, lv, 0);
                int pal = en instanceof Player p ? WinchesterItem.palanca(p, s) : EquilibrioArmas.winchesterPalanca();
                return d >= 1 && d < pal * 0.6F ? 1F : 0F;
            });
            // Derringer: se ve en tercera persona solo justo después de disparar; abierta al recargar
            ItemProperties.register(ModItems.DERRINGER.get(), rl("visible"), (s, l, en, seed) ->
                    DerringerItem.visible(s, nivel(l, en)) || en instanceof Player pl && com.copperslug.armasfuego.comun.Apuntar.apuntando(pl) ? 1F : 0F);
            ItemProperties.register(ModItems.DERRINGER.get(), rl("abierta"), (s, l, en, seed) -> recargando(en, s) ? 1F : 0F);
            // Thompson: sin tambor durante la primera parte del cambio
            ItemProperties.register(ModItems.THOMPSON.get(), rl("sin_tambor"), (s, l, en, seed) ->
                    recargando(en, s) && en.getTicksUsingItem() < EquilibrioArmas.thompsonRecarga() * 0.6F ? 1F : 0F);
            // mosquete: la baqueta entra y sale durante la recarga (3 posiciones)
            ItemProperties.register(ModItems.MOSQUETE.get(), rl("baqueta"), (s, l, en, seed) -> {
                if (!recargando(en, s)) return 0F;
                float f = en.getTicksUsingItem() / (float) Math.max(1, EquilibrioArmas.mosqueteRecarga());
                if (f < 0.25F) return 0F;
                int k = (int) (en.getTicksUsingItem() / 4) % 4;   // arriba y abajo
                int[] fr = {1, 2, 3, 2};
                return fr[k] / 3F;
            });
            // el cobre de las seis nuevas (0, 0,25, 0,5, 0,75, como el revólver)
            for (var it : java.util.List.of(ModItems.GATLING, ModItems.WINCHESTER, ModItems.DERRINGER, ModItems.THOMPSON, ModItems.MOSQUETE, ModItems.CANON_MANO, ModItems.CERBATANA, ModItems.LANZALLAMAS))
                ItemProperties.register(it.get(), rl("oxido"), (s, l, en, seed) -> com.copperslug.armasfuego.comun.Cobre.oxido(s) / 4F);
            // mosquete: la hoja de la bayoneta (0 sin, 1 madera .. 6 netherita)
            ItemProperties.register(ModItems.MOSQUETE.get(), rl("bayoneta"), (s, l, en, seed) -> com.copperslug.armasfuego.oeste.MosqueteItem.material(s) / 10F);
            // cañón: la mecha encendida
            ItemProperties.register(ModItems.CANON_MANO.get(), rl("mecha"), (s, l, en, seed) -> CanonManoItem.mecha(s) >= 0 ? 1F : 0F);
            // revólver: el tambor abierto un momento al meter cada bala
            ItemProperties.register(ModItems.REVOLVER.get(), rl("abierto"), (s, l, en, seed) -> {
                Level lv = nivel(l, en);
                if (lv == null || !s.hasTag()) return 0F;
                long t = lv.getGameTime() - s.getTag().getLong(com.copperslug.armasfuego.pistola.Revolver.CARGA_T);
                return t >= 0 && t < 12 ? 1F : 0F;
            });
        });
    }

    @SubscribeEvent
    public static void particulas(RegisterParticleProvidersEvent e) {
        e.registerSpriteSet(ArmasFuegoRegistro.FOGONAZO.get(), FuegoParticulas.FogonazoProv::new);
        e.registerSpriteSet(ArmasFuegoRegistro.CASQUILLO.get(), FuegoParticulas.CasquilloProv::new);
        e.registerSpriteSet(ArmasFuegoRegistro.TRAZO.get(), s -> new FuegoParticulas.TrazoProv(s, 1.0F, 0.86F, 0.45F));
        e.registerSpriteSet(ArmasFuegoRegistro.TRAZO_FUEGO.get(), s -> new FuegoParticulas.TrazoProv(s, 1.0F, 0.45F, 0.15F));
        e.registerSpriteSet(ArmasFuegoRegistro.TRAZO_FRIO.get(), s -> new FuegoParticulas.TrazoProv(s, 0.7F, 0.9F, 1.0F));
        e.registerSpriteSet(ArmasFuegoRegistro.TRAZO_VERDE.get(), s -> new FuegoParticulas.TrazoProv(s, 0.5F, 1.0F, 0.45F));
    }

    @SubscribeEvent
    public static void renderers(EntityRenderersEvent.RegisterRenderers e) {
        e.registerEntityRenderer(ModEntities.GATLING.get(), GatlingRenderer::new);
        e.registerEntityRenderer(ModEntities.BOLA_CANON.get(), BolaCanonRenderer::new);
    }

    @SubscribeEvent
    public static void modelos(ModelEvent.RegisterAdditional e) {
        for (ResourceLocation r : GatlingRenderer.TODOS) e.register(r);
        for (ResourceLocation r : GatlingRenderer.CUERPOS) e.register(r);
        for (ResourceLocation r : com.copperslug.client.armasfuego.pistola.RevolverTambor.MODELOS) e.register(r);
        for (ResourceLocation r : AccesoriosVisibles.MODELOS) e.register(r);
    }

    @SubscribeEvent
    public static void colores(RegisterColorHandlersEvent.Item e) {
        e.register((s, capa) -> capa == 1 ? Pintura.rgb(Pintura.color(s)) : 0xFFFFFFFF, ModItems.BALA_PINTURA.get());
    }

    @SubscribeEvent
    public static void teclas(com.copperslug.shim.client.event.RegisterKeyMappingsEvent e) {
        e.register(FuegoCliente.MANGA);
        e.register(Inspeccion.TECLA);
    }

    @SubscribeEvent
    public static void overlays(RegisterGuiOverlaysEvent e) {
        e.registerAbove(VanillaGuiOverlay.CROSSHAIR.id(), "armafuego_balas", FuegoCliente::hud);
        e.registerAbove(VanillaGuiOverlay.CROSSHAIR.id(), "armafuego_mira", Apuntado::hud);
    }
}

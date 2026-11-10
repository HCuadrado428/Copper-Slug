package com.copperslug.neoforge.cliente;

import com.copperslug.CopperSlug;
import com.copperslug.client.ClienteInicio;
import com.copperslug.plataforma.Extensiones;
import com.copperslug.shim.client.gui.overlay.ForgeGui;
import com.copperslug.shim.eventbus.api.Bus;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.gui.LayeredDraw;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.resources.model.ModelResourceLocation;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.event.ClientPlayerNetworkEvent;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.neoforged.neoforge.client.event.InputEvent;
import net.neoforged.neoforge.client.event.ModelEvent;
import net.neoforged.neoforge.client.event.RegisterColorHandlersEvent;
import net.neoforged.neoforge.client.event.RegisterGuiLayersEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.client.event.RegisterParticleProvidersEvent;
import net.neoforged.neoforge.client.event.RenderFrameEvent;
import net.neoforged.neoforge.client.event.RenderLevelStageEvent;
import net.neoforged.neoforge.client.event.RenderPlayerEvent;
import net.neoforged.neoforge.client.event.ViewportEvent;
import net.neoforged.neoforge.client.extensions.common.IClientItemExtensions;
import net.neoforged.neoforge.client.extensions.common.RegisterClientExtensionsEvent;
import net.neoforged.neoforge.client.gui.VanillaGuiLayers;
import net.neoforged.neoforge.common.NeoForge;

import java.util.Map;

/** El cliente en NeoForge 1.21.1: pasa los eventos de NeoForge a los del shim y engancha las extensiones de las armas. */
public final class ClienteNeoForge {
    private ClienteNeoForge() {}

    private static final Map<RenderLevelStageEvent.Stage, com.copperslug.shim.client.event.RenderLevelStageEvent.Stage> ETAPAS = Map.of(
            RenderLevelStageEvent.Stage.AFTER_SKY, com.copperslug.shim.client.event.RenderLevelStageEvent.Stage.AFTER_SKY,
            RenderLevelStageEvent.Stage.AFTER_SOLID_BLOCKS, com.copperslug.shim.client.event.RenderLevelStageEvent.Stage.AFTER_SOLID_BLOCKS,
            RenderLevelStageEvent.Stage.AFTER_ENTITIES, com.copperslug.shim.client.event.RenderLevelStageEvent.Stage.AFTER_ENTITIES,
            RenderLevelStageEvent.Stage.AFTER_BLOCK_ENTITIES, com.copperslug.shim.client.event.RenderLevelStageEvent.Stage.AFTER_BLOCK_ENTITIES,
            RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS, com.copperslug.shim.client.event.RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS,
            RenderLevelStageEvent.Stage.AFTER_PARTICLES, com.copperslug.shim.client.event.RenderLevelStageEvent.Stage.AFTER_PARTICLES,
            RenderLevelStageEvent.Stage.AFTER_WEATHER, com.copperslug.shim.client.event.RenderLevelStageEvent.Stage.AFTER_WEATHER,
            RenderLevelStageEvent.Stage.AFTER_LEVEL, com.copperslug.shim.client.event.RenderLevelStageEvent.Stage.AFTER_LEVEL);

    public static void iniciar(IEventBus mod) {
        ClienteInicio.iniciar();

        // ---- bus del mod
        mod.addListener((FMLClientSetupEvent e) -> e.enqueueWork(() -> Bus.post(new com.copperslug.shim.fml.event.lifecycle.FMLClientSetupEvent())));
        mod.addListener(ClienteNeoForge::extensiones);
        mod.addListener((EntityRenderersEvent.RegisterRenderers e) ->
                Bus.post(new com.copperslug.shim.client.event.EntityRenderersEvent.RegisterRenderers((t, p) -> registrarRender(e, t, p))));
        mod.addListener((RegisterParticleProvidersEvent e) ->
                Bus.post(new com.copperslug.shim.client.event.RegisterParticleProvidersEvent(e::registerSpriteSet)));
        mod.addListener((ModelEvent.RegisterAdditional e) ->
                Bus.post(new com.copperslug.shim.client.event.ModelEvent.RegisterAdditional(rl -> e.register(ModelResourceLocation.standalone(rl)))));
        // los modelos de las armas usan el cargador de Forge (forge:separate_transforms): en NeoForge 1.21 es el mismo con otro nombre
        mod.addListener((ModelEvent.RegisterGeometryLoaders e) -> e.register(ResourceLocation.fromNamespaceAndPath("forge", "separate_transforms"),
                net.neoforged.neoforge.client.model.SeparateTransformsModel.Loader.INSTANCE));
        mod.addListener((RegisterColorHandlersEvent.Item e) -> Bus.post(new com.copperslug.shim.client.event.RegisterColorHandlersEvent.Item(e::register)));
        mod.addListener((RegisterKeyMappingsEvent e) -> Bus.post(new com.copperslug.shim.client.event.RegisterKeyMappingsEvent(e::register)));
        mod.addListener((RegisterGuiLayersEvent e) -> {
            for (var c : com.copperslug.shim.client.event.RegisterGuiOverlaysEvent.CAPAS) {
                ResourceLocation id = ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, c.id());
                LayeredDraw.Layer capa = (g, dt) -> c.capa().render(ForgeGui.I, g, dt.getGameTimeDeltaPartialTick(false), g.guiWidth(), g.guiHeight());
                if (c.encima() != null) e.registerAbove(capaVanilla(c.encima()), id, capa);
                else e.registerAboveAll(id, capa);
            }
        });

        // ---- bus de NeoForge
        var f = NeoForge.EVENT_BUS;
        f.addListener((ClientTickEvent.Pre e) -> Bus.post(new com.copperslug.shim.event.TickEvent.ClientTickEvent(com.copperslug.shim.event.TickEvent.Phase.START)));
        f.addListener((ClientTickEvent.Post e) -> Bus.post(new com.copperslug.shim.event.TickEvent.ClientTickEvent(com.copperslug.shim.event.TickEvent.Phase.END)));
        f.addListener((RenderFrameEvent.Pre e) -> Bus.post(new com.copperslug.shim.event.TickEvent.RenderTickEvent(com.copperslug.shim.event.TickEvent.Phase.START,
                e.getPartialTick().getGameTimeDeltaPartialTick(false))));
        f.addListener((RenderFrameEvent.Post e) -> Bus.post(new com.copperslug.shim.event.TickEvent.RenderTickEvent(com.copperslug.shim.event.TickEvent.Phase.END,
                e.getPartialTick().getGameTimeDeltaPartialTick(false))));
        f.addListener((InputEvent.InteractionKeyMappingTriggered e) -> {
            int b = e.isAttack() ? 0 : e.isUseItem() ? 1 : 2;
            var s = Bus.post(new com.copperslug.shim.client.event.InputEvent.InteractionKeyMappingTriggered(b, e.getKeyMapping(), e.getHand()));
            if (s.isCanceled()) {
                e.setCanceled(true);
                e.setSwingHand(s.shouldSwingHand());
            }
        });
        f.addListener((RenderLevelStageEvent e) -> {
            var et = ETAPAS.get(e.getStage());
            if (et != null) Bus.post(new com.copperslug.shim.client.event.RenderLevelStageEvent(et, e.getLevelRenderer(), e.getPoseStack(),
                    e.getProjectionMatrix(), e.getRenderTick(), e.getPartialTick().getGameTimeDeltaPartialTick(false), e.getCamera()));
        });
        f.addListener((ViewportEvent.ComputeCameraAngles e) -> {
            var s = Bus.post(new com.copperslug.shim.client.event.ViewportEvent.ComputeCameraAngles(e.getCamera(), e.getPartialTick(), e.getYaw(), e.getPitch(), e.getRoll()));
            e.setYaw(s.getYaw());
            e.setPitch(s.getPitch());
            e.setRoll(s.getRoll());
        });
        f.addListener((RenderPlayerEvent.Pre e) -> {
            var s = Bus.post(new com.copperslug.shim.client.event.RenderPlayerEvent.Pre(e.getEntity(), e.getRenderer(), e.getPartialTick(),
                    e.getPoseStack(), e.getMultiBufferSource(), e.getPackedLight()));
            if (s.isCanceled()) e.setCanceled(true);
        });
        f.addListener((ClientPlayerNetworkEvent.LoggingOut e) -> Bus.post(new com.copperslug.shim.client.event.ClientPlayerNetworkEvent.LoggingOut()));
        f.addListener((ClientPlayerNetworkEvent.LoggingIn e) -> Bus.post(new com.copperslug.shim.client.event.ClientPlayerNetworkEvent.LoggingIn()));
    }

    /** En 1.21 el catalejo va dentro de la capa de los efectos de cámara. */
    private static ResourceLocation capaVanilla(ResourceLocation id) {
        return id.getPath().equals("spyglass") ? VanillaGuiLayers.CAMERA_OVERLAYS : id;
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static void registrarRender(EntityRenderersEvent.RegisterRenderers e, net.minecraft.world.entity.EntityType t,
                                        net.minecraft.client.renderer.entity.EntityRendererProvider p) {
        e.registerEntityRenderer(t, p);
    }

    /** A cada arma con extensiones de cliente se le ponen como extensiones de cliente de NeoForge. */
    private static void extensiones(RegisterClientExtensionsEvent ev) {
        for (var e : BuiltInRegistries.ITEM.entrySet()) {
            if (!CopperSlug.MOD_ID.equals(e.getKey().location().getNamespace())) continue;
            var x = Extensiones.de(e.getValue());
            if (x == null) continue;
            ev.registerItem(new IClientItemExtensions() {
                @Override
                public HumanoidModel.ArmPose getArmPose(LivingEntity en, InteractionHand h, ItemStack s) {
                    return x.getArmPose(en, h, s);
                }

                @Override
                public boolean applyForgeHandTransform(PoseStack ps, LocalPlayer p, HumanoidArm brazo, ItemStack s, float pt, float equipar, float golpe) {
                    return x.applyForgeHandTransform(ps, p, brazo, s, pt, equipar, golpe);
                }
            }, e.getValue());
        }
    }
}

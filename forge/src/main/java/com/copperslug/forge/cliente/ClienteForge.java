package com.copperslug.forge.cliente;

import com.copperslug.CopperSlug;
import com.copperslug.client.ClienteInicio;
import com.copperslug.forge.mixin.ItemRenderAccessor;
import com.copperslug.plataforma.Extensiones;
import com.copperslug.shim.client.gui.overlay.ForgeGui;
import com.copperslug.shim.eventbus.api.Bus;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.client.event.ClientPlayerNetworkEvent;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.client.event.InputEvent;
import net.minecraftforge.client.event.ModelEvent;
import net.minecraftforge.client.event.RegisterColorHandlersEvent;
import net.minecraftforge.client.event.RegisterGuiOverlaysEvent;
import net.minecraftforge.client.event.RegisterKeyMappingsEvent;
import net.minecraftforge.client.event.RegisterParticleProvidersEvent;
import net.minecraftforge.client.event.RenderLevelStageEvent;
import net.minecraftforge.client.event.RenderPlayerEvent;
import net.minecraftforge.client.event.ViewportEvent;
import net.minecraftforge.client.extensions.common.IClientItemExtensions;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;

import java.util.Map;

/** El cliente en Forge: pasa los eventos de Forge a los del shim y engancha las extensiones de las armas. */
public final class ClienteForge {
    private ClienteForge() {}

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
        mod.addListener((FMLClientSetupEvent e) -> {
            e.enqueueWork(ClienteForge::extensiones);
            Bus.post(new com.copperslug.shim.fml.event.lifecycle.FMLClientSetupEvent());
        });
        mod.addListener((EntityRenderersEvent.RegisterRenderers e) ->
                Bus.post(new com.copperslug.shim.client.event.EntityRenderersEvent.RegisterRenderers((t, p) -> registrarRender(e, t, p))));
        mod.addListener((RegisterParticleProvidersEvent e) ->
                Bus.post(new com.copperslug.shim.client.event.RegisterParticleProvidersEvent(e::registerSpriteSet)));
        mod.addListener((ModelEvent.RegisterAdditional e) -> Bus.post(new com.copperslug.shim.client.event.ModelEvent.RegisterAdditional(e::register)));
        mod.addListener((RegisterColorHandlersEvent.Item e) -> Bus.post(new com.copperslug.shim.client.event.RegisterColorHandlersEvent.Item(e::register)));
        mod.addListener((RegisterKeyMappingsEvent e) -> Bus.post(new com.copperslug.shim.client.event.RegisterKeyMappingsEvent(e::register)));
        mod.addListener((RegisterGuiOverlaysEvent e) -> {
            for (var c : com.copperslug.shim.client.event.RegisterGuiOverlaysEvent.CAPAS) {
                if (c.encima() != null) e.registerAbove(c.encima(), c.id(), (gui, g, pt, w, h) -> c.capa().render(ForgeGui.I, g, pt, w, h));
                else e.registerAboveAll(c.id(), (gui, g, pt, w, h) -> c.capa().render(ForgeGui.I, g, pt, w, h));
            }
        });

        // ---- bus de Forge
        var f = MinecraftForge.EVENT_BUS;
        f.addListener((TickEvent.ClientTickEvent e) -> Bus.post(new com.copperslug.shim.event.TickEvent.ClientTickEvent(fase(e.phase))));
        f.addListener((TickEvent.RenderTickEvent e) -> Bus.post(new com.copperslug.shim.event.TickEvent.RenderTickEvent(fase(e.phase), e.renderTickTime)));
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
                    e.getProjectionMatrix(), e.getRenderTick(), e.getPartialTick(), e.getCamera()));
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

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static void registrarRender(EntityRenderersEvent.RegisterRenderers e, net.minecraft.world.entity.EntityType t,
                                        net.minecraft.client.renderer.entity.EntityRendererProvider p) {
        e.registerEntityRenderer(t, p);
    }

    private static com.copperslug.shim.event.TickEvent.Phase fase(TickEvent.Phase p) {
        return p == TickEvent.Phase.START ? com.copperslug.shim.event.TickEvent.Phase.START : com.copperslug.shim.event.TickEvent.Phase.END;
    }

    /** A cada arma con extensiones de cliente se le ponen como propiedades de render de Forge. */
    private static void extensiones() {
        for (var e : BuiltInRegistries.ITEM.entrySet()) {
            if (!CopperSlug.MOD_ID.equals(e.getKey().location().getNamespace())) continue;
            var x = Extensiones.de(e.getValue());
            if (x == null) continue;
            ((ItemRenderAccessor) e.getValue()).copperslug$ponerRender(new IClientItemExtensions() {
                @Override
                public HumanoidModel.ArmPose getArmPose(LivingEntity en, InteractionHand h, ItemStack s) {
                    return x.getArmPose(en, h, s);
                }

                @Override
                public boolean applyForgeHandTransform(PoseStack ps, LocalPlayer p, HumanoidArm brazo, ItemStack s, float pt, float equipar, float golpe) {
                    return x.applyForgeHandTransform(ps, p, brazo, s, pt, equipar, golpe);
                }
            });
        }
    }
}

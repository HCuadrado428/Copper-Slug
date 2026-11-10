package com.copperslug.fabric.cliente;

import com.copperslug.client.ClienteInicio;
import com.copperslug.shim.client.event.RenderLevelStageEvent;
import com.copperslug.shim.event.TickEvent;
import com.copperslug.shim.eventbus.api.Bus;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.fabricmc.fabric.api.client.model.loading.v1.ModelLoadingPlugin;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayConnectionEvents;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.client.particle.v1.ParticleFactoryRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.ColorProviderRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderContext;
import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleType;
import net.minecraft.client.particle.ParticleEngine;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EntityType;

import java.util.ArrayList;
import java.util.List;

/** El cliente en Fabric: registra lo del cliente con Fabric API y pasa sus eventos a los del shim. */
public class ClienteFabric implements ClientModInitializer {
    @Override
    @SuppressWarnings({"unchecked", "rawtypes"})
    public void onInitializeClient() {
        ClienteInicio.iniciar();
        for (var d : com.copperslug.fabric.PlataformaFabric.AL_CLIENTE) recibir(d);

        Bus.post(new com.copperslug.shim.client.event.RegisterKeyMappingsEvent(KeyBindingHelper::registerKeyBinding));
        Bus.post(new com.copperslug.shim.client.event.RegisterParticleProvidersEvent(new com.copperslug.shim.client.event.RegisterParticleProvidersEvent.Registrador() {
            @Override
            public <T extends ParticleOptions> void conSprites(ParticleType<T> tipo, ParticleEngine.SpriteParticleRegistration<T> prov) {
                ParticleFactoryRegistry.getInstance().register(tipo, prov::create);
            }
        }));
        Bus.post(new com.copperslug.shim.client.event.EntityRenderersEvent.RegisterRenderers((t, p) ->
                EntityRendererRegistry.register((EntityType) t, (EntityRendererProvider) p)));
        List<ResourceLocation> modelos = new ArrayList<>();
        Bus.post(new com.copperslug.shim.client.event.ModelEvent.RegisterAdditional(modelos::add));
        ModelLoadingPlugin.register(ctx -> ctx.addModels(modelos));
        Bus.post(new com.copperslug.shim.client.event.RegisterColorHandlersEvent.Item((c, items) -> ColorProviderRegistry.ITEM.register(c, items)));
        Bus.post(new com.copperslug.shim.fml.event.lifecycle.FMLClientSetupEvent());

        ClientTickEvents.START_CLIENT_TICK.register(mc -> Bus.post(new TickEvent.ClientTickEvent(TickEvent.Phase.START)));
        ClientTickEvents.END_CLIENT_TICK.register(mc -> Bus.post(new TickEvent.ClientTickEvent(TickEvent.Phase.END)));
        ClientTickEvents.START_WORLD_TICK.register(l -> Bus.post(new TickEvent.LevelTickEvent(TickEvent.LogicalSide.CLIENT, TickEvent.Phase.START, l)));
        ClientTickEvents.END_WORLD_TICK.register(l -> Bus.post(new TickEvent.LevelTickEvent(TickEvent.LogicalSide.CLIENT, TickEvent.Phase.END, l)));
        WorldRenderEvents.AFTER_ENTITIES.register(c -> etapa(RenderLevelStageEvent.Stage.AFTER_ENTITIES, c));
        WorldRenderEvents.AFTER_TRANSLUCENT.register(c -> {
            etapa(RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS, c);
            etapa(RenderLevelStageEvent.Stage.AFTER_PARTICLES, c);
        });
        WorldRenderEvents.LAST.register(c -> etapa(RenderLevelStageEvent.Stage.AFTER_LEVEL, c));
        HudRenderCallback.EVENT.register(ClienteInicio::dibujarHud);
        ClientPlayConnectionEvents.DISCONNECT.register((h, mc) -> Bus.post(new com.copperslug.shim.client.event.ClientPlayerNetworkEvent.LoggingOut()));
        ClientPlayConnectionEvents.JOIN.register((h, s, mc) -> Bus.post(new com.copperslug.shim.client.event.ClientPlayerNetworkEvent.LoggingIn()));
    }

    private static void etapa(RenderLevelStageEvent.Stage st, WorldRenderContext c) {
        Bus.post(new RenderLevelStageEvent(st, c.worldRenderer(), c.matrixStack(), c.projectionMatrix(), 0, c.tickDelta(), c.camera()));
    }

    private static <T> void recibir(com.copperslug.fabric.PlataformaFabric.Def<T> d) {
        ClientPlayNetworking.registerGlobalReceiver(d.id(), (mc, h, buf, sender) -> {
            T m = d.leer().apply(buf);
            mc.execute(() -> d.cliente().accept(m));
        });
    }

    public static void enviar(ResourceLocation id, FriendlyByteBuf b) {
        ClientPlayNetworking.send(id, b);
    }
}

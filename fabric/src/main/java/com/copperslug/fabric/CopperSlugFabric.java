package com.copperslug.fabric;

import com.copperslug.CopperSlug;
import com.copperslug.shim.event.TickEvent;
import com.copperslug.shim.event.entity.player.PlayerEvent;
import com.copperslug.shim.event.entity.player.PlayerInteractEvent;
import com.copperslug.shim.eventbus.api.Bus;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.entity.event.v1.ServerEntityWorldChangeEvents;
import net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.UseEntityCallback;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.world.InteractionResult;

/** Copper Slug en Fabric: pasa los eventos de Fabric API al código común. */
public class CopperSlugFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        CopperSlug.iniciar();
        BotinFabric.registrar();

        ServerTickEvents.START_SERVER_TICK.register(s -> Bus.post(new TickEvent.ServerTickEvent(TickEvent.Phase.START, s)));
        ServerTickEvents.END_SERVER_TICK.register(s -> Bus.post(new TickEvent.ServerTickEvent(TickEvent.Phase.END, s)));
        ServerTickEvents.START_WORLD_TICK.register(l -> Bus.post(new TickEvent.LevelTickEvent(TickEvent.LogicalSide.SERVER, TickEvent.Phase.START, l)));
        ServerTickEvents.END_WORLD_TICK.register(l -> Bus.post(new TickEvent.LevelTickEvent(TickEvent.LogicalSide.SERVER, TickEvent.Phase.END, l)));
        ServerPlayConnectionEvents.JOIN.register((h, sender, s) -> Bus.post(new PlayerEvent.PlayerLoggedInEvent(h.getPlayer())));
        ServerPlayConnectionEvents.DISCONNECT.register((h, s) -> Bus.post(new PlayerEvent.PlayerLoggedOutEvent(h.getPlayer())));
        ServerEntityWorldChangeEvents.AFTER_PLAYER_CHANGE_WORLD.register((p, de, a) ->
                Bus.post(new PlayerEvent.PlayerChangedDimensionEvent(p, de.dimension(), a.dimension())));
        ServerPlayerEvents.AFTER_RESPAWN.register((viejo, nuevo, vivo) -> Bus.post(new PlayerEvent.PlayerRespawnEvent(nuevo, vivo)));
        ServerLifecycleEvents.SERVER_STARTING.register(CopperSlug::servidorArrancando);
        ServerLifecycleEvents.SERVER_STOPPED.register(CopperSlug::servidorParado);
        CommandRegistrationCallback.EVENT.register((d, ctx, sel) -> Bus.post(new com.copperslug.shim.event.RegisterCommandsEvent(d, ctx)));
        UseEntityCallback.EVENT.register((p, l, mano, e, hit) -> {
            // como el EntityInteract de Forge (que va antes que el interactAt): solo sin hit (el clic normal)
            if (hit != null) return InteractionResult.PASS;
            var ev = Bus.post(new PlayerInteractEvent.EntityInteract(p, mano, e));
            return ev.isCanceled() ? ev.getCancellationResult() : InteractionResult.PASS;
        });
    }
}

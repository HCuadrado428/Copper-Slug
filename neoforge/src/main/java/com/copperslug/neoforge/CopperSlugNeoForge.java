package com.copperslug.neoforge;

import com.copperslug.CopperSlug;
import com.copperslug.shim.event.TickEvent.LogicalSide;
import com.copperslug.shim.event.TickEvent.Phase;
import com.copperslug.shim.eventbus.api.Bus;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.loading.FMLEnvironment;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.RegisterCommandsEvent;
import net.neoforged.neoforge.event.entity.living.LivingEvent;
import net.neoforged.neoforge.event.entity.player.ItemEntityPickupEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.event.server.ServerStartingEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.LevelTickEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;

/** Copper Slug en NeoForge 1.21.1: pasa los eventos de NeoForge al código común. */
@Mod(CopperSlug.MOD_ID)
public class CopperSlugNeoForge {
    public CopperSlugNeoForge(IEventBus bus, ModContainer mod) {
        PlataformaNeoForge.busMod = bus;
        BotinNeoForge.SERIALIZERS.register(bus);
        bus.addListener((RegisterPayloadHandlersEvent e) -> PlataformaNeoForge.registrarPaquetes(e.registrar("1")));
        CopperSlug.iniciar();
        if (FMLEnvironment.dist.isClient()) com.copperslug.neoforge.cliente.ClienteNeoForge.iniciar(bus);

        var f = NeoForge.EVENT_BUS;
        f.addListener((ServerTickEvent.Pre e) -> Bus.post(new com.copperslug.shim.event.TickEvent.ServerTickEvent(Phase.START, e.getServer())));
        f.addListener((ServerTickEvent.Post e) -> Bus.post(new com.copperslug.shim.event.TickEvent.ServerTickEvent(Phase.END, e.getServer())));
        f.addListener((LevelTickEvent.Pre e) -> Bus.post(new com.copperslug.shim.event.TickEvent.LevelTickEvent(
                e.getLevel().isClientSide ? LogicalSide.CLIENT : LogicalSide.SERVER, Phase.START, e.getLevel())));
        f.addListener((LevelTickEvent.Post e) -> Bus.post(new com.copperslug.shim.event.TickEvent.LevelTickEvent(
                e.getLevel().isClientSide ? LogicalSide.CLIENT : LogicalSide.SERVER, Phase.END, e.getLevel())));
        f.addListener((PlayerEvent.PlayerLoggedInEvent e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerEvent.PlayerLoggedInEvent(e.getEntity())));
        f.addListener((PlayerEvent.PlayerLoggedOutEvent e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerEvent.PlayerLoggedOutEvent(e.getEntity())));
        f.addListener((PlayerEvent.PlayerChangedDimensionEvent e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerEvent.PlayerChangedDimensionEvent(
                e.getEntity(), e.getFrom(), e.getTo())));
        f.addListener((PlayerEvent.PlayerRespawnEvent e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerEvent.PlayerRespawnEvent(
                e.getEntity(), e.isEndConquered())));
        f.addListener((ItemEntityPickupEvent.Post e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerEvent.ItemPickupEvent(
                e.getPlayer(), e.getItemEntity(), e.getOriginalStack())));
        f.addListener((PlayerInteractEvent.EntityInteract e) -> {
            var s = Bus.post(new com.copperslug.shim.event.entity.player.PlayerInteractEvent.EntityInteract(e.getEntity(), e.getHand(), e.getTarget()));
            if (s.isCanceled()) {
                e.setCanceled(true);
                e.setCancellationResult(s.getCancellationResult());
            }
        });
        f.addListener((LivingEvent.LivingJumpEvent e) -> Bus.post(new com.copperslug.shim.event.entity.living.LivingEvent.LivingJumpEvent(e.getEntity())));
        f.addListener((RegisterCommandsEvent e) -> Bus.post(new com.copperslug.shim.event.RegisterCommandsEvent(e.getDispatcher(), e.getBuildContext())));
        f.addListener((ServerStartingEvent e) -> CopperSlug.servidorArrancando(e.getServer()));
        f.addListener((ServerStoppedEvent e) -> CopperSlug.servidorParado(e.getServer()));
    }
}

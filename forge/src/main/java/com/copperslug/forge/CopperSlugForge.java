package com.copperslug.forge;

import com.copperslug.CopperSlug;
import com.copperslug.shim.event.TickEvent.LogicalSide;
import com.copperslug.shim.event.TickEvent.Phase;
import com.copperslug.shim.eventbus.api.Bus;
import net.minecraft.server.level.ServerPlayer;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.RegisterCommandsEvent;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.living.LivingEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.event.server.ServerStartingEvent;
import net.minecraftforge.event.server.ServerStoppedEvent;
import net.minecraftforge.fml.DistExecutor;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

/** Copper Slug en Forge (y en NeoForge 1.20.1, que carga los mismos jars): pasa los eventos de Forge al código común. */
@Mod(CopperSlug.MOD_ID)
public class CopperSlugForge {
    public CopperSlugForge() {
        var bus = FMLJavaModLoadingContext.get().getModEventBus();
        PlataformaForge.busMod = bus;
        BotinForge.SERIALIZERS.register(bus);
        CopperSlug.iniciar();
        DistExecutor.unsafeRunWhenOn(net.minecraftforge.api.distmarker.Dist.CLIENT, () -> () -> com.copperslug.forge.cliente.ClienteForge.iniciar(bus));

        var f = MinecraftForge.EVENT_BUS;
        f.addListener((TickEvent.ServerTickEvent e) -> Bus.post(new com.copperslug.shim.event.TickEvent.ServerTickEvent(fase(e.phase), e.getServer())));
        f.addListener((TickEvent.LevelTickEvent e) -> Bus.post(new com.copperslug.shim.event.TickEvent.LevelTickEvent(
                e.side.isClient() ? LogicalSide.CLIENT : LogicalSide.SERVER, fase(e.phase), e.level)));
        f.addListener((PlayerEvent.PlayerLoggedInEvent e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerEvent.PlayerLoggedInEvent(e.getEntity())));
        f.addListener((PlayerEvent.PlayerLoggedOutEvent e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerEvent.PlayerLoggedOutEvent(e.getEntity())));
        f.addListener((PlayerEvent.PlayerChangedDimensionEvent e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerEvent.PlayerChangedDimensionEvent(
                e.getEntity(), e.getFrom(), e.getTo())));
        f.addListener((PlayerEvent.PlayerRespawnEvent e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerEvent.PlayerRespawnEvent(
                e.getEntity(), e.isEndConquered())));
        f.addListener((net.minecraftforge.event.entity.player.PlayerXpEvent.PickupXp e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerXpEvent.PickupXp(
                e.getEntity(), e.getOrb())));
        f.addListener((PlayerEvent.ItemPickupEvent e) -> Bus.post(new com.copperslug.shim.event.entity.player.PlayerEvent.ItemPickupEvent(
                e.getEntity(), e.getOriginalEntity(), e.getStack())));
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

    static Phase fase(TickEvent.Phase p) {
        return p == TickEvent.Phase.START ? Phase.START : Phase.END;
    }

    static boolean esServidor(Object o) {
        return o instanceof ServerPlayer;
    }
}

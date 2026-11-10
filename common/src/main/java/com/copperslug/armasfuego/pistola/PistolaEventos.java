package com.copperslug.armasfuego.pistola;

import com.copperslug.CopperSlug;
import net.minecraft.server.level.ServerPlayer;
import com.copperslug.shim.event.RegisterCommandsEvent;
import com.copperslug.shim.event.TickEvent;
import com.copperslug.shim.event.entity.player.PlayerEvent;
import com.copperslug.shim.eventbus.api.SubscribeEvent;
import com.copperslug.shim.fml.common.Mod;

/** Lo que el revólver necesita en cada tick del servidor (luces de bengala, balas imán, duelos) y al salir. */
@Mod.EventBusSubscriber(modid = CopperSlug.MOD_ID)
public final class PistolaEventos {
    private PistolaEventos() {}

    @SubscribeEvent
    public static void tick(TickEvent.ServerTickEvent e) {
        if (e.phase != TickEvent.Phase.END) return;
        Revolver.tickTirones(e.getServer());
        LucesTemporales.tick(e.getServer());
        Duelo.tick(e.getServer());
    }

    @SubscribeEvent
    public static void sale(PlayerEvent.PlayerLoggedOutEvent e) {
        if (e.getEntity() instanceof ServerPlayer p) {
            Duelo.salir(p);
            Revolver.olvidar(p.getUUID());
        }
    }

    /** Al cerrar el mundo (un jugador: se puede abrir otro sin reiniciar el juego) no se queda nada colgando. */
    @SubscribeEvent
    public static void para(com.copperslug.shim.event.server.ServerStoppedEvent e) {
        Duelo.limpiar();
        Revolver.limpiar();
    }

    @SubscribeEvent
    public static void comandos(RegisterCommandsEvent e) {
        Duelo.comando(e.getDispatcher());
    }
}

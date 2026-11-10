package com.copperslug.logros;

import com.copperslug.CopperSlug;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import com.copperslug.shim.server.ServerLifecycleHooks;

import javax.annotation.Nullable;
import java.util.UUID;

/**
 * Los logros de Miscelánea (pestaña propia, {@code data/copperslug/advancements}). Los que no salen con criterios de
 * vanilla usan el criterio {@code copperslug:accion}; desde cualquier sitio del código basta con
 * {@code LogrosMiscelanea.dar(jugador, "accion")}. Si el jugador no es de verdad (null, un FakePlayer, una entidad que no
 * es jugador) no hace nada, y si se llama fuera del hilo del servidor se pasa a él.
 */
public final class LogrosMiscelanea {
    private LogrosMiscelanea() {}

    @Nullable
    private static java.util.function.Supplier<net.minecraft.advancements.CriterionTrigger<?>> registrado;

    /** Al cargar el mod (antes de cerrar los registros): da de alta el criterio en el registro de criterios. */
    public static void registrar() {
        if (registrado == null) registrado = com.copperslug.plataforma.Plataforma.get().registrar(net.minecraft.core.registries.Registries.TRIGGER_TYPE, LogroTrigger.ID, () -> new LogroTrigger());
    }

    /** El jugador ha hecho {@code accion}: se cumplen los logros que la esperan. */
    public static void dar(@Nullable Entity e, String accion) {
        if (!(e instanceof ServerPlayer p) || com.copperslug.plataforma.Plataforma.get().esJugadorFalso(p) || accion == null || registrado == null) return;
        MinecraftServer s = p.server;
        if (s == null) return;
        if (!s.isSameThread()) {
            s.execute(() -> dar(p, accion));
            return;
        }
        if (p.hasDisconnected()) return;
        try {
            ((LogroTrigger) registrado.get()).trigger(p, accion);
        } catch (Throwable t) {
            CopperSlug.LOG.warn("[Logros] no se pudo dar '{}' a {}", accion, p.getGameProfile().getName(), t);
        }
    }

    /** Igual, para un jugador por su UUID (si está conectado). */
    public static void dar(@Nullable MinecraftServer s, @Nullable UUID u, String accion) {
        if (u == null) return;
        if (s == null) s = ServerLifecycleHooks.getCurrentServer();
        if (s == null) return;
        dar(s.getPlayerList().getPlayer(u), accion);
    }

    public static void dar(@Nullable UUID u, String accion) {
        dar(null, u, accion);
    }
}

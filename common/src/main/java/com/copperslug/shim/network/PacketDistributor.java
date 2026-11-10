package com.copperslug.shim.network;

import com.copperslug.shim.server.ServerLifecycleHooks;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.Level;

import java.util.List;
import java.util.function.Function;
import java.util.function.Supplier;

/** Los destinos de PacketDistributor que usan las armas. */
public final class PacketDistributor<T> {
    public static final PacketDistributor<ServerPlayer> PLAYER = new PacketDistributor<>(s -> List.of(s.get()));
    public static final PacketDistributor<ResourceKey<Level>> DIMENSION = new PacketDistributor<>(s -> {
        MinecraftServer srv = ServerLifecycleHooks.getCurrentServer();
        ServerLevel l = srv == null ? null : srv.getLevel(s.get());
        return l == null ? List.of() : List.copyOf(l.players());
    });
    public static final PacketDistributor<Void> ALL = new PacketDistributor<>(s -> {
        MinecraftServer srv = ServerLifecycleHooks.getCurrentServer();
        return srv == null ? List.of() : List.copyOf(srv.getPlayerList().getPlayers());
    });

    private final Function<Supplier<T>, List<ServerPlayer>> f;

    private PacketDistributor(Function<Supplier<T>, List<ServerPlayer>> f) {
        this.f = f;
    }

    public PacketTarget with(Supplier<T> s) {
        return new PacketTarget(() -> f.apply(s));
    }

    public PacketTarget noArg() {
        return new PacketTarget(() -> f.apply(() -> null));
    }

    public static final class PacketTarget {
        private final Supplier<List<ServerPlayer>> j;

        PacketTarget(Supplier<List<ServerPlayer>> j) {
            this.j = j;
        }

        public List<ServerPlayer> jugadores() {
            return j.get();
        }
    }
}

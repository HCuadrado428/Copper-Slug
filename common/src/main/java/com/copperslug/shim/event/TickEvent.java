package com.copperslug.shim.event;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/** Los ticks, como en Forge: cada uno con su fase (START o END). */
public class TickEvent extends Event {
    public enum Phase {START, END}

    public enum Type {LEVEL, PLAYER, CLIENT, SERVER, RENDER}

    public enum LogicalSide {
        CLIENT, SERVER;

        public boolean isClient() {
            return this == CLIENT;
        }

        public boolean isServer() {
            return this == SERVER;
        }
    }

    public final Type type;
    public final LogicalSide side;
    public final Phase phase;

    public TickEvent(Type type, LogicalSide side, Phase phase) {
        this.type = type;
        this.side = side;
        this.phase = phase;
    }

    public static class ServerTickEvent extends TickEvent {
        private final MinecraftServer server;

        public ServerTickEvent(Phase phase, MinecraftServer server) {
            super(Type.SERVER, LogicalSide.SERVER, phase);
            this.server = server;
        }

        public MinecraftServer getServer() {
            return server;
        }
    }

    public static class ClientTickEvent extends TickEvent {
        public ClientTickEvent(Phase phase) {
            super(Type.CLIENT, LogicalSide.CLIENT, phase);
        }
    }

    public static class RenderTickEvent extends TickEvent {
        public final float renderTickTime;

        public RenderTickEvent(Phase phase, float renderTickTime) {
            super(Type.RENDER, LogicalSide.CLIENT, phase);
            this.renderTickTime = renderTickTime;
        }
    }

    public static class LevelTickEvent extends TickEvent {
        public final Level level;

        public LevelTickEvent(LogicalSide side, Phase phase, Level level) {
            super(Type.LEVEL, side, phase);
            this.level = level;
        }
    }

    public static class PlayerTickEvent extends TickEvent {
        public final Player player;

        public PlayerTickEvent(Phase phase, Player player) {
            super(Type.PLAYER, player.level().isClientSide ? LogicalSide.CLIENT : LogicalSide.SERVER, phase);
            this.player = player;
        }
    }
}

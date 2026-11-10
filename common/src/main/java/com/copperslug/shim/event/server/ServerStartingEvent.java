package com.copperslug.shim.event.server;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.server.MinecraftServer;

public class ServerStartingEvent extends Event {
    private final MinecraftServer s;

    public ServerStartingEvent(MinecraftServer s) {
        this.s = s;
    }

    public MinecraftServer getServer() {
        return s;
    }
}

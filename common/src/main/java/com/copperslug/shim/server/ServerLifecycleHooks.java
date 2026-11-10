package com.copperslug.shim.server;

import net.minecraft.server.MinecraftServer;

/** El servidor en marcha (lo apuntan los cargadores al arrancar y pararlo). */
public final class ServerLifecycleHooks {
    private ServerLifecycleHooks() {}

    private static volatile MinecraftServer servidor;

    public static MinecraftServer getCurrentServer() {
        return servidor;
    }

    public static void poner(MinecraftServer s) {
        servidor = s;
    }
}

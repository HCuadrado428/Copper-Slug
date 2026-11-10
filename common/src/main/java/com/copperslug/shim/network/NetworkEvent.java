package com.copperslug.shim.network;

import net.minecraft.server.level.ServerPlayer;

/** Lo que usan los paquetes del NetworkEvent de Forge. Los paquetes ya llegan en el hilo principal. */
public final class NetworkEvent {
    private NetworkEvent() {}

    public static final class Context {
        private final ServerPlayer sender;

        public Context(ServerPlayer sender) {
            this.sender = sender;
        }

        public ServerPlayer getSender() {
            return sender;
        }

        public void enqueueWork(Runnable r) {
            r.run();
        }

        public void setPacketHandled(boolean b) {}
    }
}

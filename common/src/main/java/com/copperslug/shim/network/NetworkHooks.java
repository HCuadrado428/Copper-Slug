package com.copperslug.shim.network;

import net.minecraft.network.protocol.Packet;
import net.minecraft.network.protocol.game.ClientGamePacketListener;
import net.minecraft.network.protocol.game.ClientboundAddEntityPacket;
import net.minecraft.world.entity.Entity;

/** Las entidades de las armas no mandan datos extra al aparecer: basta el paquete vanilla. */
public final class NetworkHooks {
    private NetworkHooks() {}

    public static Packet<ClientGamePacketListener> getEntitySpawningPacket(Entity e) {
        return new ClientboundAddEntityPacket(e);
    }
}

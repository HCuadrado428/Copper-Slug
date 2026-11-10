package com.copperslug.armasfuego.oeste;

import net.minecraft.network.FriendlyByteBuf;
import com.copperslug.shim.network.NetworkEvent;

import java.util.function.Supplier;

/** Cliente → servidor: la tecla de la manga (saca de golpe la Derringer a la mano, esté donde esté en el inventario). */
public class MangaPacket {
    public MangaPacket() {}

    public MangaPacket(FriendlyByteBuf b) {}

    public void encode(FriendlyByteBuf b) {}

    public void handle(Supplier<NetworkEvent.Context> ctx) {
        var p = ctx.get().getSender();
        if (p != null) DerringerItem.sacarDeLaManga(p);
    }
}

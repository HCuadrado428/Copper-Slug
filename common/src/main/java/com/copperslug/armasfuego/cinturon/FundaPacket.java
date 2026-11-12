package com.copperslug.armasfuego.cinturon;

import net.minecraft.network.FriendlyByteBuf;
import com.copperslug.shim.network.NetworkEvent;

import java.util.function.Supplier;

/** Cliente → servidor: la tecla de la funda (enfundar o desenfundar el arma corta). */
public class FundaPacket {
    public FundaPacket() {}

    public FundaPacket(FriendlyByteBuf b) {}

    public void encode(FriendlyByteBuf b) {}

    public void handle(Supplier<NetworkEvent.Context> ctx) {
        var p = ctx.get().getSender();
        if (p != null) FundaItem.tecla(p);
    }
}

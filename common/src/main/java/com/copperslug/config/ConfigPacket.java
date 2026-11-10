package com.copperslug.config;

import com.copperslug.ConfigServidor;
import com.copperslug.shim.network.NetworkEvent;
import net.minecraft.network.FriendlyByteBuf;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Supplier;

/** Servidor → cliente: los valores de la config del servidor (los usan también el HUD y las animaciones). */
public class ConfigPacket {
    private final Map<String, String> valores;

    public ConfigPacket() {
        valores = new LinkedHashMap<>();
        for (var v : ConfigServidor.SPEC.valores.values()) valores.put(v.ruta(), v.texto());
    }

    public ConfigPacket(FriendlyByteBuf b) {
        int n = Math.min(b.readVarInt(), 1024);
        valores = new LinkedHashMap<>();
        for (int i = 0; i < n; i++) valores.put(b.readUtf(256), b.readUtf(256));
    }

    public void encode(FriendlyByteBuf b) {
        b.writeVarInt(valores.size());
        valores.forEach((k, v) -> {
            b.writeUtf(k, 256);
            b.writeUtf(v, 256);
        });
    }

    public void handle(Supplier<NetworkEvent.Context> ctx) {
        for (var v : ConfigServidor.SPEC.valores.values()) {
            String s = valores.get(v.ruta());
            if (s != null) v.leer(s);
        }
        ConfigServidor.SPEC.cargada = true;
    }
}

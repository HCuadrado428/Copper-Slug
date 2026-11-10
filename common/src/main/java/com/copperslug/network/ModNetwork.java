package com.copperslug.network;

import com.copperslug.CopperSlug;
import com.copperslug.plataforma.Plataforma;
import com.copperslug.shim.network.NetworkEvent;
import com.copperslug.shim.network.PacketDistributor;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;

import java.util.function.BiConsumer;
import java.util.function.Function;
import java.util.function.Supplier;

/**
 * Los paquetes de las armas. Cada uno va por su propio canal ({@code copperslug:<nombre>}); el código de las armas
 * los manda como en Miscelánea: {@code ModNetwork.CHANNEL.sendToServer(...)} y {@code ModNetwork.CHANNEL.send(...)}.
 */
public final class ModNetwork {
    private ModNetwork() {}

    /** Sube si cambia algún paquete (cliente y servidor tienen que llevar la misma). */
    public static final String PROTOCOLO = "1";

    public static final Canal CHANNEL = new Canal();

    public static final class Canal {
        public void sendToServer(Object msg) {
            Plataforma.get().enviarAlServidor(msg);
        }

        public void send(PacketDistributor.PacketTarget t, Object msg) {
            for (ServerPlayer p : t.jugadores()) Plataforma.get().enviarA(p, msg);
        }
    }

    public interface Manejador<T> {
        void handle(T msg, Supplier<NetworkEvent.Context> ctx);
    }

    private static <T> void alServidor(String n, Class<T> c, BiConsumer<T, FriendlyByteBuf> enc, Function<FriendlyByteBuf, T> dec, Manejador<T> h) {
        Plataforma.get().paqueteAlServidor(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, n), c, enc, dec, (m, p) -> {
            NetworkEvent.Context ctx = new NetworkEvent.Context(p);
            h.handle(m, () -> ctx);
        });
    }

    private static <T> void alCliente(String n, Class<T> c, BiConsumer<T, FriendlyByteBuf> enc, Function<FriendlyByteBuf, T> dec, Manejador<T> h) {
        Plataforma.get().paqueteAlCliente(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, n), c, enc, dec, m -> {
            NetworkEvent.Context ctx = new NetworkEvent.Context(null);
            h.handle(m, () -> ctx);
        });
    }

    public static void registrar() {
        alServidor("revolver_girar", com.copperslug.armasfuego.pistola.GirarPacket.class, com.copperslug.armasfuego.pistola.GirarPacket::encode,
                com.copperslug.armasfuego.pistola.GirarPacket::new, com.copperslug.armasfuego.pistola.GirarPacket::handle);
        alServidor("escopeta_disparar", com.copperslug.armasfuego.escopeta.DispararPresionPacket.class, com.copperslug.armasfuego.escopeta.DispararPresionPacket::encode,
                com.copperslug.armasfuego.escopeta.DispararPresionPacket::new, com.copperslug.armasfuego.escopeta.DispararPresionPacket::handle);
        alServidor("rifle_accion", com.copperslug.armasfuego.rifle.RifleAccionPacket.class, com.copperslug.armasfuego.rifle.RifleAccionPacket::encode,
                com.copperslug.armasfuego.rifle.RifleAccionPacket::new, com.copperslug.armasfuego.rifle.RifleAccionPacket::handle);
        alCliente("tirolinas", com.copperslug.armasfuego.rifle.TirolinasPacket.class, com.copperslug.armasfuego.rifle.TirolinasPacket::encode,
                com.copperslug.armasfuego.rifle.TirolinasPacket::new, com.copperslug.armasfuego.rifle.TirolinasPacket::handle);
        alServidor("gatling", com.copperslug.armasfuego.gatling.GatlingPacket.class, com.copperslug.armasfuego.gatling.GatlingPacket::encode,
                com.copperslug.armasfuego.gatling.GatlingPacket::new, com.copperslug.armasfuego.gatling.GatlingPacket::handle);
        alServidor("manga", com.copperslug.armasfuego.oeste.MangaPacket.class, com.copperslug.armasfuego.oeste.MangaPacket::encode,
                com.copperslug.armasfuego.oeste.MangaPacket::new, com.copperslug.armasfuego.oeste.MangaPacket::handle);
        alCliente("config", com.copperslug.config.ConfigPacket.class, com.copperslug.config.ConfigPacket::encode,
                com.copperslug.config.ConfigPacket::new, com.copperslug.config.ConfigPacket::handle);
    }
}

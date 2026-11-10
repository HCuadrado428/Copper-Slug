package com.copperslug.fabric;

import com.copperslug.plataforma.Plataforma;
import net.fabricmc.api.EnvType;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;

public class PlataformaFabric implements Plataforma {
    private record Pendiente<T>(ResourceKey<? extends Registry<T>> reg, ResourceLocation id, Supplier<? extends T> f, Object[] hueco) {}

    private final List<Pendiente<?>> pendientes = new ArrayList<>();

    /** Cada paquete del código común va envuelto en un payload con su propio tipo (copperslug:<nombre>). */
    public record Envoltorio(CustomPacketPayload.Type<Envoltorio> tipo, Object paquete) implements CustomPacketPayload {
        @Override
        public Type<? extends CustomPacketPayload> type() {
            return tipo;
        }
    }

    /** Paquetes: su tipo, cómo se escriben y qué hace el cliente al recibirlos. */
    public record Def<T>(CustomPacketPayload.Type<Envoltorio> tipo, Consumer<T> cliente) {}

    static final Map<Class<?>, Def<?>> DEFS = new HashMap<>();
    public static final List<Def<?>> AL_CLIENTE = new ArrayList<>();

    @SuppressWarnings("unchecked")
    private static <T> StreamCodec<RegistryFriendlyByteBuf, Envoltorio> codec(CustomPacketPayload.Type<Envoltorio> tipo, BiConsumer<T, FriendlyByteBuf> escribir,
                                                                            Function<FriendlyByteBuf, T> leer) {
        return StreamCodec.of((buf, env) -> escribir.accept((T) env.paquete(), buf), buf -> new Envoltorio(tipo, leer.apply(buf)));
    }

    @Override
    public String nombre() {
        return "fabric";
    }

    @Override
    public boolean esCliente() {
        return FabricLoader.getInstance().getEnvironmentType() == EnvType.CLIENT;
    }

    @Override
    public boolean modCargado(String id) {
        return FabricLoader.getInstance().isModLoaded(id);
    }

    @Override
    public Path carpetaConfig() {
        return FabricLoader.getInstance().getConfigDir();
    }

    @Override
    @SuppressWarnings("unchecked")
    public <T> Supplier<T> registrar(ResourceKey<? extends Registry<T>> registro, ResourceLocation id, Supplier<? extends T> fabrica) {
        Object[] hueco = new Object[1];
        if (pendientes == null) throw new IllegalStateException("registros cerrados");
        pendientes.add(new Pendiente<>(registro, id, fabrica, hueco));
        return () -> (T) hueco[0];
    }

    @Override
    @SuppressWarnings({"unchecked", "rawtypes"})
    public void registrosListos() {
        for (Pendiente p : pendientes) {
            Registry r = BuiltInRegistries.REGISTRY.get(p.reg().location());
            if (r == null) throw new IllegalStateException("no hay registro " + p.reg());
            p.hueco()[0] = Registry.register(r, p.id(), p.f().get());
        }
        pendientes.clear();
    }

    @Override
    public boolean esJugadorFalso(ServerPlayer p) {
        return p instanceof net.fabricmc.fabric.api.entity.FakePlayer;
    }

    @Override
    public ServerPlayer jugadorFalso(net.minecraft.server.level.ServerLevel l, com.mojang.authlib.GameProfile perfil) {
        return net.fabricmc.fabric.api.entity.FakePlayer.get(l, perfil);
    }

    @Override
    @SuppressWarnings("unchecked")
    public <T> void paqueteAlServidor(ResourceLocation id, Class<T> clase, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer,
                                      BiConsumer<T, ServerPlayer> manejar) {
        var tipo = new CustomPacketPayload.Type<Envoltorio>(id);
        DEFS.put(clase, new Def<>(tipo, null));
        PayloadTypeRegistry.playC2S().register(tipo, codec(tipo, escribir, leer));
        // en 1.21 Fabric ya llama al receptor en el hilo del servidor
        ServerPlayNetworking.registerGlobalReceiver(tipo, (env, ctx) -> manejar.accept((T) env.paquete(), ctx.player()));
    }

    @Override
    public <T> void paqueteAlCliente(ResourceLocation id, Class<T> clase, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer,
                                     Consumer<T> manejar) {
        var tipo = new CustomPacketPayload.Type<Envoltorio>(id);
        Def<T> d = new Def<>(tipo, manejar);
        DEFS.put(clase, d);
        AL_CLIENTE.add(d);
        PayloadTypeRegistry.playS2C().register(tipo, codec(tipo, escribir, leer));
    }

    static Envoltorio envolver(Object paquete) {
        Def<?> d = DEFS.get(paquete.getClass());
        if (d == null) throw new IllegalArgumentException("paquete sin registrar: " + paquete.getClass());
        return new Envoltorio(d.tipo(), paquete);
    }

    @Override
    public void enviarAlServidor(Object paquete) {
        com.copperslug.fabric.cliente.ClienteFabric.enviar(envolver(paquete));
    }

    @Override
    public void enviarA(ServerPlayer p, Object paquete) {
        Envoltorio e = envolver(paquete);
        if (ServerPlayNetworking.canSend(p, e.tipo())) ServerPlayNetworking.send(p, e);
    }
}

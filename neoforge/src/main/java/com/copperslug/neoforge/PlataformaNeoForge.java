package com.copperslug.neoforge;

import com.copperslug.plataforma.Plataforma;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.Registry;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModList;
import net.neoforged.fml.loading.FMLEnvironment;
import net.neoforged.fml.loading.FMLPaths;
import net.neoforged.neoforge.common.util.BlockSnapshot;
import net.neoforged.neoforge.common.util.FakePlayer;
import net.neoforged.neoforge.event.EventHooks;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;

public class PlataformaNeoForge implements Plataforma {
    static IEventBus busMod;
    private final Map<ResourceKey<?>, DeferredRegister<?>> registros = new LinkedHashMap<>();

    /** Cada paquete del código común va envuelto en un payload con su propio tipo (copperslug:<nombre>). */
    record Envoltorio(CustomPacketPayload.Type<Envoltorio> tipo, Object paquete) implements CustomPacketPayload {
        @Override
        public Type<? extends CustomPacketPayload> type() {
            return tipo;
        }
    }

    private record Paquete<T>(CustomPacketPayload.Type<Envoltorio> tipo, boolean alServidor, BiConsumer<T, FriendlyByteBuf> escribir,
                              Function<FriendlyByteBuf, T> leer, BiConsumer<T, ServerPlayer> enServidor, Consumer<T> enCliente) {
        @SuppressWarnings("unchecked")
        StreamCodec<RegistryFriendlyByteBuf, Envoltorio> codec() {
            return StreamCodec.of((buf, env) -> escribir.accept((T) env.paquete(), buf), buf -> new Envoltorio(tipo, leer.apply(buf)));
        }
    }

    private static final List<Paquete<?>> PAQUETES = new ArrayList<>();
    private static final Map<Class<?>, CustomPacketPayload.Type<Envoltorio>> TIPOS = new HashMap<>();

    @SuppressWarnings("unchecked")
    static void registrarPaquetes(PayloadRegistrar r) {
        for (Paquete<?> p0 : PAQUETES) {
            Paquete<Object> p = (Paquete<Object>) p0;
            if (p.alServidor()) r.playToServer(p.tipo(), p.codec(), (env, ctx) -> {
                if (ctx.player() instanceof ServerPlayer sp) p.enServidor().accept(env.paquete(), sp);
            });
            else r.playToClient(p.tipo(), p.codec(), (env, ctx) -> p.enCliente().accept(env.paquete()));
        }
    }

    @Override
    public String nombre() {
        return "neoforge";
    }

    @Override
    public boolean esCliente() {
        return FMLEnvironment.dist.isClient();
    }

    @Override
    public boolean modCargado(String id) {
        return ModList.get().isLoaded(id);
    }

    @Override
    public Path carpetaConfig() {
        return FMLPaths.CONFIGDIR.get();
    }

    @Override
    @SuppressWarnings("unchecked")
    public <T> Supplier<T> registrar(ResourceKey<? extends Registry<T>> registro, ResourceLocation id, Supplier<? extends T> fabrica) {
        DeferredRegister<T> dr = (DeferredRegister<T>) registros.computeIfAbsent(registro, k -> {
            DeferredRegister<T> d = DeferredRegister.create((ResourceKey<? extends Registry<T>>) k, id.getNamespace());
            if (busMod != null) d.register(busMod);
            return d;
        });
        return dr.register(id.getPath(), fabrica);
    }

    @Override
    public boolean puedeColocar(Player p, Level l, BlockPos pos) {
        return !EventHooks.onBlockPlace(p, BlockSnapshot.create(l.dimension(), l, pos), Direction.UP);
    }

    @Override
    public boolean esJugadorFalso(ServerPlayer p) {
        return p instanceof FakePlayer;
    }

    @Override
    public ServerPlayer jugadorFalso(net.minecraft.server.level.ServerLevel l, com.mojang.authlib.GameProfile perfil) {
        return net.neoforged.neoforge.common.util.FakePlayerFactory.get(l, perfil);
    }

    @Override
    public <T> void paqueteAlServidor(ResourceLocation id, Class<T> clase, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer,
                                      BiConsumer<T, ServerPlayer> manejar) {
        var tipo = new CustomPacketPayload.Type<Envoltorio>(id);
        TIPOS.put(clase, tipo);
        PAQUETES.add(new Paquete<>(tipo, true, escribir, leer, manejar, null));
    }

    @Override
    public <T> void paqueteAlCliente(ResourceLocation id, Class<T> clase, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer,
                                     Consumer<T> manejar) {
        var tipo = new CustomPacketPayload.Type<Envoltorio>(id);
        TIPOS.put(clase, tipo);
        PAQUETES.add(new Paquete<>(tipo, false, escribir, leer, null, manejar));
    }

    private static Envoltorio envolver(Object paquete) {
        var tipo = TIPOS.get(paquete.getClass());
        if (tipo == null) throw new IllegalArgumentException("Copper Slug: paquete sin registrar " + paquete.getClass());
        return new Envoltorio(tipo, paquete);
    }

    @Override
    public void enviarAlServidor(Object paquete) {
        PacketDistributor.sendToServer(envolver(paquete));
    }

    @Override
    public void enviarA(ServerPlayer p, Object paquete) {
        PacketDistributor.sendToPlayer(p, envolver(paquete));
    }
}

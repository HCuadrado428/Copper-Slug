package com.copperslug.fabric;

import com.copperslug.plataforma.Plataforma;
import net.fabricmc.api.EnvType;
import net.fabricmc.fabric.api.networking.v1.PacketByteBufs;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.enchantment.EnchantmentCategory;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;

public class PlataformaFabric implements Plataforma {
    private record Pendiente<T>(ResourceKey<? extends Registry<T>> reg, ResourceLocation id, Supplier<? extends T> f, Object[] hueco) {}

    private final List<Pendiente<?>> pendientes = new ArrayList<>();

    /** Paquetes: cómo se escribe cada clase y por qué canal va. */
    public record Def<T>(ResourceLocation id, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer, Consumer<T> cliente) {}

    static final Map<Class<?>, Def<?>> DEFS = new HashMap<>();
    public static final List<Def<?>> AL_CLIENTE = new ArrayList<>();

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
    public EnchantmentCategory categoria(String nombre, Predicate<Item> filtro) {
        return CategoriasFabric.nueva(nombre, filtro);
    }

    @Override
    public Attribute alcanceAtaque() {
        return null;
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
    public <T> void paqueteAlServidor(ResourceLocation id, Class<T> clase, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer,
                                      BiConsumer<T, ServerPlayer> manejar) {
        DEFS.put(clase, new Def<>(id, escribir, leer, null));
        ServerPlayNetworking.registerGlobalReceiver(id, (server, player, handler, buf, sender) -> {
            T m = leer.apply(buf);
            server.execute(() -> manejar.accept(m, player));
        });
    }

    @Override
    public <T> void paqueteAlCliente(ResourceLocation id, Class<T> clase, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer,
                                     Consumer<T> manejar) {
        Def<T> d = new Def<>(id, escribir, leer, manejar);
        DEFS.put(clase, d);
        AL_CLIENTE.add(d);
    }

    @SuppressWarnings("unchecked")
    static <T> FriendlyByteBuf escribir(Object paquete, Def<T>[] defOut) {
        Def<T> d = (Def<T>) DEFS.get(paquete.getClass());
        if (d == null) throw new IllegalArgumentException("paquete sin registrar: " + paquete.getClass());
        FriendlyByteBuf b = PacketByteBufs.create();
        d.escribir().accept((T) paquete, b);
        defOut[0] = d;
        return b;
    }

    @Override
    @SuppressWarnings({"unchecked", "rawtypes"})
    public void enviarAlServidor(Object paquete) {
        Def[] d = new Def[1];
        FriendlyByteBuf b = escribir(paquete, d);
        com.copperslug.fabric.cliente.ClienteFabric.enviar(d[0].id(), b);
    }

    @Override
    @SuppressWarnings({"unchecked", "rawtypes"})
    public void enviarA(ServerPlayer p, Object paquete) {
        Def[] d = new Def[1];
        FriendlyByteBuf b = escribir(paquete, d);
        if (ServerPlayNetworking.canSend(p, d[0].id())) ServerPlayNetworking.send(p, d[0].id(), b);
    }
}

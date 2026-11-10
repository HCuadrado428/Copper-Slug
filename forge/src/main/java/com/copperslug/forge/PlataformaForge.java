package com.copperslug.forge;

import com.copperslug.CopperSlug;
import com.copperslug.network.ModNetwork;
import com.copperslug.plataforma.Plataforma;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.Registry;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.enchantment.EnchantmentCategory;
import net.minecraft.world.level.Level;
import net.minecraftforge.common.ForgeMod;
import net.minecraftforge.common.util.BlockSnapshot;
import net.minecraftforge.common.util.FakePlayer;
import net.minecraftforge.event.ForgeEventFactory;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.ModList;
import net.minecraftforge.fml.loading.FMLEnvironment;
import net.minecraftforge.fml.loading.FMLPaths;
import net.minecraftforge.network.NetworkDirection;
import net.minecraftforge.network.NetworkEvent;
import net.minecraftforge.network.NetworkRegistry;
import net.minecraftforge.network.PacketDistributor;
import net.minecraftforge.network.simple.SimpleChannel;
import net.minecraftforge.registries.DeferredRegister;

import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;

public class PlataformaForge implements Plataforma {
    static IEventBus busMod;
    private final Map<ResourceKey<?>, DeferredRegister<?>> registros = new LinkedHashMap<>();

    private static final SimpleChannel CANAL = NetworkRegistry.newSimpleChannel(new ResourceLocation(CopperSlug.MOD_ID, "main"),
            () -> ModNetwork.PROTOCOLO, ModNetwork.PROTOCOLO::equals, ModNetwork.PROTOCOLO::equals);
    private int idPaquete;

    @Override
    public String nombre() {
        return ModList.get().isLoaded("neoforge") ? "neoforge" : "forge";
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
    public EnchantmentCategory categoria(String nombre, Predicate<Item> filtro) {
        return EnchantmentCategory.create(nombre, filtro::test);
    }

    @Override
    public Attribute alcanceAtaque() {
        return ForgeMod.ENTITY_REACH.get();
    }

    @Override
    public boolean puedeColocar(Player p, Level l, BlockPos pos) {
        return !ForgeEventFactory.onBlockPlace(p, BlockSnapshot.create(l.dimension(), l, pos), Direction.UP);
    }

    @Override
    public boolean esJugadorFalso(ServerPlayer p) {
        return p instanceof FakePlayer;
    }

    @Override
    public ServerPlayer jugadorFalso(net.minecraft.server.level.ServerLevel l, com.mojang.authlib.GameProfile perfil) {
        return net.minecraftforge.common.util.FakePlayerFactory.get(l, perfil);
    }

    @Override
    public <T> void paqueteAlServidor(ResourceLocation id, Class<T> clase, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer,
                                      BiConsumer<T, ServerPlayer> manejar) {
        CANAL.messageBuilder(clase, idPaquete++, NetworkDirection.PLAY_TO_SERVER)
                .encoder(escribir).decoder(leer)
                .consumerMainThread((T m, Supplier<NetworkEvent.Context> c) -> {
                    ServerPlayer p = c.get().getSender();
                    if (p != null) manejar.accept(m, p);
                }).add();
    }

    @Override
    public <T> void paqueteAlCliente(ResourceLocation id, Class<T> clase, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer,
                                     Consumer<T> manejar) {
        CANAL.messageBuilder(clase, idPaquete++, NetworkDirection.PLAY_TO_CLIENT)
                .encoder(escribir).decoder(leer)
                .consumerMainThread((T m, Supplier<NetworkEvent.Context> c) -> manejar.accept(m)).add();
    }

    @Override
    public void enviarAlServidor(Object paquete) {
        CANAL.sendToServer(paquete);
    }

    @Override
    public void enviarA(ServerPlayer p, Object paquete) {
        CANAL.send(PacketDistributor.PLAYER.with(() -> p), paquete);
    }

    static Optional<?> nada() {
        return Optional.empty();
    }
}

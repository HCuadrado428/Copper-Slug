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
import net.minecraft.world.level.Level;
import net.minecraftforge.common.ForgeMod;
import net.minecraftforge.common.util.BlockSnapshot;
import net.minecraftforge.event.ForgeEventFactory;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.ModList;
import net.minecraftforge.fml.loading.FMLEnvironment;
import net.minecraftforge.fml.loading.FMLPaths;
import net.minecraftforge.network.NetworkDirection;
import net.minecraftforge.network.ChannelBuilder;
import net.minecraftforge.network.PacketDistributor;
import net.minecraftforge.network.SimpleChannel;
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

    private static final SimpleChannel CANAL = ChannelBuilder.named(ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "main"))
            .networkProtocolVersion(1).simpleChannel();
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
    public boolean puedeColocar(Player p, Level l, BlockPos pos) {
        return !ForgeEventFactory.onBlockPlace(p, BlockSnapshot.create(l.dimension(), l, pos), Direction.UP);
    }

    @Override
    public boolean esJugadorFalso(ServerPlayer p) {
        // Forge 52 no trae FakePlayer: los de mentira son los nuestros (la prueba) o los que no tienen conexión
        return p instanceof JugadorFalso || p.connection == null;
    }

    @Override
    public ServerPlayer jugadorFalso(net.minecraft.server.level.ServerLevel l, com.mojang.authlib.GameProfile perfil) {
        return new JugadorFalso(l, perfil);
    }

    @Override
    public <T> void paqueteAlServidor(ResourceLocation id, Class<T> clase, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer,
                                      BiConsumer<T, ServerPlayer> manejar) {
        CANAL.messageBuilder(clase, idPaquete++, NetworkDirection.PLAY_TO_SERVER)
                .encoder((T m, net.minecraft.network.RegistryFriendlyByteBuf b) -> escribir.accept(m, b)).decoder(b -> leer.apply(b))
                .consumerMainThread((T m, net.minecraftforge.event.network.CustomPayloadEvent.Context c) -> {
                    ServerPlayer p = c.getSender();
                    if (p != null) manejar.accept(m, p);
                }).add();
    }

    @Override
    public <T> void paqueteAlCliente(ResourceLocation id, Class<T> clase, BiConsumer<T, FriendlyByteBuf> escribir, Function<FriendlyByteBuf, T> leer,
                                     Consumer<T> manejar) {
        CANAL.messageBuilder(clase, idPaquete++, NetworkDirection.PLAY_TO_CLIENT)
                .encoder((T m, net.minecraft.network.RegistryFriendlyByteBuf b) -> escribir.accept(m, b)).decoder(b -> leer.apply(b))
                .consumerMainThread((T m, net.minecraftforge.event.network.CustomPayloadEvent.Context c) -> manejar.accept(m)).add();
    }

    @Override
    public void enviarAlServidor(Object paquete) {
        CANAL.send(paquete, PacketDistributor.SERVER.noArg());
    }

    @Override
    public void enviarA(ServerPlayer p, Object paquete) {
        CANAL.send(paquete, PacketDistributor.PLAYER.with(p));
    }

    /** Un jugador de mentira, sin conexión de verdad. */
    static final class JugadorFalso extends ServerPlayer {
        JugadorFalso(net.minecraft.server.level.ServerLevel l, com.mojang.authlib.GameProfile perfil) {
            super(l.getServer(), l, perfil, net.minecraft.server.level.ClientInformation.createDefault());
            // sin cliente: la conexión no envía nada (sin esto, mandar un título o un mensaje al forastero da NPE)
            this.connection = new net.minecraft.server.network.ServerGamePacketListenerImpl(l.getServer(),
                    new net.minecraft.network.Connection(net.minecraft.network.protocol.PacketFlow.SERVERBOUND) {
                        @Override
                        public void send(net.minecraft.network.protocol.Packet<?> paquete) {}

                        @Override
                        public void send(net.minecraft.network.protocol.Packet<?> paquete, net.minecraft.network.PacketSendListener listener) {}
                    }, this, net.minecraft.server.network.CommonListenerCookie.createInitial(perfil, false));
        }

        @Override
        public boolean isSpectator() {
            return false;
        }

        @Override
        public boolean isCreative() {
            return false;
        }
    }

    static Optional<?> nada() {
        return Optional.empty();
    }
}

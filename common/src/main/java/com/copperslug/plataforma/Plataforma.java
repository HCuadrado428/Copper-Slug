package com.copperslug.plataforma;

import net.minecraft.core.BlockPos;
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

import java.nio.file.Path;
import java.util.ServiceLoader;
import java.util.function.Predicate;
import java.util.function.Supplier;

/**
 * Lo que cambia de un cargador a otro (Forge, NeoForge, Fabric). Cada cargador da su implementación con
 * META-INF/services; el código común solo usa esto (casi siempre a través de los shims de com.copperslug.shim).
 */
public interface Plataforma {
    Plataforma P = cargar();

    static Plataforma get() {
        return P;
    }

    private static Plataforma cargar() {
        return ServiceLoader.load(Plataforma.class, Plataforma.class.getClassLoader()).findFirst()
                .orElseThrow(() -> new IllegalStateException("Copper Slug: no hay implementación de Plataforma"));
    }

    /** "forge", "neoforge" o "fabric". */
    String nombre();

    boolean esCliente();

    boolean modCargado(String id);

    Path carpetaConfig();

    /** Da de alta algo en un registro vanilla; el Supplier devuelve el objeto ya registrado (Forge: cuando toque). */
    <T> Supplier<T> registrar(ResourceKey<? extends Registry<T>> registro, ResourceLocation id, Supplier<? extends T> fabrica);

    /** Cierra los registros pendientes (Fabric registra aquí todo lo que se pidió en los static de los registros). */
    default void registrosListos() {}

    /** Una categoría de encantamiento nueva (Forge: una constante nueva del enum; Fabric, ver CategoriasFabric). */
    EnchantmentCategory categoria(String nombre, Predicate<Item> filtro);

    /** El atributo de alcance de ataque del cargador (null si no hay). */
    Attribute alcanceAtaque();

    /** ¿Puede este jugador colocar un bloque ahí? (protecciones de los cargadores que las tienen). */
    default boolean puedeColocar(Player p, Level l, BlockPos pos) {
        return l.mayInteract(p, pos);
    }

    boolean esJugadorFalso(ServerPlayer p);

    // ---------------------------------------------------------------- red
    /** Un canal por paquete; id: copperslug:<nombre>. */
    <T> void paqueteAlServidor(ResourceLocation id, Class<T> clase, java.util.function.BiConsumer<T, FriendlyByteBuf> escribir,
                               java.util.function.Function<FriendlyByteBuf, T> leer, java.util.function.BiConsumer<T, ServerPlayer> manejar);

    <T> void paqueteAlCliente(ResourceLocation id, Class<T> clase, java.util.function.BiConsumer<T, FriendlyByteBuf> escribir,
                              java.util.function.Function<FriendlyByteBuf, T> leer, java.util.function.Consumer<T> manejar);

    void enviarAlServidor(Object paquete);

    void enviarA(ServerPlayer p, Object paquete);
}

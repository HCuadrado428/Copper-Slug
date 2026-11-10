package com.copperslug;

import com.copperslug.config.ConfigArchivo;
import com.copperslug.config.ConfigPacket;
import com.copperslug.logros.LogrosMiscelanea;
import com.copperslug.network.ModNetwork;
import com.copperslug.plataforma.Plataforma;
import com.copperslug.registry.ModEnchantments;
import com.copperslug.registry.ModItems;
import com.copperslug.shim.event.entity.player.PlayerEvent;
import com.copperslug.shim.event.server.ServerStoppedEvent;
import com.copperslug.shim.eventbus.api.Bus;
import com.copperslug.shim.eventbus.api.SubscribeEvent;
import com.copperslug.shim.network.PacketDistributor;
import com.copperslug.shim.server.ServerLifecycleHooks;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.EnchantedBookItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.EnchantmentInstance;
import net.minecraft.world.level.storage.LevelResource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.invoke.MethodHandles;
import java.util.List;
import java.util.function.Supplier;

/** Copper Slug: las nueve armas de fuego de cobre. Lo común a todos los cargadores empieza aquí. */
public final class CopperSlug {
    private CopperSlug() {}

    public static final String MOD_ID = "copperslug";
    public static final Logger LOG = LoggerFactory.getLogger("Copper Slug");

    public static Supplier<CreativeModeTab> PESTANA;

    private static void cargar(Class<?>... cs) {
        for (Class<?> c : cs) {
            try {
                MethodHandles.lookup().ensureInitialized(c);
            } catch (IllegalAccessException e) {
                throw new RuntimeException(e);
            }
        }
    }

    /** Al cargar el mod (en Forge, en el constructor; en Fabric, en onInitialize). */
    public static void iniciar() {
        cargar(ModItems.class, com.copperslug.registry.ModSounds.class, com.copperslug.registry.ModEntities.class, ModEnchantments.class,
                com.copperslug.registry.ModEffects.class, com.copperslug.registry.ModRecipes.class,
                com.copperslug.armasfuego.comun.ArmasFuegoRegistro.class, ConfigServidor.class);
        PESTANA = Plataforma.get().registrar(Registries.CREATIVE_MODE_TAB, net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(MOD_ID, "armas"),
                () -> CreativeModeTab.builder(CreativeModeTab.Row.TOP, 0)
                        .title(Component.translatable("itemGroup.copperslug"))
                        .icon(() -> new ItemStack(ModItems.REVOLVER.get()))
                        .displayItems((params, out) -> Pestana.llenar(out::accept))
                        .build());
        Plataforma.get().registrosListos();
        LogrosMiscelanea.registrar();
        ModNetwork.registrar();
        Bus.suscribir(CopperSlug.class);
        for (String c : Suscriptores.COMUN) {
            try {
                Bus.suscribir(Class.forName(c));
            } catch (ClassNotFoundException e) {
                throw new RuntimeException(e);
            }
        }
        LOG.info("Copper Slug cargado ({})", Plataforma.get().nombre());
    }

    /** El servidor arranca (integrado o dedicado): la config del mundo. */
    public static void servidorArrancando(MinecraftServer s) {
        ServerLifecycleHooks.poner(s);
        ConfigArchivo.cargar(ConfigServidor.SPEC, s.getWorldPath(LevelResource.ROOT).resolve("serverconfig").resolve(MOD_ID + "-server.toml"));
    }

    public static void servidorParado(MinecraftServer s) {
        Bus.post(new ServerStoppedEvent(s));
        ServerLifecycleHooks.poner(null);
    }

    @SubscribeEvent
    public static void entra(PlayerEvent.PlayerLoggedInEvent e) {
        if (e.getEntity() instanceof ServerPlayer p) ModNetwork.CHANNEL.send(PacketDistributor.PLAYER.with(() -> p), new ConfigPacket());
    }

    /** Lo que sale en la pestaña del modo creativo (lo mismo y en el orden de Miscelánea). */
    public static final class Pestana {
        public static void llenar(java.util.function.Consumer<ItemStack> out) {
            for (var en : List.of(ModEnchantments.REVOLVER_ABANICO, ModEnchantments.REVOLVER_CARAMBOLA,
                    ModEnchantments.REVOLVER_DESENFUNDE, ModEnchantments.REVOLVER_SENALERO)) libro(out, en.get());
            out.accept(new ItemStack(ModItems.REVOLVER.get()));
            for (var m : List.of(ModItems.REVOLVER_BALA, ModItems.REVOLVER_BENGALA, ModItems.REVOLVER_DARDO, ModItems.REVOLVER_FOGUEO,
                    ModItems.REVOLVER_IMAN, ModItems.REVOLVER_TIEMPO)) out.accept(new ItemStack(m.get()));
            out.accept(new ItemStack(ModItems.ESCOPETA_PRESION.get()));
            for (var t : com.copperslug.armasfuego.escopeta.TipoCartucho.values()) out.accept(new ItemStack(t.item()));
            out.accept(new ItemStack(ModItems.RIFLE.get()));
            out.accept(new ItemStack(ModItems.BALA_RIFLE.get()));
            out.accept(new ItemStack(ModItems.BALA_TRAZADORA.get()));
            out.accept(new ItemStack(ModItems.BALA_CUERDA.get()));
            out.accept(new ItemStack(ModItems.CASQUILLO_RIFLE.get()));
            for (int c = 0; c < 16; c++) out.accept(com.copperslug.armasfuego.rifle.Pintura.bala(c));
            out.accept(new ItemStack(ModItems.GATLING.get()));
            out.accept(new ItemStack(ModItems.CINTA_GATLING.get()));
            out.accept(new ItemStack(ModItems.WINCHESTER.get()));
            out.accept(new ItemStack(ModItems.DERRINGER.get()));
            out.accept(new ItemStack(ModItems.BALA_DERRINGER.get()));
            out.accept(com.copperslug.armasfuego.oeste.EstucheViolinItem.con(new ItemStack(ModItems.THOMPSON.get())));
            out.accept(new ItemStack(ModItems.THOMPSON.get()));
            out.accept(new ItemStack(ModItems.ESTUCHE_VIOLIN.get()));
            out.accept(new ItemStack(ModItems.CARGADOR_THOMPSON.get()));
            out.accept(new ItemStack(ModItems.MOSQUETE.get()));
            out.accept(new ItemStack(ModItems.BOLA_MOSQUETE.get()));
            out.accept(new ItemStack(ModItems.CANON_MANO.get()));
            for (var m : List.of(ModItems.BALA_PLATA, ModItems.BALA_DINAMITA, ModItems.CARTA_MARCADA, ModItems.BALA_ORO, ModItems.TAMBOR_TRAZADOR,
                    ModItems.TAMBOR_AGUA, ModItems.CINTA_INCENDIARIA, ModItems.CINTA_PALOMITAS, ModItems.PALOMITAS, ModItems.METRALLA, ModItems.BOLA_CADENA,
                    ModItems.BOLANO_INCENDIARIO, ModItems.BOLANO_FUEGOS, ModItems.BALA_HIELO, ModItems.BALA_HUMO, ModItems.TAMBOR_TINTA,
                    ModItems.CINTA_GUISANTES, ModItems.BOLA_ARPON, ModItems.BOLANO_SALTARIN)) out.accept(new ItemStack(m.get()));
            // los libros de los encantamientos propios de las demás armas
            var rev = List.of(ModEnchantments.REVOLVER_ABANICO, ModEnchantments.REVOLVER_CARAMBOLA,
                    ModEnchantments.REVOLVER_DESENFUNDE, ModEnchantments.REVOLVER_SENALERO);
            for (var e : net.minecraft.core.registries.BuiltInRegistries.ENCHANTMENT.entrySet())
                if (MOD_ID.equals(e.getKey().location().getNamespace()) && !rev.contains(e.getValue())) libro(out, e.getValue());
        }

        private static void libro(java.util.function.Consumer<ItemStack> out, net.minecraft.world.item.enchantment.Enchantment en) {
            out.accept(EnchantedBookItem.createForEnchantment(new EnchantmentInstance(en, en.getMaxLevel())));
        }
    }
}

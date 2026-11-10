package com.copperslug.fabric;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.BotinArmas;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.fabricmc.fabric.api.loot.v3.LootTableEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.world.level.storage.loot.entries.LootPoolEntryType;
import net.minecraft.world.level.storage.loot.entries.LootPoolSingletonContainer;
import net.minecraft.world.level.storage.loot.functions.LootItemFunction;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.minecraft.world.level.storage.loot.providers.number.ConstantValue;

import java.util.List;
import java.util.function.Consumer;

/**
 * El botín de las armas en Fabric: a las tablas de los cofres donde puede salir alguna se les añade una tirada con una
 * entrada propia que, al abrir el cofre, decide con BotinArmas (la misma probabilidad y lo mismo que en Forge).
 */
public final class BotinFabric {
    private BotinFabric() {}

    static LootPoolEntryType TIPO;

    static void registrar() {
        TIPO = Registry.register(BuiltInRegistries.LOOT_POOL_ENTRY_TYPE, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "armas_fuego"),
                new LootPoolEntryType(Entrada.CODEC));
        LootTableEvents.MODIFY.register((clave, tabla, fuente, registros) -> {
            ResourceLocation id = clave.location();
            if (!fuente.isBuiltin() || BotinArmas.arma(id) == null && !id.getPath().startsWith("chests/village/")) return;
            tabla.withPool(LootPool.lootPool().setRolls(ConstantValue.exactly(1)).add(Entrada.de(id)));
        });
    }

    static final class Entrada extends LootPoolSingletonContainer {
        static final MapCodec<Entrada> CODEC = RecordCodecBuilder.mapCodec(i -> i.group(
                ResourceLocation.CODEC.fieldOf("tabla").forGetter(e -> e.tabla)).and(singletonFields(i)).apply(i, Entrada::new));

        private final ResourceLocation tabla;

        Entrada(ResourceLocation tabla, int peso, int calidad, List<LootItemCondition> cond, List<LootItemFunction> fun) {
            super(peso, calidad, cond, fun);
            this.tabla = tabla;
        }

        static LootPoolSingletonContainer.Builder<?> de(ResourceLocation tabla) {
            return simpleBuilder((p, q, c, f) -> new Entrada(tabla, p, q, c, f));
        }

        @Override
        public LootPoolEntryType getType() {
            return TIPO;
        }

        @Override
        protected void createItemStack(Consumer<ItemStack> out, LootContext ctx) {
            for (ItemStack s : BotinArmas.aplicar(tabla, ctx.getRandom())) out.accept(s);
        }
    }
}

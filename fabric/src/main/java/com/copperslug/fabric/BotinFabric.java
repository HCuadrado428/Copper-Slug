package com.copperslug.fabric;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.BotinArmas;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonObject;
import com.google.gson.JsonSerializationContext;
import net.fabricmc.fabric.api.loot.v2.LootTableEvents;
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

import java.util.function.Consumer;

/**
 * El botín de las armas en Fabric: a las tablas de los cofres donde puede salir alguna se les añade una tirada con una
 * entrada propia que, al abrir el cofre, decide con BotinArmas (la misma probabilidad y lo mismo que en Forge).
 */
public final class BotinFabric {
    private BotinFabric() {}

    static LootPoolEntryType TIPO;

    static void registrar() {
        TIPO = Registry.register(BuiltInRegistries.LOOT_POOL_ENTRY_TYPE, new ResourceLocation(CopperSlug.MOD_ID, "armas_fuego"),
                new LootPoolEntryType(new Entrada.Serializador()));
        LootTableEvents.MODIFY.register((recursos, gestor, id, tabla, fuente) -> {
            if (!fuente.isBuiltin() || BotinArmas.arma(id) == null && !id.getPath().startsWith("chests/village/")
                    && !id.getPath().equals("chests/simple_dungeon") && !id.getPath().equals("chests/abandoned_mineshaft")
                    && !id.getPath().equals("chests/pillager_outpost")) return;   // (los tres últimos, también por las granadas)
            tabla.withPool(LootPool.lootPool().setRolls(ConstantValue.exactly(1)).add(Entrada.de(id)));
        });
    }

    static final class Entrada extends LootPoolSingletonContainer {
        private final ResourceLocation tabla;

        Entrada(ResourceLocation tabla, int peso, int calidad, LootItemCondition[] cond, LootItemFunction[] fun) {
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

        static final class Serializador extends LootPoolSingletonContainer.Serializer<Entrada> {
            @Override
            public void serializeCustom(JsonObject o, Entrada e, JsonSerializationContext c) {
                super.serializeCustom(o, e, c);
                o.addProperty("tabla", e.tabla.toString());
            }

            @Override
            protected Entrada deserialize(JsonObject o, JsonDeserializationContext c, int peso, int calidad, LootItemCondition[] cond, LootItemFunction[] fun) {
                return new Entrada(new ResourceLocation(o.get("tabla").getAsString()), peso, calidad, cond, fun);
            }
        }
    }
}

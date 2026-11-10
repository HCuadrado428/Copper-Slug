package com.copperslug.neoforge;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.BotinArmas;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;
import net.neoforged.neoforge.common.loot.LootModifier;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;

import java.util.function.Supplier;

/** El botín de las armas en NeoForge: un Global Loot Modifier (data/copperslug/loot_modifiers/armas_fuego.json). */
public class BotinNeoForge extends LootModifier {
    public static final DeferredRegister<MapCodec<? extends IGlobalLootModifier>> SERIALIZERS =
            DeferredRegister.create(NeoForgeRegistries.Keys.GLOBAL_LOOT_MODIFIER_SERIALIZERS, CopperSlug.MOD_ID);
    public static final MapCodec<BotinNeoForge> CODEC = RecordCodecBuilder.mapCodec(inst -> codecStart(inst).apply(inst, BotinNeoForge::new));
    public static final Supplier<MapCodec<BotinNeoForge>> TIPO = SERIALIZERS.register("armas_fuego", () -> CODEC);

    public BotinNeoForge(LootItemCondition[] condiciones) {
        super(condiciones);
    }

    @Override
    protected ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack> botin, LootContext ctx) {
        botin.addAll(BotinArmas.aplicar(ctx.getQueriedLootTableId(), ctx.getRandom()));
        return botin;
    }

    @Override
    public MapCodec<? extends IGlobalLootModifier> codec() {
        return CODEC;
    }
}

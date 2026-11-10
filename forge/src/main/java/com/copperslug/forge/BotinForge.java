package com.copperslug.forge;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.BotinArmas;
import com.google.common.base.Suppliers;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.minecraftforge.common.loot.IGlobalLootModifier;
import net.minecraftforge.common.loot.LootModifier;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.function.Supplier;

/** El botín de las armas en Forge: un Global Loot Modifier (data/copperslug/loot_modifiers/armas_fuego.json). */
public class BotinForge extends LootModifier {
    public static final DeferredRegister<Codec<? extends IGlobalLootModifier>> SERIALIZERS =
            DeferredRegister.create(ForgeRegistries.Keys.GLOBAL_LOOT_MODIFIER_SERIALIZERS, CopperSlug.MOD_ID);
    public static final Supplier<Codec<BotinForge>> CODEC = Suppliers.memoize(
            () -> RecordCodecBuilder.create(inst -> codecStart(inst).apply(inst, BotinForge::new)));
    public static final RegistryObject<Codec<BotinForge>> TIPO = SERIALIZERS.register("armas_fuego", CODEC);

    public BotinForge(LootItemCondition[] condiciones) {
        super(condiciones);
    }

    @Override
    protected ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack> botin, LootContext ctx) {
        botin.addAll(BotinArmas.aplicar(ctx.getQueriedLootTableId(), ctx.getRandom()));
        return botin;
    }

    @Override
    public Codec<? extends IGlobalLootModifier> codec() {
        return CODEC.get();
    }
}

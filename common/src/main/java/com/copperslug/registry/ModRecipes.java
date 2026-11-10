package com.copperslug.registry;

import com.copperslug.CopperSlug;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.SimpleCraftingRecipeSerializer;
import com.copperslug.shim.registries.DeferredRegister;
import com.copperslug.shim.registries.ForgeRegistries;
import com.copperslug.shim.registries.RegistryObject;

/** Generado por herramientas/portar.py a partir del ModRecipes de Miscelánea (solo lo de las armas). */
public final class ModRecipes {
    public static final DeferredRegister<RecipeSerializer<?>> SERIALIZERS =
            DeferredRegister.create(ForgeRegistries.RECIPE_SERIALIZERS, CopperSlug.MOD_ID);
    public static final RegistryObject<RecipeSerializer<com.copperslug.armasfuego.oeste.MosqueteBayonetaRecipe>> MOSQUETE_BAYONETA =
            SERIALIZERS.register("mosquete_bayoneta", () -> new SimpleCraftingRecipeSerializer<>(com.copperslug.armasfuego.oeste.MosqueteBayonetaRecipe::new));

    private ModRecipes() {}
}

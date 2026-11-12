package com.copperslug.compat.jei;

import com.copperslug.CopperSlug;
import com.copperslug.registry.ModItems;
import mezz.jei.api.IModPlugin;
import mezz.jei.api.JeiPlugin;
import mezz.jei.api.constants.VanillaTypes;
import mezz.jei.api.registration.IRecipeRegistration;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

import java.util.function.Supplier;

/**
 * Plugin de JEI (opcional: solo se carga si JEI está instalado). Lo de las armas del de Miscelánea: dónde se encuentra
 * cada una (no se fabrican), lo que hacen además de disparar y las recetas de ejemplo de la bayoneta del mosquete.
 * En Forge lo encuentra la anotación; en Fabric, la entrada "jei_mod_plugin" de fabric.mod.json.
 */
@JeiPlugin
public class CopperSlugJei implements IModPlugin {
    private static final ResourceLocation ID = net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "jei");

    @Override
    public ResourceLocation getPluginUid() {
        return ID;
    }

    @Override
    public void registerRecipes(IRecipeRegistration r) {
        // ---- armas de fuego: no se fabrican, se encuentran
        info(r, ModItems.REVOLVER, "revolver_botin");
        info(r, ModItems.ESCOPETA_PRESION, "escopeta_botin");
        info(r, ModItems.RIFLE, "rifle_botin");
        info(r, ModItems.GATLING, "gatling_botin");
        info(r, ModItems.WINCHESTER, "winchester_botin");
        info(r, ModItems.DERRINGER, "derringer_botin");
        info(r, ModItems.CERBATANA, "cerbatana_botin");
        info(r, ModItems.THOMPSON, "thompson_botin");
        info(r, ModItems.MOSQUETE, "mosquete_botin");
        info(r, ModItems.CANON_MANO, "canon_botin");
        // ---- lo que hacen además de disparar
        info(r, ModItems.GATLING, "gatling_utilidad");
        info(r, ModItems.WINCHESTER, "winchester_deposito");
        info(r, ModItems.DERRINGER, "derringer_manga");
        info(r, ModItems.ESTUCHE_VIOLIN, "estuche_violin");
        info(r, ModItems.MOSQUETE, "mosquete_bayoneta");
        info(r, ModItems.CANON_MANO, "canon_bloques");
        // la bayoneta del mosquete en la mesa: una receta de ejemplo por espada vanilla (y la de quitarla)
        java.util.List<net.minecraft.world.item.crafting.RecipeHolder<net.minecraft.world.item.crafting.CraftingRecipe>> bay = new java.util.ArrayList<>();
        Item[] espadas = {Items.WOODEN_SWORD, Items.STONE_SWORD, Items.IRON_SWORD, Items.GOLDEN_SWORD, Items.DIAMOND_SWORD, Items.NETHERITE_SWORD};
        for (Item e : espadas) {
            ItemStack sin = new ItemStack(ModItems.MOSQUETE.get());
            com.copperslug.armasfuego.oeste.MosqueteItem.ponerBayoneta(sin, ItemStack.EMPTY);
            ItemStack con = new ItemStack(ModItems.MOSQUETE.get());
            com.copperslug.armasfuego.oeste.MosqueteItem.ponerBayoneta(con, new ItemStack(e));
            var id = net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "jei/mosquete_bayoneta_" + BuiltInRegistries.ITEM.getKey(e).getPath());
            bay.add(new net.minecraft.world.item.crafting.RecipeHolder<>(id, new net.minecraft.world.item.crafting.ShapelessRecipe("mosquete_bayoneta", net.minecraft.world.item.crafting.CraftingBookCategory.EQUIPMENT, con,
                    net.minecraft.core.NonNullList.of(net.minecraft.world.item.crafting.Ingredient.EMPTY,
                            net.minecraft.world.item.crafting.Ingredient.of(sin), net.minecraft.world.item.crafting.Ingredient.of(e)))));
        }
        ItemStack con = new ItemStack(ModItems.MOSQUETE.get());
        com.copperslug.armasfuego.oeste.MosqueteItem.ponerBayoneta(con, new ItemStack(Items.DIAMOND_SWORD));
        ItemStack sin = new ItemStack(ModItems.MOSQUETE.get());
        com.copperslug.armasfuego.oeste.MosqueteItem.ponerBayoneta(sin, ItemStack.EMPTY);
        bay.add(new net.minecraft.world.item.crafting.RecipeHolder<>(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "jei/mosquete_quitar_bayoneta"), new net.minecraft.world.item.crafting.ShapelessRecipe("mosquete_bayoneta",
                net.minecraft.world.item.crafting.CraftingBookCategory.EQUIPMENT, sin,
                net.minecraft.core.NonNullList.of(net.minecraft.world.item.crafting.Ingredient.EMPTY, net.minecraft.world.item.crafting.Ingredient.of(con)))));
        r.addRecipes(mezz.jei.api.constants.RecipeTypes.CRAFTING, bay);
    }

    private static void info(IRecipeRegistration r, Supplier<? extends Item> item, String clave) {
        r.addIngredientInfo(new ItemStack(item.get()), VanillaTypes.ITEM_STACK, Component.translatable("jei.copperslug.info." + clave));
    }
}

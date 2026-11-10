package com.copperslug.shim.client.extensions.common;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;

/**
 * Lo que usan las armas de IClientItemExtensions de Forge: la pose del brazo y la animación en primera persona. Cada
 * cargador lo engancha a su manera (Forge: las propiedades de render del objeto; Fabric: mixins).
 */
public interface IClientItemExtensions {
    default HumanoidModel.ArmPose getArmPose(LivingEntity e, InteractionHand h, ItemStack s) {
        return null;
    }

    /** true: el arma ya está colocada (vanilla no la mueve más); false: vanilla sigue con lo suyo. */
    default boolean applyForgeHandTransform(PoseStack ps, LocalPlayer p, HumanoidArm brazo, ItemStack s, float pt, float equipar, float golpe) {
        return false;
    }
}

package com.copperslug.forge.cliente;

import com.copperslug.plataforma.ClienteComun;
import com.copperslug.plataforma.PlataformaCliente;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;

public class PlataformaClienteForge implements PlataformaCliente {
    @Override
    public BakedModel modelo(ResourceLocation id) {
        return Minecraft.getInstance().getModelManager().getModel(new net.minecraft.client.resources.model.ModelResourceLocation(id, "standalone"));
    }

    @Override
    public BakedModel modeloPara(BakedModel m, net.minecraft.world.item.ItemDisplayContext ctx) {
        return m.applyTransform(ctx, new com.mojang.blaze3d.vertex.PoseStack(), false);
    }

    @Override
    public HumanoidModel.ArmPose poseBrazo(String nombre, boolean dosManos, ClienteComun.Pose pose) {
        return HumanoidModel.ArmPose.create(nombre, dosManos, pose::aplicar);
    }
}

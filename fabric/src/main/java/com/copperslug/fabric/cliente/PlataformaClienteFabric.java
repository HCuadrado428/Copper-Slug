package com.copperslug.fabric.cliente;

import com.copperslug.plataforma.ClienteComun;
import com.copperslug.plataforma.PlataformaCliente;
import net.fabricmc.fabric.api.client.model.BakedModelManagerHelper;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;

public class PlataformaClienteFabric implements PlataformaCliente {
    @Override
    public BakedModel modelo(ResourceLocation id) {
        var mm = Minecraft.getInstance().getModelManager();
        BakedModel m = BakedModelManagerHelper.getModel(mm, id);
        return m != null ? m : mm.getMissingModel();
    }

    @Override
    public HumanoidModel.ArmPose poseBrazo(String nombre, boolean dosManos, ClienteComun.Pose pose) {
        return PosesFabric.nueva(pose);
    }
}

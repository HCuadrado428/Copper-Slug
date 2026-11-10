package com.copperslug.plataforma;

import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;

import java.util.ServiceLoader;

/** Lo del cliente que cambia de un cargador a otro. */
public interface PlataformaCliente {
    PlataformaCliente P = ServiceLoader.load(PlataformaCliente.class, PlataformaCliente.class.getClassLoader()).findFirst()
            .orElseThrow(() -> new IllegalStateException("Copper Slug: no hay implementación de PlataformaCliente"));

    /** Un modelo suelto registrado con ModelEvent.RegisterAdditional. */
    BakedModel modelo(ResourceLocation id);

    /** Una pose de brazo nueva (Forge: constante nueva del enum; Fabric: ver PosesFabric). */
    HumanoidModel.ArmPose poseBrazo(String nombre, boolean dosManos, ClienteComun.Pose pose);
}

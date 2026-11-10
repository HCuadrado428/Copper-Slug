package com.copperslug.plataforma;

import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.entity.LivingEntity;

/** Atajos del cliente para el código de las armas (los usan los cambios de herramientas/portar.py). */
public final class ClienteComun {
    private ClienteComun() {}

    @FunctionalInterface
    public interface Pose {
        void aplicar(HumanoidModel<?> modelo, LivingEntity e, HumanoidArm brazo);
    }

    public static net.minecraft.world.level.Level nivel() {
        return net.minecraft.client.Minecraft.getInstance().level;
    }

    public static net.minecraft.core.RegistryAccess registros() {
        var l = net.minecraft.client.Minecraft.getInstance().level;
        return l == null ? null : l.registryAccess();
    }

    public static BakedModel modelo(ResourceLocation id) {
        return PlataformaCliente.P.modelo(id);
    }

    public static HumanoidModel.ArmPose poseBrazo(String nombre, boolean dosManos, Pose p) {
        return PlataformaCliente.P.poseBrazo(nombre, dosManos, p);
    }
}

package com.copperslug.neoforge.cliente;

import com.copperslug.plataforma.ClienteComun;
import net.minecraft.client.model.HumanoidModel;
import net.neoforged.fml.common.asm.enumextension.EnumProxy;
import net.neoforged.neoforge.client.IArmPoseTransformer;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Las poses de brazo nuevas: en NeoForge 1.21 se añaden al enum desde META-INF/enumextensions.json; cada una llama a la
 * pose que el código común le da con {@link ClienteComun#poseBrazo}.
 */
public final class PosesNeoForge {
    private PosesNeoForge() {}

    static final Map<String, ClienteComun.Pose> POSES = new ConcurrentHashMap<>();

    public static final EnumProxy<HumanoidModel.ArmPose> REVOLVER = new EnumProxy<>(HumanoidModel.ArmPose.class, false, transformador("COPPERSLUG_REVOLVER"));

    private static IArmPoseTransformer transformador(String nombre) {
        return (modelo, entidad, brazo) -> {
            var p = POSES.get(nombre);
            if (p != null) p.aplicar(modelo, entidad, brazo);
        };
    }
}

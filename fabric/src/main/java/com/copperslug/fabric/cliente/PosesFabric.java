package com.copperslug.fabric.cliente;

import com.copperslug.plataforma.ClienteComun;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.entity.LivingEntity;

import java.util.HashMap;
import java.util.Map;
import java.util.WeakHashMap;

/**
 * Poses de brazo propias en Fabric (en Forge son constantes nuevas de ArmPose). Cada una usa como marca una pose
 * vanilla que las armas no usan; cuando la pose de un brazo sale de las extensiones de un arma, se apunta para esa
 * entidad y, al final de setupAnim del modelo, se aplica la de verdad (ver HumanoidModelMixin).
 */
public final class PosesFabric {
    private PosesFabric() {}

    private static final HumanoidModel.ArmPose[] MARCAS = {HumanoidModel.ArmPose.TOOT_HORN, HumanoidModel.ArmPose.BRUSH};
    private static final Map<HumanoidModel.ArmPose, ClienteComun.Pose> POSES = new HashMap<>();
    private static final Map<LivingEntity, ClienteComun.Pose[]> AHORA = new WeakHashMap<>();
    private static int n;

    static HumanoidModel.ArmPose nueva(ClienteComun.Pose p) {
        HumanoidModel.ArmPose m = MARCAS[n++];
        POSES.put(m, p);
        return m;
    }

    /** Lo llama el mixin de getArmPose: lo que da el arma para ese brazo (null: nada propio). */
    public static void apuntar(LivingEntity e, HumanoidArm brazo, HumanoidModel.ArmPose pose) {
        ClienteComun.Pose p = pose == null ? null : POSES.get(pose);
        ClienteComun.Pose[] a = AHORA.get(e);
        if (p == null && a == null) return;
        if (a == null) AHORA.put(e, a = new ClienteComun.Pose[2]);
        a[brazo.ordinal()] = p;
    }

    public static void aplicar(HumanoidModel<?> m, LivingEntity e) {
        ClienteComun.Pose[] a = AHORA.get(e);
        if (a == null) return;
        if (a[HumanoidArm.RIGHT.ordinal()] != null) a[HumanoidArm.RIGHT.ordinal()].aplicar(m, e, HumanoidArm.RIGHT);
        if (a[HumanoidArm.LEFT.ordinal()] != null) a[HumanoidArm.LEFT.ordinal()].aplicar(m, e, HumanoidArm.LEFT);
    }
}

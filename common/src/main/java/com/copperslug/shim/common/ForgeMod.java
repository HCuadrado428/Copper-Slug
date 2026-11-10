package com.copperslug.shim.common;

import com.copperslug.plataforma.Plataforma;
import net.minecraft.world.entity.ai.attributes.Attribute;

import java.util.function.Supplier;

public final class ForgeMod {
    private ForgeMod() {}

    /** El alcance de ataque del cargador (null en Fabric 1.20.1, que no tiene). */
    public static final Supplier<Attribute> ENTITY_REACH = () -> Plataforma.get().alcanceAtaque();
}

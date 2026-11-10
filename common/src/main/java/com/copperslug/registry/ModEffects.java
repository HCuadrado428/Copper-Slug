package com.copperslug.registry;

import com.copperslug.CopperSlug;
import net.minecraft.world.effect.MobEffect;
import com.copperslug.shim.registries.DeferredRegister;
import com.copperslug.shim.registries.ForgeRegistries;
import com.copperslug.shim.registries.RegistryObject;

/** Generado por herramientas/portar.py a partir del ModEffects de Miscelánea (solo lo de las armas). */
public final class ModEffects {
    public static final DeferredRegister<MobEffect> EFFECTS =
            DeferredRegister.create(ForgeRegistries.MOB_EFFECTS, CopperSlug.MOD_ID);
    // ---- Escopeta de presión: pringado de miel (no deja saltar)
    public static final RegistryObject<MobEffect> PRINGADO = EFFECTS.register("pringado", com.copperslug.armasfuego.escopeta.PringadoEffect::new);

    private ModEffects() {}
}

package com.copperslug.armasfuego.comun;

import com.copperslug.CopperSlug;
import net.minecraft.core.particles.ParticleType;
import net.minecraft.core.particles.SimpleParticleType;
import com.copperslug.shim.eventbus.api.IEventBus;
import com.copperslug.shim.registries.DeferredRegister;
import com.copperslug.shim.registries.ForgeRegistries;
import com.copperslug.shim.registries.RegistryObject;

/** Partículas de las armas de fuego: el fogonazo de la boca y los casquillos que caen (las usan todas). */
public final class ArmasFuegoRegistro {
    private ArmasFuegoRegistro() {}

    public static final DeferredRegister<ParticleType<?>> PARTICULAS = DeferredRegister.create(ForgeRegistries.PARTICLE_TYPES, CopperSlug.MOD_ID);

    /** Fogonazo: una estrella de fuego que dura 2 ticks y brilla a oscuras (siempre se ve, aunque esté lejos). */
    public static final RegistryObject<SimpleParticleType> FOGONAZO = PARTICULAS.register("armafuego_fogonazo", () -> new SimpleParticleType(true));
    /** Casquillo de latón: sale volando, cae, rebota una vez en el suelo y desaparece. */
    public static final RegistryObject<SimpleParticleType> CASQUILLO = PARTICULAS.register("armafuego_casquillo", () -> new SimpleParticleType(false));

    public static void registrar(IEventBus bus) {
        PARTICULAS.register(bus);
    }
}

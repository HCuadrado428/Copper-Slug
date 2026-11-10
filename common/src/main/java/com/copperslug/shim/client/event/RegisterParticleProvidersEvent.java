package com.copperslug.shim.client.event;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.client.particle.ParticleEngine;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleType;

public class RegisterParticleProvidersEvent extends Event {
    public interface Registrador {
        <T extends ParticleOptions> void conSprites(ParticleType<T> tipo, ParticleEngine.SpriteParticleRegistration<T> prov);
    }

    private final Registrador r;

    public RegisterParticleProvidersEvent(Registrador r) {
        this.r = r;
    }

    public <T extends ParticleOptions> void registerSpriteSet(ParticleType<T> tipo, ParticleEngine.SpriteParticleRegistration<T> prov) {
        r.conSprites(tipo, prov);
    }
}

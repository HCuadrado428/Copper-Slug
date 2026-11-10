package com.copperslug.shim.client.event;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.resources.ResourceLocation;

import java.util.function.Consumer;

public class ModelEvent extends Event {
    /** Modelos sueltos (que no son de ningún objeto ni bloque) para dibujarlos a mano. */
    public static class RegisterAdditional extends ModelEvent {
        private final Consumer<ResourceLocation> f;

        public RegisterAdditional(Consumer<ResourceLocation> f) {
            this.f = f;
        }

        public void register(ResourceLocation r) {
            f.accept(r);
        }
    }
}

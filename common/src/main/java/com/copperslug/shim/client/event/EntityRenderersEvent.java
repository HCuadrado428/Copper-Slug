package com.copperslug.shim.client.event;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;

import java.util.function.BiConsumer;

public class EntityRenderersEvent extends Event {
    public static class RegisterRenderers extends EntityRenderersEvent {
        private final BiConsumer<EntityType<?>, EntityRendererProvider<?>> f;

        public RegisterRenderers(BiConsumer<EntityType<?>, EntityRendererProvider<?>> f) {
            this.f = f;
        }

        public <T extends Entity> void registerEntityRenderer(EntityType<? extends T> tipo, EntityRendererProvider<T> prov) {
            f.accept(tipo, prov);
        }
    }
}

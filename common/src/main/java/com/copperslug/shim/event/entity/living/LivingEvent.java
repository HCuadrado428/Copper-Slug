package com.copperslug.shim.event.entity.living;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.world.entity.LivingEntity;

public class LivingEvent extends Event {
    private final LivingEntity e;

    public LivingEvent(LivingEntity e) {
        this.e = e;
    }

    public LivingEntity getEntity() {
        return e;
    }

    public static class LivingJumpEvent extends LivingEvent {
        public LivingJumpEvent(LivingEntity e) {
            super(e);
        }
    }
}

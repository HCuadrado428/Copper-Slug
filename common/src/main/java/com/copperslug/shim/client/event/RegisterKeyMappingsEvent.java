package com.copperslug.shim.client.event;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.client.KeyMapping;

import java.util.function.Consumer;

public class RegisterKeyMappingsEvent extends Event {
    private final Consumer<KeyMapping> f;

    public RegisterKeyMappingsEvent(Consumer<KeyMapping> f) {
        this.f = f;
    }

    public void register(KeyMapping k) {
        f.accept(k);
    }
}

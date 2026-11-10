package com.copperslug.shim.registries;

import net.minecraft.resources.ResourceLocation;

import java.util.function.Supplier;

/** Lo registrado: get() da el objeto (en Forge, una vez cerrado el registro). */
public final class RegistryObject<T> implements Supplier<T> {
    private final ResourceLocation id;
    private final Supplier<T> s;

    RegistryObject(ResourceLocation id, Supplier<T> s) {
        this.id = id;
        this.s = s;
    }

    @Override
    public T get() {
        T t = s.get();
        if (t == null) throw new IllegalStateException("Copper Slug: " + id + " todavía no está registrado");
        return t;
    }

    public ResourceLocation getId() {
        return id;
    }

    public boolean isPresent() {
        try {
            return s.get() != null;
        } catch (RuntimeException e) {
            return false;
        }
    }
}

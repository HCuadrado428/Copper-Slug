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

    private net.minecraft.core.Holder<T> holder;

    /** En 1.21 muchas cosas (efectos, sonidos...) van como Holder. */
    @SuppressWarnings({"unchecked", "rawtypes"})
    public net.minecraft.core.Holder<T> holder() {
        if (holder != null) return holder;
        for (var r : net.minecraft.core.registries.BuiltInRegistries.REGISTRY) {
            if (r.containsKey(id) && r.get(id) == get()) return holder = ((net.minecraft.core.Registry) r).wrapAsHolder(get());
        }
        throw new IllegalStateException("Copper Slug: no encuentro el registro de " + id);
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

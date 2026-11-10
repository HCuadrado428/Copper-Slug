package com.copperslug.shim.registries;

import com.copperslug.plataforma.Plataforma;
import com.copperslug.shim.eventbus.api.IEventBus;
import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;

import java.util.function.Supplier;

/** Como el de Forge: cada register(...) se pasa a la plataforma, que lo da de alta cuando toque. */
public final class DeferredRegister<T> {
    private final ResourceKey<? extends Registry<T>> clave;
    private final String modid;

    private DeferredRegister(ResourceKey<? extends Registry<T>> clave, String modid) {
        this.clave = clave;
        this.modid = modid;
    }

    public static <T> DeferredRegister<T> create(ForgeRegistries.R<T> r, String modid) {
        return new DeferredRegister<>(r.clave(), modid);
    }

    public static <T> DeferredRegister<T> create(ResourceKey<? extends Registry<T>> clave, String modid) {
        return new DeferredRegister<>(clave, modid);
    }

    public <I extends T> RegistryObject<I> register(String nombre, Supplier<? extends I> fabrica) {
        ResourceLocation id = new ResourceLocation(modid, nombre);
        @SuppressWarnings("unchecked")
        Supplier<I> s = (Supplier<I>) (Supplier<?>) Plataforma.get().registrar(clave, id, fabrica);
        return new RegistryObject<>(id, s);
    }

    public void register(IEventBus bus) {}
}

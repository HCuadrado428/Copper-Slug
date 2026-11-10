package com.copperslug.shim.fml;

import com.copperslug.plataforma.Plataforma;
import com.copperslug.shim.api.distmarker.Dist;

import java.util.function.Supplier;

public final class DistExecutor {
    private DistExecutor() {}

    public static void unsafeRunWhenOn(Dist d, Supplier<Runnable> r) {
        if ((d == Dist.CLIENT) == Plataforma.get().esCliente()) r.get().run();
    }
}

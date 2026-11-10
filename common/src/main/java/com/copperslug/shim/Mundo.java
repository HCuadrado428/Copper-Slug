package com.copperslug.shim;

import com.copperslug.plataforma.Plataforma;
import net.minecraft.world.level.Level;

/** El nivel del cliente (las descripciones de los objetos, que en 1.21 ya no lo reciben). null en el servidor. */
public final class Mundo {
    private Mundo() {}

    public static Level cliente() {
        return Plataforma.get().esCliente() ? com.copperslug.plataforma.ClienteComun.nivel() : null;
    }
}

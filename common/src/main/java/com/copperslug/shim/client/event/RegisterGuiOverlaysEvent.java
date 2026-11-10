package com.copperslug.shim.client.event;

import com.copperslug.shim.client.gui.overlay.IGuiOverlay;
import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.resources.ResourceLocation;

import java.util.ArrayList;
import java.util.List;

/**
 * Capas del HUD. Aquí todas se dibujan al final del HUD vanilla, en el orden en que se registran (las que van "encima"
 * de la mira o del catalejo quedan igual encima de ellos).
 */
public class RegisterGuiOverlaysEvent extends Event {
    public record Capa(ResourceLocation encima, String id, IGuiOverlay capa) {}

    public static final List<Capa> CAPAS = new ArrayList<>();

    public void registerAbove(ResourceLocation otra, String id, IGuiOverlay o) {
        CAPAS.add(new Capa(otra, id, o));
    }

    public void registerAboveAll(String id, IGuiOverlay o) {
        CAPAS.add(new Capa(null, id, o));
    }

    public void registerBelowAll(String id, IGuiOverlay o) {
        CAPAS.add(0, new Capa(null, id, o));
    }
}

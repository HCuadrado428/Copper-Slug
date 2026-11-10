package com.copperslug.client;

import com.copperslug.Suscriptores;
import com.copperslug.shim.client.event.RegisterGuiOverlaysEvent;
import com.copperslug.shim.client.gui.overlay.ForgeGui;
import com.copperslug.shim.eventbus.api.Bus;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;

/** Arranque del cliente, común a los cargadores: suscribe las clases de cliente y guarda las capas del HUD. */
public final class ClienteInicio {
    private ClienteInicio() {}

    private static boolean hecho;

    public static void iniciar() {
        if (hecho) return;
        hecho = true;
        for (String c : Suscriptores.CLIENTE) {
            try {
                Bus.suscribir(Class.forName(c));
            } catch (ClassNotFoundException e) {
                throw new RuntimeException(e);
            }
        }
        if (com.copperslug.client.prueba.PruebaCI.ACTIVA) Bus.suscribir(com.copperslug.client.prueba.PruebaCI.class);
        Bus.post(new RegisterGuiOverlaysEvent());
    }

    /** Las capas del HUD de las armas, en orden (para los cargadores que no tienen capas con nombre). */
    public static void dibujarHud(GuiGraphics g, float pt) {
        Minecraft mc = Minecraft.getInstance();
        if (mc.options.hideGui) return;
        int w = g.guiWidth(), h = g.guiHeight();
        for (var c : RegisterGuiOverlaysEvent.CAPAS) c.capa().render(ForgeGui.I, g, pt, w, h);
    }
}

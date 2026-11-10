package com.copperslug.shim.client.gui.overlay;

import net.minecraft.client.gui.GuiGraphics;

@FunctionalInterface
public interface IGuiOverlay {
    void render(ForgeGui gui, GuiGraphics g, float pt, int ancho, int alto);
}

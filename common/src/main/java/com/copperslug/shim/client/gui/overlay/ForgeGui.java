package com.copperslug.shim.client.gui.overlay;

import net.minecraft.client.Minecraft;

/** El Gui de Forge en las capas del HUD: las armas solo miran el Minecraft. */
public final class ForgeGui {
    public static final ForgeGui I = new ForgeGui();

    private ForgeGui() {}

    public Minecraft getMinecraft() {
        return Minecraft.getInstance();
    }
}

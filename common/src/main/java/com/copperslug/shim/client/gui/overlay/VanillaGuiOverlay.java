package com.copperslug.shim.client.gui.overlay;

import net.minecraft.resources.ResourceLocation;

public enum VanillaGuiOverlay {
    CROSSHAIR("crosshair"), SPYGLASS("spyglass"), HOTBAR("hotbar"), HELMET("helmet");

    private final ResourceLocation id;

    VanillaGuiOverlay(String n) {
        id = new ResourceLocation("minecraft", n);
    }

    public ResourceLocation id() {
        return id;
    }
}

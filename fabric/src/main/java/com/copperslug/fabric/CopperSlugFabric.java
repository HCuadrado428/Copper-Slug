package com.copperslug.fabric;

import com.copperslug.CopperSlug;
import net.fabricmc.api.ModInitializer;

public class CopperSlugFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        CopperSlug.iniciar();
    }
}

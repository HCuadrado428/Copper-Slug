package com.copperslug;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Copper Slug: las nueve armas de fuego de cobre. Lo común a todos los cargadores empieza aquí. */
public final class CopperSlug {
    private CopperSlug() {}

    public static final String MOD_ID = "copperslug";
    public static final Logger LOG = LoggerFactory.getLogger("Copper Slug");

    public static void iniciar() {
        LOG.info("Copper Slug: cargando las armas de fuego");
    }
}

package com.copperslug;

import com.copperslug.armasfuego.comun.EquilibrioArmas;
import com.copperslug.shim.common.ForgeConfigSpec;

/**
 * Config del servidor (serverconfig/copperslug-server.toml dentro del mundo): dónde salen las tres primeras armas y,
 * en su sección, el equilibrio de todas ({@link EquilibrioArmas}). Las claves son las de Miscelánea.
 */
public final class ConfigServidor {
    private ConfigServidor() {}

    private static final ForgeConfigSpec.DoubleValue BOTIN_REVOLVER_HERREROS, BOTIN_REVOLVER_CASAS, BOTIN_ESCOPETA, BOTIN_RIFLE, BOTIN_ENCANTADA;
    public static final ForgeConfigSpec SPEC;

    static {
        ForgeConfigSpec.Builder b = new ForgeConfigSpec.Builder();
        b.comment("Armas de fuego: no se fabrican, se encuentran en cofres de estructuras vanilla.").push("armas");
        b.comment("Probabilidad (0-1) de que salga el arma en cada cofre.").push("armas_de_fuego");
        BOTIN_REVOLVER_HERREROS = b.comment("Revólver: cofres del armero, del herrero de herramientas y del de armas de las aldeas.")
                .defineInRange("revolver_aldea_herreros", 0.25, 0.0, 1.0);
        BOTIN_REVOLVER_CASAS = b.comment("Revólver: cofres de las casas de las aldeas.").defineInRange("revolver_aldea_casas", 0.06, 0.0, 1.0);
        BOTIN_ESCOPETA = b.comment("Escopeta de presión: cofres de los barcos hundidos (provisiones, tesoro y mapas).").defineInRange("escopeta_barco_hundido", 0.2, 0.0, 1.0);
        BOTIN_RIFLE = b.comment("Rifle de catalejo: cofres de los puestos de saqueadores.").defineInRange("rifle_puesto_saqueadores", 0.25, 0.0, 1.0);
        BOTIN_ENCANTADA = b.comment("Probabilidad de que el arma encontrada lleve uno de sus encantamientos propios.").defineInRange("encantada", 0.25, 0.0, 1.0);
        b.pop();
        b.pop();
        EquilibrioArmas.definir(b);
        SPEC = b.build();
    }

    public static double botinRevolverHerreros() { return BOTIN_REVOLVER_HERREROS.get(); }
    public static double botinRevolverCasas() { return BOTIN_REVOLVER_CASAS.get(); }
    public static double botinEscopeta() { return BOTIN_ESCOPETA.get(); }
    public static double botinRifle() { return BOTIN_RIFLE.get(); }
    public static double botinEncantada() { return BOTIN_ENCANTADA.get(); }
}

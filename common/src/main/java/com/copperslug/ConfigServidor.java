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
    private static final ForgeConfigSpec.BooleanValue MOBS_ACTIVADO;
    private static final ForgeConfigSpec.DoubleValue MOBS_PROB, MOBS_PROB_CAPITAN, MOBS_DANO, MOBS_SUELTA, MOBS_FALLO;
    private static final ForgeConfigSpec.IntValue MOBS_CADENCIA;
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
        b.comment("Mobs con armas: algunos saqueadores salen con una Winchester y disparan de verdad.").push("mobs_armados");
        MOBS_ACTIVADO = b.comment("Apagar esto deja a todos los mobs como en vanilla.").define("activado", true);
        MOBS_PROB = b.comment("Probabilidad (0-1) de que un saqueador salga armado.").defineInRange("probabilidad_saqueador", 0.05, 0.0, 1.0);
        MOBS_PROB_CAPITAN = b.comment("Lo mismo para el capitan de la patrulla (el del estandarte).").defineInRange("probabilidad_capitan", 0.3, 0.0, 1.0);
        MOBS_DANO = b.comment("Dano de cada bala de un mob (2 = un corazon).").defineInRange("dano", 4.0, 0.0, 40.0);
        MOBS_CADENCIA = b.comment("Ticks entre disparo y disparo de un mob (20 = 1 s).").defineInRange("cadencia", 40, 5, 400);
        MOBS_FALLO = b.comment("Cuanto fallan: multiplica la dispersion de los mobs (0 = no fallan nunca, 1 = normal, 2 = fallan el doble).").defineInRange("fallo", 1.0, 0.0, 5.0);
        MOBS_SUELTA = b.comment("Probabilidad (0-1) de que suelte el arma al morir.").defineInRange("suelta", 0.1, 0.0, 1.0);
        b.pop();
        EquilibrioArmas.definir(b);
        SPEC = b.build();
    }

    public static double botinRevolverHerreros() { return BOTIN_REVOLVER_HERREROS.get(); }
    public static double botinRevolverCasas() { return BOTIN_REVOLVER_CASAS.get(); }
    public static double botinEscopeta() { return BOTIN_ESCOPETA.get(); }
    public static double botinRifle() { return BOTIN_RIFLE.get(); }
    public static double botinEncantada() { return BOTIN_ENCANTADA.get(); }

    private static boolean b(ForgeConfigSpec.BooleanValue v) { try { return SPEC.isLoaded() ? v.get() : v.getDefault(); } catch (Exception e) { return v.getDefault(); } }
    private static double d(ForgeConfigSpec.DoubleValue v) { try { return SPEC.isLoaded() ? v.get() : v.getDefault(); } catch (Exception e) { return v.getDefault(); } }
    private static int i(ForgeConfigSpec.IntValue v) { try { return SPEC.isLoaded() ? v.get() : v.getDefault(); } catch (Exception e) { return v.getDefault(); } }
    public static boolean mobsArmados() { return b(MOBS_ACTIVADO); }
    public static double mobsProb() { return d(MOBS_PROB); }
    public static double mobsProbCapitan() { return d(MOBS_PROB_CAPITAN); }
    public static float mobsDano() { return (float) d(MOBS_DANO); }
    public static int mobsCadencia() { return i(MOBS_CADENCIA); }
    public static double mobsFallo() { return d(MOBS_FALLO); }
    public static float mobsSuelta() { return (float) d(MOBS_SUELTA); }
}

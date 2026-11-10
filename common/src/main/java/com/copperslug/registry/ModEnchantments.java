package com.copperslug.registry;

import com.copperslug.CopperSlug;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentCategory;
import com.copperslug.shim.registries.DeferredRegister;
import com.copperslug.shim.registries.ForgeRegistries;
import com.copperslug.shim.registries.RegistryObject;

/** Generado por herramientas/portar.py a partir del ModEnchantments de Miscelánea (solo lo de las armas). */
public final class ModEnchantments {
    public static final DeferredRegister<Enchantment> ENCHANTMENTS =
            DeferredRegister.create(ForgeRegistries.ENCHANTMENTS, CopperSlug.MOD_ID);
    // ---- Pistola (revólver de ruleta)
    public static final EnchantmentCategory REVOLVER =
            com.copperslug.shim.Categorias.create("COPPERSLUG_REVOLVER", item -> item instanceof com.copperslug.armasfuego.pistola.RevolverItem);
    public static final RegistryObject<Enchantment> REVOLVER_ABANICO = ENCHANTMENTS.register("revolver_abanico",
            () -> new com.copperslug.armasfuego.pistola.EncantamientoRevolver(Enchantment.Rarity.RARE, 1, 20, 0, ModEnchantments.REVOLVER_DESENFUNDE));
    public static final RegistryObject<Enchantment> REVOLVER_CARAMBOLA = ENCHANTMENTS.register("revolver_carambola",
            () -> new com.copperslug.armasfuego.pistola.EncantamientoRevolver(Enchantment.Rarity.UNCOMMON, 2, 10, 12, null));
    public static final RegistryObject<Enchantment> REVOLVER_DESENFUNDE = ENCHANTMENTS.register("revolver_desenfunde",
            () -> new com.copperslug.armasfuego.pistola.EncantamientoRevolver(Enchantment.Rarity.UNCOMMON, 1, 15, 0, ModEnchantments.REVOLVER_ABANICO));
    public static final RegistryObject<Enchantment> REVOLVER_SENALERO = ENCHANTMENTS.register("revolver_senalero",
            () -> new com.copperslug.armasfuego.pistola.EncantamientoRevolver(Enchantment.Rarity.UNCOMMON, 1, 8, 0, null));
    // ---- Rifle
    /** Solo para el rifle de catalejo. */
    public static final EnchantmentCategory RIFLE =
            com.copperslug.shim.Categorias.create("COPPERSLUG_RIFLE", item -> item instanceof com.copperslug.armasfuego.rifle.RifleItem);
    /** Mira quieta 2 s: el siguiente disparo va recto y hace más daño. */
    public static final RegistryObject<Enchantment> RESPIRACION = ENCHANTMENTS.register("respiracion_contenida",
            () -> new com.copperslug.armasfuego.rifle.RifleEncantamiento(Enchantment.Rarity.UNCOMMON, 3, 10, 10, RIFLE));
    /** La bala pasa por varios mobs y por bloques blandos. */
    public static final RegistryObject<Enchantment> ATRAVESAR = ENCHANTMENTS.register("atravesar",
            () -> new com.copperslug.armasfuego.rifle.RifleEncantamiento(Enchantment.Rarity.RARE, 3, 5, 10, RIFLE));
    /** Lo que se mira con la mira brilla un rato. */
    public static final RegistryObject<Enchantment> OJO_HALCON = ENCHANTMENTS.register("ojo_halcon",
            () -> new com.copperslug.armasfuego.rifle.RifleEncantamiento(Enchantment.Rarity.UNCOMMON, 2, 12, 15, RIFLE));
    /** Tirolinas más largas y más rápidas. */
    public static final RegistryObject<Enchantment> TIROLINERO = ENCHANTMENTS.register("tirolinero",
            () -> new com.copperslug.armasfuego.rifle.RifleEncantamiento(Enchantment.Rarity.UNCOMMON, 3, 5, 9, RIFLE));
    /** El disparo casi no hace ruido (ni lo notan el sculk ni el Warden). */
    public static final RegistryObject<Enchantment> SILENCIADOR = ENCHANTMENTS.register("silenciador",
            () -> new com.copperslug.armasfuego.rifle.RifleEncantamiento(Enchantment.Rarity.RARE, 1, 20, 0, RIFLE));
    // ---- Escopeta de presión
    public static final EnchantmentCategory ESCOPETA_PRESION =
            com.copperslug.shim.Categorias.create("COPPERSLUG_ESCOPETA_PRESION", item -> item instanceof com.copperslug.armasfuego.escopeta.EscopetaPresionItem);
    public static final RegistryObject<Enchantment> ESCOPETA_COMPRESOR = ENCHANTMENTS.register("escopeta_compresor",
            () -> new com.copperslug.armasfuego.escopeta.EncantamientoEscopeta(com.copperslug.armasfuego.escopeta.Presion.Encantamiento.COMPRESOR, Enchantment.Rarity.UNCOMMON, 3, 10, 15));
    public static final RegistryObject<Enchantment> ESCOPETA_VALVULA = ENCHANTMENTS.register("escopeta_valvula_seguridad",
            () -> new com.copperslug.armasfuego.escopeta.EncantamientoEscopeta(com.copperslug.armasfuego.escopeta.Presion.Encantamiento.VALVULA, Enchantment.Rarity.RARE, 1, 20, 0));
    public static final RegistryObject<Enchantment> ESCOPETA_DOBLE_CAMARA = ENCHANTMENTS.register("escopeta_doble_camara",
            () -> new com.copperslug.armasfuego.escopeta.EncantamientoEscopeta(com.copperslug.armasfuego.escopeta.Presion.Encantamiento.DOBLE_CAMARA, Enchantment.Rarity.RARE, 1, 20, 0));
    public static final RegistryObject<Enchantment> ESCOPETA_FUELLE = ENCHANTMENTS.register("escopeta_fuelle",
            () -> new com.copperslug.armasfuego.escopeta.EncantamientoEscopeta(com.copperslug.armasfuego.escopeta.Presion.Encantamiento.FUELLE, Enchantment.Rarity.COMMON, 3, 5, 10));
    public static final RegistryObject<Enchantment> ESCOPETA_RECICLAJE = ENCHANTMENTS.register("escopeta_reciclaje",
            () -> new com.copperslug.armasfuego.escopeta.EncantamientoEscopeta(com.copperslug.armasfuego.escopeta.Presion.Encantamiento.RECICLAJE, Enchantment.Rarity.UNCOMMON, 3, 10, 12));
    // ---- Armas de fuego, segunda tanda: dos o tres encantamientos propios por arma (mesa y libros)
    public static final EnchantmentCategory GATLING = com.copperslug.shim.Categorias.create("COPPERSLUG_GATLING", item -> item instanceof com.copperslug.armasfuego.gatling.GatlingItem);
    public static final RegistryObject<Enchantment> GATLING_REFRIGERACION = ENCHANTMENTS.register("gatling_refrigeracion",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, GATLING, 3, 8, 10));
    public static final RegistryObject<Enchantment> GATLING_CINTA_LARGA = ENCHANTMENTS.register("gatling_cinta_larga",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, GATLING, 2, 10, 12));
    public static final RegistryObject<Enchantment> GATLING_ENGRASADA = ENCHANTMENTS.register("gatling_engrasada",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.RARE, GATLING, 1, 15, 0));
    /** Torreta (Portal): con redstone y nadie a los mandos, apunta sola a lo hostil que tenga delante. */
    public static final RegistryObject<Enchantment> GATLING_TORRETA = ENCHANTMENTS.register("gatling_torreta",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.VERY_RARE, GATLING, 1, 20, 0));
    public static final EnchantmentCategory WINCHESTER = com.copperslug.shim.Categorias.create("COPPERSLUG_WINCHESTER", item -> item instanceof com.copperslug.armasfuego.oeste.WinchesterItem);
    public static final RegistryObject<Enchantment> WINCHESTER_REPETICION = ENCHANTMENTS.register("winchester_repeticion",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, WINCHESTER, 3, 8, 10));
    public static final RegistryObject<Enchantment> WINCHESTER_DEAD_EYE = ENCHANTMENTS.register("winchester_dead_eye",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.RARE, WINCHESTER, 1, 20, 0));
    public static final RegistryObject<Enchantment> WINCHESTER_CARGA_RAPIDA = ENCHANTMENTS.register("winchester_carga_rapida",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.COMMON, WINCHESTER, 2, 5, 10));
    /** Depósito largo: 3 balas más por nivel. */
    public static final RegistryObject<Enchantment> WINCHESTER_DEPOSITO = ENCHANTMENTS.register("winchester_deposito",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, WINCHESTER, 2, 8, 12));
    public static final EnchantmentCategory DERRINGER = com.copperslug.shim.Categorias.create("COPPERSLUG_DERRINGER", item -> item instanceof com.copperslug.armasfuego.oeste.DerringerItem);
    public static final RegistryObject<Enchantment> DERRINGER_AS = ENCHANTMENTS.register("derringer_as",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, DERRINGER, 2, 10, 12));
    public static final RegistryObject<Enchantment> DERRINGER_DOBLE = ENCHANTMENTS.register("derringer_doble",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.RARE, DERRINGER, 1, 18, 0));
    /** Prestidigitador: al sacarla de la manga, mete sola una bala si le falta. */
    public static final RegistryObject<Enchantment> DERRINGER_PRESTIDIGITADOR = ENCHANTMENTS.register("derringer_prestidigitador",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.RARE, DERRINGER, 1, 15, 0));
    public static final EnchantmentCategory THOMPSON = com.copperslug.shim.Categorias.create("COPPERSLUG_THOMPSON", item -> item instanceof com.copperslug.armasfuego.oeste.ThompsonItem);
    public static final RegistryObject<Enchantment> THOMPSON_CHICAGO = ENCHANTMENTS.register("thompson_chicago",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, THOMPSON, 2, 10, 12));
    public static final RegistryObject<Enchantment> THOMPSON_COMPENSADOR = ENCHANTMENTS.register("thompson_compensador",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.COMMON, THOMPSON, 3, 5, 9));
    /** Gatillo fácil: dispara más deprisa (un 25 % más de balas por segundo por nivel). */
    public static final RegistryObject<Enchantment> THOMPSON_GATILLO = ENCHANTMENTS.register("thompson_gatillo",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, THOMPSON, 2, 10, 12));
    public static final EnchantmentCategory MOSQUETE = com.copperslug.shim.Categorias.create("COPPERSLUG_MOSQUETE", item -> item instanceof com.copperslug.armasfuego.oeste.MosqueteItem);
    public static final RegistryObject<Enchantment> MOSQUETE_BAQUETA = ENCHANTMENTS.register("mosquete_baqueta",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.COMMON, MOSQUETE, 3, 5, 9));
    public static final RegistryObject<Enchantment> MOSQUETE_POLVORA_SECA = ENCHANTMENTS.register("mosquete_polvora_seca",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.RARE, MOSQUETE, 1, 15, 0));
    public static final RegistryObject<Enchantment> MOSQUETE_CARGA = ENCHANTMENTS.register("mosquete_carga",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, MOSQUETE, 2, 10, 10));
    /** Pedernal fino: la chispa prende antes y falla menos. */
    public static final RegistryObject<Enchantment> MOSQUETE_PEDERNAL = ENCHANTMENTS.register("mosquete_pedernal",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, MOSQUETE, 2, 8, 12));
    public static final EnchantmentCategory CANON = com.copperslug.shim.Categorias.create("COPPERSLUG_CANON", item -> item instanceof com.copperslug.armasfuego.oeste.CanonManoItem);
    public static final RegistryObject<Enchantment> CANON_MECHA_CORTA = ENCHANTMENTS.register("canon_mecha_corta",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, CANON, 2, 8, 12));
    public static final RegistryObject<Enchantment> CANON_BIEN_FUNDIDO = ENCHANTMENTS.register("canon_bien_fundido",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.RARE, CANON, 1, 15, 0));
    /** Pólvora fina: el bolaño sale un 20 % más deprisa (llega más lejos) por nivel. */
    public static final RegistryObject<Enchantment> CANON_POLVORA_FINA = ENCHANTMENTS.register("canon_polvora_fina",
            () -> new com.copperslug.armasfuego.comun.EncantamientoFuego(Enchantment.Rarity.UNCOMMON, CANON, 2, 8, 12));

    private ModEnchantments() {}
}

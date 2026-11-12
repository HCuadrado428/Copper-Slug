package com.copperslug.registry;

import com.copperslug.CopperSlug;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.enchantment.Enchantment;

/**
 * Los encantamientos de las armas. En 1.21 son datos (data/copperslug/enchantment, generados por
 * herramientas/a_1_21_1.py desde el ModEnchantments de 1.20.1); aquí solo quedan sus claves.
 */
public final class ModEnchantments {
    private ModEnchantments() {}

    public static final ResourceKey<Enchantment> REVOLVER_ABANICO = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "revolver_abanico"));
    public static final ResourceKey<Enchantment> REVOLVER_CARAMBOLA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "revolver_carambola"));
    public static final ResourceKey<Enchantment> REVOLVER_DESENFUNDE = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "revolver_desenfunde"));
    public static final ResourceKey<Enchantment> REVOLVER_SENALERO = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "revolver_senalero"));
    public static final ResourceKey<Enchantment> RESPIRACION = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "respiracion_contenida"));
    public static final ResourceKey<Enchantment> ATRAVESAR = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "atravesar"));
    public static final ResourceKey<Enchantment> OJO_HALCON = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "ojo_halcon"));
    public static final ResourceKey<Enchantment> TIROLINERO = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "tirolinero"));
    public static final ResourceKey<Enchantment> SILENCIADOR = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "silenciador"));
    public static final ResourceKey<Enchantment> ESCOPETA_COMPRESOR = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "escopeta_compresor"));
    public static final ResourceKey<Enchantment> ESCOPETA_VALVULA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "escopeta_valvula_seguridad"));
    public static final ResourceKey<Enchantment> ESCOPETA_DOBLE_CAMARA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "escopeta_doble_camara"));
    public static final ResourceKey<Enchantment> ESCOPETA_FUELLE = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "escopeta_fuelle"));
    public static final ResourceKey<Enchantment> ESCOPETA_RECICLAJE = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "escopeta_reciclaje"));
    public static final ResourceKey<Enchantment> GATLING_REFRIGERACION = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "gatling_refrigeracion"));
    public static final ResourceKey<Enchantment> GATLING_CINTA_LARGA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "gatling_cinta_larga"));
    public static final ResourceKey<Enchantment> GATLING_ENGRASADA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "gatling_engrasada"));
    public static final ResourceKey<Enchantment> GATLING_TORRETA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "gatling_torreta"));
    public static final ResourceKey<Enchantment> WINCHESTER_REPETICION = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "winchester_repeticion"));
    public static final ResourceKey<Enchantment> WINCHESTER_DEAD_EYE = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "winchester_dead_eye"));
    public static final ResourceKey<Enchantment> WINCHESTER_CARGA_RAPIDA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "winchester_carga_rapida"));
    public static final ResourceKey<Enchantment> WINCHESTER_DEPOSITO = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "winchester_deposito"));
    public static final ResourceKey<Enchantment> DERRINGER_AS = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "derringer_as"));
    public static final ResourceKey<Enchantment> DERRINGER_DOBLE = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "derringer_doble"));
    public static final ResourceKey<Enchantment> DERRINGER_PRESTIDIGITADOR = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "derringer_prestidigitador"));
    public static final ResourceKey<Enchantment> THOMPSON_CHICAGO = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "thompson_chicago"));
    public static final ResourceKey<Enchantment> THOMPSON_COMPENSADOR = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "thompson_compensador"));
    public static final ResourceKey<Enchantment> THOMPSON_GATILLO = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "thompson_gatillo"));
    public static final ResourceKey<Enchantment> MOSQUETE_BAQUETA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "mosquete_baqueta"));
    public static final ResourceKey<Enchantment> MOSQUETE_POLVORA_SECA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "mosquete_polvora_seca"));
    public static final ResourceKey<Enchantment> MOSQUETE_CARGA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "mosquete_carga"));
    public static final ResourceKey<Enchantment> MOSQUETE_PEDERNAL = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "mosquete_pedernal"));
    public static final ResourceKey<Enchantment> CANON_MECHA_CORTA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "canon_mecha_corta"));
    public static final ResourceKey<Enchantment> CANON_BIEN_FUNDIDO = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "canon_bien_fundido"));
    public static final ResourceKey<Enchantment> CANON_POLVORA_FINA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "canon_polvora_fina"));
    /** Pulso firme: apuntando, dispersa menos y se anda menos lento (data/copperslug/enchantment/pulso_firme.json). */
    public static final ResourceKey<Enchantment> PULSO_FIRME = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "pulso_firme"));
    public static final ResourceKey<Enchantment> CANON_LARGO = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "revolver_canon_largo"));
    public static final ResourceKey<Enchantment> ESCOPETA_ESTRANGULADOR = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "escopeta_estrangulador"));
    public static final ResourceKey<Enchantment> MOSQUETE_MIRA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "mosquete_mira"));
    public static final ResourceKey<Enchantment> CANON_ANIMA = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "canon_anima"));
}

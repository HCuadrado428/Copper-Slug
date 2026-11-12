package com.copperslug.registry;

import com.copperslug.CopperSlug;
import net.minecraft.world.item.Tiers;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import com.copperslug.shim.registries.DeferredRegister;
import com.copperslug.shim.registries.ForgeRegistries;
import com.copperslug.shim.registries.RegistryObject;

/** Generado por herramientas/portar.py a partir del ModItems de Miscelánea (solo lo de las armas). */
public final class ModItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, CopperSlug.MOD_ID);
    // ---- Pistola (revólver de ruleta de cobre y su munición)
    public static final RegistryObject<Item> REVOLVER = ITEMS.register("revolver",
            () -> new com.copperslug.armasfuego.pistola.RevolverItem(new Item.Properties().stacksTo(1).rarity(Rarity.UNCOMMON)));
    public static final RegistryObject<Item> REVOLVER_BALA = ITEMS.register("revolver_bala", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> REVOLVER_BENGALA = ITEMS.register("revolver_bengala", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> REVOLVER_DARDO = ITEMS.register("revolver_dardo", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> REVOLVER_FOGUEO = ITEMS.register("revolver_fogueo", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> REVOLVER_IMAN = ITEMS.register("revolver_iman", () -> new Item(new Item.Properties()));
    // ---- Rifle
    /** Rifle de catalejo: rifle de cerrojo con un catalejo montado (durabilidad: se puede encantar). */
    public static final RegistryObject<Item> RIFLE = ITEMS.register("rifle",
            () -> new com.copperslug.armasfuego.rifle.RifleItem(new Item.Properties().durability(500).rarity(Rarity.UNCOMMON)));
    public static final RegistryObject<Item> BALA_RIFLE = ITEMS.register("bala_rifle",
            () -> new com.copperslug.armasfuego.rifle.MunicionRifleItem("item.copperslug.bala_rifle.ayuda", new Item.Properties()));
    public static final RegistryObject<Item> BALA_TRAZADORA = ITEMS.register("bala_trazadora",
            () -> new com.copperslug.armasfuego.rifle.MunicionRifleItem("item.copperslug.bala_trazadora.ayuda", new Item.Properties()));
    public static final RegistryObject<Item> BALA_CUERDA = ITEMS.register("bala_cuerda",
            () -> new com.copperslug.armasfuego.rifle.MunicionRifleItem("item.copperslug.bala_cuerda.ayuda", new Item.Properties().stacksTo(16)));
    public static final RegistryObject<Item> CASQUILLO_RIFLE = ITEMS.register("casquillo_rifle", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> PALOMITAS = ITEMS.register("palomitas",
            () -> new Item(new Item.Properties().stacksTo(16).food(new net.minecraft.world.food.FoodProperties.Builder().nutrition(6).saturationModifier(0.5F).build())));
    // ---- Escopeta de presión
    public static final RegistryObject<Item> ESCOPETA_PRESION = ITEMS.register("escopeta_presion",
            () -> new com.copperslug.armasfuego.escopeta.EscopetaPresionItem(new Item.Properties().durability(350).rarity(Rarity.UNCOMMON)));
    private static final java.util.Map<com.copperslug.armasfuego.escopeta.TipoCartucho, RegistryObject<Item>> ESCOPETA_CARTUCHOS =
            new java.util.EnumMap<>(com.copperslug.armasfuego.escopeta.TipoCartucho.class);
    static {
        for (com.copperslug.armasfuego.escopeta.TipoCartucho t : com.copperslug.armasfuego.escopeta.TipoCartucho.values())
            ESCOPETA_CARTUCHOS.put(t, ITEMS.register("escopeta_cartucho_" + t.id,
                    () -> new com.copperslug.armasfuego.escopeta.CartuchoPresionItem(t, new Item.Properties())));
    }
    public static Item escopetaCartucho(com.copperslug.armasfuego.escopeta.TipoCartucho t) {
        return ESCOPETA_CARTUCHOS.get(t).get();
    }
    // ---- Armas de fuego (segunda tanda): Gatling, Winchester, Derringer, Thompson, mosquete y cañón de mano
    public static final RegistryObject<Item> GATLING = ITEMS.register("gatling",
            () -> new com.copperslug.armasfuego.gatling.GatlingItem(new Item.Properties().durability(1500).rarity(Rarity.RARE)));
    public static final RegistryObject<Item> CINTA_GATLING = ITEMS.register("cinta_gatling",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(16)));
    public static final RegistryObject<Item> WINCHESTER = ITEMS.register("winchester",
            () -> new com.copperslug.armasfuego.oeste.WinchesterItem(new Item.Properties().durability(700).rarity(Rarity.UNCOMMON)));
    public static final RegistryObject<Item> DERRINGER = ITEMS.register("derringer",
            () -> new com.copperslug.armasfuego.oeste.DerringerItem(new Item.Properties().durability(300).rarity(Rarity.UNCOMMON)));
    public static final RegistryObject<Item> BALA_DERRINGER = ITEMS.register("bala_derringer",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> THOMPSON = ITEMS.register("thompson",
            () -> new com.copperslug.armasfuego.oeste.ThompsonItem(new Item.Properties().durability(1200).rarity(Rarity.RARE)));
    public static final RegistryObject<Item> CARGADOR_THOMPSON = ITEMS.register("cargador_thompson",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(8)));
    public static final RegistryObject<Item> ESTUCHE_VIOLIN = ITEMS.register("estuche_violin",
            () -> new com.copperslug.armasfuego.oeste.EstucheViolinItem(new Item.Properties().stacksTo(1)));
    public static final RegistryObject<Item> MOSQUETE = ITEMS.register("mosquete",
            () -> new com.copperslug.armasfuego.oeste.MosqueteItem(new Item.Properties().durability(500).rarity(Rarity.UNCOMMON)));
    public static final RegistryObject<Item> BOLA_MOSQUETE = ITEMS.register("bola_mosquete",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> CANON_MANO = ITEMS.register("canon_mano",
            () -> new com.copperslug.armasfuego.oeste.CanonManoItem(new Item.Properties().durability(250).rarity(Rarity.UNCOMMON)));
    // munición rara nueva para las tres primeras: tiempo bala (revólver) y pintura (rifle); la de goma va con los cartuchos de la escopeta
    public static final RegistryObject<Item> REVOLVER_TIEMPO = ITEMS.register("revolver_tiempo", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> BALA_PINTURA = ITEMS.register("bala_pintura",
            () -> new com.copperslug.armasfuego.rifle.MunicionRifleItem("item.copperslug.bala_pintura.ayuda", new Item.Properties()));
    // munición especial de las seis nuevas (dos por arma)
    public static final RegistryObject<Item> BALA_PLATA = ITEMS.register("bala_plata",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> BALA_DINAMITA = ITEMS.register("bala_dinamita",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> CARTA_MARCADA = ITEMS.register("carta_marcada",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> BALA_ORO = ITEMS.register("bala_oro",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> TAMBOR_TRAZADOR = ITEMS.register("tambor_trazador",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(8)));
    public static final RegistryObject<Item> TAMBOR_AGUA = ITEMS.register("tambor_agua",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(8)));
    public static final RegistryObject<Item> CINTA_INCENDIARIA = ITEMS.register("cinta_incendiaria",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(16)));
    public static final RegistryObject<Item> CINTA_PALOMITAS = ITEMS.register("cinta_palomitas",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(16)));
    public static final RegistryObject<Item> METRALLA = ITEMS.register("metralla",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> BOLA_CADENA = ITEMS.register("bola_cadena",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> BOLANO_INCENDIARIO = ITEMS.register("bolano_incendiario",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(16)));
    public static final RegistryObject<Item> BOLANO_FUEGOS = ITEMS.register("bolano_fuegos",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(16)));
    // la tercera munición especial de cada una (1.1.0)
    public static final RegistryObject<Item> BALA_HIELO = ITEMS.register("bala_hielo",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> BALA_HUMO = ITEMS.register("bala_humo",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> TAMBOR_TINTA = ITEMS.register("tambor_tinta",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(8)));
    public static final RegistryObject<Item> CINTA_GUISANTES = ITEMS.register("cinta_guisantes",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(16)));
    public static final RegistryObject<Item> BOLA_ARPON = ITEMS.register("bola_arpon",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> BOLANO_SALTARIN = ITEMS.register("bolano_saltarin",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(16)));

    // ---- Cerbatana de cobre (templos de la jungla) y sus dardos
    public static final RegistryObject<Item> CERBATANA = ITEMS.register("cerbatana",
            () -> new com.copperslug.armasfuego.selva.CerbatanaItem(new Item.Properties().durability(250).rarity(Rarity.UNCOMMON)));
    public static final RegistryObject<Item> DARDO_CERBATANA = ITEMS.register("dardo_cerbatana",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> DARDO_VENENO = ITEMS.register("dardo_veneno",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));
    public static final RegistryObject<Item> DARDO_SOMNIFERO = ITEMS.register("dardo_somnifero",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties()));

    // ---- Lanzallamas de cobre (fortalezas del Nether) y su bidón
    public static final RegistryObject<Item> LANZALLAMAS = ITEMS.register("lanzallamas",
            () -> new com.copperslug.armasfuego.nether.LanzallamasItem(new Item.Properties().durability(400).rarity(Rarity.RARE)));
    public static final RegistryObject<Item> BIDON_COMBUSTIBLE = ITEMS.register("bidon_combustible",
            () -> new com.copperslug.armasfuego.comun.MunicionItem(new Item.Properties().stacksTo(8)));

    private ModItems() {}
}

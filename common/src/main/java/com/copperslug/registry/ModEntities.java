package com.copperslug.registry;

import com.copperslug.CopperSlug;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import com.copperslug.shim.registries.DeferredRegister;
import com.copperslug.shim.registries.ForgeRegistries;
import com.copperslug.shim.registries.RegistryObject;

/** Generado por herramientas/portar.py a partir del ModEntities de Miscelánea (solo lo de las armas). */
public final class ModEntities {
    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(ForgeRegistries.ENTITY_TYPES, CopperSlug.MOD_ID);
    // ---- Pistola (bengala del revólver: se ve de lejos)
    public static final RegistryObject<EntityType<com.copperslug.armasfuego.pistola.BengalaEntity>> REVOLVER_BENGALA = ENTITIES.register("revolver_bengala",
            () -> EntityType.Builder.<com.copperslug.armasfuego.pistola.BengalaEntity>of(com.copperslug.armasfuego.pistola.BengalaEntity::new, MobCategory.MISC)
                    .sized(0.25F, 0.25F).clientTrackingRange(16).updateInterval(2).fireImmune().build("revolver_bengala"));
    // ---- Rifle
    public static final RegistryObject<EntityType<com.copperslug.armasfuego.rifle.BalaRifle>> BALA_RIFLE = ENTITIES.register("bala_rifle",
            () -> EntityType.Builder.<com.copperslug.armasfuego.rifle.BalaRifle>of(com.copperslug.armasfuego.rifle.BalaRifle::new, MobCategory.MISC)
                    .sized(0.1F, 0.1F).clientTrackingRange(12).updateInterval(1).noSummon().build("bala_rifle"));
    public static final RegistryObject<EntityType<com.copperslug.armasfuego.rifle.GanchoTirolina>> GANCHO_TIROLINA = ENTITIES.register("gancho_tirolina",
            () -> EntityType.Builder.<com.copperslug.armasfuego.rifle.GanchoTirolina>of(com.copperslug.armasfuego.rifle.GanchoTirolina::new, MobCategory.MISC)
                    .sized(0.4F, 0.4F).clientTrackingRange(10).updateInterval(1).noSummon().build("gancho_tirolina"));
    // ---- Armas de fuego (segunda tanda)
    public static final RegistryObject<EntityType<com.copperslug.armasfuego.gatling.GatlingEntity>> GATLING = ENTITIES.register("gatling",
            () -> EntityType.Builder.<com.copperslug.armasfuego.gatling.GatlingEntity>of(com.copperslug.armasfuego.gatling.GatlingEntity::new, MobCategory.MISC)
                    .sized(1.0F, 1.3F).clientTrackingRange(10).updateInterval(2).build("gatling"));
    public static final RegistryObject<EntityType<com.copperslug.armasfuego.oeste.BolaCanonEntity>> BOLA_CANON = ENTITIES.register("bola_canon",
            () -> EntityType.Builder.<com.copperslug.armasfuego.oeste.BolaCanonEntity>of(com.copperslug.armasfuego.oeste.BolaCanonEntity::new, MobCategory.MISC)
                    .sized(0.4F, 0.4F).clientTrackingRange(8).updateInterval(1).noSummon().build("bola_canon"));

    private ModEntities() {}
}

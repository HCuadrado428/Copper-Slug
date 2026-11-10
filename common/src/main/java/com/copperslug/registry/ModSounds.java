package com.copperslug.registry;

import com.copperslug.CopperSlug;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import com.copperslug.shim.registries.DeferredRegister;
import com.copperslug.shim.registries.ForgeRegistries;
import com.copperslug.shim.registries.RegistryObject;

/** Generado por herramientas/portar.py a partir del ModSounds de Miscelánea (solo lo de las armas). */
public final class ModSounds {
    public static final DeferredRegister<SoundEvent> SOUNDS =
            DeferredRegister.create(ForgeRegistries.SOUND_EVENTS, CopperSlug.MOD_ID);
    // ---- Pistola (revólver de ruleta)
    public static final RegistryObject<SoundEvent> REVOLVER_DISPARO = register("revolver_disparo");
    public static final RegistryObject<SoundEvent> REVOLVER_FOGUEO = register("revolver_fogueo");
    public static final RegistryObject<SoundEvent> REVOLVER_VACIO = register("revolver_vacio");
    public static final RegistryObject<SoundEvent> REVOLVER_CARGAR = register("revolver_cargar");
    public static final RegistryObject<SoundEvent> REVOLVER_RULETA = register("revolver_ruleta");
    public static final RegistryObject<SoundEvent> REVOLVER_REBOTE = register("revolver_rebote");
    public static final RegistryObject<SoundEvent> REVOLVER_AMARTILLAR = register("revolver_amartillar");
    public static final RegistryObject<SoundEvent> REVOLVER_DUELO = register("revolver_duelo");
    // ---- Armas de fuego (segunda tanda y sonidos nuevos de las tres primeras)
    public static final RegistryObject<SoundEvent> ARMAFUEGO_ATASCO = register("armafuego_atasco");
    public static final RegistryObject<SoundEvent> CASQUILLO_SUELO = register("casquillo_suelo");
    public static final RegistryObject<SoundEvent> GATLING_DISPARO = register("gatling_disparo");
    public static final RegistryObject<SoundEvent> GATLING_MANIVELA = register("gatling_manivela");
    public static final RegistryObject<SoundEvent> GATLING_VAPOR = register("gatling_vapor");
    public static final RegistryObject<SoundEvent> GATLING_CINTA = register("gatling_cinta");
    public static final RegistryObject<SoundEvent> WINCHESTER_DISPARO = register("winchester_disparo");
    public static final RegistryObject<SoundEvent> WINCHESTER_PALANCA = register("winchester_palanca");
    public static final RegistryObject<SoundEvent> WINCHESTER_CARGAR = register("winchester_cargar");
    public static final RegistryObject<SoundEvent> DERRINGER_DISPARO = register("derringer_disparo");
    public static final RegistryObject<SoundEvent> DERRINGER_ABRIR = register("derringer_abrir");
    public static final RegistryObject<SoundEvent> THOMPSON_DISPARO = register("thompson_disparo");
    public static final RegistryObject<SoundEvent> THOMPSON_TAMBOR = register("thompson_tambor");
    public static final RegistryObject<SoundEvent> MOSQUETE_CAZOLETA = register("mosquete_cazoleta");
    public static final RegistryObject<SoundEvent> MOSQUETE_DISPARO = register("mosquete_disparo");
    public static final RegistryObject<SoundEvent> MOSQUETE_BAQUETA = register("mosquete_baqueta");
    public static final RegistryObject<SoundEvent> CANON_MECHA = register("canon_mecha");
    public static final RegistryObject<SoundEvent> CANON_DISPARO = register("canon_disparo");
    public static final RegistryObject<SoundEvent> VIOLIN_DESAFINADO = register("violin_desafinado");
    public static final RegistryObject<SoundEvent> VIOLIN_NOTA = register("violin_nota");
    public static final RegistryObject<SoundEvent> ARPON = register("arpon");
    public static final RegistryObject<SoundEvent> RIFLE_CATALEJO_DISPARO = register("rifle_catalejo_disparo");
    public static final RegistryObject<SoundEvent> PRESION_DISPARO = register("presion_disparo");
    public static final RegistryObject<SoundEvent> TIEMPO_BALA = register("tiempo_bala");
    public static final RegistryObject<SoundEvent> GOMA_REBOTE = register("goma_rebote");
    public static final RegistryObject<SoundEvent> PINTURA_SPLAT = register("pintura_splat");
    private static RegistryObject<SoundEvent> register(String name) {
        return SOUNDS.register(name,
                () -> SoundEvent.createVariableRangeEvent(new ResourceLocation(CopperSlug.MOD_ID, name)));
    }

    private ModSounds() {}
}

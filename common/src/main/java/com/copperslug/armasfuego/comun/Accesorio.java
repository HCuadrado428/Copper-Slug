package com.copperslug.armasfuego.comun;

import com.copperslug.armasfuego.gatling.GatlingItem;
import com.copperslug.armasfuego.escopeta.EscopetaPresionItem;
import com.copperslug.armasfuego.oeste.CanonManoItem;
import com.copperslug.armasfuego.oeste.DerringerItem;
import com.copperslug.armasfuego.oeste.MosqueteItem;
import com.copperslug.armasfuego.oeste.ThompsonItem;
import com.copperslug.armasfuego.oeste.WinchesterItem;
import com.copperslug.armasfuego.pistola.RevolverItem;
import com.copperslug.armasfuego.rifle.RifleItem;
import net.minecraft.world.item.Item;

/**
 * Los accesorios de cobre: uno por arma, cada uno solo vale para la suya. Se montan en el yunque (arma a la izquierda,
 * accesorio a la derecha, 2 niveles); un arma lleva uno a la vez (montar otro cambia el anterior).
 */
public enum Accesorio {
    CANON_LARGO("canon_largo", RevolverItem.class, 0.6F, 1F, 0, false),
    BIPODE("bipode", RifleItem.class, 0.5F, 1F, 0, false),
    ESTRANGULADOR("estrangulador", EscopetaPresionItem.class, 0.6F, 1F, 0, false),
    RADIADOR("radiador", GatlingItem.class, 1F, 0.65F, 0, false),
    TUBO("tubo", WinchesterItem.class, 1F, 1F, 4, false),
    SILENCIADOR("silenciador", DerringerItem.class, 1F, 1F, 0, true),
    EMPUNADURA("empunadura", ThompsonItem.class, 0.7F, 1F, 0, false),
    MIRA("mira", MosqueteItem.class, 0.5F, 1F, 0, false),
    ANIMA("anima", CanonManoItem.class, 0.35F, 1F, 0, false);

    public final String id;
    private final Class<? extends Item> arma;
    /** Multiplicador de la dispersión, del calor, balas extra y si apaga el ruido. */
    public final float dispersion, calor;
    public final int capacidad;
    public final boolean silencioso;

    Accesorio(String id, Class<? extends Item> arma, float dispersion, float calor, int capacidad, boolean silencioso) {
        this.id = id;
        this.arma = arma;
        this.dispersion = dispersion;
        this.calor = calor;
        this.capacidad = capacidad;
        this.silencioso = silencioso;
    }

    /** ¿Vale para esa arma? */
    public boolean vale(Item i) {
        return arma.isInstance(i);
    }

    public String claveNombre() {
        return "accesorio.copperslug." + id;
    }

    public static Accesorio de(String id) {
        for (Accesorio a : values()) if (a.id.equals(id)) return a;
        return null;
    }
}

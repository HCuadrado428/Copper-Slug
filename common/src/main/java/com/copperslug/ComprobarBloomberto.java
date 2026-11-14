package com.copperslug;

import java.util.ArrayList;
import java.util.List;

/**
 * Comprueba al arrancar que el Bloomberto instalado trae todo lo que Copper Slug usa. Los jars de Bloomberto de distintas compilaciones
 * se llaman igual y llevan el mismo número de versión, así que el cargador no distingue uno viejo de uno nuevo: con uno viejo el juego
 * arrancaba y se caía más tarde, en el primer sitio que tocaba una clase que no está (al apuntar, al disparar...). Así se para al
 * principio y con un mensaje que dice qué hacer. Se mira con {@code getResource} (sin cargar la clase), para que valga también en un
 * servidor, donde las clases de cliente de Bloomberto no se pueden cargar.
 */
public final class ComprobarBloomberto {
    private ComprobarBloomberto() {}

    /** Las clases de Bloomberto que usa Copper Slug (salen de sus «import»). */
    private static final String[] CLASES = {
            "com.dougg865.bloomberto.api.animation.Easing",
            "com.dougg865.bloomberto.api.animation.KeyframeTrack",
            "com.dougg865.bloomberto.api.animation.model.AnimationClip",
            "com.dougg865.bloomberto.api.animation.model.AnimationController",
            "com.dougg865.bloomberto.api.animation.model.GeoModel",
            "com.dougg865.bloomberto.api.animation.model.GeoRenderer",
            "com.dougg865.bloomberto.api.animation.model.ModelLibrary",
            "com.dougg865.bloomberto.api.animation.model.Pose",
            "com.dougg865.bloomberto.api.client.ClientEvents",
            "com.dougg865.bloomberto.api.color.Color",
            "com.dougg865.bloomberto.api.effects.Particles",
            "com.dougg865.bloomberto.api.effects.Trail",
            "com.dougg865.bloomberto.api.render.CameraShake",
            "com.dougg865.bloomberto.api.render.CameraZoom",
            "com.dougg865.bloomberto.api.render.WorldDraw"
    };

    public static void verificar() {
        ClassLoader cl = ComprobarBloomberto.class.getClassLoader();
        List<String> faltan = new ArrayList<>();
        for (String c : CLASES) {
            if (cl.getResource(c.replace('.', '/') + ".class") == null) faltan.add(c.substring(c.lastIndexOf('.') + 1));
        }
        if (!faltan.isEmpty())
            throw new IllegalStateException("Copper Slug: el Bloomberto que tienes instalado es de una version anterior (le faltan " + faltan
                    + "). Usa el bloomberto-*.jar que viene en la misma descarga que Copper Slug y borra el otro de la carpeta mods.");
    }
}

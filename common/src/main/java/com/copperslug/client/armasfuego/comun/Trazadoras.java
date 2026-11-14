package com.copperslug.client.armasfuego.comun;

import com.dougg865.bloomberto.api.client.ClientEvents;
import com.dougg865.bloomberto.api.color.Color;
import com.dougg865.bloomberto.api.effects.Trail;
import com.dougg865.bloomberto.api.render.WorldDraw;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;
import java.util.List;

/**
 * La estela de cada bala (Bloomberto): una cinta que va de la boca a donde da, con la cabeza del color de la munición y
 * la cola que se apaga en unos ticks. La crea la partícula {@link FuegoParticulas.Trazo} (la bala que se ve pasar) con
 * su mismo recorrido, así que sale en todas las armas que ya la echaban.
 */
public final class Trazadoras {
    private Trazadoras() {}

    /** Cuántos ticks tarda en apagarse la cola. */
    private static final int COLA = 3;
    private static final float ANCHO = 0.05F;

    private static final class Viva {
        final Trail rastro = new Trail(COLA, 24);
        final Vec3 desde, paso;
        final int vida;
        final Color cabeza, cola;
        int edad;

        Viva(Vec3 desde, Vec3 paso, int vida, Color cabeza) {
            this.desde = desde;
            this.paso = paso;
            this.vida = vida;
            this.cabeza = cabeza;
            this.cola = cabeza.withAlpha(0);
            rastro.add(desde);
            rastro.add(desde.add(paso));
        }
    }

    private static final List<Viva> VIVAS = new ArrayList<>();
    /** Para la prueba: cuántas estelas se han creado desde que se abrió el juego. */
    public static volatile int creadas;
    private static boolean registrado;

    /** Engancha el tick y el dibujo a los eventos de cliente de Bloomberto (una vez, al arrancar el cliente). */
    public static void registrar() {
        if (registrado) return;
        registrado = true;
        ClientEvents.CLIENT_TICK.register(Trazadoras::tick);
        ClientEvents.DISCONNECT.register(VIVAS::clear);
        ClientEvents.WORLD_RENDER.register(ctx -> {
            if (VIVAS.isEmpty()) return;
            WorldDraw d = WorldDraw.of(ctx);
            for (Viva v : VIVAS) d.trail(v.rastro, ANCHO, v.cabeza, v.cola);
        });
    }

    /** Una bala que sale de {@code desde} y avanza {@code paso} cada tick durante {@code vida} ticks. */
    static void nueva(Vec3 desde, Vec3 paso, int vida, float r, float g, float b) {
        if (VIVAS.size() > 200) VIVAS.remove(0);
        VIVAS.add(new Viva(desde, paso, vida, Color.ofFloats(r, g, b, 0.85F)));
        creadas++;
    }

    private static void tick() {
        for (int i = VIVAS.size() - 1; i >= 0; i--) {
            Viva v = VIVAS.get(i);
            v.edad++;
            if (v.edad < v.vida) v.rastro.add(v.desde.add(v.paso.scale(v.edad + 1)));
            v.rastro.tick();
            if (v.edad >= v.vida && v.rastro.size() < 2) VIVAS.remove(i);
        }
    }
}

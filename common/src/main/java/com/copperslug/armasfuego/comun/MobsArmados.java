package com.copperslug.armasfuego.comun;

import com.copperslug.ConfigServidor;
import com.copperslug.armasfuego.oeste.WinchesterItem;
import com.copperslug.registry.ModItems;
import com.copperslug.registry.ModSounds;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.entity.monster.Pillager;
import net.minecraft.world.entity.raid.Raider;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;

import java.util.Map;
import java.util.WeakHashMap;

/**
 * Mobs con armas (los saqueadores; y los zombis y husks de las estructuras que los llevan puestos): algunos saqueadores salen con una Winchester en la mano (poco, y se puede apagar en la config,
 * sección mobs_armados) y disparan de verdad con la misma balística que el jugador: seis balas, una pausa para
 * recargar, y más puntería con la dificultad. El arma se suelta con una probabilidad (por defecto, baja). Se mira
 * cada 10 ticks a los saqueadores que hay cerca de algún jugador.
 */
public final class MobsArmados {
    private MobsArmados() {}

    /** Etiqueta: ya se ha tirado el dado para este mob (no se repite al recargar el mundo). */
    private static final String TIRADO = "copperslug_tirado";
    private static final int BALAS = 6, RECARGA = 80, RADIO = 64;
    private static final Map<LivingEntity, Estado> ESTADOS = new WeakHashMap<>();

    private static final class Estado {
        long proximo;
        int balas = BALAS;
    }

    /** ¿Lleva una Winchester? */
    public static boolean armado(LivingEntity m) {
        return m.getMainHandItem().getItem() instanceof WinchesterItem;
    }

    public static void tick(MinecraftServer srv) {
        if (srv.getTickCount() % 10 != 0 || !ConfigServidor.mobsArmados()) return;
        for (ServerPlayer p : srv.getPlayerList().getPlayers()) {
            ServerLevel l = p.serverLevel();
            for (Mob m : l.getEntitiesOfClass(Mob.class, p.getBoundingBox().inflate(RADIO), e -> e.isAlive() && (e instanceof Pillager || e instanceof Zombie))) {
                if (m instanceof Pillager pi && !m.getTags().contains(TIRADO)) tirar(pi);
                if (armado(m)) disparar(l, m);
            }
        }
    }

    private static void tirar(Raider m) {
        m.addTag(TIRADO);
        double prob = m.isPatrolLeader() ? ConfigServidor.mobsProbCapitan() : ConfigServidor.mobsProb();
        if (m.getRandom().nextDouble() >= prob) return;
        ItemStack arma = new ItemStack(ModItems.WINCHESTER.get());
        WinchesterItem.ponerDeposito(arma, java.util.Collections.nCopies(BALAS, ModItems.REVOLVER_BALA.get()));
        arma.setDamageValue(arma.getMaxDamage() / 2 + m.getRandom().nextInt(arma.getMaxDamage() / 3));
        m.setItemSlot(EquipmentSlot.MAINHAND, arma);
        m.setDropChance(EquipmentSlot.MAINHAND, ConfigServidor.mobsSuelta());
    }

    private static void disparar(ServerLevel l, Mob m) {
        boolean saqueador = m instanceof Pillager;
        LivingEntity v = m.getTarget();
        if (v == null || !v.isAlive()) return;
        double alcance = EquilibrioArmas.winchesterAlcance() * 0.5;
        double dist = m.distanceTo(v);
        if (dist > alcance) return;
        // el ballestero de vanilla se queda quieto; este se acerca hasta tener distancia de tiro
        m.getLookControl().setLookAt(v, 30F, 30F);
        if (!m.hasLineOfSight(v)) {
            if (saqueador && dist > 8) m.getNavigation().moveTo(v, 1.0);
            return;
        }
        if (saqueador) { if (dist > 28) m.getNavigation().moveTo(v, 1.0); else m.getNavigation().stop(); }
        Estado e = ESTADOS.computeIfAbsent(m, k -> new Estado());
        long t = l.getGameTime();
        if (t < e.proximo) return;
        if (e.balas <= 0) {
            e.balas = BALAS;
            e.proximo = t + RECARGA;
            l.playSound(null, m.getX(), m.getY(), m.getZ(), ModSounds.WINCHESTER_CARGAR.get(), SoundSource.HOSTILE, 0.8F, 1.0F);
            return;
        }
        e.balas--;
        e.proximo = t + ConfigServidor.mobsCadencia();
        Vec3 ojo = m.getEyePosition();
        Vec3 punto = v.position().add(0, v.getBbHeight() * 0.6, 0);
        Vec3 mira = punto.subtract(ojo).normalize();
        double disp = switch (l.getDifficulty()) {
            case HARD -> 0.02;
            case NORMAL -> 0.04;
            default -> 0.07;
        };
        Vec3 dir = Balistica.dispersar(mira, disp, m.getRandom());
        Vec3 der = mira.cross(new Vec3(0, 1, 0));
        der = der.lengthSqr() < 1e-4 ? new Vec3(1, 0, 0) : der.normalize();
        Vec3 boca = ojo.add(mira.scale(0.8)).add(der.scale(0.3)).add(0, -0.2, 0);
        Balistica.Tiro tiro = Balistica.trazar(l, m, ojo, dir, alcance, boca, null);
        Balistica.trazo(l, boca, tiro.pos(), null);
        if (tiro.entidad() != null && !(tiro.entidad() instanceof Raider)) {
            float d = ConfigServidor.mobsDano() * Balistica.caida(tiro.distancia(), alcance * 0.5, alcance, 0.6F);
            Balistica.herir(tiro.entidad(), m, d, 0.1F, WinchesterItem.DANO, false);
        }
        Balistica.impacto(l, m, tiro);
        ArmaFuegoItem.efectos(l, m, boca, ModSounds.WINCHESTER_DISPARO.get(), 3.0F, 0.95F, 3, true);
    }
}

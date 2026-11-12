package com.copperslug.armasfuego.comun;

import com.copperslug.ConfigServidor;
import com.copperslug.armasfuego.oeste.DerringerItem;
import com.copperslug.armasfuego.oeste.MosqueteItem;
import com.copperslug.armasfuego.oeste.ThompsonItem;
import com.copperslug.armasfuego.oeste.WinchesterItem;
import com.copperslug.armasfuego.pistola.Revolver;
import com.copperslug.armasfuego.pistola.RevolverItem;
import com.copperslug.registry.ModItems;
import com.copperslug.registry.ModSounds;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.damagesource.DamageType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.monster.Pillager;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.entity.raid.Raider;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;

import java.util.Collections;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.WeakHashMap;

/**
 * Mobs con armas: los saqueadores (algunos, poco y configurable) y los zombis y husks de las estructuras que llevan una puesta
 * disparan de verdad con la misma balística que el jugador, y cada arma tiene su manera: el revólver dispara seis tiros
 * deprisa, la Winchester más despacio y más lejos, la Derringer solo dos y de cerca, la Thompson en ráfagas de tres y el
 * mosquete un solo tiro enorme cada mucho. Cada estructura reparte las suyas (la pirámide, mosquetes y Derringers; la mina,
 * revólveres y Winchesters). El daño y la cadencia de la config (sección mobs_armados) son los de la Winchester y las demás
 * armas los escalan. El arma se suelta con una probabilidad (por defecto, baja).
 */
public final class MobsArmados {
    private MobsArmados() {}

    /** Etiqueta: ya se ha tirado el dado para este mob (no se repite al recargar el mundo). */
    private static final String TIRADO = "copperslug_tirado";
    private static final int RADIO = 64;
    private static final Set<Mob> ARMADOS = Collections.newSetFromMap(new WeakHashMap<>());
    private static final Map<LivingEntity, Estado> ESTADOS = new WeakHashMap<>();

    private static final class Estado {
        long proximo;
        int balas = -1, pendientes;
    }

    /** Cómo dispara cada arma, relativo a la Winchester (daño y cadencia de la config). */
    private record Perfil(float dano, float cadencia, int balas, int recarga, double alcance, double disp, int rafaga,
                          ResourceKey<DamageType> tipo, SoundEvent sonido, float tono, float vol, SoundEvent cargar) {}

    private static Perfil perfil(Item i) {
        if (i instanceof RevolverItem)
            return new Perfil(1.1F, 0.6F, 6, 70, 28, 1.0, 1, Revolver.DISPARO, ModSounds.REVOLVER_DISPARO.get(), 1.0F, 2.5F, ModSounds.REVOLVER_CARGAR.get());
        if (i instanceof WinchesterItem)
            return new Perfil(1.0F, 1.0F, 6, 80, EquilibrioArmas.winchesterAlcance() * 0.5, 0.8, 1, WinchesterItem.DANO, ModSounds.WINCHESTER_DISPARO.get(), 0.95F, 3.0F, ModSounds.WINCHESTER_CARGAR.get());
        if (i instanceof DerringerItem)
            return new Perfil(1.4F, 0.8F, 2, 70, 18, 1.3, 1, DerringerItem.DANO, ModSounds.DERRINGER_DISPARO.get(), 1.1F, 2.0F, ModSounds.REVOLVER_CARGAR.get());
        if (i instanceof ThompsonItem)
            return new Perfil(0.55F, 1.0F, 30, 100, 26, 1.6, 3, ThompsonItem.DANO, ModSounds.THOMPSON_DISPARO.get(), 1.0F, 2.5F, ModSounds.WINCHESTER_CARGAR.get());
        if (i instanceof MosqueteItem)
            return new Perfil(2.2F, 2.0F, 1, 100, 40, 0.5, 1, MosqueteItem.DANO, ModSounds.MOSQUETE_DISPARO.get(), 0.9F, 4.0F, ModSounds.MOSQUETE_BAQUETA.get());
        return null;
    }

    /** ¿Lleva un arma de fuego de las que sabe usar? (revólver, Winchester, Derringer, Thompson o mosquete) */
    public static boolean armado(LivingEntity m) {
        return perfil(m.getMainHandItem().getItem()) != null;
    }

    public static void tick(MinecraftServer srv) {
        if (!ConfigServidor.mobsArmados()) return;
        if (srv.getTickCount() % 10 == 0) refrescar(srv);
        Iterator<Mob> it = ARMADOS.iterator();
        while (it.hasNext()) {
            Mob m = it.next();
            if (!m.isAlive() || m.isRemoved() || !armado(m) || !(m.level() instanceof ServerLevel l)) {
                it.remove();
                continue;
            }
            if (l.getNearestPlayer(m, RADIO) != null) disparar(l, m);
        }
    }

    /** Busca los saqueadores y zombis cercanos a los jugadores, tira el dado a los saqueadores nuevos y apunta a los armados. */
    private static void refrescar(MinecraftServer srv) {
        for (ServerPlayer p : srv.getPlayerList().getPlayers()) {
            ServerLevel l = p.serverLevel();
            for (Mob m : l.getEntitiesOfClass(Mob.class, p.getBoundingBox().inflate(RADIO), e -> e.isAlive() && (e instanceof Pillager || e instanceof Zombie))) {
                if (m instanceof Pillager pi && !m.getTags().contains(TIRADO)) tirar(pi);
                if (armado(m)) ARMADOS.add(m);
            }
        }
    }

    /** Un saqueador nuevo: con la probabilidad de la config sale con un arma (revólver o Winchester). */
    private static void tirar(Raider m) {
        m.addTag(TIRADO);
        double prob = m.isPatrolLeader() ? ConfigServidor.mobsProbCapitan() : ConfigServidor.mobsProb();
        if (m.getRandom().nextDouble() >= prob) return;
        ItemStack arma;
        if (m.getRandom().nextFloat() < 0.4F) {
            arma = new ItemStack(ModItems.REVOLVER.get());
        } else {
            arma = new ItemStack(ModItems.WINCHESTER.get());
            WinchesterItem.ponerDeposito(arma, Collections.nCopies(6, ModItems.REVOLVER_BALA.get()));
        }
        arma.setDamageValue(arma.getMaxDamage() / 2 + m.getRandom().nextInt(Math.max(1, arma.getMaxDamage() / 3)));
        m.setItemSlot(EquipmentSlot.MAINHAND, arma);
        m.setDropChance(EquipmentSlot.MAINHAND, ConfigServidor.mobsSuelta());
    }

    private static void disparar(ServerLevel l, Mob m) {
        Perfil pf = perfil(m.getMainHandItem().getItem());
        if (pf == null) return;
        boolean saqueador = m instanceof Pillager;
        LivingEntity v = m.getTarget();
        if (v == null || !v.isAlive()) return;
        double alcance = pf.alcance();
        double dist = m.distanceTo(v);
        if (dist > alcance) return;
        // el ballestero de vanilla se queda quieto; este se acerca hasta tener distancia de tiro
        m.getLookControl().setLookAt(v, 30F, 30F);
        boolean ruta = m.tickCount % 10 == 0;
        if (!m.hasLineOfSight(v)) {
            if (saqueador && ruta && dist > 8) m.getNavigation().moveTo(v, 1.0);
            return;
        }
        if (saqueador && ruta) { if (dist > alcance * 0.7) m.getNavigation().moveTo(v, 1.0); else m.getNavigation().stop(); }
        Estado e = ESTADOS.computeIfAbsent(m, k -> new Estado());
        if (e.balas < 0) e.balas = pf.balas();
        long t = l.getGameTime();
        if (t < e.proximo) return;
        if (e.balas <= 0) {
            e.balas = pf.balas();
            e.proximo = t + pf.recarga();
            l.playSound(null, m.getX(), m.getY(), m.getZ(), pf.cargar(), SoundSource.HOSTILE, 0.8F, 1.0F);
            return;
        }
        e.balas--;
        if (e.pendientes <= 0) e.pendientes = pf.rafaga();
        e.pendientes--;
        e.proximo = t + (e.pendientes > 0 ? 3 : Math.max(4, Math.round(ConfigServidor.mobsCadencia() * pf.cadencia())));
        Vec3 ojo = m.getEyePosition();
        Vec3 punto = v.position().add(0, v.getBbHeight() * 0.6, 0);
        Vec3 mira = punto.subtract(ojo).normalize();
        double disp = pf.disp() * switch (l.getDifficulty()) {
            case HARD -> 0.025;
            case NORMAL -> 0.05;
            default -> 0.085;
        };
        Vec3 dir = Balistica.dispersar(mira, disp, m.getRandom());
        Vec3 der = mira.cross(new Vec3(0, 1, 0));
        der = der.lengthSqr() < 1e-4 ? new Vec3(1, 0, 0) : der.normalize();
        Vec3 boca = ojo.add(mira.scale(0.8)).add(der.scale(0.3)).add(0, -0.2, 0);
        Balistica.Tiro tiro = Balistica.trazar(l, m, ojo, dir, alcance, boca, null);
        Balistica.trazo(l, boca, tiro.pos(), null);
        if (tiro.entidad() != null && !(tiro.entidad() instanceof Raider)) {
            float d = ConfigServidor.mobsDano() * pf.dano() * Balistica.caida(tiro.distancia(), alcance * 0.5, alcance, 0.6F);
            Balistica.herir(tiro.entidad(), m, d, 0.1F, pf.tipo(), pf.rafaga() > 1);
        }
        Balistica.impacto(l, m, tiro);
        ArmaFuegoItem.efectos(l, m, boca, pf.sonido(), pf.vol(), pf.tono(), 3, true);
    }
}

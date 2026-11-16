package com.copperslug.recompensas;

import com.copperslug.CopperSlug;
import com.copperslug.registry.ModEnchantments;
import com.copperslug.registry.ModItems;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderSet;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.BossEvent;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ExperienceOrb;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Pillager;
import net.minecraft.world.entity.npc.Villager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.WeakHashMap;

/**
 * Los forajidos de los carteles de «Se busca»: dónde se esconden, cuándo aparecen (con su banda), la barra de jefe, qué
 * pasa al matarlos y el cobro de la recompensa a un aldeano. Todo vive en el cartel (sus datos) y en las etiquetas del
 * forajido, así que sobrevive a cerrar el mundo.
 */
public final class Forajidos {
    private Forajidos() {}

    public enum Estado {
        EN_BLANCO, BUSCADO, CAZADO;

        static Estado de(String s) {
            for (Estado e : values()) if (e.name().equals(s)) return e;
            return EN_BLANCO;
        }
    }

    static final String ESTADO = "estado", ID = "forajido", APODO = "apodo", APELLIDO = "apellido", X = "x", Z = "z", PAGO = "pago",
            APARECIDO = "aparecido";
    /** Etiqueta de todos los forajidos; cada uno lleva además la suya, con el id de su cartel. */
    public static final String JEFE = "copperslug_forajido";
    /** Distancia (en horizontal) a la que aparece el forajido al llegar a su escondite. */
    private static final int LLEGAR = 40;
    private static final int APODOS = 12;
    private static final String[] APELLIDOS = {"Ramírez", "McCoy", "Dalton", "Cassidy", "Morales", "O'Hara", "Calhoun", "Vega", "Black",
            "Montoya", "Garrett", "Escobedo"};

    private static final Map<Mob, ServerBossEvent> JEFES = new WeakHashMap<>();

    public static Component nombre(CompoundTag d) {
        return Component.translatable("copperslug.forajido.nombre", Component.translatable("copperslug.forajido.apodo." + Math.floorMod(d.getInt(APODO), APODOS)),
                APELLIDOS[Math.floorMod(d.getInt(APELLIDO), APELLIDOS.length)]);
    }

    /** Rellena un cartel en blanco: un forajido nuevo y su escondite ({@code forzado}, si se da; si no, el campamento más cercano). */
    public static void nuevo(ServerLevel l, ServerPlayer p, ItemStack s, BlockPos forzado) {
        RandomSource r = l.getRandom();
        CompoundTag d = CartelItem.datos(s);
        BlockPos donde = forzado != null ? forzado : escondite(l, p.blockPosition(), r);
        d.putString(ESTADO, Estado.BUSCADO.name());
        d.putString(ID, UUID.randomUUID().toString());
        d.putInt(APODO, r.nextInt(APODOS));
        d.putInt(APELLIDO, r.nextInt(APELLIDOS.length));
        d.putInt(X, donde.getX());
        d.putInt(Z, donde.getZ());
        d.putInt(PAGO, 12 + r.nextInt(13));
        p.sendSystemMessage(Component.translatable("copperslug.cartel.nuevo", nombre(d), donde.getX(), donde.getZ()));
        l.playSound(null, p.getX(), p.getY(), p.getZ(), SoundEvents.BOOK_PAGE_TURN, SoundSource.PLAYERS, 1F, 0.8F);
    }

    /** El campamento de saqueadores más cercano (a más de 64 bloques); si no hay, un sitio a 300-600 bloques. */
    private static BlockPos escondite(ServerLevel l, BlockPos desde, RandomSource r) {
        try {
            var reg = l.registryAccess().registryOrThrow(Registries.STRUCTURE);
            var campamento = reg.getHolder(ResourceKey.create(Registries.STRUCTURE, new ResourceLocation(CopperSlug.MOD_ID, "campamento")));
            if (campamento.isPresent()) {
                var par = l.getChunkSource().getGenerator().findNearestMapStructure(l, HolderSet.<Structure>direct(campamento.get()), desde, 40, false);
                if (par != null && par.getFirst().distSqr(desde) > 64 * 64) return par.getFirst();
            }
        } catch (RuntimeException ignorada) {
            // sin campamentos (otro tipo de mundo, desactivados): a un sitio cualquiera
        }
        double a = r.nextDouble() * Math.PI * 2, dist = 300 + r.nextInt(300);
        return desde.offset((int) (Math.cos(a) * dist), 0, (int) (Math.sin(a) * dist));
    }

    public static void tick(MinecraftServer srv) {
        int t = srv.getTickCount();
        if (t % 20 == 0) {
            for (ServerPlayer p : srv.getPlayerList().getPlayers()) {
                ServerLevel l = p.serverLevel();
                for (ItemStack s : carteles(p)) {
                    CompoundTag d = s.getTag();
                    if (CartelItem.estado(s) != Estado.BUSCADO || d.getBoolean(APARECIDO)) continue;
                    double dx = p.getX() - d.getInt(X), dz = p.getZ() - d.getInt(Z);
                    if (dx * dx + dz * dz < LLEGAR * LLEGAR) aparecer(l, p, s);
                }
                for (Mob m : l.getEntitiesOfClass(Mob.class, p.getBoundingBox().inflate(64), m -> m.getTags().contains(JEFE)))
                    JEFES.computeIfAbsent(m, k -> {
                        var b = new ServerBossEvent(k.getDisplayName(), BossEvent.BossBarColor.RED, BossEvent.BossBarOverlay.NOTCHED_10);
                        b.setDarkenScreen(false);
                        return b;
                    });
            }
        }
        if (t % 5 != 0) return;
        Iterator<Map.Entry<Mob, ServerBossEvent>> it = JEFES.entrySet().iterator();
        while (it.hasNext()) {
            var e = it.next();
            Mob m = e.getKey();
            ServerBossEvent b = e.getValue();
            boolean muerto = m.isDeadOrDying() || m.getRemovalReason() == Entity.RemovalReason.KILLED;
            if (muerto || m.isRemoved()) {
                b.removeAllPlayers();
                it.remove();
                if (muerto) cazado(srv, m);
                continue;
            }
            b.setProgress(Math.max(0F, Math.min(1F, m.getHealth() / m.getMaxHealth())));
            for (ServerPlayer p : List.copyOf(b.getPlayers())) if (p.level() != m.level() || p.distanceToSqr(m) > 48 * 48) b.removePlayer(p);
            if (m.level() instanceof ServerLevel l)
                for (ServerPlayer p : l.players()) if (p.distanceToSqr(m) <= 48 * 48) b.addPlayer(p);
        }
    }

    /** Los carteles que lleva el jugador (inventario y mano izquierda). */
    private static List<ItemStack> carteles(Player p) {
        List<ItemStack> out = new ArrayList<>();
        for (ItemStack s : p.getInventory().items) if (s.getItem() instanceof CartelItem) out.add(s);
        for (ItemStack s : p.getInventory().offhand) if (s.getItem() instanceof CartelItem) out.add(s);
        return out;
    }

    /** El forajido sale en su escondite, con su arma única y dos de su banda. */
    public static Mob aparecer(ServerLevel l, ServerPlayer p, ItemStack s) {
        CompoundTag d = s.getTag();
        RandomSource r = l.getRandom();
        int x = d.getInt(X), z = d.getInt(Z);
        int y = l.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
        Pillager jefe = EntityType.PILLAGER.create(l);
        if (jefe == null) return null;
        jefe.moveTo(x + 0.5, y, z + 0.5, r.nextFloat() * 360F, 0);
        jefe.addTag("copperslug_tirado");   // que MobsArmados no le tire el dado
        jefe.addTag(JEFE);
        jefe.addTag(JEFE + "_" + d.getString(ID));
        var vida = jefe.getAttribute(Attributes.MAX_HEALTH);
        if (vida != null) vida.setBaseValue(80);
        jefe.setHealth(80);
        jefe.setCustomName(nombre(d));
        jefe.setCustomNameVisible(true);
        jefe.setPersistenceRequired();
        jefe.setItemSlot(EquipmentSlot.MAINHAND, armaUnica(d, r));
        jefe.setDropChance(EquipmentSlot.MAINHAND, 2.0F);   // más de 1: siempre, y sin desgastar
        l.addFreshEntity(jefe);
        for (int i = 0; i < 2; i++) {
            Pillager b = EntityType.PILLAGER.create(l);
            if (b == null) continue;
            int bx = x + (i == 0 ? 3 : -3), bz = z + (i == 0 ? 2 : -2);
            b.moveTo(bx + 0.5, l.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, bx, bz), bz + 0.5, r.nextFloat() * 360F, 0);
            b.addTag("copperslug_tirado");
            b.addTag("copperslug_arma_revolver");
            b.setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(ModItems.REVOLVER.get()));
            b.setDropChance(EquipmentSlot.MAINHAND, com.copperslug.ConfigServidor.mobsSuelta());
            b.setPersistenceRequired();
            l.addFreshEntity(b);
        }
        d.putBoolean(APARECIDO, true);
        p.sendSystemMessage(Component.translatable("copperslug.cartel.aparece", nombre(d)));
        l.playSound(null, x, y, z, SoundEvents.PILLAGER_CELEBRATE, SoundSource.HOSTILE, 2F, 0.8F);
        return jefe;
    }

    /** Su arma: una de las que saben usar los mobs, con su nombre grabado, Pulso firme II y un encantamiento propio. */
    private static ItemStack armaUnica(CompoundTag d, RandomSource r) {
        ItemStack a;
        switch (r.nextInt(4)) {
            case 0 -> {
                a = new ItemStack(ModItems.WINCHESTER.get());
                com.copperslug.armasfuego.oeste.WinchesterItem.ponerDeposito(a, java.util.Collections.nCopies(6, ModItems.REVOLVER_BALA.get()));
                a.enchant(ModEnchantments.WINCHESTER_CARGA_RAPIDA.get(), 1);
            }
            case 1 -> {
                a = new ItemStack(ModItems.DERRINGER.get());
                a.enchant(ModEnchantments.DERRINGER_DOBLE.get(), 1);
            }
            case 2 -> {
                a = new ItemStack(ModItems.THOMPSON.get());
                a.enchant(ModEnchantments.THOMPSON_COMPENSADOR.get(), 1);
            }
            default -> {
                a = new ItemStack(ModItems.REVOLVER.get());
                a.enchant(ModEnchantments.REVOLVER_DESENFUNDE.get(), 1);
            }
        }
        a.enchant(ModEnchantments.PULSO_FIRME.get(), 2);
        a.setHoverName(Component.translatable("copperslug.forajido.arma", a.getItem().getDescription(), nombre(d)));
        return a;
    }

    /** Ha muerto un forajido: su cartel (lo lleve quien lo lleve) queda cazado. */
    private static void cazado(MinecraftServer srv, Mob m) {
        String id = null;
        for (String t : m.getTags()) if (t.startsWith(JEFE + "_")) id = t.substring(JEFE.length() + 1);
        if (id == null) return;
        for (ServerPlayer p : srv.getPlayerList().getPlayers())
            for (ItemStack s : carteles(p)) {
                if (CartelItem.estado(s) != Estado.BUSCADO || !id.equals(s.getTag().getString(ID))) continue;
                s.getTag().putString(ESTADO, Estado.CAZADO.name());
                p.sendSystemMessage(Component.translatable("copperslug.cartel.cazado_msg", nombre(s.getTag()), s.getTag().getInt(PAGO)));
                p.level().playSound(null, p.getX(), p.getY(), p.getZ(), SoundEvents.PLAYER_LEVELUP, SoundSource.PLAYERS, 0.8F, 1.2F);
            }
    }

    /** Clic derecho a un aldeano con un cartel cazado: paga la recompensa. Devuelve null si no es el caso. */
    public static InteractionResult cobrar(Player p, ItemStack s, Entity objetivo) {
        if (CartelItem.estado(s) != Estado.CAZADO || !(objetivo instanceof Villager v) || v.isBaby()) return null;
        if (p.level() instanceof ServerLevel l) {
            int pago = s.getTag().getInt(PAGO);
            ItemStack esmeraldas = new ItemStack(Items.EMERALD, pago);
            if (!p.getInventory().add(esmeraldas)) p.drop(esmeraldas, false);
            ExperienceOrb.award(l, p.position(), 20);
            l.sendParticles(ParticleTypes.HAPPY_VILLAGER, v.getX(), v.getY() + 1.8, v.getZ(), 8, 0.4, 0.4, 0.4, 0);
            v.playSound(SoundEvents.VILLAGER_YES, 1F, 1F);
            p.sendSystemMessage(Component.translatable("copperslug.cartel.cobrado", nombre(s.getTag()), pago));
            if (!p.getAbilities().instabuild) s.shrink(1);
            Recompensas.cobradas++;
        }
        return InteractionResult.sidedSuccess(p.level().isClientSide);
    }

    /** Contadores para la prueba del CI. */
    public static final class Recompensas {
        public static volatile int cobradas;
    }
}

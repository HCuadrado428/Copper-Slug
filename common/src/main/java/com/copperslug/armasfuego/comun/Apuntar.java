package com.copperslug.armasfuego.comun;

import com.copperslug.armasfuego.gatling.GatlingEntity;
import com.copperslug.armasfuego.pistola.RevolverItem;
import com.copperslug.armasfuego.rifle.RifleItem;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

/**
 * Apuntar con el clic derecho mantenido (todas las armas menos la escopeta de presión, que dispara solo desde la
 * cadera). El que apunta anda más lento, dispersa menos y, en el cliente, se le cierra el campo de visión y el arma se
 * alinea con el centro de la pantalla.
 * <p>
 * El estado es un modificador de la velocidad de movimiento con un id fijo: el servidor lo pone y lo quita (lo pide el
 * cliente con {@link ApuntarPacket}), y como los atributos se mandan a todos los que ven al jugador, los demás clientes
 * saben que apunta (para la pose de los brazos) sin más paquetes. El rifle apunta con su catalejo (usar el objeto) y la
 * Gatling plantada con sus mandos: {@link #apuntando} lo junta todo.
 */
public final class Apuntar {
    private Apuntar() {}

    public static final UUID ID = UUID.fromString("5b1f0c0e-3a57-4a3c-9d53-c0bb3e51a001");

    /** Los que apuntan (servidor): se repasan cada tick por si han cambiado de objeto. */
    private static final Set<UUID> APUNTANDO = new HashSet<>();

    /** ¿Se apunta con este objeto con el modificador? (el rifle va por su catalejo; la escopeta no apunta) */
    public static boolean apuntable(ItemStack s) {
        return s.getItem() instanceof ArmaFuegoItem || s.getItem() instanceof RevolverItem;
    }

    public static boolean apuntando(Player p) {
        GatlingEntity g = GatlingEntity.deJugador(p);
        if (g != null) return g.apuntando();
        ItemStack s = p.getMainHandItem();
        if (s.getItem() instanceof RifleItem) return p.isUsingItem() && p.getUsedItemHand() == InteractionHand.MAIN_HAND;
        if (!apuntable(s)) return false;
        AttributeInstance a = p.getAttribute(Attributes.MOVEMENT_SPEED);
        return a != null && a.getModifier(ID) != null;
    }

    /** Pone o quita el apuntado (en el servidor, y en el cliente para no esperar a que llegue el atributo). */
    public static void poner(Player p, boolean si) {
        AttributeInstance a = p.getAttribute(Attributes.MOVEMENT_SPEED);
        if (a == null) return;
        if (a.getModifier(ID) != null) a.removeModifier(ID);
        boolean vale = si && apuntable(p.getMainHandItem()) && !p.isUsingItem() && !p.isSpectator();
        if (vale) a.addTransientModifier(new AttributeModifier(ID, "copperslug.apuntar", -EquilibrioArmas.apuntarLentitud(), AttributeModifier.Operation.MULTIPLY_TOTAL));
        if (!p.level().isClientSide) {
            if (vale) APUNTANDO.add(p.getUUID());
            else APUNTANDO.remove(p.getUUID());
        }
    }

    /** Por cuánto se multiplica la dispersión del que dispara (1 desde la cadera). */
    public static double dispersion(Player p) {
        return apuntando(p) ? EquilibrioArmas.apuntarDispersion() : 1.0;
    }

    /** Cada tick del servidor: el que ya no lleva el arma en la mano (o se ha puesto a recargar) deja de apuntar. */
    public static void tick(MinecraftServer srv) {
        if (APUNTANDO.isEmpty()) return;
        for (UUID id : APUNTANDO.toArray(new UUID[0])) {
            ServerPlayer p = srv.getPlayerList().getPlayer(id);
            if (p == null) APUNTANDO.remove(id);
            else if (!apuntable(p.getMainHandItem()) || p.isUsingItem() || !p.isAlive()) poner(p, false);
        }
    }

    public static void limpiar() {
        APUNTANDO.clear();
    }
}

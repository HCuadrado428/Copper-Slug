package com.copperslug.shim.event.entity.player;

import net.minecraft.world.entity.ExperienceOrb;
import net.minecraft.world.entity.player.Player;

/** La experiencia que recoge un jugador (Forge: PlayerXpEvent; Fabric: ExperienceOrbMixin). */
public class PlayerXpEvent extends PlayerEvent {
    public PlayerXpEvent(Player p) {
        super(p);
    }

    /** Un orbe que el jugador va a recoger (antes de que vanilla arregle lo que lleva con Reparación). */
    public static class PickupXp extends PlayerXpEvent {
        private final ExperienceOrb orbe;

        public PickupXp(Player p, ExperienceOrb orbe) {
            super(p);
            this.orbe = orbe;
        }

        public ExperienceOrb getOrb() {
            return orbe;
        }
    }
}

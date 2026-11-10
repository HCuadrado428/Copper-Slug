package com.copperslug.shim.client.event;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.world.InteractionHand;

public class InputEvent extends Event {
    /** Clic de atacar, usar o elegir bloque (antes de que vanilla lo haga). Cancelado: vanilla no hace nada. */
    public static class InteractionKeyMappingTriggered extends InputEvent {
        private final int boton;
        private final KeyMapping tecla;
        private final InteractionHand mano;
        private boolean balancear = true;

        public InteractionKeyMappingTriggered(int boton, KeyMapping tecla, InteractionHand mano) {
            this.boton = boton;
            this.tecla = tecla;
            this.mano = mano;
        }

        @Override
        public boolean isCancelable() {
            return true;
        }

        public boolean isAttack() {
            return boton == 0;
        }

        public boolean isUseItem() {
            return boton == 1;
        }

        public boolean isPickBlock() {
            return boton == 2;
        }

        public KeyMapping getKeyMapping() {
            return tecla;
        }

        public InteractionHand getHand() {
            return mano;
        }

        public void setSwingHand(boolean b) {
            balancear = b;
        }

        public boolean shouldSwingHand() {
            return balancear;
        }

        public static InteractionKeyMappingTriggered ataque(InteractionHand mano) {
            return new InteractionKeyMappingTriggered(0, Minecraft.getInstance().options.keyAttack, mano);
        }

        public static InteractionKeyMappingTriggered uso(InteractionHand mano) {
            return new InteractionKeyMappingTriggered(1, Minecraft.getInstance().options.keyUse, mano);
        }
    }
}

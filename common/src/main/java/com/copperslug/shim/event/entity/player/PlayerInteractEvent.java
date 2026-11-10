package com.copperslug.shim.event.entity.player;

import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

public class PlayerInteractEvent extends PlayerEvent {
    private final InteractionHand hand;
    private InteractionResult resultado = InteractionResult.PASS;

    public PlayerInteractEvent(Player p, InteractionHand hand) {
        super(p);
        this.hand = hand;
    }

    public InteractionHand getHand() {
        return hand;
    }

    public ItemStack getItemStack() {
        return getEntity().getItemInHand(hand);
    }

    public Level getLevel() {
        return getEntity().level();
    }

    @Override
    public boolean isCancelable() {
        return true;
    }

    public void setCancellationResult(InteractionResult r) {
        resultado = r;
    }

    public InteractionResult getCancellationResult() {
        return resultado;
    }

    public static class EntityInteract extends PlayerInteractEvent {
        private final Entity target;

        public EntityInteract(Player p, InteractionHand hand, Entity target) {
            super(p, hand);
            this.target = target;
        }

        public Entity getTarget() {
            return target;
        }
    }
}

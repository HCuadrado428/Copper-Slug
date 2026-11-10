package com.copperslug.shim.event.entity.player;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

public class PlayerEvent extends Event {
    private final Player p;

    public PlayerEvent(Player p) {
        this.p = p;
    }

    public Player getEntity() {
        return p;
    }

    public static class PlayerLoggedInEvent extends PlayerEvent {
        public PlayerLoggedInEvent(Player p) {
            super(p);
        }
    }

    public static class PlayerLoggedOutEvent extends PlayerEvent {
        public PlayerLoggedOutEvent(Player p) {
            super(p);
        }
    }

    public static class PlayerRespawnEvent extends PlayerEvent {
        private final boolean endConquered;

        public PlayerRespawnEvent(Player p, boolean endConquered) {
            super(p);
            this.endConquered = endConquered;
        }

        public boolean isEndConquered() {
            return endConquered;
        }
    }

    public static class PlayerChangedDimensionEvent extends PlayerEvent {
        private final ResourceKey<Level> de, a;

        public PlayerChangedDimensionEvent(Player p, ResourceKey<Level> de, ResourceKey<Level> a) {
            super(p);
            this.de = de;
            this.a = a;
        }

        public ResourceKey<Level> getFrom() {
            return de;
        }

        public ResourceKey<Level> getTo() {
            return a;
        }
    }

    public static class ItemPickupEvent extends PlayerEvent {
        private final ItemEntity original;
        private final ItemStack stack;

        public ItemPickupEvent(Player p, ItemEntity original, ItemStack stack) {
            super(p);
            this.original = original;
            this.stack = stack;
        }

        public ItemEntity getOriginalEntity() {
            return original;
        }

        public ItemStack getStack() {
            return stack;
        }
    }
}

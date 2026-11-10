package com.copperslug.shim.client.event;

import com.copperslug.shim.eventbus.api.Event;
import net.minecraft.client.color.item.ItemColor;
import net.minecraft.world.level.ItemLike;

import java.util.function.BiConsumer;

public class RegisterColorHandlersEvent extends Event {
    public static class Item extends RegisterColorHandlersEvent {
        private final BiConsumer<ItemColor, ItemLike[]> f;

        public Item(BiConsumer<ItemColor, ItemLike[]> f) {
            this.f = f;
        }

        public void register(ItemColor c, ItemLike... items) {
            f.accept(c, items);
        }
    }
}

package com.copperslug.shim;

import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.Tag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;

import java.util.List;
import java.util.UUID;

/**
 * El NBT de los objetos como en 1.20.1 (getOrCreateTag, getTag, hasTag...), en 1.21 sobre el componente
 * minecraft:custom_data. {@link #tag} da una etiqueta "viva": cada cambio en ella (put..., remove) se guarda en el
 * objeto al momento. Ojo: lo que se cambie dentro de una etiqueta anidada no se guarda solo (se vuelve a poner con put).
 * Los usa el código de las armas a través de herramientas/a_1_21_1.py.
 */
public final class Nbt {
    private Nbt() {}

    /** getOrCreateTag(). */
    public static CompoundTag tag(ItemStack s) {
        return new Viva(s);
    }

    /** getTag(): null si no tiene datos. */
    public static CompoundTag leer(ItemStack s) {
        return tiene(s) ? new Viva(s) : null;
    }

    /** hasTag(). */
    public static boolean tiene(ItemStack s) {
        CustomData d = s.get(DataComponents.CUSTOM_DATA);
        return d != null && !d.isEmpty();
    }

    /** removeTagKey(k). */
    public static void quitar(ItemStack s, String k) {
        if (!tiene(s)) return;
        CustomData.update(DataComponents.CUSTOM_DATA, s, t -> t.remove(k));
    }

    /** setTag(t). */
    public static void poner(ItemStack s, CompoundTag t) {
        if (t == null || t.isEmpty()) s.remove(DataComponents.CUSTOM_DATA);
        else s.set(DataComponents.CUSTOM_DATA, CustomData.of(t));
    }

    /** Una etiqueta que se guarda en el objeto cada vez que cambia. */
    static final class Viva extends CompoundTag {
        private final ItemStack s;
        private boolean cargando = true;

        Viva(ItemStack s) {
            this.s = s;
            CustomData d = s.get(DataComponents.CUSTOM_DATA);
            if (d != null) {
                CompoundTag t = d.copyTag();
                for (String k : t.getAllKeys()) super.put(k, t.get(k));
            }
            cargando = false;
        }

        private void guardar() {
            if (cargando) return;
            if (isEmpty()) s.remove(DataComponents.CUSTOM_DATA);
            else s.set(DataComponents.CUSTOM_DATA, CustomData.of(this));
        }

        @Override
        public Tag put(String k, Tag v) {
            Tag r = super.put(k, v);
            guardar();
            return r;
        }

        @Override
        public void putByte(String k, byte v) {
            super.putByte(k, v);
            guardar();
        }

        @Override
        public void putShort(String k, short v) {
            super.putShort(k, v);
            guardar();
        }

        @Override
        public void putInt(String k, int v) {
            super.putInt(k, v);
            guardar();
        }

        @Override
        public void putLong(String k, long v) {
            super.putLong(k, v);
            guardar();
        }

        @Override
        public void putUUID(String k, UUID v) {
            super.putUUID(k, v);
            guardar();
        }

        @Override
        public void putFloat(String k, float v) {
            super.putFloat(k, v);
            guardar();
        }

        @Override
        public void putDouble(String k, double v) {
            super.putDouble(k, v);
            guardar();
        }

        @Override
        public void putString(String k, String v) {
            super.putString(k, v);
            guardar();
        }

        @Override
        public void putByteArray(String k, byte[] v) {
            super.putByteArray(k, v);
            guardar();
        }

        @Override
        public void putByteArray(String k, List<Byte> v) {
            super.putByteArray(k, v);
            guardar();
        }

        @Override
        public void putIntArray(String k, int[] v) {
            super.putIntArray(k, v);
            guardar();
        }

        @Override
        public void putIntArray(String k, List<Integer> v) {
            super.putIntArray(k, v);
            guardar();
        }

        @Override
        public void putLongArray(String k, long[] v) {
            super.putLongArray(k, v);
            guardar();
        }

        @Override
        public void putLongArray(String k, List<Long> v) {
            super.putLongArray(k, v);
            guardar();
        }

        @Override
        public void putBoolean(String k, boolean v) {
            super.putBoolean(k, v);
            guardar();
        }

        @Override
        public void remove(String k) {
            super.remove(k);
            guardar();
        }

        @Override
        public CompoundTag merge(CompoundTag o) {
            super.merge(o);
            guardar();
            return this;
        }
    }
}

package com.copperslug.shim.event;

import com.copperslug.plataforma.Plataforma;
import com.copperslug.shim.common.util.BlockSnapshot;
import net.minecraft.core.Direction;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

public final class ForgeEventFactory {
    private ForgeEventFactory() {}

    /** true si algo (una protección) no deja colocar el bloque. */
    public static boolean onBlockPlace(Entity e, BlockSnapshot s, Direction d) {
        if (!(e instanceof Player p) || !(s.level() instanceof Level l)) return false;
        return !Plataforma.get().puedeColocar(p, l, s.pos());
    }
}

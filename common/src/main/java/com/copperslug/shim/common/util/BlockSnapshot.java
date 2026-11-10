package com.copperslug.shim.common.util;

import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelAccessor;

public record BlockSnapshot(ResourceKey<Level> dim, LevelAccessor level, BlockPos pos) {
    public static BlockSnapshot create(ResourceKey<Level> dim, LevelAccessor level, BlockPos pos) {
        return new BlockSnapshot(dim, level, pos);
    }
}

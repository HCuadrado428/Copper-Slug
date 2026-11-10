package com.copperslug.shim.client.event;

import com.copperslug.shim.eventbus.api.Event;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Camera;
import net.minecraft.client.renderer.LevelRenderer;
import org.joml.Matrix4f;

public class RenderLevelStageEvent extends Event {
    public enum Stage {AFTER_SKY, AFTER_SOLID_BLOCKS, AFTER_ENTITIES, AFTER_BLOCK_ENTITIES, AFTER_TRANSLUCENT_BLOCKS, AFTER_PARTICLES, AFTER_WEATHER, AFTER_LEVEL}

    private final Stage stage;
    private final LevelRenderer lr;
    private final PoseStack ps;
    private final Matrix4f proy;
    private final int tick;
    private final float pt;
    private final Camera cam;

    public RenderLevelStageEvent(Stage stage, LevelRenderer lr, PoseStack ps, Matrix4f proy, int tick, float pt, Camera cam) {
        this.stage = stage;
        this.lr = lr;
        this.ps = ps;
        this.proy = proy;
        this.tick = tick;
        this.pt = pt;
        this.cam = cam;
    }

    public Stage getStage() {
        return stage;
    }

    public LevelRenderer getLevelRenderer() {
        return lr;
    }

    public PoseStack getPoseStack() {
        return ps;
    }

    public Matrix4f getProjectionMatrix() {
        return proy;
    }

    public int getRenderTick() {
        return tick;
    }

    public float getPartialTick() {
        return pt;
    }

    public Camera getCamera() {
        return cam;
    }
}

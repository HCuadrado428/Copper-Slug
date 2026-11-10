package com.copperslug.shim.client.event;

import com.copperslug.shim.eventbus.api.Event;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.player.PlayerRenderer;
import net.minecraft.world.entity.player.Player;

public class RenderPlayerEvent extends Event {
    private final Player p;
    private final PlayerRenderer r;
    private final float pt;
    private final PoseStack ps;
    private final MultiBufferSource buf;
    private final int luz;

    public RenderPlayerEvent(Player p, PlayerRenderer r, float pt, PoseStack ps, MultiBufferSource buf, int luz) {
        this.p = p;
        this.r = r;
        this.pt = pt;
        this.ps = ps;
        this.buf = buf;
        this.luz = luz;
    }

    public Player getEntity() {
        return p;
    }

    public PlayerRenderer getRenderer() {
        return r;
    }

    public float getPartialTick() {
        return pt;
    }

    public PoseStack getPoseStack() {
        return ps;
    }

    public MultiBufferSource getMultiBufferSource() {
        return buf;
    }

    public int getPackedLight() {
        return luz;
    }

    /** Después de poner las poses del modelo y antes de dibujarlo. */
    public static class Pre extends RenderPlayerEvent {
        public Pre(Player p, PlayerRenderer r, float pt, PoseStack ps, MultiBufferSource buf, int luz) {
            super(p, r, pt, ps, buf, luz);
        }

        @Override
        public boolean isCancelable() {
            return true;
        }
    }
}

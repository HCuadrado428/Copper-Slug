package com.copperslug.client.armasfuego.comun;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.comun.ArmaFuegoItem;
import com.copperslug.armasfuego.comun.Cobre;
import com.copperslug.armasfuego.comun.EquilibrioArmas;
import com.copperslug.armasfuego.oeste.WinchesterItem;
import com.copperslug.armasfuego.rifle.Rifle;
import com.copperslug.armasfuego.rifle.RifleItem;
import com.copperslug.plataforma.PlataformaCliente;
import com.dougg865.bloomberto.api.animation.model.AnimationClip;
import com.dougg865.bloomberto.api.animation.model.GeoModel;
import com.dougg865.bloomberto.api.animation.model.GeoRenderer;
import com.dougg865.bloomberto.api.animation.model.ModelLibrary;
import com.dougg865.bloomberto.api.animation.model.Pose;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;

/**
 * Las piezas que se mueven del Winchester (la palanca) y del rifle (el cerrojo): modelos de Bloomberto
 * (geo/winchester_palanca, geo/rifle_cerrojo, de herramientas/piezas_geo.py) que se dibujan encima del arma, que ya no
 * las lleva en su modelo. La pose sale de la animación muestreada según el ciclo del arma (1 segundo de animación = el
 * ciclo entero), así que va igual en la mano, en tercera persona y en el suelo, sin estado en el cliente.
 */
public final class PiezasAnimadas {
    private PiezasAnimadas() {}

    private record Pieza(ResourceLocation geo, ResourceLocation anim, String clip, ResourceLocation[] atlas) {
        static Pieza de(String n) {
            ResourceLocation[] a = new ResourceLocation[4];
            for (int i = 0; i < 4; i++) a[i] = new ResourceLocation(CopperSlug.MOD_ID, "textures/geo/" + n + "_" + i + ".png");
            return new Pieza(new ResourceLocation(CopperSlug.MOD_ID, "geo/" + n + ".geo.json"),
                    new ResourceLocation(CopperSlug.MOD_ID, "animations/" + n + ".animation.json"), "animation." + n, a);
        }
    }

    private static final Pieza PALANCA = Pieza.de("winchester_palanca");
    private static final Pieza CERROJO = Pieza.de("rifle_cerrojo");

    /** Para la prueba: lo más que se ha visto abrir la palanca (grados) y tirar del cerrojo (píxeles) en primera persona. */
    public static volatile float palancaMax, cerrojoMax;

    /** Después de dibujar el arma (mixin del ItemRenderer): su pieza móvil, si la tiene. */
    public static void dibujar(ItemStack s, ItemDisplayContext ctx, boolean izq, PoseStack ps, MultiBufferSource buf, int luz, int overlay,
                               BakedModel m) {
        Minecraft mc = Minecraft.getInstance();
        float pt = mc.getFrameTime();
        Pieza pieza;
        float t;
        int ox;
        if (s.getItem() instanceof WinchesterItem) {
            pieza = PALANCA;
            float d = ArmaFuegoItem.desdeDisparo(s, mc.level, pt);
            Player p = mc.player;
            boolean suya = p != null && (p.getMainHandItem() == s || p.getOffhandItem() == s);
            int pal = suya ? WinchesterItem.palanca(p, s) : EquilibrioArmas.winchesterPalanca();
            t = d >= 0 && d < pal ? d / pal : 0F;
            ox = Cobre.oxido(s);
        } else if (s.getItem() instanceof RifleItem) {
            pieza = CERROJO;
            int c = Rifle.cerrojo(s);
            t = c > 0 ? Mth.clamp((Rifle.CERROJO_TICKS - c + pt) / Rifle.CERROJO_TICKS, 0F, 1F) : 0F;
            ox = Rifle.oxido(s);
        } else return;

        GeoModel geo = ModelLibrary.model(pieza.geo());
        if (geo == ModelLibrary.EMPTY_MODEL) return;
        AnimationClip clip = ModelLibrary.animations(pieza.anim()).clips().get(pieza.clip());
        Pose pose = clip == null ? new Pose() : clip.sample(t);
        boolean primera = ctx == ItemDisplayContext.FIRST_PERSON_RIGHT_HAND || ctx == ItemDisplayContext.FIRST_PERSON_LEFT_HAND;
        if (primera) {
            if (pose.has("palanca")) palancaMax = Math.max(palancaMax, Math.abs(pose.get("palanca").rotation[0]));
            if (pose.has("cerrojo")) cerrojoMax = Math.max(cerrojoMax, pose.get("cerrojo").position[2]);
        }
        BakedModel real = PlataformaCliente.P.modeloPara(m, ctx);
        ps.pushPose();
        // la misma colocación que hace el ItemRenderer con el modelo del arma
        real.getTransforms().getTransform(ctx).apply(izq, ps);
        ps.translate(-0.5, -0.5, -0.5);
        GeoRenderer.render(geo, pose, ps, buf.getBuffer(RenderType.entityCutoutNoCull(pieza.atlas()[Mth.clamp(ox, 0, 3)])), luz, overlay, 0xFFFFFFFF);
        ps.popPose();
    }
}

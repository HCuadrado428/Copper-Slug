package com.copperslug.client.armasfuego.pistola;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.pistola.Carga;
import com.copperslug.armasfuego.pistola.Revolver;
import com.copperslug.armasfuego.pistola.Tambor;
import com.copperslug.plataforma.ClienteComun;
import com.copperslug.plataforma.PlataformaCliente;
import com.dougg865.bloomberto.api.animation.model.AnimationController;
import com.dougg865.bloomberto.api.animation.model.GeoModel;
import com.dougg865.bloomberto.api.animation.model.GeoRenderer;
import com.dougg865.bloomberto.api.animation.model.ModelLibrary;
import com.dougg865.bloomberto.api.animation.model.Pose;
import com.dougg865.bloomberto.api.client.ClientEvents;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.Util;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.entity.player.Player;

/**
 * El tambor del revólver, dibujado por código encima del armazón (que es el modelo 3D del objeto, sin tambor): así gira de
 * verdad (hasta la recámara que toca, con un frenazo suave; en la ruleta rusa da vueltas) y cada recámara cargada lleva el
 * culote de su tipo de bala, tintado del mismo color que en el HUD. Con el tambor girado no se enseña ninguna bala.
 * <p>
 * Se llama desde el mixin de ItemRenderer.render, así que vale en la mano (primera y tercera persona), en el suelo y en
 * los marcos. El tambor es un modelo de Bloomberto (geo/revolver_tambor.geo.json, de herramientas/tambor_geo.py) con
 * dos huesos: la grúa, que al cargar saca el tambor hacia la izquierda con la animación «abrir» y lo devuelve con
 * «cerrar» (animations/revolver_tambor.animation.json), y el tambor, que gira. Si ese modelo no se pudiera leer se dibuja
 * el de objeto de antes, con el tambor desplazado al abrir. El culote es un modelo adicional; la geometría (el centro del
 * tambor y el anillo de recámaras) es la de herramientas/generar_tambor.py.
 */
public final class RevolverTambor {
    private RevolverTambor() {}

    private static ResourceLocation rl(String n) {
        return ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "item/armas3d/" + n);
    }

    /** Un tambor por nivel de óxido (cobre nuevo, expuesto, erosionado, oxidado). */
    private static final ResourceLocation[] CILINDRO = {rl("revolver_cilindro_0"), rl("revolver_cilindro_1"), rl("revolver_cilindro_2"), rl("revolver_cilindro_3")};
    private static final ResourceLocation CULOTE = rl("revolver_culote");
    public static final ResourceLocation[] MODELOS = {CILINDRO[0], CILINDRO[1], CILINDRO[2], CILINDRO[3], CULOTE};

    // la geometría del modelo (píxeles de modelo): centro del tambor, anillo de recámaras y cara de atrás
    private static final double CX = 8.0, CY = 8.9, ANILLO = 1.0, Z_ATRAS = 11.0, DESPLAZA_ABIERTO = 3.4;
    // la grúa (herramientas/tambor_geo.py): su eje y cuánto gira abierta
    private static final double GX = 8.0, GY = 5.4;
    private static final float ABIERTA = 55F;

    private static final ResourceLocation GEO = ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "geo/revolver_tambor.geo.json");
    private static final ResourceLocation ANIM = ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "animations/revolver_tambor.animation.json");
    private static final ResourceLocation[] ATLAS = {atlas(0), atlas(1), atlas(2), atlas(3)};

    private static ResourceLocation atlas(int ox) {
        return ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "textures/geo/revolver_tambor_" + ox + ".png");
    }

    /** La grúa del revólver de la mano (primera persona): abrir y cerrar con la animación de Bloomberto. */
    private static AnimationController grua;
    private static boolean gruaAbierta;
    private static int abiertoTicks;
    /** Para la prueba: cuántas veces se ha abierto y cerrado la grúa con la animación, y el último ángulo dibujado. */
    public static volatile int aperturas, cierres;
    public static volatile float gruaVista, gruaMax;
    private static boolean registrado;

    /** Engancha el tick de la animación a Bloomberto (una vez, al arrancar el cliente). */
    public static void registrar() {
        if (registrado) return;
        registrado = true;
        ClientEvents.CLIENT_TICK.register(RevolverTambor::tick);
        ClientEvents.DISCONNECT.register(() -> {
            grua = null;
            gruaAbierta = false;
        });
    }

    private static void tick() {
        Minecraft mc = Minecraft.getInstance();
        Player p = mc.player;
        if (p == null || mc.level == null) return;
        ItemStack s = p.getMainHandItem().getItem() instanceof com.copperslug.armasfuego.pistola.RevolverItem ? p.getMainHandItem() : p.getOffhandItem();
        if (!(s.getItem() instanceof com.copperslug.armasfuego.pistola.RevolverItem)) return;
        if (grua == null) {
            grua = ModelLibrary.animations(ANIM).controller();
            try {
                grua.play("animation.revolver_tambor.cerrar");
            } catch (IllegalArgumentException e) {
                return;   // sin el archivo de animaciones: se queda con el tambor de antes
            }
        }
        // la marca de carga del objeto puede durar solo un tick en el cliente (lo que predice y lo que manda el servidor no
        // siempre coinciden): la grúa se queda abierta al menos 12 ticks desde la última vez que se vio
        if (abierto(s, mc)) abiertoTicks = 12;
        else if (abiertoTicks > 0) abiertoTicks--;
        boolean abierto = abiertoTicks > 0;
        if (abierto != gruaAbierta) {
            gruaAbierta = abierto;
            grua.play(abierto ? "animation.revolver_tambor.abrir" : "animation.revolver_tambor.cerrar");
            if (abierto) aperturas++;
            else cierres++;
        }
        grua.tick();
    }

    private static boolean abierto(ItemStack s, Minecraft mc) {
        if (!com.copperslug.shim.Nbt.tiene(s)) return false;
        long t = mc.level.getGameTime() - com.copperslug.shim.Nbt.leer(s).getLong(Revolver.CARGA_T);
        return t >= 0 && t < 12;
    }

    /** Animación del giro (solo la mano de primera persona): el ángulo que se ve y cuándo se dibujó la última vez. */
    private static float angVisto = Float.NaN;
    private static long tAntes, giroVisto = Long.MIN_VALUE, giroDesdeMs;

    public static void dibujar(ItemStack s, ItemDisplayContext ctx, boolean izq, PoseStack ps, MultiBufferSource buf, int luz, int overlay, BakedModel m) {
        Minecraft mc = Minecraft.getInstance();
        if (mc.level == null) return;
        boolean primera = ctx == ItemDisplayContext.FIRST_PERSON_RIGHT_HAND || ctx == ItemDisplayContext.FIRST_PERSON_LEFT_HAND;
        int pos = Tambor.pos(s);
        boolean girado = Tambor.girado(s);
        float objetivo = 60F * pos, ang = objetivo;
        if (primera) {
            long ahora = System.nanoTime();
            float dt = tAntes == 0 ? 0F : Math.min(0.1F, (ahora - tAntes) / 1e9F);
            tAntes = ahora;
            if (Float.isNaN(angVisto)) angVisto = objetivo;
            // cada paso de recámara: el tambor gira hasta la que toca y frena (suavizado independiente de los fps)
            angVisto += Mth.wrapDegrees(objetivo - angVisto) * (1F - (float) Math.exp(-dt * 16F));
            ang = angVisto;
            // la ruleta rusa: gira rápido y frena (como el tambor del HUD)
            long giroT = Tambor.giroT(s), edad = mc.level.getGameTime() - giroT;
            if (giroT != giroVisto) {
                giroVisto = giroT;
                giroDesdeMs = Util.getMillis() - Math.max(0L, edad) * 50L;
            }
            float prog = (Util.getMillis() - giroDesdeMs) / (Tambor.GIRO_TICKS * 50F);
            // solo si el giro es reciente (el valor inicial, 0, no cuenta como giro)
            if (edad >= 0 && edad < Tambor.GIRO_TICKS + 2 && prog >= 0F && prog < 1F) {
                float k = 1F - prog;
                ang += 720F * k * k;
            }
        }
        boolean abierto = abierto(s, mc);
        BakedModel real = PlataformaCliente.P.modeloPara(m, ctx);
        GeoModel geo = ModelLibrary.model(GEO);
        boolean conGeo = geo != ModelLibrary.EMPTY_MODEL;
        ps.pushPose();
        // la misma colocación que hace el ItemRenderer con el modelo: la transformación de la perspectiva y el origen en la esquina
        real.getTransforms().getTransform(ctx).apply(izq, ps);
        ps.translate(-0.5, -0.5, -0.5);
        if (conGeo) {
            // la grúa: en la mano de primera persona, la animación; en lo demás, abierta o cerrada sin más
            float g = abierto ? ABIERTA : 0F;
            if (primera && grua != null) {
                Pose pose = grua.pose(mc.getTimer().getGameTimeDeltaPartialTick(false));
                if (pose.has("grua")) g = pose.get("grua").rotation[2];
                gruaVista = g;
                gruaMax = Math.max(gruaMax, Math.abs(g));
            }
            ps.translate(GX / 16.0, GY / 16.0, 0);
            ps.mulPose(Axis.ZP.rotationDegrees(g));
            ps.translate(-GX / 16.0, -GY / 16.0, 0);
        } else if (abierto) ps.translate(-DESPLAZA_ABIERTO / 16.0, 0, 0);
        ps.translate(CX / 16.0, CY / 16.0, 0);
        ps.mulPose(Axis.ZP.rotationDegrees(ang));
        ps.translate(-CX / 16.0, -CY / 16.0, 0);
        int ox = Mth.clamp(Tambor.oxido(s), 0, 3);
        if (conGeo) GeoRenderer.render(geo, new Pose(), ps, buf.getBuffer(RenderType.entityCutoutNoCull(ATLAS[ox])), luz, overlay, 0xFFFFFFFF);
        else modelo(CILINDRO[ox], ps, buf, luz, overlay, 1F, 1F, 1F);
        if (!girado) {
            for (int j = 0; j < Tambor.N; j++) {
                Carga c = Tambor.en(s, j);
                if (c == Carga.VACIA) continue;
                double a = Math.toRadians(60.0 * j);
                ps.pushPose();
                ps.translate((CX + ANILLO * Math.sin(a)) / 16.0, (CY + ANILLO * Math.cos(a)) / 16.0, Z_ATRAS / 16.0);
                modelo(CULOTE, ps, buf, luz, overlay, (c.color >> 16 & 255) / 255F, (c.color >> 8 & 255) / 255F, (c.color & 255) / 255F);
                ps.popPose();
            }
        }
        ps.popPose();
    }

    private static void modelo(ResourceLocation id, PoseStack ps, MultiBufferSource buf, int luz, int overlay, float r, float g, float b) {
        BakedModel bm = ClienteComun.modelo(id);
        Minecraft.getInstance().getBlockRenderer().getModelRenderer().renderModel(ps.last(), buf.getBuffer(Sheets.cutoutBlockSheet()), null, bm, r, g, b, luz, overlay);
    }
}

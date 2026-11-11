package com.copperslug.client.armasfuego.comun;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.comun.Apuntar;
import com.copperslug.armasfuego.comun.ApuntarPacket;
import com.copperslug.armasfuego.comun.ArmaFuegoItem;
import com.copperslug.armasfuego.comun.EquilibrioArmas;
import com.copperslug.armasfuego.comun.GatilloPacket;
import com.copperslug.armasfuego.gatling.GatlingEntity;
import com.copperslug.armasfuego.oeste.CanonManoItem;
import com.copperslug.armasfuego.oeste.DerringerItem;
import com.copperslug.armasfuego.oeste.MosqueteItem;
import com.copperslug.armasfuego.oeste.ThompsonItem;
import com.copperslug.armasfuego.oeste.WinchesterItem;
import com.copperslug.armasfuego.pistola.Carga;
import com.copperslug.armasfuego.pistola.RevolverItem;
import com.copperslug.armasfuego.pistola.Tambor;
import com.copperslug.network.ModNetwork;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.ChatFormatting;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.network.chat.Component;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import com.copperslug.shim.api.distmarker.Dist;
import com.copperslug.shim.client.event.InputEvent;
import com.copperslug.shim.client.gui.overlay.ForgeGui;
import com.copperslug.shim.event.TickEvent;
import com.copperslug.shim.eventbus.api.SubscribeEvent;
import com.copperslug.shim.fml.common.Mod;
import org.joml.Quaternionf;
import org.joml.Vector3f;

/**
 * Apuntar y disparar en el cliente, como en los juegos de tiros: mantener el clic derecho apunta (el arma se alinea
 * con el centro de la pantalla, el campo de visión se cierra y cada arma enseña su mira) y el clic izquierdo dispara,
 * apuntando o desde la cadera. Vale para el revólver y las armas de la segunda tanda (Winchester, Derringer, Thompson,
 * mosquete y cañón de mano) y, a los mandos, para la Gatling. El rifle ya apuntaba así con su catalejo y la escopeta de
 * presión no apunta (dispara solo desde la cadera).
 */
@Mod.EventBusSubscriber(modid = CopperSlug.MOD_ID, value = Dist.CLIENT)
public final class Apuntado {
    private Apuntado() {}

    /** El jugador apunta con el arma de la mano (ni el rifle ni la Gatling: esos van por su lado). */
    public static boolean apunta;
    /** Cuánto de apuntada está el arma (0 en la cadera, 1 con la mira puesta) y el del tick anterior. */
    public static float k, kO;
    /** La Gatling: el de los mandos apunta. */
    public static boolean gatlingApunta;
    private static boolean rafaga;
    private static int rafagaT;
    /** Para la prueba del CI: apuntar y mantener el gatillo sin el ratón, y cuántas veces se ha apretado. */
    public static boolean apuntarPrueba, gatilloPrueba;
    public static int gatillos;

    // ------------------------------------------------------------------ la pose en tercera persona

    /** Apuntando, los dos brazos van al frente a la altura de los ojos (lo ven los demás jugadores). */
    public static final HumanoidModel.ArmPose POSE = com.copperslug.plataforma.ClienteComun.poseBrazo("COPPERSLUG_APUNTAR", true, (model, entity, arm) -> {
        boolean der = arm == HumanoidArm.RIGHT;
        ModelPart b = der ? model.rightArm : model.leftArm, o = der ? model.leftArm : model.rightArm;
        b.xRot = model.head.xRot - Mth.HALF_PI + 0.03F;
        b.yRot = model.head.yRot + (der ? -0.08F : 0.08F);
        b.zRot = 0;
        o.xRot = model.head.xRot - Mth.HALF_PI + 0.1F;
        o.yRot = model.head.yRot + (der ? 0.6F : -0.6F);
        o.zRot = 0;
    });

    public static void init() {}

    // ------------------------------------------------------------------ teclas

    public static boolean disparaConClic(LocalPlayer p, ItemStack s) {
        if (s.getItem() instanceof RevolverItem) return !p.isShiftKeyDown();   // agachado, el clic izquierdo gira el tambor
        if (s.getItem() instanceof MosqueteItem)   // sin bola, encasquillado o agachado: la bayoneta (el golpe de siempre)
            return !p.isShiftKeyDown() && ArmaFuegoItem.balas(s) > 0 && !ArmaFuegoItem.atascada(s);
        return s.getItem() instanceof ArmaFuegoItem;
    }

    @SubscribeEvent
    public static void tick(TickEvent.ClientTickEvent e) {
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer p = mc.player;
        if (p == null || mc.level == null) {
            apunta = rafaga = gatlingApunta = false;
            k = kO = 0;
            return;
        }
        ItemStack s = p.getMainHandItem();
        boolean gat = GatlingEntity.deJugador(p) != null;
        if (e.phase == TickEvent.Phase.START) {
            // los clics del gatillo se cogen aquí, antes de que el juego los gaste en pegar o picar
            if (!gat && mc.screen == null && mc.getOverlay() == null && disparaConClic(p, s))
                while (mc.options.keyAttack.consumeClick()) gatillo();
            return;
        }
        boolean quiere = !gat && Apuntar.apuntable(s) && mc.screen == null && (mc.options.keyUse.isDown() || apuntarPrueba)
                && !p.isUsingItem() && (apunta || !p.isShiftKeyDown()) && !p.isSpectator();
        if (quiere != apunta) {
            apunta = quiere;
            Apuntar.poner(p, quiere);
            ModNetwork.CHANNEL.sendToServer(new ApuntarPacket(quiere));
            // un clic suave de cobre al poner la mira y otro más grave al soltarla (solo lo oye el que apunta)
            p.level().playLocalSound(p.getX(), p.getY(), p.getZ(), net.minecraft.sounds.SoundEvents.COPPER_HIT, net.minecraft.sounds.SoundSource.PLAYERS,
                    quiere ? 0.30F : 0.18F, quiere ? 1.7F : 1.3F, false);
        } else if (apunta && !Apuntar.apuntando(p)) Apuntar.poner(p, true);
        gatlingApunta = gat && mc.screen == null && (mc.options.keyUse.isDown() || apuntarPrueba);
        kO = k;
        k = Mth.clamp(k + (apunta || gatlingApunta ? 0.25F : -0.25F), 0F, 1F);
        // al sacar el mosquete con su bayoneta: un destello en la punta de la hoja (solo en primera persona)
        Item actual = s.getItem();
        if (actual != ultimoObjeto) {
            if (actual instanceof MosqueteItem && !MosqueteItem.bayoneta(s).isEmpty() && mc.options.getCameraType().isFirstPerson()) brilloBayoneta(mc, p);
            ultimoObjeto = actual;
        }
        // la ráfaga de la Thompson: cada tick mientras se mantiene el gatillo
        if (rafaga) {
            boolean sigue = s.getItem() instanceof ArmaFuegoItem && mc.screen == null && (mc.options.keyAttack.isDown() || gatilloPrueba) && !p.isUsingItem();
            if (!sigue) {
                rafaga = false;
                ModNetwork.CHANNEL.sendToServer(new GatilloPacket(false));
            } else ((ArmaFuegoItem) s.getItem()).rafaga(mc.level, p, s, rafagaT++);
        }
    }

    /**
     * Con un arma que dispara con el clic izquierdo, el clic no pega ni pica. Y el clic derecho, que es apuntar, no se
     * le pasa al juego: vanilla lo repite cada 4 ticks y cada vez que el objeto «se usa» baja y sube la mano (la
     * animación de equipar), con lo que el arma apuntando iba arriba y abajo en primera persona. Agachado y sin apuntar
     * sí pasa (recargar, encerar, rascar).
     */
    @SubscribeEvent
    public static void clic(InputEvent.InteractionKeyMappingTriggered e) {
        LocalPlayer p = Minecraft.getInstance().player;
        if (p == null) return;
        if (e.isUseItem()) {
            if (GatlingEntity.deJugador(p) == null && Apuntar.apuntable(p.getMainHandItem()) && (!p.isShiftKeyDown() || apunta)) {
                e.setCanceled(true);
                e.setSwingHand(false);
            }
            return;
        }
        if (!e.isAttack()) return;
        if (GatlingEntity.deJugador(p) != null || disparaConClic(p, p.getMainHandItem())) {
            e.setCanceled(true);
            e.setSwingHand(false);
        }
    }

    /** El objeto de la mano en el tick anterior (para notar que se acaba de sacar uno). */
    private static Item ultimoObjeto;

    /** Tres destellos a lo largo de la punta de la bayoneta y un tintineo corto. */
    private static void brilloBayoneta(Minecraft mc, LocalPlayer p) {
        Vec3 mira = p.getViewVector(1F);
        Vec3 der = new Vec3(-mira.z, 0, mira.x);
        der = der.lengthSqr() < 1e-4 ? new Vec3(1, 0, 0) : der.normalize();
        for (int i = 0; i < 3; i++) {
            Vec3 q = p.getEyePosition().add(mira.scale(1.3 + 0.25 * i)).add(der.scale(0.22)).add(0, -0.18 + 0.03 * i, 0);
            mc.level.addParticle(net.minecraft.core.particles.ParticleTypes.END_ROD, q.x, q.y, q.z, 0, 0.012, 0);
        }
        p.level().playLocalSound(p.getX(), p.getY(), p.getZ(), net.minecraft.sounds.SoundEvents.AMETHYST_BLOCK_CHIME, net.minecraft.sounds.SoundSource.PLAYERS, 0.22F, 2.0F, false);
    }

    /** Aprieta el gatillo del arma de la mano: en el cliente (retroceso, espera) y se lo pide al servidor. */
    public static void gatillo() {
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer p = mc.player;
        if (p == null || mc.level == null || p.isUsingItem() || p.isSpectator()) return;
        ItemStack s = p.getMainHandItem();
        if (s.getItem() instanceof ArmaFuegoItem a) a.gatillo(mc.level, p, s);
        else if (s.getItem() instanceof RevolverItem r) r.gatillo(mc.level, p, s);
        else return;
        gatillos++;
        ModNetwork.CHANNEL.sendToServer(new GatilloPacket(true));
    }

    /** La ráfaga en el cliente (el retroceso de cada bala): la empieza y la acaba el arma. */
    public static void rafagaLocal(boolean si) {
        rafaga = si;
        if (si) rafagaT = 0;
    }

    // ------------------------------------------------------------------ campo de visión

    /** Cuánto cierra el campo de visión cada arma (1 = todo lo que diga la config). */
    private static float pesoFov(LocalPlayer p) {
        if (gatlingApunta) return 0.9F;
        Item i = p.getMainHandItem().getItem();
        if (i instanceof RevolverItem) return 0.6F;
        if (i instanceof DerringerItem) return 0.45F;
        if (i instanceof ThompsonItem) return 0.8F;
        if (i instanceof CanonManoItem) return 0.55F;
        return 1F;   // Winchester y mosquete
    }

    /**
     * Por cuánto se multiplica el campo de visión del jugador (lo usa el mixin de {@code getFieldOfViewModifier}). El
     * juego ya lo cierra un poco por andar más lento: se descuenta para que mande el valor de la config.
     */
    public static float fov(LocalPlayer p) {
        if (k <= 0F) return 1F;
        float f = 1F - (1F - EquilibrioArmas.apuntarFov()) * pesoFov(p) * k;
        if (apunta && Apuntar.apuntando(p)) f /= (float) (2.0 - Apuntar.lentitud(p)) / 2F;
        return f;
    }

    /** El retroceso se nota menos apuntando (el arma va encarada). */
    public static float retroceso() {
        return 1F - 0.4F * k;
    }

    // ------------------------------------------------------------------ el arma, al centro (primera persona)

    /**
     * Cómo va cada modelo en la mano (su transformación de primera persona) y dónde tiene la mira: con eso se calcula
     * el giro y el traslado que dejan la línea de mira en el eje de la vista.
     * {@code rx, ry}: giro del modelo; {@code tx, ty, tz}: traslado (en píxeles); {@code s}: escala; {@code (yr, zr)}:
     * el alza (atrás); {@code (yf, zf)}: el punto de mira (delante); {@code prof}: a qué distancia del ojo queda el alza.
     */
    private record Mira(float rx, float ry, float tx, float ty, float tz, float s, float yr, float zr, float yf, float zf, float prof) {}

    private static final Mira REVOLVER = new Mira(2, 20, 0.5F, 1.0F, -5, 0.8F, 12.25F, 12.5F, 11.25F, 2.5F, 0.55F);
    private static final Mira WINCHESTER = new Mira(2, 16, -1, 0.5F, -11, 0.62F, 11.3F, 1.0F, 11.5F, -13.25F, 0.36F);
    private static final Mira DERRINGER = new Mira(4, 18, 1.5F, 4.5F, -2, 0.45F, 12.3F, 10.6F, 11.4F, 1.2F, 0.5F);
    private static final Mira THOMPSON = new Mira(2, 16, -1, 0.5F, -11, 0.62F, 12.25F, 9.5F, 10.6F, -11F, 0.4F);
    private static final Mira MOSQUETE = new Mira(2, 14, -1, 2.5F, -9, 0.5F, 10.8F, 12F, 11.0F, -9F, 0.42F);
    private static final Mira CANON = new Mira(2, 12, -1, 3.0F, -11, 0.58F, 12.4F, 2.75F, 10.75F, -8F, 0.4F);

    private static Mira mira(Item i) {
        if (i instanceof RevolverItem) return REVOLVER;
        if (i instanceof WinchesterItem) return WINCHESTER;
        if (i instanceof DerringerItem) return DERRINGER;
        if (i instanceof ThompsonItem) return THOMPSON;
        if (i instanceof MosqueteItem) return MOSQUETE;
        if (i instanceof CanonManoItem) return CANON;
        return null;
    }

    /**
     * Lleva el arma de la cadera a la mira según {@link #k} (va antes de las demás animaciones de la mano). El punto
     * del alza acaba en el eje de la vista y el cañón, paralelo a él.
     */
    public static void alinear(PoseStack ps, int lado, ItemStack st, float pt) {
        Inspeccion.aplicar(ps, lado, st, pt);   // inspeccionar el arma (tecla N)
        float kk = Mth.lerp(pt, kO, k);
        if (kk <= 0.001F || gatlingApunta) return;
        Mira m = mira(st.getItem());
        if (m == null) return;
        kk = kk * kk * (3 - 2 * kk);
        // el giro del modelo en la mano (el de la mano izquierda va en espejo) y dónde cae el alza
        Quaternionf r = new Quaternionf().rotationXYZ(m.rx * Mth.DEG_TO_RAD, lado * m.ry * Mth.DEG_TO_RAD, 0);
        Vector3f alza = new Vector3f(0, (m.yr / 16F - 0.5F) * m.s, (m.zr / 16F - 0.5F) * m.s);
        r.transform(alza);
        float cx = lado * (0.56F + m.tx / 16F) + alza.x, cy = -0.52F + m.ty / 16F + alza.y, cz = -0.72F + m.tz / 16F + alza.z;
        // deshacer ese giro y levantar la boca lo justo para que el punto de mira quede a la altura del alza
        float sube = (float) Math.atan2(m.yr - m.yf, m.zr - m.zf);
        Quaternionf q = new Quaternionf().rotationX(sube).mul(new Quaternionf(r).invert());
        Quaternionf parte = new Quaternionf().slerp(q, kk);
        ps.translate((0 - cx) * kk, (-0.004F - cy) * kk, (-m.prof - cz) * kk);
        ps.translate(cx, cy, cz);
        ps.mulPose(parte);
        ps.translate(-cx, -cy, -cz);
    }

    // ------------------------------------------------------------------ las miras (HUD)

    /**
     * Lo que enseña la mira del revólver: la bala que toca, o null si no se puede saber (tras girar el tambor o con el
     * cañón en la sien: en la ruleta rusa no se ve nunca).
     */
    public static Carga revolverSiguiente(ItemStack s, float xRot) {
        if (Tambor.girado(s) || xRot >= 80F) return null;
        return Tambor.siguiente(s);
    }

    public static void hud(ForgeGui gui, GuiGraphics g, float pt, int w, int h) {
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer p = mc.player;
        if (p == null || mc.options.hideGui || mc.level == null || !mc.options.getCameraType().isFirstPerson()) return;
        float kk = Mth.lerp(pt, kO, k);
        if (kk < 0.6F) return;
        int cx = w / 2, cy = h / 2;
        GatlingEntity gat = GatlingEntity.deJugador(p);
        if (gat != null) {
            if (gatlingApunta) miraGatling(g, gat, cx, cy);
            return;
        }
        if (!apunta) return;
        ItemStack s = p.getMainHandItem();
        Item i = s.getItem();
        var f = mc.font;
        if (i instanceof RevolverItem) {
            // el tambor grande (x2) con los agujeros de las recámaras y las balas dentro, a la derecha de la mira; el
            // pequeño de siempre se oculta mientras se apunta (PistolaCliente.hud) para que no se pisen
            g.fill(cx - 7, cy, cx - 3, cy + 1, 0xC0FFFFFF);
            g.fill(cx + 4, cy, cx + 8, cy + 1, 0xC0FFFFFF);
            g.pose().pushPose();
            g.pose().translate(cx + 34, cy + 2, 0);
            g.pose().scale(2F, 2F, 1F);
            com.copperslug.client.armasfuego.pistola.PistolaCliente.dibujar(g, s, 0, 0, mc.level.getGameTime(), pt);
            g.pose().popPose();
            // y el nombre de la que toca debajo (en la ruleta rusa no se sabe: ya lo dice el interrogante del tambor)
            Carga c = revolverSiguiente(s, p.getXRot());
            if (c != null) {
                Component nombre = Component.translatable(c.clave() + ".corto");
                g.drawString(f, nombre, cx + 34 - f.width(nombre) / 2, cy + 28, c == Carga.VACIA ? 0xFF909090 : 0xFF000000 | c.color, true);
            }
        } else if (i instanceof WinchesterItem) {
            // alza de cuernos: dos patillas y la bala que va a salir
            g.fill(cx - 9, cy - 2, cx - 8, cy + 3, 0xC0FFFFFF);
            g.fill(cx + 9, cy - 2, cx + 10, cy + 3, 0xC0FFFFFF);
            g.fill(cx - 8, cy + 2, cx - 4, cy + 3, 0xC0FFFFFF);
            g.fill(cx + 5, cy + 2, cx + 9, cy + 3, 0xC0FFFFFF);
            var dep = WinchesterItem.deposito(s);
            if (!dep.isEmpty()) {
                Item b = dep.get(dep.size() - 1);
                g.fill(cx + 14, cy - 9, cx + 17, cy - 3, WinchesterItem.color(b));
                g.drawString(f, b.getDescription(), cx + 20, cy - 10, 0xFFE8E0D0, true);
            }
        } else if (i instanceof DerringerItem) {
            // dos cañones: un punto por cada bala que queda
            int n = ArmaFuegoItem.balas(s);
            for (int j = 0; j < 2; j++) g.fill(cx - 4 + j * 6, cy + 6, cx - 1 + j * 6, cy + 9, j < n ? 0xFFD6A632 : 0x80403020);
        } else if (i instanceof ThompsonItem) {
            // cuatro rayas que se abren con la ráfaga (lo que dispersa)
            int r = 5 + Math.min(10, ThompsonItem.rafagaN(s) / 3);
            g.fill(cx - r - 4, cy, cx - r, cy + 1, 0xC0FFFFFF);
            g.fill(cx + r + 1, cy, cx + r + 5, cy + 1, 0xC0FFFFFF);
            g.fill(cx, cy - r - 4, cx + 1, cy - r, 0xC0FFFFFF);
            g.fill(cx, cy + r + 1, cx + 1, cy + r + 5, 0xC0FFFFFF);
        } else if (i instanceof MosqueteItem) {
            // el punto de mira del cañón largo: un poste, y la bola cargada o no
            g.fill(cx, cy + 3, cx + 1, cy + 9, 0xC0FFFFFF);
            g.fill(cx - 3, cy + 9, cx + 4, cy + 10, 0xC0FFFFFF);
            boolean lista = ArmaFuegoItem.balas(s) > 0 && !ArmaFuegoItem.atascada(s);
            g.fill(cx + 8, cy - 2, cx + 12, cy + 2, lista ? 0xFFB0B6BC : 0x80403020);
        } else if (i instanceof CanonManoItem) {
            parabola(g, mc, p, s, w, h, pt);
        }
    }

    /** La Gatling: el calor del cañón en un arco alrededor de la mira (verde, amarillo y rojo). */
    private static void miraGatling(GuiGraphics g, GatlingEntity gat, int cx, int cy) {
        float c = Mth.clamp(gat.calor() / 100F, 0F, 1F);
        int n = 16;
        for (int j = 0; j < n; j++) {
            double a = Math.toRadians(-210 + 240.0 * j / (n - 1));
            int x = cx + (int) Math.round(Math.cos(a) * 14), y = cy + (int) Math.round(Math.sin(a) * 14);
            float fr = j / (float) (n - 1);
            int col = fr >= c ? 0x60202020 : fr < 0.5F ? 0xFF5FD35F : fr < 0.8F ? 0xFFE8C840 : 0xFFE84030;
            g.fill(x - 1, y - 1, x + 1, y + 1, col);
        }
    }

    /** Para la prueba: los puntos de la última parábola dibujada y si acaba en un bloque. */
    public static int parabolaPuntos;
    public static boolean parabolaCae;

    /**
     * El cañón de mano: la parábola que va a hacer el bolaño (la misma cuenta que el proyectil: velocidad, rozamiento
     * y gravedad), en puntos sobre la pantalla, y una cruz donde cae.
     */
    private static void parabola(GuiGraphics g, Minecraft mc, LocalPlayer p, ItemStack s, int w, int h, float pt) {
        Vec3 mira = p.getViewVector(pt);
        Vec3 q = ArmaFuegoItem.boca(p, 1.2, 0.3, 0.2);
        Vec3 v = mira.scale(CanonManoItem.velocidad(s));
        var cam = mc.gameRenderer.getMainCamera();
        Vec3 ojo = cam.getPosition();
        Quaternionf inv = new Quaternionf(cam.rotation()).conjugate();
        double fov = Math.toRadians(mc.options.fov().get() * Mth.lerp(mc.options.fovEffectScale().get().floatValue(), 1F, p.getFieldOfViewModifier()));
        double foco = (h / 2.0) / Math.tan(fov / 2);
        parabolaPuntos = 0;
        parabolaCae = false;
        for (int t = 0; t < 120; t++) {
            Vec3 sig = q.add(v);
            BlockHitResult bh = mc.level.clip(new ClipContext(q, sig, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, p));
            boolean da = bh.getType() != HitResult.Type.MISS;
            if (da) sig = bh.getLocation();
            Vector3f d = new Vector3f((float) (sig.x - ojo.x), (float) (sig.y - ojo.y), (float) (sig.z - ojo.z));
            inv.transform(d);
            if (d.z < -0.3F) {
                int x = w / 2 + (int) Math.round(d.x / -d.z * foco), y = h / 2 - (int) Math.round(d.y / -d.z * foco);
                if (x > 2 && x < w - 2 && y > 2 && y < h - 2) {
                    if (da) {
                        for (int j = -3; j <= 3; j++) {
                            g.fill(x + j, y + j, x + j + 1, y + j + 1, 0xFFFF7A20);
                            g.fill(x + j, y - j, x + j + 1, y - j + 1, 0xFFFF7A20);
                        }
                    } else if (t % 2 == 0) g.fill(x, y, x + 1, y + 1, 0xD0FFE0A0);
                    parabolaPuntos++;
                }
            }
            if (da) {
                parabolaCae = true;
                break;
            }
            q = sig;
            v = v.scale(0.99).add(0, -0.035, 0);
            if (q.y < mc.level.getMinBuildHeight() - 8) break;
        }
        if (CanonManoItem.mecha(s) >= 0) g.drawString(mc.font, Component.translatable("hud.copperslug.canon.mecha").withStyle(ChatFormatting.GOLD), w / 2 + 12, h / 2 - 12, 0xFFFF7A20, true);
    }
}

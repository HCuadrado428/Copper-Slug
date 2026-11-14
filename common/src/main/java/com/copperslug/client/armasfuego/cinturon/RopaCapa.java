package com.copperslug.client.armasfuego.cinturon;

import com.copperslug.CopperSlug;
import com.copperslug.registry.ModItems;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ItemStack;

/**
 * Las partes de la ropa cosmética que no caben en la textura de la armadura de vanilla (que es una caja alrededor de cada parte del cuerpo):
 * los sombreros con ala, la estrella de sheriff en relieve, las espuelas y la esclavina del poncho. Son modelos 3D (generar_ropa_3d.py) pegados
 * a la cabeza, el cuerpo o las piernas, y van por el mismo mixin que la cartuchera.
 */
public class RopaCapa extends RenderLayer<AbstractClientPlayer, PlayerModel<AbstractClientPlayer>> {
    public static final ResourceLocation SOMBRERO_VAQUERO = rl("ropa_sombrero_vaquero"), SOMBRERO_BANDIDO = rl("ropa_sombrero_bandido"),
            ESTRELLA = rl("ropa_estrella"), ESPUELA = rl("ropa_espuela"), ESCLAVINA = rl("ropa_esclavina");
    public static final ResourceLocation[] MODELOS = {SOMBRERO_VAQUERO, SOMBRERO_BANDIDO, ESTRELLA, ESPUELA, ESCLAVINA};

    private static ResourceLocation rl(String n) {
        return new ResourceLocation(CopperSlug.MOD_ID, "item/armas3d/" + n);
    }

    public RopaCapa(RenderLayerParent<AbstractClientPlayer, PlayerModel<AbstractClientPlayer>> padre) {
        super(padre);
    }

    @Override
    public void render(PoseStack ps, MultiBufferSource buf, int luz, AbstractClientPlayer p, float a, float b, float pt, float edad, float yaw, float pitch) {
        if (p.isInvisible()) return;
        ItemStack cabeza = p.getItemBySlot(EquipmentSlot.HEAD), pecho = p.getItemBySlot(EquipmentSlot.CHEST), pies = p.getItemBySlot(EquipmentSlot.FEET);
        if (cabeza.is(ModItems.SOMBRERO_VAQUERO.get())) pegar(ps, buf, luz, getParentModel().head, SOMBRERO_VAQUERO);
        else if (cabeza.is(ModItems.SOMBRERO_BANDIDO.get())) pegar(ps, buf, luz, getParentModel().head, SOMBRERO_BANDIDO);
        if (pecho.is(ModItems.CHALECO_VAQUERO.get())) pegar(ps, buf, luz, getParentModel().body, ESTRELLA);
        else if (pecho.is(ModItems.PONCHO_BANDIDO.get())) pegar(ps, buf, luz, getParentModel().body, ESCLAVINA);
        if (pies.is(ModItems.BOTAS_VAQUERO.get())) {
            pegar(ps, buf, luz, getParentModel().rightLeg, ESPUELA);
            pegar(ps, buf, luz, getParentModel().leftLeg, ESPUELA);
        }
    }

    /** Pone el modelo en la parte del cuerpo: su origen es el de la parte, con la y hacia arriba y el frente en la z grande. */
    private static void pegar(PoseStack ps, MultiBufferSource buf, int luz, ModelPart parte, ResourceLocation rl) {
        ps.pushPose();
        parte.translateAndRotate(ps);
        ps.scale(1F, -1F, -1F);
        ps.translate(-0.5, 0, -0.5);
        BakedModel bm = com.copperslug.plataforma.ClienteComun.modelo(rl);
        Minecraft.getInstance().getBlockRenderer().getModelRenderer().renderModel(ps.last(), buf.getBuffer(Sheets.cutoutBlockSheet()), null, bm,
                1F, 1F, 1F, luz, OverlayTexture.NO_OVERLAY);
        ps.popPose();
    }
}

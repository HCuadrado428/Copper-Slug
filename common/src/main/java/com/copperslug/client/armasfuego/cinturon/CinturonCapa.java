package com.copperslug.client.armasfuego.cinturon;

import com.copperslug.CopperSlug;
import com.copperslug.armasfuego.cinturon.CartucheraItem;
import com.copperslug.armasfuego.cinturon.Cinturon;
import com.copperslug.armasfuego.cinturon.FundaItem;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;

/**
 * Dibuja en el jugador lo que lleva en el cinturón: la cartuchera alrededor de la cintura y la funda en la cadera
 * derecha (con la culata asomando si lleva un arma). Se ve en el hueco de cinturón de Curios/Trinkets (que se sincroniza
 * con los demás jugadores) y, desde el inventario, solo para uno mismo (los demás no reciben el inventario ajeno).
 */
public class CinturonCapa extends RenderLayer<AbstractClientPlayer, PlayerModel<AbstractClientPlayer>> {
    public static final ResourceLocation CARTUCHERA = rl("cinturon_cartuchera"), FUNDA = rl("cinturon_funda"), FUNDA_LLENA = rl("cinturon_funda_llena");
    public static final ResourceLocation[] MODELOS = {CARTUCHERA, FUNDA, FUNDA_LLENA};

    private static ResourceLocation rl(String n) {
        return net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "item/armas3d/" + n);
    }

    public CinturonCapa(RenderLayerParent<AbstractClientPlayer, PlayerModel<AbstractClientPlayer>> padre) {
        super(padre);
    }

    @Override
    public void render(PoseStack ps, MultiBufferSource buf, int luz, AbstractClientPlayer p, float a, float b, float pt, float edad, float yaw, float pitch) {
        if (p.isInvisible()) return;
        ItemStack cart = Cinturon.buscar(p, x -> x.getItem() instanceof CartucheraItem);
        ItemStack funda = Cinturon.buscar(p, x -> x.getItem() instanceof FundaItem);
        if (cart.isEmpty() && funda.isEmpty()) return;
        ps.pushPose();
        getParentModel().body.translateAndRotate(ps);
        // a la cintura; el modelo tiene y hacia arriba y el frente en z grande
        ps.translate(0, 9.75 / 16.0, 0);
        ps.scale(1F, -1F, -1F);
        ps.translate(-0.5, -0.5, -0.5);
        if (!cart.isEmpty()) dibujar(ps, buf, CARTUCHERA, luz);
        if (!funda.isEmpty()) dibujar(ps, buf, FundaItem.arma(funda).isEmpty() ? FUNDA : FUNDA_LLENA, luz);
        ps.popPose();
    }

    private static void dibujar(PoseStack ps, MultiBufferSource buf, ResourceLocation rl, int luz) {
        BakedModel bm = com.copperslug.plataforma.ClienteComun.modelo(rl);
        Minecraft.getInstance().getBlockRenderer().getModelRenderer().renderModel(ps.last(), buf.getBuffer(Sheets.cutoutBlockSheet()), null, bm,
                1F, 1F, 1F, luz, OverlayTexture.NO_OVERLAY);
    }
}

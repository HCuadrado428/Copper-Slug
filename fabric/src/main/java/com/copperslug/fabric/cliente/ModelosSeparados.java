package com.copperslug.fabric.cliente;

import com.copperslug.CopperSlug;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.fabricmc.fabric.api.client.model.BakedModelManagerHelper;
import net.fabricmc.fabric.api.client.model.loading.v1.PreparableModelLoadingPlugin;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.block.model.BlockModel;
import net.minecraft.client.renderer.block.model.ItemOverrides;
import net.minecraft.client.renderer.block.model.ItemTransforms;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.client.resources.model.ModelResourceLocation;
import net.minecraft.core.Direction;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.level.block.state.BlockState;

import java.io.Reader;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;

/**
 * El cargador de modelos {@code forge:separate_transforms} en Fabric (las armas: 3D en la mano y plano en el
 * inventario). Cada modelo así se carga como su "base" (con los overrides de arriba) y su vista "gui" como un modelo
 * gemelo ({@code <id>__gui}); al dibujar en el inventario, ItemRendererMixin cambia uno por otro.
 */
public final class ModelosSeparados {
    private ModelosSeparados() {}

    record Par(String base, String gui, boolean luzFrente) {}

    static void registrar() {
        PreparableModelLoadingPlugin.register(ModelosSeparados::leer, (datos, ctx) -> {
            ctx.addModels(datos.keySet().stream().map(ModelosSeparados::gemelo).toList());
            ctx.resolveModel().register(rc -> {
                ResourceLocation id = rc.id();
                Par p = datos.get(id);
                if (p != null) return modelo(id, p.base());
                if (id.getPath().endsWith("__gui")) {
                    Par q = datos.get(new ResourceLocation(id.getNamespace(), id.getPath().substring(0, id.getPath().length() - 5)));
                    if (q != null) return modelo(id, q.gui());
                }
                return null;
            });
            ctx.modifyModelAfterBake().register((m, c) -> {
                if (m == null) return null;
                ResourceLocation id = c.id();
                if (id instanceof ModelResourceLocation mrl && "inventory".equals(mrl.getVariant()))
                    id = new ResourceLocation(mrl.getNamespace(), "item/" + mrl.getPath());
                Par p = datos.get(id);
                return p == null || m instanceof Separado ? m : new Separado(m, gemelo(id), p.luzFrente());
            });
        });
    }

    private static ResourceLocation gemelo(ResourceLocation id) {
        return new ResourceLocation(id.getNamespace(), id.getPath() + "__gui");
    }

    private static BlockModel modelo(ResourceLocation id, String json) {
        BlockModel b = BlockModel.fromString(json);
        b.name = id.toString();
        return b;
    }

    private static CompletableFuture<Map<ResourceLocation, Par>> leer(ResourceManager rm, Executor ex) {
        return CompletableFuture.supplyAsync(() -> {
            Map<ResourceLocation, Par> out = new HashMap<>();
            var todos = rm.listResources("models/item", r -> r.getNamespace().equals(CopperSlug.MOD_ID) && r.getPath().endsWith(".json"));
            todos.forEach((rl, res) -> {
                try (Reader r = res.openAsReader()) {
                    JsonElement e = JsonParser.parseReader(r);
                    if (!e.isJsonObject()) return;
                    JsonObject o = e.getAsJsonObject();
                    if (!o.has("loader") || !"forge:separate_transforms".equals(o.get("loader").getAsString())) return;
                    JsonObject base = o.getAsJsonObject("base").deepCopy();
                    if (o.has("overrides")) base.add("overrides", o.get("overrides"));
                    if (o.has("gui_light")) base.add("gui_light", o.get("gui_light"));
                    JsonObject gui = o.getAsJsonObject("perspectives").getAsJsonObject("gui");
                    String p = rl.getPath();
                    ResourceLocation id = new ResourceLocation(rl.getNamespace(), p.substring("models/".length(), p.length() - ".json".length()));
                    out.put(id, new Par(base.toString(), gui.toString(), o.has("gui_light") && "front".equals(o.get("gui_light").getAsString())));
                } catch (Exception x) {
                    CopperSlug.LOG.warn("Copper Slug: no se pudo leer el modelo {}", rl, x);
                }
            });
            return out;
        }, ex);
    }

    /** El modelo de un arma: en todo es su base 3D; en el inventario, ItemRendererMixin usa {@link #gui()}. */
    public static final class Separado implements BakedModel {
        public final BakedModel base;
        private final ResourceLocation gemelo;
        private final boolean luzFrente;
        private BakedModel gui;

        Separado(BakedModel base, ResourceLocation gemelo, boolean luzFrente) {
            this.base = base;
            this.gemelo = gemelo;
            this.luzFrente = luzFrente;
        }

        public BakedModel gui() {
            if (gui == null) {
                BakedModel g = BakedModelManagerHelper.getModel(Minecraft.getInstance().getModelManager(), gemelo);
                gui = g != null ? g : base;
            }
            return gui;
        }

        public BakedModel para(ItemDisplayContext ctx) {
            return ctx == ItemDisplayContext.GUI ? gui() : base;
        }

        @Override
        public List<net.minecraft.client.renderer.block.model.BakedQuad> getQuads(BlockState st, Direction d, RandomSource r) {
            return base.getQuads(st, d, r);
        }

        @Override
        public boolean useAmbientOcclusion() {
            return base.useAmbientOcclusion();
        }

        @Override
        public boolean isGui3d() {
            return base.isGui3d();
        }

        @Override
        public boolean usesBlockLight() {
            return !luzFrente && base.usesBlockLight();
        }

        @Override
        public boolean isCustomRenderer() {
            return base.isCustomRenderer();
        }

        @Override
        public TextureAtlasSprite getParticleIcon() {
            return base.getParticleIcon();
        }

        @Override
        public ItemTransforms getTransforms() {
            return base.getTransforms();
        }

        @Override
        public ItemOverrides getOverrides() {
            return base.getOverrides();
        }
    }
}

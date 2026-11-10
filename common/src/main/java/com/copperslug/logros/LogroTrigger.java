package com.copperslug.logros;

import com.copperslug.CopperSlug;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.advancements.critereon.ContextAwarePredicate;
import net.minecraft.advancements.critereon.EntityPredicate;
import net.minecraft.advancements.critereon.SimpleCriterionTrigger;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;

import java.util.Optional;

/**
 * El criterio propio de los logros, {@code copperslug:accion}: se cumple cuando el código del mod avisa de que el
 * jugador ha hecho esa acción ({@link LogrosMiscelanea#dar}). En el JSON: {@code {"trigger": "copperslug:accion",
 * "conditions": {"accion": "foto"}}}.
 */
public class LogroTrigger extends SimpleCriterionTrigger<LogroTrigger.Instancia> {
    public static final ResourceLocation ID = net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(CopperSlug.MOD_ID, "accion");

    @Override
    public Codec<Instancia> codec() {
        return Instancia.CODEC;
    }

    public void trigger(ServerPlayer p, String accion) {
        trigger(p, i -> i.accion.equals(accion));
    }

    public record Instancia(Optional<ContextAwarePredicate> player, String accion) implements SimpleCriterionTrigger.SimpleInstance {
        public static final Codec<Instancia> CODEC = RecordCodecBuilder.create(i -> i.group(
                EntityPredicate.ADVANCEMENT_CODEC.optionalFieldOf("player").forGetter(Instancia::player),
                Codec.STRING.fieldOf("accion").forGetter(Instancia::accion)
        ).apply(i, Instancia::new));
    }
}

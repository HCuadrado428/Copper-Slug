# Portar cambios de las armas desde Miscelánea

Las armas de Copper Slug salen del código de Miscelánea (rama `arreglos`) casi sin tocar. El paso de un mod al otro es
mecánico (`herramientas/portar.py`): se cambian los paquetes y el id, y se eligen los recursos. Por eso, para traer
cambios nuevos, lo más fiable es **portar la diferencia** entre dos commits de Miscelánea y fusionarla con lo de aquí.

## Lo normal: traer lo nuevo

```sh
# en la raíz de Copper Slug, con un clon de Miscelánea al lado
git -C ../miscelanio_nova fetch origin arreglos
herramientas/portar_cambios.py ../miscelanio_nova $(cat herramientas/ultimo_portado.txt) origin/arreglos
```

Qué hace:

1. Pasa por `portar.py` los dos commits de Miscelánea (el último portado y el nuevo).
2. Para cada fichero que haya cambiado, hace una fusión a tres bandas (`git merge-file`). La base es lo portado del commit
   viejo, «la nuestra» es el fichero de aquí y «la otra» es lo portado del nuevo. Así entran los cambios sin perder los
   retoques de Copper Slug.
3. Copia los ficheros nuevos, lista los borrados (no los borra) y avisa de los binarios que han cambiado en los dos lados.
4. Apunta el commit nuevo en `herramientas/ultimo_portado.txt`.

Si sale **CON CONFLICTOS**, busca `<<<<<<<` en los ficheros que dice y arréglalos a mano. Después compila (el workflow
«Compilar» lo hace al subir) y deja que pase «Probar en el juego».

En la rama `1.21.1` se añade `--rama-mc 1.21.1`. Así se aplican antes los cambios de API de 1.21.1
(`herramientas/a_1_21_1.py`) a las dos versiones portadas, y la fusión compara lo mismo.

## Qué cambia `portar.py` (y por qué casi todo entra solo)

- `com.miscelanea.*` pasa a `com.copperslug.*`, el id `miscelanea` a `copperslug` (también en claves de idioma y en JSON)
  y `Miscelanea.MOD_ID` a `CopperSlug.MOD_ID`.
- `net.minecraftforge.*` pasa a `com.copperslug.shim.*`. Los shims imitan la parte de la API de Forge que usan las armas
  (eventos con `@SubscribeEvent`, `DeferredRegister`/`RegistryObject`, `ForgeConfigSpec`, `NetworkEvent`,
  `PacketDistributor`, `IClientItemExtensions`…). Cada cargador los alimenta desde sus eventos (`forge/`, `fabric/`,
  `neoforge/`).
- Los métodos de las extensiones de Forge (`shouldCauseReequipAnimation`, `onEntitySwing`, `getAttributeModifiers(slot,
  stack)`…) pierden el `@Override`. En Forge siguen sobrescribiendo; en Fabric los llaman los mixins de `fabric/`.
  `initializeClient` pasa a llamarse `extensionesCliente`.
- `EnchantmentCategory.create`, `ArmPose.create`, `getModel(ResourceLocation)` e `ItemProperties.register` pasan por la
  plataforma (`com.copperslug.plataforma`).
- Los registros (`ModItems`, `ModSounds`, `ModEntities`, `ModEnchantments`, `ModEffects`, `ModRecipes`) se generan con
  solo las entradas de las armas. `Suscriptores.java` se genera con las clases que tienen `@Mod.EventBusSubscriber`.
- Recursos: los modelos y texturas de los objetos registrados (y lo que nombra el código), los sonidos que usan, las
  partículas, los logros de `armas/`, las recetas de su munición y las claves de idioma que se usan. Lo propio de Copper
  Slug está en `herramientas/lang_extra/`.

## Si añaden algo nuevo en Miscelánea

- **Una clase nueva** dentro de `armasfuego/` o `client/armasfuego/`: entra sola. Si usa algo de Forge que el shim no
  tiene, no compilará: añade lo que falte en `common/.../shim` y, si es un evento, reenvíalo en `CopperSlugForge`,
  `ClienteForge`, `CopperSlugFabric` y `ClienteFabric` (y en NeoForge en la rama 1.21.1).
- **Un objeto, sonido, encantamiento o entidad**: entra solo si su declaración en el registro de Miscelánea menciona
  `armasfuego`. Si no (munición simple, `new Item(...)`), añade su nombre a `ITEMS_EXTRA` en `portar.py`.
- **Un paquete de red**: regístralo en `network/ModNetwork.java` (una línea).
- **Algo de otra parte de Miscelánea** (el móvil, la feria…): Copper Slug no lo tiene. Sustitúyelo con criterio y
  apúntalo en el commit.
- **Pruebas nuevas en PruebaCI de Miscelánea**: `client/prueba/PruebaCI.java` es una copia adaptada. Copia a mano los
  pasos nuevos de armas.

## Lo que se quitó o se cambió respecto a Miscelánea

- Fotos con la mira del rifle: van siempre a la carpeta de capturas. No hay móvil.
- Cinta de palomitas: lleva su propio «cucurucho de palomitas» (semillas de trigo al horno, al ahumador o a la hoguera).
- Tecla de la manga de la Derringer: va en la categoría «Copper Slug» de los controles.
- El reparto de daño `DanoArma`: solo queda la marca `extra`. Las armas de fuego hacen su reparto en su propio código.
- Fabric 1.20.1 no tiene atributo de alcance: la bayoneta del mosquete no llega más lejos (en Forge y NeoForge sí).
- Las texturas de la polea, las palomitas y la bengala se han redibujado a 16×16. Todo lo de objetos y bloques es
  16×16 (lo comprueban el CI y la prueba en el juego).

## Rama 1.21.1: estado (en curso)

Ya está:
- La compilación: NeoForge y common con ModDevGradle, Forge con ForgeGradle 6 y Fabric con Loom.
- El volcado del classpath.
- `herramientas/a_1_21_1.py` convierte el código de main:
  - `ResourceLocation` y las firmas nuevas (tooltips, `getUseDuration`, `hurtAndBreak`, `defineSynchedData`,
    `getAddEntityPacket`);
  - el NBT de los objetos, a `shim/Nbt` (sobre `custom_data`, con una etiqueta viva);
  - los encantamientos: pasan a datos (`data/copperslug/enchantment` y sus etiquetas, generados desde ModEnchantments),
    y en el código se leen con `shim/Enc`;
  - las carpetas y el formato de las recetas y los logros.

Falta, en common (93 errores al compilar):
- `LogroTrigger`: el criterio con codec, y registrarlo con `Registries.TRIGGER_TYPE`.
- `Tirolinas` y `LucesTemporales`: `SavedData.Factory` y `save(tag, provider)`.
- `MosqueteBayonetaRecipe` (`CraftingInput`) y su serializador.
- Los atributos de la bayoneta del mosquete: componente `ATTRIBUTE_MODIFIERS` en el objeto.
- Los `VertexConsumer` de tres renderers (`addVertex`/`setColor`/`setUv`…).
- La pestaña del creativo: los libros con `Holder` de los encantamientos.
- El plugin de JEI (`ShapelessRecipe` y `RecipeHolder`).
- PruebaCI: lo de los encantamientos con `Holder`, `getLootData`, `getRecipeFor` con `CraftingInput` y los logros con
  `AdvancementHolder`.

Falta en los cargadores:
- NeoForge: la plataforma (eventos de `net.neoforged`, ticks Pre/Post, red con `CustomPacketPayload`, GLM con
  `MapCodec`, `RegisterClientExtensionsEvent`).
- Fabric: la red con payloads, `LootTableEvents` nuevo y el AW de 1.21.1.
- Forge 52: la plataforma.
- En los tres: los modelos `separate_transforms`, que en NeoForge son `neoforge:separate_transforms`.
- La prueba en el juego de 1.21.1 en `probar.yml`.

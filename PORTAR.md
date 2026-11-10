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

Hecho a mano después (ya no hay errores de compilación en ninguno de los cuatro):
- common: el criterio de los logros con códec (registrado en `Registries.TRIGGER_TYPE`), `SavedData.Factory` (lo hace
  ya el conversor), la receta del mosquete con `CraftingInput`, los vértices nuevos, los libros de la pestaña con
  `Holder`, JEI con `RecipeHolder` y PruebaCI (una clase `V` con lo que cambia de API).
- La bayoneta del mosquete: los atributos ya no se piden por objeto; `MosqueteItem.atributos` los calcula y se ponen
  en el componente `ATTRIBUTE_MODIFIERS` al calar o quitar la espada y en cada tick del inventario. El alcance es el
  atributo vanilla `entity_interaction_range`, en los tres cargadores.
- NeoForge: la plataforma entera (`neoforge/`). La red envuelve cada paquete en un `CustomPacketPayload` con su tipo;
  la pose del revólver va por `enumextensions.json`; el cargador `forge:separate_transforms` se registra como alias del
  de NeoForge, así los modelos no cambian.
- Forge 52: red con `ChannelBuilder`, GLM con `MapCodec`. No tiene evento de capas del HUD ni `FakePlayer`: el HUD lo
  dibuja `GuiMixin` al final del HUD vanilla y el jugador de mentira es uno propio.
- Fabric: red con `PayloadTypeRegistry`, botín con `LootTableEvents` v3 y códec, modelos con `FabricBakedModelManager`.
  Ya no hay categorías de encantamiento (los encantamientos son datos), así que fuera sus mixins.
- AT de NeoForge y de Forge y AW de Fabric con lo mismo que el AT de common.
- `probar-1211.yml` (en main, porque los `workflow_run` usan el archivo de main): servidores de los tres y el juego en
  los tres; en NeoForge con PruebaCI y capturas.

Falta comprobar en el juego (los mixins de cliente de Fabric no los comprueba el compilador) y lo que salga en la
prueba de NeoForge.

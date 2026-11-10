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
- Los encantamientos de la espada calada en la bayoneta: en Forge van por `getEnchantmentLevel`/`getAllEnchantments`
  del objeto y `PlayerXpEvent.PickupXp` (Reparación). En Fabric los hacen `EnchantmentHelperMixin` (nivel y recorrido
  de los encantamientos al golpear) y `ExperienceOrbMixin` (el `PickupXp` del shim).
- Las texturas de la polea, las palomitas y la bengala se han redibujado a 16×16. Todo lo de objetos y bloques es
  16×16 (lo comprueban el CI y la prueba en el juego).

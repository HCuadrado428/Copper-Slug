# Notas para Bloomberto, desde Copper Slug

Copper Slug usó Bloomberto 0.1.0 durante unos días y se ha quitado. Aquí queda lo que usaba, lo que falló y qué haría falta para volver a
integrarlo sin problemas. No es una crítica: casi todo lo que falló tiene arreglo en el lado de Bloomberto.

## Por qué se ha quitado

1. **Un jar viejo con el mismo número de versión se cae al apuntar.** Todas las compilaciones de Bloomberto se llaman igual
   (`bloomberto-0.1.0+1.20.1-fabric.jar`), así que Fabric y Forge no pueden distinguir un jar viejo de uno nuevo. El jugador tenía uno
   anterior a `CameraZoom` y el juego arrancó bien; se cayó más tarde, al apuntar con el revólver:

   ```
   java.lang.NoClassDefFoundError: com/dougg865/bloomberto/api/render/CameraZoom
       at com.copperslug.client.armasfuego.comun.Apuntado.zoom(Apuntado.java:244)
   ```

   Copper Slug comprobaba al arrancar que estuvieran las 15 clases que usa (con `ClassLoader.getResource`, sin cargarlas, para no
   tocar clases de cliente en un servidor) y paraba con un mensaje claro. Se ha quitado junto con la dependencia, pero la idea es buena.

2. **Un fallo propio de Bloomberto al arrancar en Fabric 1.20.1.** Dos informes del 13 de noviembre:

   ```
   Caused by: java.lang.NullPointerException: Cannot invoke "net.minecraft.class_3304.method_14477(net.minecraft.class_3302)"
       because the return value of "net.minecraft.class_310.method_1478()" is null   (Minecraft.getResourceManager())
       at com.dougg865.bloomberto.api.render.Shaders.listenForReloads(Shaders.java:38)
       at com.dougg865.bloomberto.Bloomberto.initClient(Bloomberto.java:63)
       at com.dougg865.bloomberto.platform.fabric.BloombertoFabricClient.onInitializeClient(BloombertoFabricClient.java:14)
   ```

   En el entrypoint `client` de Fabric el `ResourceManager` de Minecraft todavía no existe. Se registra un recargador de recursos
   en ese momento en lugar de pedirlo después. En Fabric lo normal es `ResourceManagerHelper.get(ResourceType.CLIENT_RESOURCES)
   .registerReloadListener(...)`, que funciona desde el entrypoint; en Forge, `RegisterClientReloadListenersEvent`.
   Entorno donde salió: Modrinth App, Windows 11, Minecraft 1.20.1, Fabric Loader 0.20.1, Fabric API 0.92.12, Iris 1.7.6 y Sodium
   0.5.12.

3. **Distribución.** Copper Slug exigía Bloomberto (`mandatory = true` en Forge, `depends` en Fabric) y Bloomberto no estaba
   publicado: el CI de Copper Slug lo compilaba desde un commit (`bloomberto.properties` + `herramientas/bloomberto.sh`) y lo adjuntaba a
   cada build. Quien instalaba Copper Slug tenía que poner además el jar de Bloomberto en `mods/`, y ese jar era el del punto 1.

## Qué usaba Copper Slug (15 clases)

| Clase | Para qué |
|---|---|
| `api.render.CameraZoom` | Zoom de la mira. `CameraZoom.shared().zoomTo(aumento, ticks, easing)` y `reset(0, Easing.LINEAR)`. Se acerca en 5 ticks con `OUT_CUBIC` y se suelta en 4 con `IN_OUT_SINE`. El aumento se calculaba como `tan(fov/2) / tan(fov/2 * f)` a partir del multiplicador de campo de visión `f` de la config. |
| `api.render.CameraShake` | Temblor al disparar: `CameraShake.shared().shake(intensidad 0..1, ticks, 2.5F)`. |
| `api.animation.Easing`, `KeyframeTrack` | Curvas del retroceso: `KeyframeTrack.create().at(0, 0F).at(1, 1F, Easing.OUT_CUBIC).at(6, 0F, Easing.OUT_BACK)` para la cámara y otra para la mano. |
| `api.effects.Particles` | Patrones de partículas en las granadas: `Particles.of(tipo).sphere(c, 0.4, 28).speed(0.45).spawn(nivel)`, también `.ring(...)` y `.spiral(...)`. |
| `api.effects.Trail`, `api.render.WorldDraw`, `api.color.Color`, `api.client.ClientEvents` | Estelas de las balas: `new Trail(cola, 24)`, `ClientEvents.CLIENT_TICK`, `DISCONNECT` y `WORLD_RENDER` (con `WorldDraw.of(ctx)`), y `Color.ofFloats(r, g, b, a)`. |
| `api.animation.model.GeoModel`, `GeoRenderer`, `ModelLibrary`, `AnimationClip`, `AnimationController`, `Pose` | Piezas de armas animadas: la grúa y el tambor del revólver, la palanca de la Winchester y el cerrojo del rifle. Modelos en `assets/copperslug/geo/*.geo.json`, animaciones en `assets/copperslug/animations/*.animation.json`, y el atlas en `textures/geo/` (las texturas de `textures/item/` tienen que ser de 16x16, así que el atlas no podía ir ahí). Se dibujaban con `GeoRenderer.render(geo, pose, ps, buffer, luz, overlay, color)` y `ModelLibrary.animations(...).controller()`. |

El código de todo esto sigue en el historial de Copper Slug. El último estado con Bloomberto es el commit `cbe2e83` de `main`; por
ejemplo:

```
git show cbe2e83:common/src/main/java/com/copperslug/client/armasfuego/comun/PiezasAnimadas.java
git show cbe2e83:common/src/main/java/com/copperslug/client/armasfuego/pistola/RevolverTambor.java
```

## Qué haría falta para volver a usarlo

- **Versión que cambie con cada compilación.** Por ejemplo `0.1.0+build.N`, o al menos un número de API que se suba cuando se añada o
  quite una clase pública, y que Copper Slug pueda exigir (`>=`). Hoy el cargador acepta cualquier jar.
- **Arreglar el `NullPointerException` del arranque** (punto 2) y probar el arranque en Fabric y Forge con y sin Iris/Sodium.
- **Publicarlo** (Modrinth) antes que cualquier mod que lo exija, con un jar por versión de Minecraft y cargador: 1.20.1 Forge y
  Fabric; 1.21.1 NeoForge, Forge y Fabric.
- **Una comprobación de arranque** como la del punto 1, o que Bloomberto exponga una constante de versión de API para que cada mod la
  compruebe.
- Dejar claro qué es API estable y qué puede cambiar entre 0.x: Copper Slug llegó a depender de 15 clases a la vez.

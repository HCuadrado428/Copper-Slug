# Copper Slug

**English** · [Castellano](#castellano)

Nine copper firearms for Minecraft, from the Wild West and beyond: the Russian-roulette **revolver**, the **scoped
rifle** (with ziplines), the **pressure shotgun**, the **Gatling** gun, the **Winchester 1873**, the **Derringer**, the
**Thompson** (in its violin case), the **musket** with bayonet and the **hand cannon**. Each one has its own special
ammo and enchantments.

- Guns are not crafted: they are found in vanilla structure chests. Most ammo, the violin case and the bayonet fitting
  can be crafted.
- The copper rusts over time: wax it, or scrape it with an axe. Each rust phase trades accuracy for damage.
- Every gun has a HUD, sounds, particles, 3D models in hand (flat icons in the inventory) and its own advancement tab
  (57 advancements).
- Server config: `<world>/serverconfig/copperslug-server.toml` (damage, fire rate, range, rust, wax, loot chances…).

## Weapons

| Weapon | What it does |
|--------|--------------|
| Roulette revolver | Six-shot cylinder. Russian roulette, quick draw, duels against other players, special bullets (blank, magnet, sedative dart, flare). |
| Spyglass rifle | Scoped. Hold your breath for more damage, headshots, ziplines with rope bullets, paint and tracer bullets. |
| Pressure shotgun | Pump it to build pressure: cartridges go in a hopper, it sucks in items and pulls mobs, and the cartridges have effects (gravel, incendiary, frost, honey, salt, seeds, confetti, rubber). |
| Crank Gatling Gun | Automatic, stationary. Overheats if you keep cranking; belts of peas or popcorn; can be a redstone turret. |
| Winchester 1873 | Lever-action rifle with a tube magazine. Ice, silver and mixed ammo. |
| Derringer | Hidden up the sleeve. Quick draw trick, smoke, cards and gold bullets. |
| Thompson | Drum-fed submachine gun inside a violin case. Water, ink and tracer drums. Play the case with a bow for music. |
| Bayonet musket | Long musket with bolas, harpoon bolas and chain bolas. Fit a sword on it as a bayonet: it keeps the sword's enchantments (Sharpness, Fire Aspect, Looting, Sweeping Edge and Mending). |
| Hand cannon | Fires iron bolas that explode. Incendiary, fireworks and bouncing bolas, falling blocks and anvils. |

## Controls

Left click shoots and holding right click aims, as in most shooters. Aiming brings the gun to the centre of the screen,
narrows the field of view, tightens the spread and slows you down; other players see you raise the gun.

| Weapon | Left click | Hold right click | Sneaking |
|--------|------------|------------------|----------|
| Roulette revolver | Shoot (looking straight down: at your own temple) | Aim. The sight shows the next round, except in Russian roulette (after spinning the cylinder, or at your temple) | Left click spins the cylinder. Right click loads the ammo in your other hand, waxes (honeycomb) or scrapes (axe), fans the hammer (with Fanning) or challenges a player to a duel |
| Spyglass rifle | Shoot, or work the bolt if no round is ready | Aim through the spyglass (zoom and rangefinder) | Left click works the bolt by hand; while aiming, it takes a photo |
| Pressure shotgun | Shoot, from the hip only: it does not aim | Pump | Hold right click to suck in items and pull mobs |
| Winchester 1873 | Shoot | Aim (the sight shows the round about to leave) | Hold right click to reload round by round, or to clear a jam |
| Derringer | Shoot | Aim | Hold right click to reload. The sleeve key (K) draws it from anywhere in the inventory |
| Thompson | Hold for burst fire | Aim (the sight opens up as the burst goes on) | Hold right click to change the drum |
| Bayonet musket | Shoot. With no ball loaded, jammed or sneaking, it is a bayonet thrust | Aim | Hold right click to reload (powder, ball, ramrod) |
| Hand cannon | Light the fuse | Aim. The sight draws the arc of the ball | Hold right click to reload |
| Crank Gatling Gun (at the controls) | Hold to turn the crank and fire | Aim. The sight shows the barrel heat | Right click picks it up |

Every copper gun: sneak + right click with a honeycomb or an axe in the other hand waxes or scrapes it. The aiming values
(spread, field of view and slowdown) are in the server config, section `armas_de_fuego_equilibrio.apuntado`. Press N to
inspect the gun in your hand (rebindable under Controls > Copper Slug).

## Downloads

There are no versioned releases yet: every CI build is published as a `build-N` prerelease.

| Minecraft | Loader | Jar |
|-----------|--------|-----|
| 1.20.1 | Forge 47.x (also works on NeoForge 1.20.1 47.1) | `copperslug-forge-1.20.1-1.0.0.jar` |
| 1.20.1 | Fabric | `copperslug-fabric-1.20.1-1.0.0.jar` |
| 1.21.1 | NeoForge | `copperslug-neoforge-1.21.1-1.0.0.jar` |
| 1.21.1 | Forge | `copperslug-forge-1.21.1-1.0.0.jar` |
| 1.21.1 | Fabric | `copperslug-fabric-1.21.1-1.0.0.jar` |

## Requirements

- **Forge / NeoForge:** nothing else.
- **Fabric:** [Fabric API](https://modrinth.com/mod/fabric-api).
- Optional: [JEI](https://modrinth.com/mod/jei) shows where each weapon is found and the bayonet recipe.
- Shaders (Embeddium/Oculus on Forge, Sodium/Iris on Fabric) work.

Copper Slug is the firearms part of the Miscelánea mod as a standalone mod. It isn't meant to be installed together with
Miscelánea.

---

## Castellano

Nueve armas de fuego de cobre para Minecraft, del Oeste y de más allá: el **revólver** de ruleta rusa, el **rifle de
catalejo** (con tirolinas), la **escopeta de presión**, la **Gatling**, la **Winchester 1873**, la **Derringer**, la
**Thompson** (en su estuche de violín), el **mosquete** con bayoneta y el **cañón de mano**. Cada una con su munición
especial y sus encantamientos.

- Las armas no se fabrican: se encuentran en los cofres de estructuras vanilla. La mayor parte de la munición, el estuche
  de violín y la forma de calar la bayoneta sí se fabrican.
- El cobre se oxida con el tiempo: se encera o se rasca con un hacha. Cada fase de óxido cambia precisión por daño.
- Cada arma tiene HUD, sonidos, partículas, modelos 3D en la mano (iconos planos en el inventario) y su propia pestaña de
  logros (57 logros).
- Config del servidor: `<mundo>/serverconfig/copperslug-server.toml` (daño, cadencia, alcance, óxido, cera, probabilidad
  en cofres…).

## Armas

| Arma | Qué hace |
|------|----------|
| Revólver de ruleta | Tambor de seis. Ruleta rusa, desenfunde, duelos contra otros jugadores y balas especiales (fogueo, imán, dardo de sedante, bengala). |
| Rifle de catalejo | Con mira. Contener la respiración da más daño, hay headshots, tirolinas con bala de cuerda, pintura y balas trazadoras. |
| Escopeta de presión | Se bombea para subir la presión: los cartuchos van a la tolva, aspira objetos y tira de los mobs, y cada cartucho tiene su efecto (grava, incendiario, escarcha, miel, sal, semillas, confeti, goma). |
| Gatling de manivela | Automática y fija. Se calienta si no paras de girar la manivela; cintas de guisantes o palomitas; puede ser una torreta con redstone. |
| Winchester 1873 | Palanca de repetición con depósito tubular. Balas de hielo, de plata y mezclas. |
| Derringer | Escondida en la manga. Truco de tahúr al sacarla, balas de humo, cartas marcadas y balas de oro. |
| Thompson | Subfusil con tambor, dentro de un estuche de violín. Tambores de agua, de tinta y trazadores. Toca el estuche con un arco para hacer música. |
| Mosquete con bayoneta | Mosquete largo con bolas, bolas arpón y bolas encadenadas. Cala una espada en el mosquete como bayoneta: conserva los encantamientos de la espada (Filo, Aspecto ígneo, Botín, Barrido, Reparación). |
| Cañón de mano | Dispara bolaños que estallan. Bolaños incendiarios, de fuegos artificiales y saltarines, y bloques que caen o yunques disparados. |

## Controles

El clic izquierdo dispara y mantener el clic derecho apunta, como en casi todos los juegos de tiros. Al apuntar, el arma
va al centro de la pantalla, se cierra el campo de visión, se dispersa menos y se anda más lento; los demás jugadores
ven que encaras el arma.

| Arma | Clic izquierdo | Mantener clic derecho | Agachado |
|------|----------------|------------------------|----------|
| Revólver de ruleta | Disparar (mirando al suelo del todo: a tu propia sien) | Apuntar. La mira enseña la bala que toca, salvo en la ruleta rusa (tras girar el tambor, o con el cañón en la sien) | El clic izquierdo gira el tambor. El clic derecho carga la munición de la otra mano, encera (panal) o rasca (hacha), dispara en abanico (con Abanico) o reta a un jugador a un duelo |
| Rifle de catalejo | Disparar, o accionar el cerrojo si no hay bala lista | Apuntar por el catalejo (zoom y telémetro) | El clic izquierdo acciona el cerrojo a mano; apuntando, saca una foto |
| Escopeta de presión | Disparar, solo desde la cadera: no apunta | Bombear | Mantener clic derecho aspira objetos y tira de los mobs |
| Winchester 1873 | Disparar | Apuntar (la mira enseña la bala que va a salir) | Mantener clic derecho recarga bala a bala, o la desatasca |
| Derringer | Disparar | Apuntar | Mantener clic derecho recarga. La tecla de la manga (K) la saca de cualquier hueco del inventario |
| Thompson | Mantener: ráfaga | Apuntar (la mira se abre según dura la ráfaga) | Mantener clic derecho cambia el tambor |
| Mosquete con bayoneta | Disparar. Sin bola, encasquillado o agachado, es la estocada de la bayoneta | Apuntar | Mantener clic derecho recarga (pólvora, bola y baqueta) |
| Cañón de mano | Prender la mecha | Apuntar. La mira dibuja la parábola del bolaño | Mantener clic derecho recarga |
| Gatling de manivela (a los mandos) | Mantener: girar la manivela y disparar | Apuntar. La mira enseña el calor del cañón | El clic derecho la recoge |

Todas las armas de cobre: agachado + clic derecho con un panal o un hacha en la otra mano la encera o la rasca. Los
valores del apuntado (dispersión, campo de visión y lentitud) están en la config del servidor, sección
`armas_de_fuego_equilibrio.apuntado`. La N inspecciona el arma de la mano (se puede cambiar en Controles > Copper Slug).

## Descargas

Todavía no hay versiones publicadas: cada compilación del CI sale como prerelease `build-N`.

| Minecraft | Cargador | Jar |
|-----------|----------|-----|
| 1.20.1 | Forge 47.x (vale también para NeoForge 1.20.1 47.1) | `copperslug-forge-1.20.1-1.0.0.jar` |
| 1.20.1 | Fabric | `copperslug-fabric-1.20.1-1.0.0.jar` |
| 1.21.1 | NeoForge | `copperslug-neoforge-1.21.1-1.0.0.jar` |
| 1.21.1 | Forge | `copperslug-forge-1.21.1-1.0.0.jar` |
| 1.21.1 | Fabric | `copperslug-fabric-1.21.1-1.0.0.jar` |

## Requisitos

- **Forge / NeoForge:** nada más.
- **Fabric:** [Fabric API](https://modrinth.com/mod/fabric-api).
- Opcional: [JEI](https://modrinth.com/mod/jei), que enseña dónde se encuentra cada arma y la receta de la bayoneta.
- Los shaders (Embeddium/Oculus en Forge, Sodium/Iris en Fabric) funcionan.

Copper Slug es la parte de armas de fuego del mod Miscelánea como mod independiente. No está pensado para instalarlo a la
vez que Miscelánea.

All Rights Reserved · HCuadrado428

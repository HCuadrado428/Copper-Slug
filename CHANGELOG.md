# Changelog

**English** · [Castellano](#castellano)

## 1.0.0 (unreleased)

- First version of Copper Slug: the nine firearms of Miscelánea as a standalone mod. Roulette revolver, spyglass rifle
  with ziplines, pressure shotgun, Crank Gatling Gun, Winchester 1873, Derringer, Thompson in its violin case, bayonet
  musket and hand cannon.
- Every gun has its own ammo (special ammo included), its own enchantments, copper that rusts (wax it, or scrape it with
  an axe), a HUD, sounds, particles and 3D models.
- Guns are found in vanilla structure chests. They have 57 advancements in their own tab, the honey effect (Sticky) and a
  server balance config.
- JEI (optional): where each gun is found and the bayonet recipe.
- Copper rust is a trade-off: each phase jams and scatters more, but hits and pierces harder. Config list
  `armas_de_fuego_equilibrio.cobre`.
- Wax lasts 200 shots (1500 on the Gatling and the Thompson), with a counter in the tooltip.
- The bayonet uses the enchantments of its sword (Sharpness, Fire Aspect, Looting, Sweeping Edge, Mending). Sweeping Edge
  does not count as a bonus on the bayonet, because a bayonet is a thrust.
- The violin is played with a bow in the other hand: sustained note and staff on the HUD.
- New advancements: "Professional Polisher" (wax the same gun five times) and "Flambéed Bayonet" (finish something with a
  bayonet that has Fire Aspect). "Paganini of the West" changed.
- Controls like a shooter: left click shoots and holding right click aims (revolver, Winchester, Derringer, Thompson,
  musket, hand cannon and the Gatling at its controls; the rifle aims through its spyglass). Aiming centres the gun,
  narrows the field of view, tightens the spread and slows you down, and other players see the pose. The pressure shotgun
  does not aim: it fires from the hip only. Sneak + right click still reloads; on the musket, left click with no ball
  loaded, jammed or sneaking is the bayonet thrust. Values in `armas_de_fuego_equilibrio.apuntado`.
- Each sight shows something: the revolver shows the next round (never in Russian roulette), the Winchester the round about
  to leave, the Thompson its spread, the hand cannon the arc of the ball and the Gatling its barrel heat.
- More visual detail: bullets are seen flying, coloured by their ammo; impacts depend on the block (sparks on metal,
  splinters on wood, dust on earth, chips on stone, shards on glass); special ammo adds its own muzzle effect; the cannon
  ball and the rope bullet spin in flight; recoil is lighter while aiming.
- Balance: revolver 10 ticks between shots (every shot counts against the invulnerability window), rifle headshot x1.5,
  Thompson 1.6 per bullet, shotgun pellet 1.5.
- Minecraft 1.20.1: Forge (also NeoForge 1.20.1) and Fabric. Minecraft 1.21.1: NeoForge, Forge and Fabric.
- Fabric has no reach attribute for the musket bayonet (Forge and NeoForge do). On 1.21.1 Fabric does not apply the camera
  roll of the rifle recoil (the rest of the recoil is applied).

---

<a id="castellano"></a>

## Castellano

## 1.0.0 (sin publicar)

- Primera versión de Copper Slug: las nueve armas de fuego de Miscelánea como mod independiente. Son el revólver de
  ruleta, el rifle de catalejo con tirolinas, la escopeta de presión, la Gatling, la Winchester 1873, la Derringer, la
  Thompson con su estuche de violín, el mosquete con bayoneta y el cañón de mano.
- Cada arma lleva su munición (también la especial), sus encantamientos propios, el cobre que se oxida (se encera y se
  rasca con un hacha), el HUD, los sonidos, las partículas y los modelos 3D.
- Salen en cofres de estructuras vanilla, tienen 57 logros en su propia pestaña, el efecto de la miel (pringado) y config
  de equilibrio del servidor.
- JEI opcional: dónde se encuentra cada arma y la receta de la bayoneta.
- El óxido es un intercambio: cada fase se encasquilla y dispersa más, pero pega y perfora más (lista
  `armas_de_fuego_equilibrio.cobre` de la config).
- La cera se gasta: 200 disparos (1500 en la Gatling y la Thompson), con el contador en el tooltip.
- La bayoneta usa los encantamientos de su espada (Filo, Aspecto ígneo, Botín, Barrido, Reparación). El Barrido no
  cuenta como bonus en la bayoneta, porque es una estocada.
- El violín se toca con un arco en la otra mano: nota sostenida y pentagrama en el HUD.
- Logros nuevos: «Abrillantador profesional» (encerar cinco veces la misma arma) y «Bayoneta flambeada» (rematar con una
  bayoneta que tenga Aspecto ígneo). «Paganini del Oeste» cambia.
- Controles de juego de tiros: el clic izquierdo dispara y mantener el clic derecho apunta (revólver, Winchester,
  Derringer, Thompson, mosquete, cañón de mano y la Gatling a sus mandos; el rifle apunta por su catalejo). Apuntar lleva
  el arma al centro, cierra el campo de visión, dispersa menos y hace andar más lento, y los demás ven la pose. La
  escopeta de presión no apunta: dispara solo desde la cadera. Agachado + clic derecho sigue recargando; en el mosquete,
  el clic izquierdo sin bola, encasquillado o agachado es la estocada de la bayoneta. Valores en
  `armas_de_fuego_equilibrio.apuntado`.
- Cada mira enseña algo: la del revólver, la bala que toca (nunca en la ruleta rusa); la de la Winchester, la bala que
  va a salir; la de la Thompson, lo que dispersa; la del cañón de mano, la parábola del bolaño; la de la Gatling, el
  calor del cañón.
- Más detalle visual: las balas se ven pasar, del color de su munición; el impacto depende del bloque (chispas en el
  metal, astillas en la madera, polvo en la tierra, esquirlas en la piedra, añicos en el cristal); la munición especial
  añade su efecto en la boca; el bolaño y la bala de cuerda giran en vuelo; el retroceso es menor apuntando.
- Equilibrio: revólver a 10 ticks entre disparos (cuentan todos los tiros contra la ventana de invulnerabilidad),
  cabeza del rifle x1,5, Thompson 1,6 por bala y perdigón de la escopeta 1,5.
- Minecraft 1.20.1: Forge (y NeoForge 1.20.1) y Fabric. Minecraft 1.21.1: NeoForge, Forge y Fabric.
- Fabric no tiene el alcance de la bayoneta del mosquete (en Forge y NeoForge sí). En 1.21.1 Fabric no aplica el giro de
  cámara del retroceso del rifle (el resto del retroceso sí).

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
- New enchantment Steady Hand (level 2): while aiming, 20% less spread per level and less slowdown, for the guns you aim
  with the right click. Dead Eye (Winchester) also works aiming still for 1.5 s, not only on horseback.
- Inspect the gun in your hand with N (rebindable): it rises to the centre and turns slowly so you can look at the copper,
  the rust and the cylinder. A soft copper click when you put the sight up, a glint on the bayonet when you draw the
  musket, and verdigris dust when a rusted gun fires.
- Every gun's main metal parts are copper now, so they all rust with the gun (only small details such as pins and
  triggers stay iron). The Derringer has two stacked copper barrels, and the revolver is a proper Colt with the
  hammer, the sight notch and a loading window: seen from behind, the cartridge bases show in each chamber (it turns
  with the cylinder, and never gives away the next round in Russian roulette).
- The aiming HUD no longer sits over the gun: the revolver drum is hidden while aiming, and the ammo counters and the
  Gatling heat move to the side. The musket and Winchester stocks were lowered so they do not fill the sight picture.
- Fabric has no reach attribute for the musket bayonet (Forge and NeoForge do). On 1.21.1 Fabric does not apply the camera
  roll of the rifle recoil (the rest of the recoil is applied).
- Armed mobs: some pillagers carry a Winchester and really shoot (six rounds, then a reload; aim depends on the
  difficulty). Config section `mobs_armados`: master switch, chance per pillager and per captain, damage, rate of fire and
  drop chance. Off means vanilla.
  Each weapon shoots its own way (revolver: six quick shots; Winchester: slower and farther; Derringer: two shots, short range;
  Thompson: bursts of three; musket: one huge shot every few seconds) and each structure hands out its own: pillagers carry
  revolvers or Winchesters, the pyramid husks muskets and Derringers, the mine zombies revolvers and Winchesters.
  Armed mobs now behave: they take a moment to react and aim, cock the gun (you hear the trigger; the musket spits sparks) before
  every shot, miss much more (farther away, against a moving or crouching target, when wounded; the first shot is often a warning
  to the side; config `fallo`), sometimes misfire with a dry click, step sideways and back away when you get close, flinch when
  hit, and reload with step by step sounds and the crossbow-loading gesture (zombies lower their arms), also between fights.
- New sounds, all synthesised (no copyrighted audio) and each weapon with its own character: the revolver dry and punchy, the rifle a
  whip crack with a long valley echo, the pressure shotgun a puff with a thump, the Gatling a short metallic tick, the Winchester a
  big-calibre bang, the Derringer a small dry pop, the Thompson a rattle, the musket a black-powder roar with a spark first and the
  hand cannon thunder. Also new: a real suppressor sound (a short puff, no bang), a far-away version of every shot for players 45 to
  150 blocks away (muffled, with echo), a room echo when shooting indoors or underground, redone reloads, levers, drums, ramrod,
  belt, crank, ricochets and shell casings, and the sounds armed mobs make (cocking, pan spark, dry click).
- New structure, the Pharaoh's Pyramid (deserts): a cinematic stepped sandstone pyramid (61 x 61) with a pylon gate and
  obelisks, and two labyrinth floors inside: an 11 x 11 maze with loops, pressure-plate TNT traps, husks (some carrying
  Winchesters) and chests in the dead ends, with the sarcophagus hall in the middle; a hand ladder leads to a smaller 7 x 7
  maze and the pharaoh's treasure chamber with four chests (ammo and, sometimes, a Winchester or a Derringer).
- New structure, the Abandoned Copper Mine (hills, mountains and badlands, underground): a 15 x 15 labyrinth with 3-wide
  tunnels, rails and chest minecarts, timber props, powder stores full of TNT, cave-ins, zombie miners with Winchesters
  and, in a corner, the vein chamber of oxidised copper with the treasure. A wooden headframe marks the shaft.
- New structure, the Raiders' Camp (plains, savannas, taigas and forests): a log palisade with four watchtowers, a campfire, three
  tents, the captain's red tent with his chest, a cage with a (decorative) prisoner, a horse corral and supply crates. It is guarded
  by armed pillagers (revolver, Winchester and, the captain, a Thompson) and two vindicators at the gate.
- Copper parts that show on the weapon, and they ARE the enchantments: a weapon carrying Suppressor shows a suppressor on its
  barrel (and its shots are almost silent; now also for the Derringer, Winchester and Thompson, not only the rifle), Muzzle
  Compensator shows the Thompson's brake, Extended Magazine shows collars and a longer tube on the Winchester. New enchantments
  with their own part: Long Barrel (revolver), Choke (pressure shotgun), Copper Sight (musket) and Rifled Bore (hand cannon); each
  also tightens the spread. The parts rust with the weapon.

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
- Encantamiento nuevo, Pulso firme (nivel 2): apuntando, dispersa un 20 % menos por nivel y se anda menos lento, para las
  armas que apuntan con el clic derecho. Dead Eye (Winchester) también vale apuntando quieto 1,5 s, no solo a caballo.
- Inspecciona el arma de la mano con la N (se puede cambiar): sube al centro y se gira despacio para ver el cobre, el óxido
  y el tambor. Un clic suave de cobre al poner la mira, un destello en la bayoneta al sacar el mosquete y polvo de
  pátina verdosa cuando dispara un arma oxidada.
- El metal principal de todas las armas es de cobre, así que todas se oxidan con el arma (solo quedan en hierro los
  detalles pequeños, como pasadores y gatillos). La Derringer tiene dos cañones de cobre apilados, y el revólver es un
  Colt de verdad con martillo, mira de muesca y ventana de carga: visto desde atrás, se ve el culote de cada bala en su
  recámara (gira con el tambor y no delata la siguiente en la ruleta rusa).
- El HUD al apuntar ya no cae sobre el arma: el tambor del revólver se oculta y los contadores de balas y el calor de la
  Gatling se apartan a un lado. Las culatas del mosquete y de la Winchester son más bajas para que no llenen la mira.
- Fabric no tiene el alcance de la bayoneta del mosquete (en Forge y NeoForge sí). En 1.21.1 Fabric no aplica el giro de
  cámara del retroceso del rifle (el resto del retroceso sí).
- Mobs armados: algunos saqueadores llevan una Winchester y disparan de verdad (seis balas y luego recargan; la puntería
  depende de la dificultad). Sección `mobs_armados` de la config: interruptor, probabilidad por saqueador y por capitán,
  daño, cadencia y probabilidad de soltar el arma. Apagado, todo es vanilla.
  Cada arma dispara a su manera (revólver: seis tiros rápidos; Winchester: más despacio y más lejos; Derringer: dos tiros de
  cerca; Thompson: ráfagas de tres; mosquete: un tiro enorme cada pocos segundos) y cada estructura reparte las suyas: los
  saqueadores llevan revólveres o Winchesters, los husks de la pirámide mosquetes y Derringers, los zombis de la mina revólveres
  y Winchesters.
  Los mobs armados ahora se comportan: tardan en reaccionar y apuntar, montan el arma antes de cada disparo (se oye el gatillo; el
  mosquete echa chispas), fallan mucho más (de lejos, contra un blanco que se mueve o va agachado, si están heridos; el primer tiro
  suele ser de aviso a un lado; config `fallo`), a veces se encasquillan con un clic en seco, se mueven de lado y retroceden si te
  acercas, se sobresaltan si les das y recargan con sonidos paso a paso y el gesto de cargar la ballesta (los zombis bajan los
  brazos), también entre combates.
- Sonidos nuevos, todos sintetizados (sin audio con copyright) y con el carácter de cada arma: el revólver seco y con pegada, el
  rifle un latigazo con eco largo de valle, la escopeta de presión un soplido con golpe, la Gatling un «tuc» metálico corto, la
  Winchester un estampido de calibre grande, la Derringer un pum pequeño y seco, la Thompson un traqueteo, el mosquete un estruendo
  de pólvora negra con chispazo antes y el cañón de mano un trueno. También nuevos: un silenciador de verdad (un soplido corto, sin
  estampido), una versión lejana de cada disparo para los jugadores a 45-150 bloques (apagada y con eco), un eco de sala al disparar
  en interiores o bajo tierra, recargas, palancas, tambores, baqueta, cinta, manivela, rebotes y casquillos rehechos, y los sonidos de
  los mobs armados (montar el arma, chispa de la cazoleta, clic en seco).
- Estructura nueva, la Pirámide del faraón (desiertos): una pirámide escalonada de arenisca de película (61 x 61) con
  pilono de entrada y obeliscos, y dos plantas laberínticas por dentro: un laberinto de 11 x 11 con bucles, trampas de TNT
  con placa de presión, husks (algunos con Winchester) y cofres en los callejones, con la sala del sarcófago en el centro;
  una escalera de mano sube a otro laberinto más pequeño (7 x 7) y a la cámara del tesoro del faraón, con cuatro cofres
  (munición y, a veces, una Winchester o una Derringer).
- Estructura nueva, la Mina de cobre abandonada (colinas, montañas y mesetas, bajo tierra): un laberinto de 15 x 15 con
  túneles de 3 de ancho, vías y vagonetas con cofre, puntales, polvorines con TNT, derrumbes, mineros zombis con Winchester
  y, en una esquina, la cámara del filón de cobre oxidado con el tesoro. Un cabrestante de madera marca el pozo.
- Estructura nueva, el Campamento de saqueadores (llanuras, sabanas, taigas y bosques): una empalizada de troncos con cuatro torres de
  vigilancia, una hoguera, tres tiendas, la tienda roja del capitán con su cofre, una jaula con un prisionero (de adorno), un corral con
  caballos y cajas de suministros. Lo guardan saqueadores armados (revólver, Winchester y, el capitán, una Thompson) y dos vindicadores en
  la puerta.
- Piezas de cobre que se ven en el arma, y SON los encantamientos: el arma con Silenciador lleva un silenciador en el cañón
  (y sus disparos casi no suenan; ahora también en la Derringer, la Winchester y la Thompson, no solo el rifle), el Compensador
  enseña el freno de la Thompson, el Depósito largo enseña unos collares y un tubo más largo en la Winchester. Encantamientos
  nuevos con su pieza: Cañón largo (revólver), Estrangulador (escopeta de presión), Mira de cobre (mosquete) y Ánima rayada
  (cañón de mano); cada uno cierra también la dispersión. Las piezas se oxidan con el arma.

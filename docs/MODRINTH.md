# Copper Slug: Modrinth page text

Text for the Modrinth project page (1.0.0). Summary first, then the long description in English and in Castellano,
and the list of advancements as they are in the code. Screenshots to upload are listed at the end of each description.

## Summary (English, 250 characters max)

Nine copper firearms with their own ammo, enchantments and rust, plus three new structures guarded by armed mobs: a labyrinth pyramid, a copper mine and a raiders' camp. Copper rusts: wax it or scrape it. Forge, Fabric, NeoForge.

## Resumen (castellano, 250 caracteres máximo)

Nueve armas de fuego de cobre con munición, encantamientos y óxido propios, y tres estructuras nuevas con mobs armados: pirámide laberíntica, mina de cobre y campamento de saqueadores. El cobre se oxida. Forge, Fabric, NeoForge.

## Description (English)

**Nine copper firearms. Rust that matters. Mobs that shoot back.**

Copper Slug brings the Wild West and some older things (a hand cannon, a bayonet musket) to Minecraft. Every gun is made
of copper, so every gun rusts, and every gun has its own ammo, enchantments, sounds, HUD and 3D model.

### The guns

- **Roulette revolver**: Russian roulette, quick draw, duels against other players, and special bullets (blank, magnet,
  sedative dart, flare).
- **Spyglass rifle**: scope, breath control for more damage, headshots, ziplines with rope bullets, paint and tracers.
- **Pressure shotgun**: pump it up, suck in items, pull mobs, and fire cartridges with effects (gravel, incendiary, frost,
  honey, salt, seeds, confetti, rubber). Pump it too far and it bursts.
- **Crank Gatling Gun**: automatic and stationary. It overheats if you keep cranking. Belts of peas or popcorn, and it can
  work as a redstone turret, on a boat or on a minecart.
- **Winchester 1873**: lever action with a tube magazine. Ice, silver and mixed ammo. Spin the lever from horseback.
- **Derringer**: hidden up your sleeve. Quick-draw trick, smoke, marked cards and gold bullets.
- **Thompson**: drum-fed submachine gun inside a violin case. Water, ink and tracer drums. Play the case with a bow.
- **Bayonet musket**: bolas, harpoon bolas and chain bolas. Fit a sword as a bayonet and it keeps the sword's enchantments.
- **Hand cannon**: explosive bolas, incendiary, firework and bouncing ones, falling blocks and anvils.

### Copper rusts

Rust is a trade-off, not a countdown. Each phase jams more and scatters more, but hits and pierces harder. Wax a gun with
honeycomb to freeze it (200 shots, 1500 on the Gatling and the Thompson) or scrape it with an axe to take a phase off.
You can see the rust on the model, including on the extra parts.

### Controls

Left click shoots and holding right click aims, as in most shooters. Aiming centres the gun, narrows the field of view,
tightens the spread and slows you down. Sneak + right click reloads. The pressure shotgun is the exception: right click
pumps it and it fires from the hip only. At the Gatling controls, hold left click to crank and right click to aim. Each
sight shows something useful: the revolver's next round (never in Russian roulette), the hand cannon's arc, the Gatling's
barrel heat. Press N to inspect the gun in your hand.

### Enchantments that show on the gun

Enchant a gun and the part appears on it, rusting along with the barrel. A Suppressor puts a suppressor on the muzzle (and
the shots become almost silent, so sculk and the Warden do not notice). Long Barrel lengthens the revolver, Choke fits
the pressure shotgun, Copper Sight adds a front sight to the musket, Rifled Bore rifles the hand cannon, the Winchester's
Long Tube adds collars and a longer tube, and the Thompson's Compensator shows its brake. Each also
changes how the gun shoots. There are many more without a part: Fanning, Ricochet, Quick Draw, Held Breath, Pierce
Through, Hawkeye, Zipliner, Steady Hand, Dead Eye, Cooling, Long Belt, Compressor, Safety Valve and others.

### Three new structures

- **Pharaoh's Pyramid** (deserts): a stepped sandstone pyramid with a pylon gate and obelisks. Inside there are two
  labyrinth floors: an 11 x 11 maze with pressure-plate TNT traps and husks (some with Winchesters or Derringers), and a
  smaller 7 x 7 maze reached by a hand ladder, ending in the pharaoh's treasure chamber with four chests.
- **Abandoned Copper Mine** (hills, mountains and badlands, underground): a 15 x 15 labyrinth of wide tunnels with rails,
  chest minecarts, timber props, powder stores full of TNT, cave-ins and zombie miners with revolvers and Winchesters. In
  a corner, the oxidised copper vein chamber holds the treasure. A wooden headframe marks the shaft from the surface.
- **Raiders' Camp** (plains, savannas, taigas and forests): a log palisade with four watchtowers, a campfire, three
  tents, the captain's red tent with his chest, a horse corral, supply crates and a caged prisoner (decoration). Pillagers
  with revolvers and Winchesters guard it, the captain carries a Thompson, and two vindicators stand at the gate.

All three are small enough to find by accident and big enough to get lost in. Guns are also found in vanilla structure
chests (villages, shipwrecks, pillager outposts and more). Most ammo, the violin case and the bayonet fitting can be
crafted.

### Mobs that shoot back

Some pillagers carry a real gun and use it: they take a moment to react, cock the gun before every shot, miss a lot
(more at long range and against moving or crouching targets; the first shot is often a warning), sometimes misfire, step
sideways and back off when you get close, flinch when hit, and reload with the crossbow gesture. Each gun has its own
rhythm (revolver in quick shots, Winchester slower and from farther, Derringer short range, Thompson in bursts of three,
musket one huge shot) and each structure hands out its own. They are rare by default and can be turned off, so vanilla is
one setting away.

### Sound

Every sound is synthesised (no copyrighted audio) and each gun has its own character: a rifle crack with a long valley
echo, a pressure shotgun puff, a Gatling tick, a black-powder musket roar. Shots heard from 45 to 150 blocks arrive muffled
with an echo, shooting indoors adds room echo, and a suppressed shot is just a short puff.

### Settings and compatibility

Server settings live in `serverconfig/copperslug-server.toml` (damage, fire rate, range, rust, wax, loot chances, armed
mobs). Every value can be changed and every feature switched off.

**Minecraft 1.20.1** (Forge, Fabric; it also runs on NeoForge 1.20.1) and **1.21.1** (NeoForge, Forge, Fabric). Fabric
needs Fabric API. JEI is optional and shows where each gun is found. Every gun has its own advancement tab (57
advancements, listed below).

This is the firearms part of Miscelánea as a standalone mod. Do not install both together.

Images to upload: the roulette revolver in hand, a rusted Winchester with its parts, the pyramid from outside, the mine
from the inside, the raiders' camp, and a pillager aiming at you.

## Descripción (castellano)

**Nueve armas de cobre. Un óxido que importa. Mobs que disparan.**

Copper Slug lleva el Oeste a Minecraft, y algo más antiguo (un cañón de mano, un mosquete con bayoneta). Todas las armas
son de cobre, así que todas se oxidan, y cada una tiene su munición, sus encantamientos, sus sonidos, su HUD y su modelo 3D.

### Las armas

- **Revólver de ruleta**: ruleta rusa, desenfunde, duelos contra otros jugadores y balas especiales (fogueo, imán, dardo
  de sedante, bengala).
- **Rifle de catalejo**: mira, contener la respiración para más daño, headshots, tirolinas con bala de cuerda, pintura y
  balas trazadoras.
- **Escopeta de presión**: se bombea, aspira objetos, tira de los mobs, y dispara cartuchos con efecto (grava,
  incendiario, escarcha, miel, sal, semillas, confeti, goma). Si la bombeas de más, revienta.
- **Gatling de manivela**: automática y fija. Se calienta si no paras de girar la manivela. Cintas de guisantes o
  palomitas, y puede ser una torreta con redstone, en un barco o en una vagoneta.
- **Winchester 1873**: palanca de repetición con depósito tubular. Balas de hielo, de plata y mezclas. Gira la palanca a
  caballo.
- **Derringer**: escondida en la manga. Truco de tahúr al sacarla, balas de humo, cartas marcadas y balas de oro.
- **Thompson**: subfusil de tambor dentro de un estuche de violín. Tambores de agua, de tinta y trazadores. Toca el estuche
  con un arco.
- **Mosquete con bayoneta**: bolas, bolas arpón y bolas encadenadas. Cala una espada como bayoneta y conserva sus
  encantamientos.
- **Cañón de mano**: bolaños que estallan, incendiarios, de fuegos artificiales y saltarines, y bloques que caen o yunques
  disparados.

### El cobre se oxida

El óxido es un intercambio, no una cuenta atrás. Cada fase encasquilla y dispersa más, pero pega y perfora más fuerte. Se
encera con panal para congelarlo (200 disparos, 1500 en la Gatling y la Thompson) o se rasca con un hacha para quitar una
fase. El óxido se ve en el modelo, también en las piezas añadidas.

### Controles

El clic izquierdo dispara y mantener el clic derecho apunta, como en casi todos los juegos de tiros. Apuntar lleva el arma
al centro, cierra el campo de visión, dispersa menos y hace andar más lento. Agachado + clic derecho recarga. La escopeta
de presión es la excepción: el clic derecho la bombea y dispara solo desde la cadera. A los mandos de la Gatling, mantener
el clic izquierdo gira la manivela y el derecho apunta. Cada mira enseña algo útil: la del revólver, la bala que toca
(nunca en la ruleta rusa); la del cañón de mano, la parábola; la de la Gatling, el calor del cañón. La N inspecciona el
arma de la mano.

### Encantamientos que se ven en el arma

Encanta un arma y la pieza aparece en ella, y se oxida junto al cañón. Silenciador pone un silenciador en la boca (y los
disparos casi no suenan, así que el sculk y el Warden no se enteran). Cañón largo alarga el revólver, Estrangulador se
monta en la escopeta de presión, Mira de cobre añade un punto de mira al mosquete, Ánima rayada raya el cañón de mano,
el Depósito largo de la Winchester le pone abrazaderas y un tubo más largo, y el Compensador de la Thompson enseña su
freno. Cada uno cambia también cómo dispara el arma. Hay muchos más sin pieza: Abanico, Carambola, Desenfunde,
Respiración contenida, Atravesar, Ojo de halcón, Tirolinero, Pulso firme, Dead Eye, Refrigeración, Cinta larga,
Compresor, Válvula de seguridad y otros.

### Tres estructuras nuevas

- **Pirámide del faraón** (desiertos): una pirámide escalonada de arenisca con un pilono de entrada y obeliscos. Por
  dentro tiene dos pisos laberínticos: un laberinto de 11 x 11 con trampas de TNT de placa de presión y husks (algunos con
  Winchester o Derringer), y otro más pequeño de 7 x 7 al que se sube por una escalera de mano y que acaba en la cámara del
  tesoro del faraón, con cuatro cofres.
- **Mina de cobre abandonada** (colinas, montañas y mesetas, bajo tierra): un laberinto de 15 x 15 de túneles anchos con
  raíles, vagonetas con cofre, puntales de madera, polvorines llenos de TNT, derrumbes y zombis mineros con revólver y
  Winchester. En una esquina, la cámara de la veta de cobre oxidado guarda el tesoro. Un castillete de madera marca el pozo
  desde la superficie.
- **Campamento de saqueadores** (llanuras, sabanas, taigas y bosques): una empalizada de troncos con cuatro torres de
  vigilancia, una hoguera, tres tiendas, la tienda roja del capitán con su cofre, un corral de caballos, cajas de
  suministros y un prisionero enjaulado (decoración). Lo guardan saqueadores con revólver y Winchester, el capitán lleva
  una Thompson y dos vindicadores vigilan la puerta.

Las tres son lo bastante pequeñas para encontrarlas por casualidad y lo bastante grandes para perderse. Las armas también
se encuentran en los cofres de estructuras vanilla (aldeas, barcos hundidos, puestos de saqueadores y más). La mayor parte
de la munición, el estuche de violín y la forma de calar la bayoneta se fabrican.

### Mobs que disparan

Algunos saqueadores llevan un arma de verdad y la usan: tardan un momento en reaccionar, amartillan antes de cada tiro,
fallan mucho (más de lejos y contra objetivos que se mueven o van agachados; el primer tiro suele ser de aviso), a veces
se les encasquilla, se desplazan de lado y retroceden si te acercas, se estremecen al recibir un golpe y recargan con el
gesto de la ballesta. Cada arma tiene su ritmo (el revólver, tiros rápidos; la Winchester, más lenta y de más lejos; la
Derringer, corto alcance; la Thompson, ráfagas de tres; el mosquete, un tiro enorme) y cada estructura reparte las suyas.
Son raros por defecto y se pueden desactivar, así que lo vanilla queda a un ajuste de distancia.

### Sonido

Todos los sonidos están sintetizados (sin audio con derechos) y cada arma tiene su carácter: el chasquido del rifle con un
largo eco de valle, el soplido de la escopeta de presión, el tic de la Gatling, el rugido de pólvora negra del mosquete.
Los disparos que se oyen de 45 a 150 bloques llegan amortiguados y con eco, disparar en interior añade eco de sala, y un
disparo silenciado es solo un soplido corto.

### Ajustes y compatibilidad

La configuración del servidor está en `serverconfig/copperslug-server.toml` (daño, cadencia, alcance, óxido, cera,
probabilidad en cofres, mobs armados). Todos los valores se pueden cambiar y todo se puede desactivar.

**Minecraft 1.20.1** (Forge, Fabric; también funciona en NeoForge 1.20.1) y **1.21.1** (NeoForge, Forge, Fabric). Fabric
necesita Fabric API. JEI es opcional y enseña dónde se encuentra cada arma. Cada arma tiene su propia pestaña de logros
(57 logros, abajo).

Es la parte de armas de fuego de Miscelánea como mod independiente. No instales los dos a la vez.

Imágenes para subir: el revólver de ruleta en la mano, una Winchester oxidada con sus piezas, la pirámide desde fuera, la
mina por dentro, el campamento de saqueadores y un saqueador apuntándote.

## Advancements / Logros

Same as in the code. The title and the description come from the language files (English and Castellano).

| Logro (ES) | Achievement (EN) | Cómo se consigue (ES) | How to get it (EN) |
|---|---|---|---|
| Arponero | Harpooner | Tira de algo (o de ti mismo) con la bola arpón del mosquete. Sea of Thieves otra vez. | Pull something (or yourself) with the musket's harpoon shot. Sea of Thieves again. |
| Roomba | Roomba | Recoge cosas del suelo aspirándolas con la escopeta de presión (agachado + clic derecho). | Pick things up off the floor by sucking them in with the pressure shotgun (sneak + right-click). |
| Uno natural | Natural One | Que se te encasquille un arma nueva. Hasta las mejores fallan una de cada cien. | Have a brand-new gun jam on you. Even the best ones fail one time in a hundred. |
| ¡A la bayoneta! | Fix Bayonets! | Acaba con algo a golpe de bayoneta. Para eso no hace falta recargar. | Finish something off with the bayonet. No reloading needed for that. |
| Bayoneta flambeada | Flambéed Bayonet | Remata a algo con una bayoneta calada que tenga Aspecto ígneo. Al punto. | Finish something off with a fixed bayonet that has Fire Aspect. Medium rare. |
| Bayoneta de gala | Parade Bayonet | Cala una espada de netherita en el mosquete. Para los desfiles. | Fix a netherite sword to the musket. For the parades. |
| Sea of Thieves | Sea of Thieves | Barre a dos o más de un solo tiro con la bola encadenada. | Sweep two or more at once with a single chain shot. |
| Tecnología punta (del siglo XIV) | Cutting-Edge Tech (of the 14th Century) | Dispara el cañón de mano. Prende la mecha y no lo sueltes. | Fire the hand cannon. Light the fuse and hold on. |
| Era de esperar | Saw That Coming | Que te reviente el cañón de mano en las manos. Por algo dejaron de usarse. | Have the hand cannon burst in your hands. There's a reason they went out of fashion. |
| Destino retorcido | Twisted Fate | Marca a alguien con una carta de la Derringer. Ahora brilla para todos. | Mark someone with a Derringer card. Now everyone can see them glow. |
| Castillo de arena | Sandcastle | Dispara un bloque que cae con el cañón de mano y que se quede donde da. | Fire a falling block from the hand cannon and have it land where it hits. |
| Abrillantador profesional | Professional Polisher | Encera cinco veces la misma arma. Brilla tanto que te ves la cara en el cañón. | Wax the same gun five times. It shines so much you can see your face in the barrel. |
| Indiana Jones | Indiana Jones | Encuentra un arma de fuego en un cofre: el revólver en las aldeas, la escopeta en los barcos hundidos, el rifle en los puestos de saqueadores... y seis más por ahí. | Find a firearm in a chest: the revolver in villages, the shotgun in shipwrecks, the rifle in pillager outposts... and six more out there. |
| El bueno, el feo y el coleccionista | The Good, the Ugly and the Collector | Consigue las nueve armas de fuego. Cada una sale en una estructura distinta. | Get all nine firearms. Each one is found in a different structure. |
| Spider-Man de barrio | Friendly Neighborhood Spider-Man | Tiende una tirolina con la bala de cuerda del rifle o cuélgate de una. | Rig a zipline with the rifle's rope bullet, or hang from one. |
| Un as en la manga | Ace Up the Sleeve | Acierta con la Derringer justo al sacarla. Nadie la vio venir. | Hit something with the Derringer right after drawing it. Nobody saw it coming. |
| ¡Tachán! | Ta-da! | Desaparece en una nube de humo con la bala de humo de la Derringer. Un mago nunca revela sus trucos. | Vanish in a cloud of smoke with the Derringer's smoke round. A magician never reveals their secrets. |
| Juego de manos | Sleight of Hand | Saca la Derringer de la manga y acierta en menos de un segundo. Nadie la ha visto venir. | Draw the Derringer from your sleeve and land a hit within a second. Nobody saw it coming. |
| Esta ciudad es pequeña para los dos | This Town Ain't Big Enough for the Two of Us | Gana un duelo con el revólver: reta a alguien (agachado + clic derecho) y desenfunda más rápido. | Win a revolver duel: challenge someone (sneak + right-click) and draw faster. |
| El óxido no perdona | Rust Never Sleeps | Que se te encasquille un revólver oxidado. Haberlo encerado. | Have a rusty revolver jam on you. Should have waxed it. |
| ¡Viva la feria! | Fun Fair! | Dispara un bolaño de feria con el cañón de mano. Más fuegos que daño. | Fire a fairground cannonball from the hand cannon. More fireworks than damage. |
| Francotirador de Call of Duty | Call of Duty Sniper | Acierta a una criatura con el rifle de catalejo a más de 100 bloques. | Hit a creature with the spyglass rifle from more than 100 blocks away. |
| ¡Gallina! | Chicken! | Rechaza un duelo. Cocococó. | Turn down a duel. Bawk bawk. |
| Brrrrrt | Brrrrrt | Suelta 40 balas seguidas con la Gatling sin soltar la manivela. | Fire 40 rounds in a row with the Gatling without letting go of the crank. |
| Bandera negra | Black Flag | Dispara la Gatling montada en un barco. El Jackdaw estaría orgulloso. | Fire the Gatling mounted on a boat. The Jackdaw would be proud. |
| Al rojo vivo | Red-Hot | Calienta la Gatling hasta que se atasque. El humo ya te avisaba. | Overheat the Gatling until it jams. The smoke was warning you. |
| Refrigeración líquida | Liquid Cooling | Enfría una Gatling caliente con un cubo de agua. Sin luces RGB, eso sí. | Cool down a hot Gatling with a water bucket. No RGB lights, though. |
| Cadena de montaje | Assembly Line | Que una tolva le meta una cinta a la Gatling. Ya no hace falta ni cargarla. | Have a hopper feed a belt into the Gatling. No need to even load it any more. |
| ¿Sigues ahí? | Are You Still There? | Que la Gatling, con redstone y sin nadie a los mandos, le dé a algo hostil. Te ha encontrado. | Have the Gatling, powered by redstone with nobody at the controls, hit something hostile. Target acquired. |
| El templo maldito | Temple of Doom | Dispara la Gatling montada en una vagoneta. La persecución de la mina, pero tú llevas la ametralladora. | Fire the Gatling mounted on a minecart. The mine chase, but you've got the machine gun. |
| Pong | Pong | Acierta a una criatura con una bola de goma que haya rebotado en una pared. | Hit a creature with a rubber ball that bounced off a wall. |
| Agricultor de gatillo fácil | Trigger-Happy Farmer | Siembra la tierra de cultivo a tiros con el cartucho de semillas. | Sow farmland by shooting it with a seed shell. |
| Plantas contra zombis | Plants vs. Zombies | Acaba con un zombi con la cinta de guisantes de la Gatling. La Lanzaguisantes Gatling, en el Oeste. | Finish off a zombie with the Gatling's pea belt. The Gatling Pea, out West. |
| ¡Preparen, apunten...! | Ready, Aim...! | Dispara el mosquete. Primero la chispa, luego el estampido y luego la nube. | Fire the musket. First the flash, then the bang, then the cloud. |
| La pistola de oro | The Golden Gun | Remata a algo con una bala de oro de la Derringer. 007 estaría celoso. | Finish something off with a golden Derringer bullet. 007 would be jealous. |
| Paganini del Oeste | Paganini of the West | Toca con el arco ocho notas distintas seguidas en el estuche de violín vacío (sin la Thompson, que desafina). | Bow eight different notes in a row on the empty violin case (without the Thompson, it's out of tune). |
| Palomitas para el espectáculo | Popcorn for the Show | Dispara palomitas con la Gatling. Nadie sale herido, todos salen merendados. | Fire popcorn from the Gatling. Nobody gets hurt, everybody gets a snack. |
| Pátina de museo | Museum Patina | Ten una de las armas nuevas oxidada del todo. Los del museo te la querrán comprar. | Own one of the new guns fully oxidized. The museum will want to buy it off you. |
| Pequeños accidentes felices | Happy Little Accidents | Pinta la pared de un tiro con la bala de pintura del rifle, o tiñe una oveja. | Paint a wall with one shot of the rifle's paint bullet, or dye a sheep. |
| Van Helsing | Van Helsing | Acaba con un no muerto con una bala de plata de la Winchester. | Finish off an undead with a silver bullet from the Winchester. |
| Mantén la pólvora seca | Keep Your Powder Dry | Intenta disparar con la pólvora mojada. Ya te lo decían. | Try to fire with wet powder. They did tell you. |
| Pájaros enfadados | Angry Birds | Haz que un bolaño saltarín rebote tres veces. Los cerdos verdes tiemblan. | Make a bouncy cannonball bounce three times. The green pigs tremble. |
| Te ha explotado en la cara | It Blew Up in Your Face | Bombea la escopeta de presión hasta que reviente. | Pump the pressure shotgun until it bursts. |
| Ruleta rusa (y sigues aquí) | Russian Roulette (and Still Here) | Apúntate a la sien con el revólver y que salga «clic». | Put the revolver to your head and hear it go "click". |
| ¡PUM!… era broma | BANG!… Just Kidding | Juega a la ruleta rusa con una bala de fogueo en el tambor. | Play Russian roulette with a blank in the cylinder. |
| Rocket jump | Rocket Jump | Sal volando con el soplido de la escopeta de presión: con mucha presión y sin cartuchos, dispara al suelo. | Launch yourself with the pressure shotgun's blast of air: lots of pressure, no shells, shoot the ground. |
| Buenas noches | Good Night | Seda a una criatura con el dardo de sedante del revólver. | Sedate a creature with the revolver's tranquilizer dart. |
| Super Soaker | Super Soaker | Apaga a alguien que arde (o moja a un enderman) con el tambor de agua de la Thompson. | Put out someone on fire (or soak an enderman) with the Thompson's water drum. |
| Mafia: edición definitiva | Mafia: Definitive Edition | Vacía un tambor entero de la Thompson en una sola ráfaga. | Empty a whole Thompson drum in a single burst. |
| Max Payne | Max Payne | Alcanza a alguien con una bala de tiempo bala. Todo va más lento... menos tu ego. | Hit someone with a bullet time round. Everything slows down... except your ego. |
| Splatoon | Splatoon | Ciega a alguien con el tambor de tinta de la Thompson. ¡Eres un calamar, ahora eres un niño! | Blind someone with the Thompson's ink drum. You're a kid, now you're a squid! |
| Concierto en Chicago | Concert in Chicago | Abre un estuche de violín. Lo que hay dentro no es un violín (y lo que suena, tampoco). | Open a violin case. What's inside isn't a violin (and neither is that sound). |
| El arma que conquistó el Oeste | The Gun That Won the West | Dispara la Winchester 1873. Palanca, tiro, palanca, tiro... | Fire the Winchester 1873. Lever, shot, lever, shot... |
| Hasta la vista, vaquero | Hasta la Vista, Cowboy | Dispara la Winchester a caballo, girando la palanca con una sola mano. | Fire the Winchester on horseback, spinning the lever with one hand. |
| Sub-Zero | Sub-Zero | Congela a alguien con una bala de hielo de la Winchester. ¡Gana! | Freeze someone with an ice round from the Winchester. Wins! |
| Ensalada de plomo | Lead Salad | Mete cuatro tipos de bala distintos en el depósito de la Winchester. Cada tiro, una sorpresa. | Load four different kinds of round into the Winchester's tube. Every shot's a surprise. |
| ¡Bip, bip! | Meep Meep! | Dale a algo con un yunque disparado con el cañón de mano. El Coyote lleva años intentándolo. | Hit something with an anvil fired from the hand cannon. Wile E. Coyote has been trying for years. |

#!/usr/bin/env bash
# Compila Bloomberto desde el commit de bloomberto.properties y deja sus jars en libs/bloomberto/:
#   bloomberto-<versión>+<mc>-<cargador>.jar      el jar de verdad (va en mods/ al jugar)
#   bloomberto-<versión>+<mc>-<cargador>-dev.jar  el mismo con nombres de Mojang (solo para compilar Copper Slug)
# Necesita JDK 21 y red para los Maven de Bloomberto. Si libs/bloomberto ya tiene los jars de ese commit, no hace nada.
set -euo pipefail
cd "$(dirname "$0")/.."
prop() { grep -E "^$1=" bloomberto.properties | cut -d= -f2-; }
COMMIT=$(prop commit)
OBJETIVOS=$(prop objetivos)
DEST=libs/bloomberto
if [ -f "$DEST/commit" ] && [ "$(cat "$DEST/commit")" = "$COMMIT" ]; then
  echo "Bloomberto $COMMIT ya está en $DEST"; ls "$DEST"; exit 0
fi
TMP=$(mktemp -d)
git init -q "$TMP/bloomberto"
git -C "$TMP/bloomberto" fetch -q --depth 1 https://github.com/HCuadrado428/Bloomberto "$COMMIT"
git -C "$TMP/bloomberto" checkout -q FETCH_HEAD
TAREAS=""
for o in $OBJETIVOS; do TAREAS="$TAREAS :$o:build"; done
( cd "$TMP/bloomberto" && chmod +x gradlew && ./gradlew $TAREAS -x test --no-daemon )
rm -rf "$DEST"; mkdir -p "$DEST"
for o in $OBJETIVOS; do
  d="$TMP/bloomberto/versions/$o/build"
  echo "== $o"; ls "$d/libs" "$d/devlibs" 2>/dev/null || true
  for j in "$d"/libs/*.jar; do case "$j" in *-sources.jar|*-dev*.jar|*-testmod*) ;; *) cp "$j" "$DEST/" ;; esac; done
  dev=$(ls "$d"/devlibs/*-dev.jar 2>/dev/null | grep -v -e sources -e testmod | head -1 || true)
  [ -n "$dev" ] || { echo "No encuentro el jar -dev de $o (con nombres de Mojang)"; exit 1; }
  base=$(ls "$DEST" | grep -e "$o.jar$" | head -1)
  cp "$dev" "$DEST/${base%.jar}-dev.jar"
done
echo "$COMMIT" > "$DEST/commit"
rm -rf "$TMP"
ls -la "$DEST"

#!/bin/bash
# pi-app-store: 1
# pi-app-store-category: games
# pi-app-store-description: Original kart-style time trial with coins, rival traffic and boosts. Not Mario Kart, no multiplayer or branded assets.
set -eu
cd -- "$(dirname -- "$0")"
case "${1:-}" in
 install) python3 -c 'from pathlib import Path;[compile(p.read_bytes(),str(p),"exec") for p in Path(".").glob("*.py")]' ;;
 run) shift; exec python3 game.py "$@" ;;
 *) echo 'Use: bash app-store.sh install OR bash app-store.sh run';exit 1 ;;
esac

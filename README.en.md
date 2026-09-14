# korea-transit-planner

A Korean-first agent skill for comparing door-to-door transit routes in Korea on one time basis.

It covers ordinary subway, city/intercity bus, village bus, Nuri Bus/DRT, walking, taxi, and mixed routes. It requires a user-supplied origin, preserves user-named stations as hard constraints, and separates official schedule/fare facts from map-planner candidates and estimates.

GTX is strictly opt-in: research or compare it only when the user explicitly says `GTX` or names a GTX station.

## Install with Hermes Agent

```bash
hermes skills inspect bohe76/korea-transit-planner-skill
hermes skills install bohe76/korea-transit-planner-skill
```

Or install the direct `SKILL.md` URL:

```bash
hermes skills install https://raw.githubusercontent.com/bohe76/korea-transit-planner-skill/main/SKILL.md
```

See the [Korean README](README.md) for features, examples, verification, privacy, and contribution guidance. This repository is a procedure skill, not a routing engine or bundled transit dataset. Compatibility with non-Hermes runtimes should be verified against their Agent Skills and local-reference support.

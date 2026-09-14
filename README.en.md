# korea-transit-planner

[![CI](https://github.com/bohe76/korea-transit-planner-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/bohe76/korea-transit-planner-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-111111.svg)](LICENSE)

<img src="docs/assets/korea-transit-planner-hero.svg" alt="korea-transit-planner: explicit origin, same-time comparison, verified sources" width="100%" />

A Korean-first agent skill for comparing door-to-door transit routes in Korea on one time basis.

`korea-transit-planner` is a reusable research procedure for ordinary subway, city/intercity bus, village bus, Nuri Bus/DRT, walking, taxi, and mixed routes. It uses map services for route candidates, then distinguishes them from official schedule and fare evidence.

> **Procedure skill, not a routing engine.** It contains no API keys, private addresses, personal calendar data, transit dataset, or map tiles.

[Korean README](README.md) · [Install](#install-with-hermes-agent) · [Example request](#example-request) · [Verification and privacy](#verification-and-privacy) · [Contributing](CONTRIBUTING.md)

## Guarantees and boundaries

- The origin must be supplied by the user; no saved home address or personal default is inferred.
- User-named boarding and alighting stations are hard constraints.
- Candidate routes are compared door-to-door against the same departure or arrival time basis.
- Volatile facts carry a check time and time zone; estimates are labeled as estimates.
- **GTX is strictly opt-in:** it is researched or compared only when the user explicitly says `GTX` or names a GTX station.

## Install, invoke, and update

This repository uses a `SKILL.md` plus local references under the [Agent Skills specification](https://agentskills.io/specification). **Install the entire `korea-transit-planner/` directory.** Saving only the raw `SKILL.md` with `curl` or `wget` omits `references/` and `examples/` and is not a complete installation.

### Hermes Agent

```bash
hermes skills inspect bohe76/korea-transit-planner-skill/korea-transit-planner
hermes skills install bohe76/korea-transit-planner-skill/korea-transit-planner
hermes -s korea-transit-planner
hermes skills check
hermes skills update
```

Hermes v0.21.2 was verified to preserve linked local references for both its GitHub identifier and URL installer. A generic raw-file download is not supported. [Hermes Skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)

### OpenAI Codex

Personal install following [Codex Agent Skills](https://developers.openai.com/codex/skills) and [discovery/customization](https://developers.openai.com/codex/concepts/customization):

```bash
git clone https://github.com/bohe76/korea-transit-planner-skill.git ~/.local/share/korea-transit-planner-skill
mkdir -p ~/.agents/skills
ln -s ~/.local/share/korea-transit-planner-skill/korea-transit-planner ~/.agents/skills/korea-transit-planner

# Invoke in Codex: $korea-transit-planner compare a trip from ...
git -C ~/.local/share/korea-transit-planner-skill pull --ff-only
```

For project scope, copy or link the same complete folder at `<project>/.agents/skills/korea-transit-planner/`. `$skill-installer` can accept skills from other repositories, but v0.1.0 was verified through the official filesystem discovery paths above. Codex plugins are a separate distribution format; this single-skill release avoids a duplicate package.

### Claude Code

Personal install following [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills):

```bash
git clone https://github.com/bohe76/korea-transit-planner-skill.git ~/.local/share/korea-transit-planner-skill
mkdir -p ~/.claude/skills
ln -s ~/.local/share/korea-transit-planner-skill/korea-transit-planner ~/.claude/skills/korea-transit-planner

# Invoke in Claude Code: /korea-transit-planner compare a trip from ...
git -C ~/.local/share/korea-transit-planner-skill pull --ff-only
```

For project scope, copy or link the same complete folder at `<project>/.claude/skills/korea-transit-planner/`. [Claude Code Plugins](https://docs.anthropic.com/en/docs/claude-code/plugins) are a separate marketplace/bundle mechanism for skills plus agents, hooks, or MCP. Manual skill installation is sufficient here, so v0.1.0 does not duplicate the skill as a plugin.

### Verified scope

| Environment | Result |
|---|---|
| Hermes Agent v0.21.2, BOVIS WSL | GitHub identifier/URL installation, complete references, and load check passed |
| Codex CLI 0.154.0, BOVIS laptop WSL | Clean personal and project discovery, frontmatter 0.1.0, and reference access passed |
| Claude Code 2.1.270, BOVIS laptop WSL | Complete-folder placement and format passed; independent runtime test was blocked by expired local OAuth (HTTP 401) |
| User desktop PC, then-current Codex and Claude Code | Both products discovered, invoked, and used the skill successfully (user attestation); exact binary versions were not captured |

CI separately validates the shared Agent Skills frontmatter, directory name, and packaged local references. It does not guarantee runtime authentication or model availability.

## Example request

```text
Origin: Busan Station. Destination: Haeundae Beach.
Compare subway, bus, and taxi for arrival by 14:00 Saturday.
Include first access, waiting, transfers, final walk, fare confidence, and a 10-minute buffer.
```

Request GTX explicitly when wanted:

```text
Origin: Seoul Station. Destination: KINTEX Exhibition Center 1.
I must alight at GTX-A KINTEX Station; compare it with ordinary subway on the same arrival basis.
```

The response should place door-to-door time, wait/transfers, walk, fare confidence, and arrival risk side by side, while separating current facts, planner candidates, and estimates. See the [fictional route-briefing structure](korea-transit-planner/examples/route-briefing.md); it contains no live transit or personal trip data.

## Verification and privacy

| Information | Preferred evidence | What the result retains |
|---|---|---|
| Schedule, fare, operating conditions | Official operator or public source | Source and check time |
| Route candidates and walking links | Map service | Candidate status; cross-check official facts |
| Traffic and dispatch waits | Currently available information | Check time, time zone, and uncertainty |

Read the detailed procedures for [map-route candidates](korea-transit-planner/references/map-routing.md), [source priority](korea-transit-planner/references/source-verification.md), [GTX opt-in](korea-transit-planner/references/gtx-routing.md), and [local modes/DRT](korea-transit-planner/references/local-modes.md).

Respect map-service terms. This repository does not redistribute scraped proprietary data or map assets. Public contributions must not include home addresses, account identifiers, calendar data, tokens, authenticated URLs, or personal preference profiles. Report a potential private-data exposure through [SECURITY.md](SECURITY.md), not a public issue.

## Development

Python 3.9+ and no external packages are required:

```bash
python scripts/validate_agent_skill.py korea-transit-planner
python scripts/validate.py .
python -m unittest discover -s tests -v
```

The validator checks structure, frontmatter, explicit-origin priority, GTX opt-in, required modes, private-string patterns, and secret patterns. GitHub Actions runs the same commands.

## Contribute

Focused pull requests—from a source correction to a regional operator reference—are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md). Generalized, privacy-safe improvements may be released under SemVer; breaking origin, GTX, station-constraint, privacy, or output-contract changes require a major version. Releases always require maintainer review and are not automated.

## License

[MIT](LICENSE)

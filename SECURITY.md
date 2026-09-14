# Security and privacy

## Supported versions

Until the first public release is created, security and privacy fixes target the default branch. Afterward, the latest released minor line receives fixes.

## Reporting

Use GitHub's private vulnerability reporting for this repository:

<https://github.com/bohe76/korea-transit-planner-skill/security/advisories/new>

Do not place credentials, private addresses, trip histories, calendar details, account identifiers, or unredacted screenshots in a public issue. Provide the smallest synthetic reproduction possible.

## Scope and guarantees

This repository contains a text procedure and deterministic validators. It does not ship a routing service, map data, API keys, or an authenticated integration. An agent using the skill may query external providers under that provider's terms and the user's authorization.

Maintainers review changes for:

- embedded secrets and credential-like values;
- personal locations and identities;
- proprietary or copyrighted data/assets;
- instructions that could trigger booking, taxi calls, reservations, or external messages without explicit authorization;
- weakening of the explicit-origin, hard-station, or GTX opt-in contracts.

No route should be treated as a safety guarantee. Travelers must recheck time-sensitive service information with the responsible operator.

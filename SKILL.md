---
name: korea-transit-planner
description: Plan privacy-safe Korean door-to-door transit routes.
version: 0.1.0
author: bohe76, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [korea, transit, routing, subway, bus, drt]
    related_skills: []
---

# Korea Transit Planner

Plan Korean door-to-door trips from an explicit origin to an exact destination. Compare practical route candidates while separating verified schedule and fare facts from estimates. This skill provides a research and response procedure; it does not bundle map data, API keys, or a routing engine.

## When to Use

- The user provides an origin and asks for Korean transit, walking, taxi, or mixed-route guidance.
- The user needs a same-time comparison, departure recommendation, exit, transfer, fare, or last-mile detail.
- The trip may involve city/intercity buses, 마을버스, 누리버스/DRT, or ordinary subway.
- Load the GTX reference only when the user explicitly says `GTX` or names a GTX station.

Do not use this skill until an origin is known. Ask for the origin instead of assuming a home, neighborhood, station, calendar identity, or saved preference.

## Inputs

Collect these before route research:

1. Explicit origin; it overrides every inferred or stored location.
2. Exact destination or a place identity that can be disambiguated.
3. Departure or required-arrival time and date, including timezone when unclear.
4. Allowed/preferred modes and accessibility, luggage, weather, budget, or transfer constraints.
5. Any user-named boarding, transfer, or alighting station; preserve it as a hard constraint.

If a place or station name is ambiguous, verify its name, address, operator context, and coordinates. Do not substitute a similarly named venue for a station.

## Source Order

1. Official operator or public transit sources for timetables, service notices, fares, and DRT eligibility.
2. Korean map planners for route candidates, walking legs, exits, and traffic-aware estimates.
3. Venue/operator pages for entrances, campus access, and last-mile instructions.
4. Secondary sources only as labeled fallback evidence.

Read [source verification](references/source-verification.md) and [map routing](references/map-routing.md) before collecting route facts. For village bus and DRT work, also read [local modes](references/local-modes.md). Never embed credentials or copy proprietary route datasets into output or repository files.

## Procedure

1. Resolve the origin and destination. Record the effective origin as user-supplied and verify both place identities.
2. Fix one comparison time. Use the same planned departure or arrival basis for every candidate; record the current/live lookup timestamp with timezone.
3. Build relevant candidates across ordinary subway, city/intercity bus, 마을버스, 누리버스/DRT, walking, taxi, and mixed routes. Omit a mode only when irrelevant, unavailable, or excluded, and say why.
4. If and only if the user explicitly mentions GTX or names a GTX station, read [GTX routing](references/gtx-routing.md) and build a GTX candidate. Otherwise perform no GTX lookup or comparison.
5. Expand each candidate into first mile, initial wait/headway, ride legs, transfers, exit/stop walking, and final mile. Confirm every user-named station appears in the expanded legs.
6. Compare door-to-door totals, not station-to-station times. Include transfer burden, walking, expected wait/headway, fare and fare confidence, traffic or reservation risk, and an appointment buffer.
7. Recommend a primary route and fallback. Identify which facts are live, scheduled, estimated, or unavailable, and attach the lookup timestamp to volatile facts.

## Output Contract

Lead with the recommendation, then provide a compact comparison table and step-by-step route.

For every viable candidate include:

- mode and exact boarding/alighting points;
- first/last-mile walking or taxi legs;
- expected wait/headway and transfers;
- door-to-door duration on the same time basis;
- fare with confidence/source status;
- exits and walking where verified;
- appointment buffer and recommended departure time when arrival is fixed;
- current/live lookup timestamp with timezone for volatile information.

Use the reusable [route briefing example](examples/route-briefing.md) as a shape, not as factual route data.

## Privacy and Safety

- Require an explicit origin and use it only for the current request.
- Do not infer or expose home addresses, calendar identities, account data, API keys, or personal preference profiles.
- Do not book tickets, reserve DRT, call a taxi, or message a third party without a separate explicit request and applicable authorization.
- Treat route planners as candidates, not proof of official fare or schedule facts.

## Pitfalls

- A fast rail segment can lose door-to-door after station access, deep platforms, waits, and last mile.
- Similar station and venue names can resolve to different coordinates.
- Future plans are not live arrivals; label the distinction.
- DRT service areas, reservation rules, and operating windows vary by operator.
- A fare estimate without passenger type, transfer rules, or surcharge data has limited confidence.

## Verification

Before answering, confirm that the origin is explicit, constrained stations remain in the route, all compared modes use one time basis, every total includes first/last mile and waits, live facts carry a timestamp, and uncertainty is field-specific. Repository maintainers can run `python scripts/validate.py .` and `python -m unittest discover -s tests -v` through the `terminal` tool.

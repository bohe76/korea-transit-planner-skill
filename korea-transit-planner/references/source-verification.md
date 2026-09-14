# Source verification

## Evidence hierarchy

1. Official operator or public authority: timetables, service changes, fares, reservation rules, accessibility, DRT boundaries.
2. Korean map/journey planner: candidate routes, traffic-aware duration, transfers, exits, and walking legs.
3. Official venue or facility page: entrance, campus shuttle, building access, and internal last mile.
4. Reputable secondary source: fallback context only, with age and uncertainty stated.

Do not promote a planner estimate to an official fact. Prefer field-specific confidence instead of calling an entire route simply “verified” or “unverified.”

## Fact ledger

For each important field, track:

- value;
- source URL or source name;
- source type (`official`, `planner`, `venue`, `secondary`);
- effective date if published;
- lookup timestamp and timezone for live/current facts;
- confidence (`high`, `medium`, `low`);
- limitation or fallback used.

## Time rules

- Use the requested trip date and one departure/arrival basis across modes.
- Label future planner output as predicted, not live.
- Use live arrivals only for imminent travel and include the lookup timestamp with timezone.
- Check temporary notices when service disruption could alter the recommendation.
- If the requested date is outside the published schedule or booking window, say when rechecking becomes necessary.

## Fare rules

Verify the exact passenger type, station or zone pair, transfer assumptions, reservation fee, toll, and surcharge where relevant. If only a planner quote or rough range is available, mark the fare confidence accordingly.

## Transparent fallback

When authoritative data is unavailable, state which field is missing, what fallback supplied the estimate, and how it could change the decision. Keep verified leg values separate from calculated buffers and estimated waits.

# Map routing verification

Use Korean map planners to discover candidate routes and detailed walking connections. Do not treat a planner as the sole authority for official schedules, service notices, or fares.

## Candidate procedure

1. Resolve the explicit origin and destination separately. Confirm displayed name, address, and coordinates before routing.
2. Set one planned departure or arrival time for every compared mode. Do not compare a current bus result with a future subway result.
3. Expand every candidate. Capture first-mile access, initial wait/headway, ride legs, transfers, exits or stops, last-mile walking, total time, and quoted fare.
4. Preserve any user-named station in the expanded legs. A collapsed label such as `rail → bus` is not proof that the required station was used.
5. Cross-check volatile schedule and fare facts against official operator or public sources. Record source status and lookup timestamp.

## Place identity

Station names may overlap with venues, districts, terminals, or buildings. Verify the result type, operator/line context, address, and coordinates. If identity remains ambiguous enough to change the route, ask the user rather than silently choosing.

## URLs and proprietary data

Share normal destination or route links when permitted by the service. Do not embed API keys, authenticated URLs, scraped route corpora, copyrighted map tiles, logos, or proprietary datasets in artifacts. Summarize only the facts needed for the current comparison and respect provider terms.

## Fallback

If one planner is blocked or omits a mode, try another map planner or official journey planner. If no current route is available, combine separately verified legs and label the result as a planning estimate. Never convert missing data into false precision.

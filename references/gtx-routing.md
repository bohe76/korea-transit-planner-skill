# GTX routing — explicit opt-in only

Open this reference only when the user explicitly says `GTX` or names a GTX station. Never research or compare GTX proactively because a destination happens to lie near a GTX corridor.

## Required checks

1. Treat every user-named GTX boarding, transfer, or alighting station as a hard constraint.
2. Verify station identity with official operator context, address, and coordinates; distinguish a station from a similarly named venue.
3. Expand the route as origin → station entrance → deep platform/wait → GTX segment → exact alighting station → final walk, bus, or taxi.
4. Use the current official operator timetable, service notice, and fare calculator for the exact station pair and passenger type.
5. For the relevant hour, report realistic departures or headway rather than a full-day average.
6. Add enough station-access and deep-platform transfer allowance before selecting a train.
7. Compare GTX with ordinary subway/bus and taxi on the same planned time basis.

## Output fields

- exact boarding and alighting stations;
- direction and official in-train time;
- candidate departure times or headway;
- official fare or an explicit unavailable note;
- station access, deep-platform transfer, and expected wait;
- final-mile mode, time, and cost confidence;
- door-to-door total, appointment buffer, and recommendation;
- source and lookup timestamp with timezone.

If a map planner omits the constrained route, combine verified segments transparently and label the total as a planning estimate. Never replace the named station with a faster one without the user's approval.

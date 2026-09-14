# Route briefing example

This is a fictional structure example, not current route data.

## Request

- Origin: `Sample Origin Terminal`
- Destination: `Sample Civic Hall`
- Required arrival: `2030-05-18 14:00 KST`
- Modes: ordinary subway, bus, walking, taxi, mixed
- Buffer: 15 minutes

## Recommendation

Choose Candidate A because its predicted door-to-door range is narrower and it reaches the appointment buffer with one transfer. Candidate B is the low-walking fallback.

| Candidate | Door to door | Wait/headway | Transfers | Walk | Fare / confidence | Arrival risk |
|---|---:|---:|---:|---:|---|---|
| A · ordinary subway | 48–55 min | 4–8 min | 1 | 12 min | source quote / medium | low–medium |
| B · city bus | 52–68 min | 6–12 min | 0 | 6 min | official base fare / high | traffic-sensitive |
| C · taxi | 35–60 min | 3–10 min | 0 | 2 min | planner range / medium | traffic-sensitive |

## Candidate A

1. Walk from the origin entrance to the first platform: about 7 minutes.
2. Board the verified line and direction; expected wait 4–8 minutes.
3. Transfer once, allowing platform walking and wait.
4. Alight at the verified destination station and use the verified exit.
5. Walk from the exit to the destination entrance: about 5 minutes.

Recommended departure: 12:50 KST for a 13:45 buffered arrival target.

## Evidence note

- Official schedule/fare checked: `2030-05-17 20:00 KST`
- Planner candidates checked: `2030-05-17 20:05 KST`
- Volatile facts must be refreshed near departure.
- Any unavailable exit, fare, or accessibility field should be named explicitly rather than guessed.

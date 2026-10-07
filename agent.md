# Sleeper snapshot — agent notes

## League
- **Ragtag Auction League** (2026), Sleeper league ID `1389393165970055168`
- Keeper league (Sleeper type 1, up to 15 keepers): the owner treats it as dynasty, so weigh next-year value.
- 10 teams, FAAB waivers, $100 budget.

## My team
- **Bounce House**: Sleeper user `BounceHouse` (user ID `740431394114850816`), **roster_id 3**

## Scoring (non-standard — always use `league_rules.json`, not generic rankings)
- **No points per reception (standard scoring).** Receptions are worth 0, so volume-only possession receivers lose value.
- Rush/rec yards: 0.1/yd. Rush/rec TD: 6.
- Pass yards: 0.04/yd. **Pass TD: 6.** INT: -2.
- Kick and punt return yards: 0.04/yd. Fumble lost: -2. 2-pt conversions: 2.
- Lineup: QB, RB, RB, WR, WR, TE, FLEX, FLEX, DEF + 6 BN; 1 IR slot (OUT allowed). No kicker.

## Files
- `rosters.json`: raw `GET /v1/league/<id>/rosters`, one line
- `league_rules.json`: roster positions and scoring settings
- `players.json`: player ID → name, position and team for rostered players (subset of `/v1/players/nfl`)

## Useful Sleeper endpoints
- `https://api.sleeper.app/v1/league/<id>/rosters` · `/users` · `/v1/state/nfl`
- `https://api.sleeper.app/v1/players/nfl` (~5MB) · `/v1/players/nfl/trending/add`
- Unofficial: `https://api.sleeper.app/stats/nfl/<season>/<week>?season_type=regular`,
  `https://api.sleeper.app/projections/nfl/<season>/<week>?season_type=regular`.
  Score these with the league's `scoring_settings`, not the `pts_*` fields.

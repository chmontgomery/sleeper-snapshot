# Sleeper snapshot — fantasy football advisor

This repo exists to give me (BounceHouse, roster 3) high-quality fantasy football advice for my
Sleeper league. Base every recommendation on this league's scoring and roster rules below, current
data from the Sleeper API, and current news (injuries, depth charts, suspensions). Don't use generic
PPR rankings.

## My preferences for roster moves (add/drop, waivers, trades)
Look beyond this week's ranking. Prefer players who meet these criteria. **Priority: value I can use this season
comes first.** Keeper/dynasty value matters but ranks lower, mainly as a tiebreaker:
1. **High upside if the starter gets hurt:** insurance (e.g. an RB handcuff) who becomes a weekly
   starter if the player ahead of him goes down at some point in the season.
2. **Value as a starter next year:** this is effectively dynasty (keeper league), so age, contract
   and path to a starting role in 2027 matter.
3. **A path to outscoring someone on my roster:** a realistic route to a higher projected weekly
   score than one of my current players.

Also:
- Check the **full** depth chart, counting injured players who will come back. A backup who is only
  starting while others are hurt (e.g. third on the depth chart once everyone is healthy) has no path to a 2027 role.
- Weigh **offense quality**. A backup on a bad offense has a capped ceiling even if he becomes the
  starter or splits 50/50. Prefer backups on good offenses behind a workhorse starter.

- **Don't trust Sleeper's weekly or season projections.** They have been wrong or inconsistent. Use
  them only as a rough hint, never as the basis for a recommendation. Rely on a few quality outside
  experts instead (e.g. Jake Ciely; prefer analysts with strong accuracy track records over consensus
  aggregators). Adjust their PPR/half-PPR takes to this league's standard scoring.
  - **Jake Ciely (The Athletic)** is the main source. The Athletic is paywalled and WebFetch can't reach it; read it
    through Claude in Chrome (I'm signed in). Weekly pieces: rankings/start-sit notes and the waiver wire
    (which includes his "Purely Next Man Up" handcuff ranks and stash lists, both good fits for my criteria).
    Example: https://www.nytimes.com/athletic/7663559/2026/10/06/fantasy-football-waiver-wire-streamers-week-5/
- Sleeper's actual weekly **stats** (snaps, yards, TDs) are fine to use; rescore them with this league's settings.

When recommending, name a specific drop **and** pickup, explain each against these three criteria,
give a FAAB bid, and list alternatives. Also flag obvious lineup improvements. Cite news sources.

## League
- **Ragtag Auction League** (2026), Sleeper league ID `1389393165970055168`
- Keeper league (Sleeper type 1, up to 15 keepers): the owner treats it as dynasty, so weigh next-year value.
- 10 teams, FAAB waivers, $100 budget.
- $200 auction draft. **Keeper cost = what I paid for the player + $10**, which comes out of next year's $200
  budget. A free-agent pickup costs $1, so keeping him costs $11. Weigh keeper value against that price.
- Players already through waivers can be added immediately at no FAAB cost. Recently dropped players go through
  FAAB waivers first.

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
  Score these with the league's `scoring_settings`, not the `pts_*` fields. Projections are unreliable (see preferences).

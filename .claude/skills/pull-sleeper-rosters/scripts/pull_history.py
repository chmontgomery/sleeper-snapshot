#!/usr/bin/env python3
"""Pull the season's week-by-week league history into history/.

Writes, for every regular-season week played so far (and the current week):
  history/matchups/week_NN.json      raw GET /league/<id>/matchups/<week>
  history/transactions/week_NN.json  raw GET /league/<id>/transactions/<week>
plus, once per run:
  history/draft_picks.json           raw GET /draft/<draft_id>/picks for the league's draft(s)
and adds any player ID seen there to players.json so names resolve.

Sleeper keeps every past week, so the first run backfills the whole season and later
runs refresh the current week and add new ones. Files only change (and get committed)
when Sleeper's data changes.

Run from the repo root, after pull_rosters.py:
  python3 .claude/skills/pull-sleeper-rosters/scripts/pull_history.py
"""
import json
import os
import time
import urllib.request

LEAGUE_ID = "1389393165970055168"
API = "https://api.sleeper.app/v1"
OUT = "history"
REGULAR_SEASON_WEEKS = 18


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** (i + 1))


def write(path, data):
    """Write compact JSON; return True if the file's content changed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = json.dumps(data, separators=(",", ":"), sort_keys=True)
    try:
        if open(path).read() == text:
            return False
    except FileNotFoundError:
        pass
    with open(path, "w") as f:
        f.write(text)
    return True


def weeks_to_pull(league, state):
    """Weeks 1..current for the league's season; all weeks once that season is over."""
    season = str(league.get("season"))
    if str(state.get("season")) != season:
        # NFL state has moved to a later season (or preseason of the next one).
        return list(range(1, REGULAR_SEASON_WEEKS + 1)) if str(state.get("season")) > season else []
    if state.get("season_type") == "post":
        return list(range(1, REGULAR_SEASON_WEEKS + 1))
    week = int(state.get("week") or 0)
    return list(range(1, min(max(week, 0), REGULAR_SEASON_WEEKS) + 1))


def player_ids(obj):
    """Every Sleeper player ID referenced in matchups, transactions or draft picks."""
    ids = set()
    if isinstance(obj, list):
        for x in obj:
            ids |= player_ids(x)
    elif isinstance(obj, dict):
        for k in ("players", "starters"):
            v = obj.get(k)
            if isinstance(v, list):
                ids |= {p for p in v if isinstance(p, str)}
        for k in ("adds", "drops"):
            v = obj.get(k)
            if isinstance(v, dict):
                ids |= set(v)
        if isinstance(obj.get("player_id"), str):
            ids.add(obj["player_id"])
    return {i for i in ids if i and i != "0"}


def main():
    league = get(f"{API}/league/{LEAGUE_ID}")
    state = get(f"{API}/state/nfl")
    weeks = weeks_to_pull(league, state)

    seen = set()
    changed = []
    for w in weeks:
        m = get(f"{API}/league/{LEAGUE_ID}/matchups/{w}") or []
        t = get(f"{API}/league/{LEAGUE_ID}/transactions/{w}") or []
        seen |= player_ids(m) | player_ids(t)
        a = write(f"{OUT}/matchups/week_{w:02d}.json", m)
        b = write(f"{OUT}/transactions/week_{w:02d}.json", t)
        if a or b:
            changed.append(f"wk {w}")

    picks = []
    for d in get(f"{API}/league/{LEAGUE_ID}/drafts") or []:
        picks.extend(get(f"{API}/draft/{d['draft_id']}/picks") or [])
    seen |= player_ids(picks)
    if picks and write(f"{OUT}/draft_picks.json", picks):
        changed.append("draft")

    # Make sure every player in the history has a name in players.json.
    try:
        names = json.load(open("players.json"))
    except FileNotFoundError:
        names = {}
    missing = seen - names.keys()
    if missing:
        # Same lookup as pull_rosters.py (team defenses use their code, e.g. "JAX").
        allp = get(f"{API}/players/nfl")
        for pid in missing:
            p = allp.get(pid, {})
            name = p.get("full_name") or f"{p.get('first_name', '')} {p.get('last_name', '')}".strip() or pid
            names[pid] = {"name": name, "position": p.get("position"), "team": p.get("team")}
        with open("players.json", "w") as f:
            json.dump(names, f, indent=2, sort_keys=True)

    span = f"weeks {weeks[0]}-{weeks[-1]}" if weeks else "no weeks yet"
    print(f"History ({span}): " + ("updated " + ", ".join(changed) if changed else "no changes"))


if __name__ == "__main__":
    main()

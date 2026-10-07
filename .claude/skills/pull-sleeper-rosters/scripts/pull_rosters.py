#!/usr/bin/env python3
"""Pull the latest Sleeper rosters into rosters.json, extend players.json, and print changes.

Run from the repo root: python3 .claude/skills/pull-sleeper-rosters/scripts/pull_rosters.py
"""
import json
import urllib.request

LEAGUE_ID = "1389393165970055168"
MY_ROSTER_ID = 3
API = "https://api.sleeper.app/v1"


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def main():
    try:
        old = {r["roster_id"]: r for r in json.load(open("rosters.json"))}
    except FileNotFoundError:
        old = {}
    new = get(f"{API}/league/{LEAGUE_ID}/rosters")
    users = {u["user_id"]: u for u in get(f"{API}/league/{LEAGUE_ID}/users")}
    try:
        names = json.load(open("players.json"))
    except FileNotFoundError:
        names = {}

    # Only download the ~5MB player DB when a roster contains an unmapped ID.
    ids = {p for r in new for p in (r["players"] or [])}
    if ids - names.keys():
        allp = get(f"{API}/players/nfl")
        for pid in ids - names.keys():
            p = allp.get(pid, {})
            name = p.get("full_name") or f"{p.get('first_name', '')} {p.get('last_name', '')}".strip() or pid
            names[pid] = {"name": name, "position": p.get("position"), "team": p.get("team")}

    with open("rosters.json", "w") as f:
        json.dump(new, f, separators=(",", ":"))
    with open("players.json", "w") as f:
        json.dump(names, f, indent=2, sort_keys=True)

    n = lambda pid: names.get(pid, {}).get("name", pid)
    changed = 0
    for r in sorted(new, key=lambda r: r["roster_id"]):
        rid, s = r["roster_id"], r["settings"]
        u = users.get(r["owner_id"], {})
        team = (u.get("metadata") or {}).get("team_name") or u.get("display_name", "?")
        cur, prev = set(r["players"] or []), set((old.get(rid) or {}).get("players") or [])
        added, dropped = sorted(cur - prev, key=n), sorted(prev - cur, key=n)
        changed += bool(added or dropped)
        mine = " (ME)" if rid == MY_ROSTER_ID else ""
        line = f"{rid:>2} {team}{mine} {s['wins']}-{s['losses']}-{s.get('ties', 0)} FAAB used {s.get('waiver_budget_used', 0)}"
        if added or dropped:
            line += f" | +{', '.join(map(n, added)) or '-'} | -{', '.join(map(n, dropped)) or '-'}"
        print(line)
    print(f"\n{changed} roster(s) changed since last snapshot.")


if __name__ == "__main__":
    main()

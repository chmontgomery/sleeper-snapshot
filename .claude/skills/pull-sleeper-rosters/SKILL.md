---
name: pull-sleeper-rosters
description: Use when the user asks to pull, refresh, update or snapshot the latest Sleeper league rosters, team members, or who is on each team in the Ragtag Auction League, or before giving roster, waiver or trade advice that depends on current rosters.
---

# Pull Sleeper rosters

Refreshes `rosters.json` (raw `/league/<id>/rosters`) and extends `players.json` (player ID → name, position, team) for the league in `CLAUDE.md`, then reports changes since the last snapshot.

## Steps

1. From the repo root, run:
   `python3 .claude/skills/pull-sleeper-rosters/scripts/pull_rosters.py`
   then, for week-by-week matchups, transactions and the draft in `history/`:
   `python3 .claude/skills/pull-sleeper-rosters/scripts/pull_history.py`
2. If `git status --short` shows changes, commit them (`git add history` first if it is new):
   `git commit -am "sleeper rosters snapshot YYYY-MM-DD"` (add a short note like `(Shipley added)` when my roster changed). Use today's date. If nothing changed, don't commit.
3. Report to the user as a table: roster, team, record and the players added and dropped (by name). Lead with my team (roster 3, marked `(ME)`), then the other teams that changed. Mention my FAAB remaining ($100 − used).

## Notes
- The script uses only the standard library and downloads the ~5MB `/players/nfl` only when there are new player IDs.
- The diff compares against the committed `rosters.json`, so it shows all changes since the last pull, not just today's.

<!-- BEGIN Coriolis process pointer (keep at top) -->
# Read the process first

This repo follows the Coriolis AI Studio process. At the start of every session, read these on `main` in `CoriolisAgency/coriolis` (local `C:\dev\coriolis` or `/coriolis`; `git pull` first). Read the live copy each time; don't work from a pasted or remembered copy.

1. `docs/process/coriolis-ai-studio-process.md` (and the short `docs/process/coriolis-ai-studio-quickstart.md`)
2. `docs/rules.md`: standing rules (page ownership, prices, where ads land, what we don't claim, security)
3. `docs/decisions/`: one file per decision; don't work against a `locked` one
4. `docs/board.md`: the work list

Then:
- Status words, and only these: decide, locked, parked, queued, coding, verifying, shipped. Only Paul locks, unlocks, queues or parks.
- Build only a board line that is `queued`, `coding` or `verifying`. Work moves `queued` → `coding` (branch start to an open PR) → `verifying` (PR open through merge until "done when" is checked) → `shipped`. One item in coding or verifying, plus one urgent fix if production is broken. If there's no line for the work, you're deciding, not building.
- Code goes on a branch and through a PR that names the decision and the board line. Never push code to `main`. Paul merges unless he says "merge N".
- Done means merged and "done when" checked. Board edits are doc-only commits on coriolis main.
- Hard stops need Paul's explicit OK: migrations or prod data writes, sends of any kind, anything that costs money, secrets or env changes, force-push, prod flag flips.

This block wins over anything below it, including any "push it" or work-on-main instructions. `BATTLEPLAN.md` and `BATTLEPLAN-ARCHIVE.md` in coriolis are a read-only archive now.
Lane for this repo: Docs / Coriolis (board prefix DOCS).
<!-- END Coriolis process pointer -->

# Coriolis Docs — agent notes

Operator docs for `docs.coriolisagency.com`: Mintlify, Git-backed MDX. `docs.json` at the repo root is the nav. Push to `main` deploys once Mintlify is connected (see `DEPLOY.md`).

Read `LOCK.md` before any change. It is the frozen v0.1 lock; do not reopen platform, host, or the title blocklist without Paul. Board line: DOCS-1 (decision `2026-10-08-operator-docs-v0-1` in coriolis `docs/decisions/`).

## Rules from the lock

- Operator and troubleshooting tasks only. Commercial intents stay on the SEO lattice owners on coriolisagency.com.
- Every page links up once to its ranking owner (table in `LOCK.md`).
- Check every title, H1 and meta description against `TITLE-BLOCKLIST.md`.
- Do not add `llms.txt` or `llms-full.txt`. Mintlify emits them.
- Do not restate the plan ladder. If a task must name a rung, use the frozen strings in `LOCK.md` and link to `/ecommerce`.
- No links to `gunsearchagent.com` or `2abetsy.com`. Links to `fflaccelerator.com` only per DOCS-2 (offer-name anchors only, never /lp/). No UTMs.

## Hard no

- Stand-alone bound-book pages, Form 4473 how-to, 4473 automation claims
- "RetailBI alternative" / "switch off RetailBI"
- Saying or implying Coriolis builds or sells its own POS
- Inventing Demand Intelligence prices
- Secrets or customer license images in any page

## Deploy

`DEPLOY.md`. Do not mount the docs at `coriolisagency.com/docs`; that host owns the commercial lattice.

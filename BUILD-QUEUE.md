# Build queue — v0.1

Locked 2026-10-08. Status: packet ready for Chief. Not deployed. Mintlify credentials are not in this workspace.

## Ticket 0 — platform (Chief, this week)

- [ ] Mintlify org
- [ ] GitHub repo `CoriolisAgency/coriolis-docs`, this folder as root
- [ ] Connect repo, deploy `main`
- [ ] Custom domain `docs.coriolisagency.com` (dashboard CNAME, TXT verify, canonical already in `docs.json`)
- [ ] Noindex or redirect the default `*.mintlify.app` host
- [ ] Search Console property, submit `sitemap-index.xml`
- [ ] Drop `/logo.svg` and set `logo` in `docs.json` before announce

## Ticket 1 — seed content (in this packet)

- [x] `docs.json` nav
- [x] Title blocklist
- [x] 16 MDX pages (12-page seed plus ownership, launch, taxes, support)
- [ ] Paul pass on payments processors and AIM “Warlord and above” wording
- [ ] Push

## Ticket 2 — lattice wiring (after seed is live)

- [ ] Lattice addendum: docs host owns operator intent only
- [ ] One link down from `/ffl-cockpit` to `/ffl-cockpit/connect`
- [ ] One link down from `/can-you-use-woocommerce-to-sell-guns` to `/woocommerce/shipping-and-ship-to-ffl`
- [ ] One link down from `/aim-pos` to `/pos/aim-sync`

## Ticket 3 — AI surface (after pages are real, not stubs)

- [ ] Confirm `/llms.txt` and `/llms-full.txt` return 200
- [ ] Assistant on
- [ ] Point Intercom Fin / Grok support bot at `llms-full.txt`

## Explicitly not in v0.1

- Other POS sync pages (GunBiz, Rapid, Trident, Corestore)
- Full distributor pages beyond the Sports South reference path
- Changelog
- Bound-book or 4473 procedure
- Any page that restates the plan ladder or a comparison H1

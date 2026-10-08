# Deploy v0.1

Chief runs this. The packet is the repo contents. Mintlify builds on push.

## 1. Mintlify project

1. Create the Mintlify org if it does not exist.
2. Create a Git repo `coriolis-docs` (GitHub, under CoriolisAgency).
3. Copy this folder in as the repo root. `docs.json` stays at the root.
4. Connect the repo in the Mintlify dashboard. Push to `main` deploys.

Mintlify emits `/llms.txt` and `/llms-full.txt` from the nav. Do not add those files.

## 2. Custom domain

Dashboard values win if they differ from public docs.

1. Mintlify → Custom domain → add `docs.coriolisagency.com`.
2. Add the TXT records the dashboard shows (`_acme-challenge`, `_cf-custom-hostname`) and wait until both verify.
3. CNAME `docs` to the target Mintlify displays (public docs have shown `cname.mintlify.builders`; the dashboard may show a different host). Use the dashboard value.
4. Canonical is already set in `docs.json` to `https://docs.coriolisagency.com`.
5. HTTPS is automatic after the CNAME resolves. Allow up to 24 hours.

The default `*.mintlify.app` host stays reachable. After the custom domain is live, noindex or redirect that default host so it does not compete in search.

Do not mount this at `coriolisagency.com/docs`. That host owns the commercial lattice.

## 3. Search Console

1. Add a property for `docs.coriolisagency.com`.
2. Submit `https://docs.coriolisagency.com/sitemap.xml` (Mintlify serves it at the root; `robots.txt` points to it).
3. Inspect three URLs after the first deploy: `/`, `/woocommerce/shipping-and-ship-to-ffl`, `/ffl-cockpit/connect`.

## 4. Assistant and support

1. Turn the Mintlify assistant on after the seed pages are real.
2. Point Intercom Fin, or the Grok support bot, at `https://docs.coriolisagency.com/llms-full.txt`.
3. Do not point a bot at the commercial site and the docs with equal weight. Docs answer tasks. The lattice pages answer “which plan / which alternative.”

## 5. Deep links down

After the seed is indexed, add one contextual link from each of these agency pages to the matching doc:

- `/ffl-cockpit` → `/ffl-cockpit/connect`
- `/can-you-use-woocommerce-to-sell-guns` → `/woocommerce/shipping-and-ship-to-ffl`
- `/aim-pos` → `/pos/aim-sync`

One link each. No UTMs.

## 6. Logo

Drop the Coriolis mark at `/logo.svg` and set `"logo": "/logo.svg"` in `docs.json` before the public announce. v0.1 can ship without it.

## 7. Review gate

Before each push: title against `TITLE-BLOCKLIST.md`, one link up, no secrets, no customer license images, updated stamp in the page if the steps changed.

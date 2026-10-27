#!/usr/bin/env python3
"""SEO-U36 / DOCS-2 acceptance check. Usage: check-links.py <coriolis-docs repo dir> [--live]
Compares external links in each MDX page against the map. --live also curls each target (200, no redirect).
UTMs: D-N6 docs tag on agency, GSE, and FFLA links (2026-10-21-paul-answers-901 answer 8;
2026-10-26-seo-handoffs-gse-agency calls (c) and (d)). Index uses docs-home. Navbar uses docs-footer.
what-you-own FFLA /plan/ stays untagged (SEO-U36 out of scope)."""
import json, re, sys, os, subprocess

A = "https://www.coriolisagency.com"
def U(slug): return f"?utm_source=docs&utm_medium=referral&utm_campaign=docs-{slug}"
def slug(page): return "home" if page == "index" else page.split("/")[-1]
MAP = {
 "index": [
    ("how the Coriolis stack fits", A+"/stack"+U("home")),
    ("FFL Accelerator", "https://fflaccelerator.com/"+U("home")),
    ("Coriolis AI Studio", A+"/ai-studio"+U("home")),
    ("Gun Store Game", "https://www.gunstoregame.com/"),
 ],
 "getting-started/what-you-own": [("FFL website plans", A+"/ecommerce"+U("what-you-own")), ("FFL Accelerator pricing", "https://fflaccelerator.com/plan/")],
 "getting-started/what-coriolis-configures-at-setup": [
    ("FFL website plans and what setup includes", A+"/ecommerce"+U("what-coriolis-configures-at-setup")),
    ("the register you already run", A+"/gun-store-pos"+U("what-coriolis-configures-at-setup")),
    ("the managed FFL website plan", "https://fflaccelerator.com/plan/"+U("what-coriolis-configures-at-setup")),
 ],
 "getting-started/launch-checklist": [
    ("Selling guns on WooCommerce", A+"/can-you-use-woocommerce-to-sell-guns"+U("launch-checklist")),
    ("email marketing for FFL ecommerce", A+"/email-marketing-for-ffl-ecommerce"+U("launch-checklist")),
 ],
 "woocommerce/domain-and-dns": [("gun store website plans", A+"/ecommerce"+U("domain-and-dns"))],
 "woocommerce/payments-for-ffl-woocommerce": [
    ("can you use WooCommerce to sell guns", A+"/can-you-use-woocommerce-to-sell-guns"+U("payments-for-ffl-woocommerce")),
    ("WooCommerce vs Shopify for gun stores", A+"/woocommerce-vs-shopify-for-gun-stores"+U("payments-for-ffl-woocommerce")),
    ("FFL payment processing", A+"/ffl-payment-processing"+U("payments-for-ffl-woocommerce")),
 ],
 "woocommerce/shipping-and-ship-to-ffl": [
    ("can you use WooCommerce to sell guns", A+"/can-you-use-woocommerce-to-sell-guns"+U("shipping-and-ship-to-ffl")),
    ("FFL dropshipping", A+"/firearms-dropshipping"+U("shipping-and-ship-to-ffl")),
 ],
 "woocommerce/products": [
    ("firearms dropshipping", A+"/firearms-dropshipping"+U("products")),
    ("selling guns online with WooCommerce", A+"/can-you-use-woocommerce-to-sell-guns"+U("products")),
    ("list your gun store inventory free", "https://www.gunsearchengine.com/for-dealers/feed"+U("products")),
 ],
 "woocommerce/taxes": [("FFL website pricing", A+"/ecommerce"+U("taxes"))],
 "woocommerce/theme-edits": [("gun store website plans", A+"/ecommerce"+U("theme-edits"))],
 "ffl-cockpit/connect": [("FFL Cockpit", A+"/ffl-cockpit"+U("connect")), ("FFL website plans", A+"/ecommerce"+U("connect"))],
 "ffl-cockpit/catalog-import": [("firearms dropshipping", A+"/firearms-dropshipping"+U("catalog-import")), ("FFL Cockpit and WooCommerce hosting", A+"/ffl-cockpit"+U("catalog-import"))],
 "ffl-cockpit/ffl-checkout": [("FFL Cockpit", A+"/ffl-cockpit"+U("ffl-checkout"))],
 "pos/aim-sync": [("FFL website plans", A+"/ecommerce"+U("aim-sync")), ("AIM POS", A+"/aim-pos"+U("aim-sync")), ("gun store POS", A+"/gun-store-pos"+U("aim-sync"))],
 "gunsearchengine/install": [
    ("GunSearchEngine.com", "https://www.gunsearchengine.com/"),
    ("FFL Analytics", "https://www.gunsearchengine.com/for-dealers/ffl-analytics"+U("install")),
    ("list your store on GunSearchEngine", "https://www.gunsearchengine.com/for-dealers/feed"+U("install")),
    ("Demand Intelligence", A+"/demand-intelligence"+U("install")),
 ],
 "support/contact": [
    ("FFL Cockpit website and WooCommerce hosting", A+"/ffl-cockpit"+U("contact")),
    ("Grok Bot setup", A+"/grok-bot-setup"+U("contact")),
    ("Botopticon", "https://www.botopticon.com/"),
 ],
}
BANNED = ["gunsearchagent.com", "2abetsy.com", "fflanalytics.com", "fflaccelerator.com/lp", "nofollow", "gun-store-pos-comparison"]
TAGGED_PREFIXES = (A+"/", "https://fflaccelerator.com/", "https://www.gunsearchengine.com/")
NAV_HREF = "https://www.coriolisagency.com/?utm_source=docs&utm_medium=referral&utm_campaign=docs-footer"

def links(text):
    out = [(m.group(1).strip(), m.group(2).strip()) for m in re.finditer(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', text)]
    for m in re.finditer(r'<Card\b([^>]*)>', text):
        t = re.search(r'title="([^"]*)"', m.group(1)); h = re.search(r'href="(https?://[^"]+)"', m.group(1))
        if h: out.append((t.group(1) if t else "", h.group(1)))
    return out

def main():
    root = sys.argv[1]; live = "--live" in sys.argv; fails = []
    for page, want in MAP.items():
        f = os.path.join(root, page + ".mdx")
        if not os.path.exists(f): fails.append(f"{page}: missing"); continue
        got = links(open(f, encoding="utf-8").read())
        if not 1 <= len(got) <= 4: fails.append(f"{page}: {len(got)} external links (want 1-4)")
        if sorted(got) != sorted(want):
            fails.append(f"{page}: links differ\n   got  {got}\n   want {want}")
    # Any query must be the D-N6 docs tag for this page, on agency / FFLA / GSE.
    for page in MAP:
        f = os.path.join(root, page + ".mdx")
        if not os.path.exists(f): continue
        for anchor, u in links(open(f, encoding="utf-8").read()):
            if "utm_" not in u and "?" not in u: continue
            base, _, qs = u.partition("?")
            if not any(base.startswith(p) for p in TAGGED_PREFIXES) or "?" + qs != U(slug(page)):
                fails.append(f"{page}: query on {u} is not the D-N6 docs tag for this page")
    docs_path = os.path.join(root, "docs.json")
    docs = json.load(open(docs_path, encoding="utf-8"))
    logo = docs.get("logo", {}).get("href", "")
    if "utm_" in logo or "?" in logo:
        fails.append("docs.json: logo href must stay untagged")
    nav = [x for x in docs.get("navbar", {}).get("links", []) if x.get("label") == "Coriolis"]
    if not nav or nav[0].get("href") != NAV_HREF:
        fails.append(f"docs.json: navbar Coriolis href want {NAV_HREF}")
    if "footer" in docs:
        fails.append("docs.json: do not add a footer block")
    if docs.get("seo", {}).get("metatags", {}).get("canonical") != "https://docs.coriolisagency.com":
        fails.append("docs.json: do not touch seo.metatags.canonical")
    for dp, _, fs in os.walk(root):
        if ".git" in dp: continue
        for n in fs:
            if n.endswith((".mdx", ".json")):
                t = open(os.path.join(dp, n), encoding="utf-8").read()
                for b in BANNED:
                    if b in t: fails.append(f"{n}: contains banned '{b}'")
    ffla = sum(1 for w in MAP.values() for _, u in w if "fflaccelerator.com" in u)
    if ffla != 3: fails.append(f"map has {ffla} fflaccelerator links (want 3: home /, setup /plan/, what-you-own /plan/)")
    if live:
        for u in sorted({u for w in MAP.values() for _, u in w}):
            r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-m", "20", "-A", "Mozilla/5.0", "-w", "%{http_code} %{redirect_url}", u], capture_output=True, text=True).stdout.strip()
            print(f"  {r:<6} {u}")
            if not r.startswith("200"): fails.append(f"live: {u} -> {r}")
    print("\n".join(fails) if fails else "OK: all DOCS-2 checks pass")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()

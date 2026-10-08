#!/usr/bin/env python3
"""DOCS-2 acceptance check. Usage: check-links.py <coriolis-docs repo dir> [--live]
Compares external links in each MDX page against the DOCS-2 map. --live also curls each target (200, no redirect)."""
import re, sys, os, subprocess

A = "https://www.coriolisagency.com"
MAP = {
 "index": [("how the Coriolis stack fits", A+"/stack"), ("Coriolis AI Studio", A+"/ai-studio"), ("Gun Store Game", "https://www.gunstoregame.com/")],
 "getting-started/what-you-own": [("FFL website plans", A+"/ecommerce"), ("FFL Accelerator pricing", "https://fflaccelerator.com/plan/")],
 "getting-started/what-coriolis-configures-at-setup": [("FFL website plans and what setup includes", A+"/ecommerce"), ("gun store POS system", A+"/gun-store-pos"), ("managed FFL ecommerce", "https://fflaccelerator.com/")],
 "getting-started/launch-checklist": [("Selling guns on WooCommerce", A+"/can-you-use-woocommerce-to-sell-guns"), ("email marketing for FFL ecommerce", A+"/email-marketing-for-ffl-ecommerce")],
 "woocommerce/domain-and-dns": [("gun store website plans", A+"/ecommerce")],
 "woocommerce/payments-for-ffl-woocommerce": [("can you use WooCommerce to sell guns", A+"/can-you-use-woocommerce-to-sell-guns"), ("WooCommerce vs Shopify for gun stores", A+"/woocommerce-vs-shopify-for-gun-stores")],
 "woocommerce/shipping-and-ship-to-ffl": [("can you use WooCommerce to sell guns", A+"/can-you-use-woocommerce-to-sell-guns"), ("FFL dropshipping", A+"/firearms-dropshipping")],
 "woocommerce/products": [("firearms dropshipping", A+"/firearms-dropshipping"), ("list your gun store inventory free", "https://www.gunsearchengine.com/for-dealers/feed")],
 "woocommerce/taxes": [("FFL website pricing", A+"/ecommerce")],
 "woocommerce/theme-edits": [("gun store website plans", A+"/ecommerce")],
 "ffl-cockpit/connect": [("FFL Cockpit", A+"/ffl-cockpit"), ("FFL website plans", A+"/ecommerce")],
 "ffl-cockpit/catalog-import": [("firearms dropshipping", A+"/firearms-dropshipping"), ("FFL Cockpit and WooCommerce hosting", A+"/ffl-cockpit")],
 "ffl-cockpit/ffl-checkout": [("FFL Cockpit", A+"/ffl-cockpit")],
 "pos/aim-sync": [("FFL website plans", A+"/ecommerce"), ("AIM POS", A+"/aim-pos"), ("gun store POS", A+"/gun-store-pos")],
 "gunsearchengine/install": [("GunSearchEngine.com", "https://www.gunsearchengine.com/"), ("FFL Analytics", "https://www.gunsearchengine.com/for-dealers/ffl-analytics"), ("Demand Intelligence", "https://www.gunsearchengine.com/demand-intelligence")],
 "support/contact": [("FFL Cockpit website and WooCommerce hosting", A+"/ffl-cockpit"), ("Grok Bot setup", A+"/grok-bot-setup"), ("Botopticon", "https://www.botopticon.com/")],
}
BANNED = ["gunsearchagent.com", "2abetsy.com", "fflanalytics.com", "fflaccelerator.com/lp", "utm_", "nofollow", "gun-store-pos-comparison"]

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
        if not 1 <= len(got) <= 3: fails.append(f"{page}: {len(got)} external links (want 1-3)")
        if sorted(got) != sorted(want):
            fails.append(f"{page}: links differ\n   got  {got}\n   want {want}")
    for dp, _, fs in os.walk(root):
        if ".git" in dp: continue
        for n in fs:
            if n.endswith((".mdx", ".json")):
                t = open(os.path.join(dp, n), encoding="utf-8").read()
                for b in BANNED:
                    if b in t: fails.append(f"{n}: contains banned '{b}'")
    ffla = sum(1 for w in MAP.values() for _, u in w if "fflaccelerator.com" in u)
    if ffla != 2: fails.append(f"map has {ffla} fflaccelerator links (want 2)")
    if live:
        for u in sorted({u for w in MAP.values() for _, u in w}):
            r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-m", "20", "-A", "Mozilla/5.0", "-w", "%{http_code} %{redirect_url}", u], capture_output=True, text=True).stdout.strip()
            print(f"  {r:<6} {u}")
            if r != "200": fails.append(f"live: {u} -> {r}")
    print("\n".join(fails) if fails else "OK: all DOCS-2 checks pass")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()

# BespokeStudio — website

Static marketing site for **BespokeStudio** (Reid & Taylor bespoke tailoring &
fabric showroom, Basaveshwaranagar, Bengaluru). Plain HTML/CSS/vanilla JS, no
build step beyond one Python script, no runtime dependencies. Deployed to
**Cloudflare Pages**.

**Live:** https://bespokestudio.pages.dev · **Canonical domain:** https://bespokestudio.co.in

## Build

```bash
python3 build.py     # emits *.html, guides/*.html, assets/js/reviews.js,
                     # sitemap.xml, robots.txt, favicon.svg, _headers
```

`build.py` is the single source of truth — business NAP, CTAs, copy, and page
templates all live there. Edit `build.py`, never the generated `*.html`.

## Live Google reviews

The reviews page shows **live** Google rating + review text via the Google Maps
JavaScript `Place` class (first-party, client-side). It is **off by default** and
degrades to an honest "Read our reviews on Google" link. To enable, set two env
vars at build time:

```bash
GMAPS_KEY=<referrer-restricted browser key> \
BSPK_PLACE_ID=<ChIJ… place id> \
python3 build.py
```

- **`BSPK_PLACE_ID`** — resolve once via Google's
  [Place ID Finder](https://developers.google.com/maps/documentation/places/web-service/place-id).
  Safe to store indefinitely (only field exempt from Google's no-cache rule).
- **`GMAPS_KEY`** — Google Maps Platform key with **billing enabled**, restricted to
  *Websites (HTTP referrer)* = `bespokestudio.co.in/*` (+ pages.dev while previewing)
  and to the **Maps JavaScript API** + **Places API (New)** only. Cost is ~₹0 at a
  single shop's traffic (1,000 free review-calls/month; the loader fires once per
  reviews-page view and on that page only).

Review content is **never** baked into the HTML (Places caching policy); it is
fetched live in the browser. Nothing is ever fabricated — no key ⇒ static link.

If you edit `assets/js/reviews.js` (the `REVIEWS_JS` constant in `build.py`), bump
the `?v=` cache-buster in `head()` — `/assets/*` is served immutable for a year.

## Deploy (Cloudflare Pages, direct upload)

Deploy a **clean** directory (static output only — never the repo root, so `.git`
and `build.py` don't go public):

```bash
python3 build.py
mkdir -p dist && cp *.html robots.txt sitemap.xml _headers dist/ && cp -R assets guides dist/
wrangler pages deploy dist --project-name=bespokestudio --branch=main
```

## Pending owner actions

- Point **bespokestudio.co.in** DNS at the Pages project (Cloudflare → Pages →
  Custom domains), then keep only that domain on the key's referrer allowlist.
- Provide `GMAPS_KEY` + `BSPK_PLACE_ID` to switch on live reviews.
- Confirm the contact email — currently `support@bespokestudio.in`; likely should
  match the `.co.in` domain.

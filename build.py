#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BespokeStudio — static site generator.
Design: "the tailor's spec sheet" — quiet-luxury sans + monospace docket voice.

Run:  python3 build.py
Emits: *.html, guides/*.html, sitemap.xml, robots.txt, assets/img/favicon.svg
No third-party dependencies. Plain HTML/CSS/JS output (fast static, per PRD s18).
"""

import os
import html
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# CONFIG  — single source of truth for NAP + CTAs.
# Anything marked REPLACE must be confirmed before publication.
# ============================================================
SITE_ORIGIN = "https://bespokestudio.in"   # REPLACE if final domain differs

BIZ = {
    "name": "BespokeStudio",
    "legal_note": "BespokeStudio · Reid & Taylor, Basaveshwaranagar",  # brand-architecture line (PRD s3)
    "street": "568, Chord Rd, 3rd Stage, Basaveshwar Nagar",
    "locality": "Bengaluru",
    "region": "Karnataka",
    "postcode": "560079",
    "country": "IN",
    "landmark": "Near Basaveshwaranagar Post Office",
    "phone_display": "080 4989 1288",
    "phone_tel": "+918049891288",
    "wa_number": "919900259407",
    "wa_display": "+91 99002 59407",
    "email": "support@bespokestudio.in",
    "hours_line": "Mon–Sat 11:00–21:00 · Sun 11:00–19:00",
    "lat": 12.9942605,
    "lng": 77.5392937,
}

ADDR_ONELINE = "568, Chord Rd, 3rd Stage, Basaveshwar Nagar, Bengaluru, Karnataka 560079"
MAPS_QUERY = quote("BespokeStudio, " + ADDR_ONELINE)
DIRECTIONS_URL = "https://www.google.com/maps/dir/?api=1&destination=" + MAPS_QUERY
MAP_EMBED_URL = "https://www.google.com/maps?q=" + MAPS_QUERY + "&output=embed"

# --- Google reviews (REAL). GBP already carries reviews + ratings. ---
# Paste the live values below; leave blank to render the "read on Google" state.
# Do NOT invent a rating or reviews — that violates PRD s20 (Compliance).
GOOGLE = {
    "profile_url": "https://www.google.com/maps/search/?api=1&query=" + MAPS_QUERY,  # REPLACE with exact listing URL
    "write_url": "",          # REPLACE with GBP "write a review" short link
    "rating": "",             # e.g. "4.9"  — paste from live Google Business Profile
    "review_count": "",       # e.g. "180"  — paste from live Google Business Profile
}
# Verified reviews to display. Paste 6+ real reviews (with permission), each:
#   {"quote": "...", "author": "First name / initial", "garment": "Custom suit · 2026"}
REVIEWS = []  # empty -> section renders review-ready slots + a link to Google

# GA4 measurement id — leave blank to ship without loading gtag (events still buffer).
GA4_ID = ""   # e.g. "G-XXXXXXXXXX"

def wa(msg):
    return "https://wa.me/" + BIZ["wa_number"] + "?text=" + quote(msg)

WA_DEFAULT = wa("Hello BespokeStudio, I would like to enquire about a custom suit / bespoke outfit.")
TEL = "tel:" + BIZ["phone_tel"]
MAILTO = "mailto:" + BIZ["email"]

# ============================================================
# ICONS  (inline SVG — zero requests)
# ============================================================
ICONS = {
    "wa": '<svg class="btn__ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.15-1.77-.87-2.04-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51l-.57-.01c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35z"/><path d="M20.5 3.4A11.9 11.9 0 0012 0C5.4 0 .1 5.3.1 11.9c0 2.1.5 4.1 1.6 5.9L0 24l6.4-1.7c1.7.9 3.6 1.4 5.6 1.4h.01C18.6 23.7 24 18.4 24 11.8c0-3.2-1.2-6.2-3.5-8.4zM12 21.5h-.01a9.6 9.6 0 01-4.9-1.34l-.35-.2-3.7.97.99-3.6-.23-.37A9.55 9.55 0 012 11.9C2 6.4 6.5 1.9 12 1.9c2.6 0 5 1 6.8 2.8a9.5 9.5 0 012.8 6.7c0 5.5-4.5 10-9.6 10z"/></svg>',
    "phone": '<svg class="btn__ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.4 3.5c.4 0 .78.28.9.66l.92 3.05a1 1 0 01-.26 1.02L6.7 9.55a13 13 0 006.6 6.6l1.32-1.26a1 1 0 011.02-.26l3.05.92c.38.12.66.5.66.9v3.05a1.5 1.5 0 01-1.62 1.5A16.5 16.5 0 013.6 5.12 1.5 1.5 0 015.1 3.5z"/></svg>',
    "pin": '<svg class="btn__ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s6.5-5.8 6.5-11a6.5 6.5 0 10-13 0C5.5 15.2 12 21 12 21z"/><circle cx="12" cy="10" r="2.4"/></svg>',
    "mail": '<svg class="btn__ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M4 6.8l8 5.5 8-5.5"/></svg>',
    "arrow": '<svg class="btn__ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h15M13.5 6l6 6-6 6"/></svg>',
}

def icon(name):
    return ICONS[name]

# ============================================================
# NAV
# ============================================================
NAV = [
    ("index.html", "Home"),
    ("bespoke-tailoring.html", "Bespoke Tailoring"),
    ("fabrics.html", "Fabrics"),
    ("craftsmanship.html", "Craftsmanship"),
    ("gallery.html", "Gallery"),
    ("reviews.html", "Reviews"),
    ("about.html", "About"),
    ("contact.html", "Visit"),
]

# ============================================================
# COMPONENTS
# ============================================================
def plate(code, label, note, variant="dark", ratio=None, glyph="BS", cls=""):
    """Art-directed photography placeholder — signals the exact shot to capture."""
    # normalise any pre-escaped entities (labels may contain "&amp;") so
    # html.escape() below doesn't double-escape into a literal "&amp;amp;"
    code, label, note = html.unescape(code), html.unescape(label), html.unescape(note)
    style = ' style="--ratio:%s"' % ratio if ratio else ""
    vcls = " plate--chalk" if variant == "chalk" else ""
    aria = "Photography plate — reserved for: %s" % label
    return (
        '<figure class="plate%s %s"%s role="img" aria-label="%s">'
        '<span class="plate__mono">%s</span>'
        '<span class="plate__glyph">%s</span>'
        '<figcaption class="plate__cap">'
        '<span class="plate__label">%s</span>'
        '<span class="plate__note">%s</span>'
        '</figcaption></figure>'
    ) % (vcls, cls, style, html.escape(aria), html.escape(code), glyph,
         html.escape(label), html.escape(note))

def cta_row(wa_msg, on_ink=False, directions=True, call=True, compact=False):
    ghost = "btn--onink" if on_ink else "btn--ghost"
    sm = " btn--sm" if compact else ""
    out = ['<div class="cta-row">']
    out.append('<a class="btn btn--wa%s" href="%s" data-evt="whatsapp_click" data-p-position="section" target="_blank" rel="noopener">%s WhatsApp us</a>'
               % (sm, wa(wa_msg), icon("wa")))
    if call:
        out.append('<a class="btn %s%s" href="%s" data-evt="call_click" data-p-position="section">%s Call %s</a>'
                   % (ghost, sm, TEL, icon("phone"), BIZ["phone_display"]))
    if directions:
        out.append('<a class="btn %s%s" href="%s" data-evt="direction_click" data-p-position="section" target="_blank" rel="noopener">%s Directions</a>'
                   % (ghost, sm, DIRECTIONS_URL, icon("pin")))
    out.append('</div>')
    return "".join(out)

def cta_band():
    return """
<section class="section section--ink weave">
  <div class="wrap">
    <div class="split">
      <div class="split__body reveal">
        <span class="eyebrow eyebrow--onink">Book a consultation</span>
        <h2 class="section-title">A measured conversation, before a single stitch.</h2>
        <p class="lede">Tell us the occasion and the finish you have in mind. We will guide you on fabric, fit, and the delivery window — most garments are ready in one to two weeks, with express work on request.</p>
        %s
      </div>
      <div class="split__media reveal">
        %s
      </div>
    </div>
  </div>
</section>""" % (
        cta_row("Hello BespokeStudio, I would like to book a wardrobe consultation.", on_ink=True),
        plate("PL · 09", "Consultation table — fabric bunch & measure card", "Reserved for showroom photography", variant="dark", ratio="16 / 10"),
    )

def reviews_block(context="home"):
    """Renders verified-Google reviews. Uses real config; never fabricates."""
    prof = GOOGLE["profile_url"]
    # header badge
    if GOOGLE["rating"] and GOOGLE["review_count"]:
        badge = ('<div class="review__tag">Verified on Google</div>'
                 '<div class="trust__n" style="margin-top:.6rem">%s <span style="color:var(--brass)">&#9733;</span></div>'
                 '<div class="trust__k">%s Google reviews</div>' % (html.escape(GOOGLE["rating"]), html.escape(GOOGLE["review_count"])))
    else:
        badge = ('<div class="review__tag">Verified on Google</div>'
                 '<p class="mt-1" style="max-width:32rem">Our customers rate us on Google. Read what they say about the fit, the fabric, and the finish — straight from the source.</p>')

    read_btn = '<a class="btn btn--brass mt-2" href="%s" data-evt="direction_click" data-p-section="reviews" target="_blank" rel="noopener">%s Read our reviews on Google</a>' % (prof, icon("arrow"))

    # cards
    if REVIEWS:
        cards = []
        for r in REVIEWS[:6]:
            cards.append(
                '<figure class="review reveal"><div class="review__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
                '<blockquote class="review__q">%s</blockquote>'
                '<figcaption class="review__meta">%s &middot; %s</figcaption></figure>'
                % (html.escape(r["quote"]), html.escape(r.get("author", "Google reviewer")), html.escape(r.get("garment", "Verified Google review")))
            )
        cards_html = '<div class="reviews">%s</div>' % "".join(cards)
        note = ""
    else:
        slots = []
        slot_labels = ["Custom suit · executive wardrobe", "Wedding sherwani · groom",
                       "Custom shirts · office", "Women's formal · blazer",
                       "Premium fabric · Reid & Taylor", "Alteration & refit"]
        for i, lab in enumerate(slot_labels, 1):
            slots.append(
                '<figure class="review reveal"><div class="review__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
                '<blockquote class="review__q" style="color:var(--ink-38)">Verified Google review — to be placed here.</blockquote>'
                '<figcaption class="review__meta">Slot %02d &middot; %s</figcaption></figure>' % (i, html.escape(lab))
            )
        cards_html = '<div class="reviews">%s</div>' % "".join(slots)
        note = ('<div class="notice"><strong>Build note.</strong> The Google Business Profile already carries reviews and ratings. '
                'Paste 6+ real reviews (with the customer&rsquo;s permission) into <code>REVIEWS</code> in build.py, and the live rating + count into '
                '<code>GOOGLE</code>. Until then, the section links out to the live Google profile — no reviews are invented.</div>')

    return """
<section class="section section--deep" id="reviews">
  <div class="wrap">
    <div class="split" style="align-items:flex-start;margin-bottom:1rem">
      <div class="split__body reveal">
        <span class="eyebrow">What customers say</span>
        <h2 class="section-title">Rated by the people who wear the work.</h2>
        %s
        %s
      </div>
      <div class="split__media reveal" style="align-self:center">%s</div>
    </div>
    %s
    %s
  </div>
</section>""" % (badge, read_btn,
                 plate("PL · 11", "Fitting room — mirror & finished suit", "Reserved for showroom photography", variant="dark", ratio="4 / 5"),
                 cards_html, note)

def trust_bar():
    cells = [
        ("20+", "Years shaping wardrobes"),
        ("20+", "Master tailors in-house"),
        ("Reid &amp; Taylor", "Premium suiting fabrics"),
        ("1&ndash;2 wks", "Typical delivery &middot; express on request"),
    ]
    inner = "".join(
        '<div class="trust__cell"><div class="trust__n">%s</div><div class="trust__k">%s</div></div>' % (n, k)
        for n, k in cells
    )
    # 5th cell — Google reviews (real). Shows rating if configured, else links out.
    if GOOGLE["rating"]:
        g = '<div class="trust__cell"><a href="%s" data-evt="direction_click" data-p-section="trust" target="_blank" rel="noopener" style="display:block"><div class="trust__n">%s <span style="color:var(--brass)">&#9733;</span></div><div class="trust__k">On Google &middot; read reviews</div></a></div>' % (GOOGLE["profile_url"], html.escape(GOOGLE["rating"]))
    else:
        g = '<div class="trust__cell"><a href="%s" data-evt="direction_click" data-p-section="trust" target="_blank" rel="noopener" style="display:block"><div class="trust__n">Google</div><div class="trust__k">Read our verified reviews &rarr;</div></a></div>' % GOOGLE["profile_url"]
    return '<section class="trust"><div class="trust__grid">%s%s</div></section>' % (inner, g)

# ============================================================
# JSON-LD  (LocalBusiness / ClothingStore — Appendix A, extended)
# ============================================================
def json_ld(page_url):
    agg = ""
    if GOOGLE["rating"] and GOOGLE["review_count"]:
        agg = ',\n  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "%s", "reviewCount": "%s"}' % (
            GOOGLE["rating"], GOOGLE["review_count"])
    return """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ClothingStore",
  "@id": "%(origin)s/#business",
  "name": "BespokeStudio",
  "description": "Premium bespoke tailoring and Reid & Taylor fabric showroom in Basaveshwaranagar, Bengaluru.",
  "url": "%(origin)s/",
  "telephone": "+91-80-4989-1288",
  "email": "support@bespokestudio.in",
  "priceRange": "$$$",
  "image": "%(origin)s/assets/img/og-cover.png",
  "address": {"@type": "PostalAddress", "streetAddress": "568, Chord Rd, 3rd Stage, Basaveshwar Nagar", "addressLocality": "Bengaluru", "addressRegion": "Karnataka", "postalCode": "560079", "addressCountry": "IN"},
  "geo": {"@type": "GeoCoordinates", "latitude": %(lat)s, "longitude": %(lng)s},
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "11:00", "closes": "21:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "11:00", "closes": "19:00"}
  ],
  "areaServed": ["Basaveshwaranagar","Rajajinagar","Vijayanagar","Malleshwaram","Bengaluru"],
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Bespoke tailoring and premium fabrics", "itemListElement": [
    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Men's bespoke suits"}},
    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Custom shirts and trousers"}},
    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Sherwani and ethnic wear tailoring"}},
    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Women's formal bespoke clothing"}},
    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Premium fabric consultation"}}
  ]}%(agg)s
}
</script>""" % {"origin": SITE_ORIGIN, "lat": BIZ["lat"], "lng": BIZ["lng"], "agg": agg}

# ============================================================
# PAGE SHELL
# ============================================================
def head(title, desc, canonical, depth=0):
    base = "../" * depth
    ga = ""
    if GA4_ID:
        ga = ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>'
              '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
              'gtag("js",new Date());gtag("config","%s");</script>') % (GA4_ID, GA4_ID)
    else:
        ga = "<!-- GA4: set GA4_ID in build.py to enable. Events buffer to dataLayer until then. -->"
    og_img = SITE_ORIGIN + "/assets/img/og-cover.png"
    return """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js')</script>
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canonical)s">
<meta name="theme-color" content="#17150F">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="business.business">
<meta property="og:site_name" content="BespokeStudio">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(og_img)s">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="%(base)sassets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="%(base)sassets/img/favicon.svg">
<link rel="preconnect" href="https://www.google.com">
<link rel="stylesheet" href="%(base)sassets/css/site.css">
%(jsonld)s
%(ga)s""" % {
        "title": html.escape(title), "desc": html.escape(desc), "canonical": canonical,
        "og_img": og_img, "base": base, "jsonld": json_ld(canonical), "ga": ga,
    }

def header(active, depth=0):
    base = "../" * depth
    links = "".join(
        '<a href="%s%s"%s>%s</a>' % (base, href, ' aria-current="page"' if href == active else "", label)
        for href, label in NAV
    )
    drawer_links = "".join(
        '<a href="%s%s"%s>%s</a>' % (base, href, ' aria-current="page"' if href == active else "", label)
        for href, label in NAV
    )
    return """
<div class="spine" aria-hidden="true"><span class="spine__thread"></span><span class="spine__label">Est. Basaveshwaranagar</span></div>

<div class="util">
  <div class="wrap"><div class="util__row">
    <div class="util__hours"><span class="util__dot"></span><span>%(hours)s</span><span class="hide-s">&middot; %(landmark)s</span></div>
    <div><a href="%(tel)s" data-evt="call_click" data-p-position="utilbar">%(phone)s</a></div>
  </div></div>
</div>

<header class="site-header">
  <div class="wrap"><div class="header__row">
    <a class="brand" href="%(base)sindex.html" aria-label="BespokeStudio home">
      <span class="brand__mark">BespokeStudio</span>
      <span class="brand__place">Basaveshwaranagar &middot; Bengaluru</span>
    </a>
    <nav class="nav" aria-label="Primary">%(links)s</nav>
    <div class="header__cta">
      <a class="btn btn--ghost btn--sm" href="%(tel)s" data-evt="call_click" data-p-position="header">%(phone_ic)s Call</a>
      <a class="btn btn--wa btn--sm" href="%(wa)s" data-evt="whatsapp_click" data-p-position="header" target="_blank" rel="noopener">%(wa_ic)s WhatsApp</a>
      <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span></span></button>
    </div>
  </div></div>
</header>

<div class="scrim" aria-hidden="true"></div>
<aside class="drawer" id="drawer" aria-label="Menu">
  <button class="drawer__close" aria-label="Close menu">Close &times;</button>
  <span class="eyebrow eyebrow--onink">BespokeStudio</span>
  %(drawer_links)s
  <div class="drawer__cta">
    <a class="btn btn--wa btn--block" href="%(wa)s" data-evt="whatsapp_click" data-p-position="drawer" target="_blank" rel="noopener">%(wa_ic)s WhatsApp us</a>
    <a class="btn btn--onink btn--block" href="%(tel)s" data-evt="call_click" data-p-position="drawer">%(phone_ic)s Call %(phone)s</a>
  </div>
</aside>""" % {
        "hours": BIZ["hours_line"], "landmark": BIZ["landmark"], "tel": TEL, "phone": BIZ["phone_display"],
        "base": base, "links": links, "drawer_links": drawer_links, "wa": WA_DEFAULT,
        "phone_ic": icon("phone"), "wa_ic": icon("wa"),
    }

def mobile_dock():
    return """
<nav class="dock" aria-label="Quick contact">
  <a class="dock--wa" href="%(wa)s" data-evt="whatsapp_click" data-p-position="dock" target="_blank" rel="noopener">%(wa)s_ic WhatsApp</a>
</nav>""".replace("%(wa)s_ic", icon("wa")).replace("%(wa)s", WA_DEFAULT)  # placeholder, replaced below

def dock():
    return """
<nav class="dock" aria-label="Quick contact">
  <a class="dock--wa" href="%(wa)s" data-evt="whatsapp_click" data-p-position="dock" target="_blank" rel="noopener">%(wa_ic)s WhatsApp</a>
  <a href="%(tel)s" data-evt="call_click" data-p-position="dock">%(phone_ic)s Call</a>
  <a href="%(dir)s" data-evt="direction_click" data-p-position="dock" target="_blank" rel="noopener">%(pin_ic)s Directions</a>
</nav>""" % {"wa": WA_DEFAULT, "tel": TEL, "dir": DIRECTIONS_URL,
            "wa_ic": icon("wa"), "phone_ic": icon("phone"), "pin_ic": icon("pin")}

def footer(depth=0):
    base = "../" * depth
    col_explore = "".join('<li><a href="%s%s">%s</a></li>' % (base, h, l) for h, l in NAV[1:6])
    col_more = "".join('<li><a href="%s%s">%s</a></li>' % (base, h, l) for h, l in [
        ("about.html", "About the atelier"), ("contact.html", "Visit &amp; directions"),
        ("guides.html", "Guides &amp; journal"), ("reviews.html", "Google reviews"),
    ])
    return """
<footer class="site-footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <span class="brand__mark">BespokeStudio</span>
        <span class="brand__place">Basaveshwaranagar &middot; Bengaluru</span>
        <p>A private atelier for bespoke tailoring and premium fabrics — custom suits, shirts, sherwani and ethnic wear, women&rsquo;s formal clothing, and Reid &amp; Taylor suiting.</p>
        <div class="cta-row mt-2">
          <a class="btn btn--onink btn--sm" href="%(wa)s" data-evt="whatsapp_click" data-p-position="footer" target="_blank" rel="noopener">%(wa_ic)s WhatsApp us</a>
        </div>
      </div>
      <div class="footer__col"><h4>Explore</h4><ul>%(explore)s</ul></div>
      <div class="footer__col"><h4>Atelier</h4><ul>%(more)s</ul></div>
      <div class="footer__col">
        <h4>Visit</h4>
        <address class="footer__data" style="font-style:normal">
          568, Chord Rd, 3rd Stage<br>Basaveshwar Nagar<br>Bengaluru, Karnataka 560079<br>
          <span style="color:var(--chalk-46)">%(landmark)s</span><br><br>
          <a href="%(tel)s" data-evt="call_click" data-p-position="footer">%(phone)s</a><br>
          <a href="%(mail)s" data-evt="email_click" data-p-position="footer">%(email)s</a><br><br>
          %(hours)s
        </address>
      </div>
    </div>
    <p class="footer__note">%(legal)s. Reid &amp; Taylor is referenced as a premium fabric house; fabric availability is confirmed at the showroom. Indicative delivery is one to two weeks with express work on request. Pricing depends on fabric, garment type, finish, and timeline — please WhatsApp us for a consultation.</p>
    <div class="footer__bar">
      <span>&copy; <span data-year>2026</span> BespokeStudio &middot; Basaveshwaranagar</span>
      <span><a href="%(dir)s" data-evt="direction_click" data-p-position="footer" target="_blank" rel="noopener">Get directions</a> &middot; <a href="%(profile)s" target="_blank" rel="noopener">Google profile</a></span>
    </div>
  </div>
</footer>
<script src="%(base)sassets/js/site.js" defer></script>""" % {
        "wa": WA_DEFAULT, "wa_ic": icon("wa"), "explore": col_explore, "more": col_more,
        "landmark": BIZ["landmark"], "tel": TEL, "phone": BIZ["phone_display"], "mail": MAILTO,
        "email": BIZ["email"], "hours": BIZ["hours_line"], "legal": BIZ["legal_note"],
        "dir": DIRECTIONS_URL, "profile": GOOGLE["profile_url"], "base": base,
    }

def page(slug, title, desc, body, active, depth=0, service=None):
    canonical = SITE_ORIGIN + "/" + slug
    page_id = slug.replace("/", "-").replace(".html", "") or "home"
    svc_attr = ' data-service="%s"' % html.escape(service) if service else ""
    doc = """<!doctype html>
<html lang="en">
<head>
%(head)s
</head>
<body data-page="%(pid)s"%(svc)s>
%(header)s
<main id="main">
%(body)s
</main>
%(footer)s
%(dock)s
</body>
</html>""" % {
        "head": head(title, desc, canonical, depth), "pid": page_id, "svc": svc_attr,
        "header": header(active, depth), "body": body, "footer": footer(depth), "dock": dock(),
    }
    return doc

# ============================================================
# SHARED SNIPPETS
# ============================================================
def phero(crumb, h1, sub, depth=0):
    base = "../" * depth
    return """
<section class="phero">
  <div class="wrap">
    <nav class="phero__crumb" aria-label="Breadcrumb"><a href="%(base)sindex.html">Home</a> &nbsp;/&nbsp; %(crumb)s</nav>
    <h1 class="reveal">%(h1)s</h1>
    <p class="lede reveal">%(sub)s</p>
  </div>
</section>""" % {"base": base, "crumb": crumb, "h1": h1, "sub": sub}

# ============================================================
# HOME
# ============================================================
def build_home():
    hero = """
<section class="section hero">
  <div class="wrap">
    <div class="hero__grid">
      <div class="hero__body reveal">
        <div class="hero__doc"><span>Doc &middot; Atelier</span><span>Basaveshwaranagar</span><span>Est. 20+ yrs</span></div>
        <h1 class="display">Bespoke tailoring and<br>premium fabrics in<br>Basaveshwaranagar</h1>
        <p class="hero__sub lede">BespokeStudio creates custom clothing for executives, wedding families, and discerning customers who value fabric, fit, and workmanship. Visit our Basaveshwaranagar showroom for Reid &amp; Taylor fabrics, refined tailoring, and a measured wardrobe consultation.</p>
        %(cta)s
      </div>
      <div class="hero__plate reveal">%(plate)s</div>
    </div>
  </div>
</section>""" % {
        "cta": cta_row("Hello BespokeStudio, I would like to enquire about a custom suit / bespoke outfit."),
        "plate": plate("PL · 01", "Storefront &amp; signage — Chord Road", "Reserved for exterior photography", variant="dark", ratio="4 / 5", cls="plate--fill"),
    }

    # Services — dockets (signature element)
    dockets = [
        ("MS", "Men's Bespoke Suits", "Structured two- and three-piece suits cut to your measurements, for boardrooms, court, and occasion.",
         [("Fit", "Made to measure"), ("Fabric", "Worsted &amp; blends"), ("Ready", "1&ndash;2 weeks")], "bespoke-tailoring.html#suits"),
        ("CS", "Custom Shirts &amp; Trousers", "Office and everyday separates with collar, cuff, and trouser options set to your preference.",
         [("Fit", "Your block"), ("Fabric", "Cotton, linen"), ("Ready", "1&ndash;2 weeks")], "bespoke-tailoring.html#shirts"),
        ("SE", "Sherwani &amp; Ethnic Wear", "Wedding, reception, and festive outfits — sherwani, bandh gala, and coordinated family looks.",
         [("Occasion", "Wedding &amp; festive"), ("Service", "Family fittings"), ("Express", "On request")], "bespoke-tailoring.html#ethnic"),
        ("WF", "Women's Formal Clothing", "Elegant blazers, trousers, and formal sets tailored for fit and a premium hand.",
         [("Fit", "Made to measure"), ("Fabric", "Premium suiting"), ("Ready", "1&ndash;2 weeks")], "bespoke-tailoring.html#women"),
        ("PF", "Premium Fabrics", "Reid &amp; Taylor suiting and a curated wall of wool, cotton, silk, linen, and refined blends.",
         [("House", "Reid &amp; Taylor"), ("Range", "Wool&middot;silk&middot;linen"), ("Guidance", "In-showroom")], "fabrics.html"),
        ("AL", "Alterations &amp; Refitting", "Careful re-cutting and refitting to bring existing garments back to a sharp line.",
         [("Scope", "Refit &amp; repair"), ("Turnaround", "By assessment"), ("Priority", "On request")], "bespoke-tailoring.html#alterations"),
    ]
    dk = []
    for i, (ref, name, blurb, spec, link) in enumerate(dockets, 1):
        specs = "".join('<li><span>%s</span><span>%s</span></li>' % (k, v) for k, v in spec)
        dk.append("""
      <a class="docket reveal" href="%(link)s">
        <div class="docket__top"><span class="docket__ref">%(ref)s &middot; No.%(idx)02d</span><span class="docket__idx">Atelier</span></div>
        <h3>%(name)s</h3>
        <p>%(blurb)s</p>
        <ul class="docket__spec">%(specs)s</ul>
        <div class="docket__foot"><span class="tlink">View service %(arrow)s</span></div>
        <span class="docket__draw"></span>
      </a>""" % {"link": link, "ref": ref, "idx": i, "name": name, "blurb": blurb, "specs": specs, "arrow": icon("arrow")})
    services = """
<section class="section section--paper">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">The offering</span>
      <h2 class="section-title">Six ways we dress you — each cut, not bought.</h2>
      <p>From an executive suit to a wedding sherwani, every commission begins the same way: a conversation about occasion, fabric, and fit. Choose where to start.</p>
    </div>
    <div class="dockets">%(dk)s</div>
  </div>
</section>""" % {"dk": "".join(dk)}

    # Fabric story (dark split)
    chips = "".join('<span class="chip">%s</span>' % c for c in
                    ["Reid &amp; Taylor", "Worsted wool", "Cotton", "Linen", "Silk", "Refined blends"])
    fabric = """
<section class="section section--char weave">
  <div class="wrap">
    <div class="split split--flip">
      <div class="split__media reveal">%(plate)s</div>
      <div class="split__body reveal">
        <span class="eyebrow eyebrow--onink">Fabric as proof</span>
        <h2 class="section-title">The cloth decides how a garment falls.</h2>
        <p class="lede">A suit is only as good as the length it is cut from. Our fabric wall is built around Reid &amp; Taylor suiting and a considered range of wool, cotton, silk, linen, and refined blends — chosen for drape, season, and how they hold a press.</p>
        <p>Come in and handle the cloth. We will talk you through weight, weave, and which fabric suits the occasion and the Bengaluru climate.</p>
        <div class="chips">%(chips)s</div>
        <div class="cta-row mt-3"><a class="tlink tlink--onink" href="fabrics.html">Explore the fabric showroom %(arrow)s</a></div>
      </div>
    </div>
  </div>
</section>""" % {"plate": plate("PL · 04", "Fabric wall — Reid &amp; Taylor suiting", "Reserved for showroom photography", variant="dark", ratio="4 / 3"),
                 "chips": chips, "arrow": icon("arrow")}

    # Process (dark, numbered — a genuine sequence)
    steps = [
        ("Consultation", "We discuss the occasion, your wardrobe, and the look you want — measured advice, no pressure."),
        ("Fabric selection", "Choose from Reid &amp; Taylor suiting and our fabric wall, guided by drape, season, and use."),
        ("Measurement", "Precise measurements taken to build your pattern and hold a clean line through the body."),
        ("Fitting &amp; trial", "A trial fitting to check balance, posture, and comfort — adjusted until it sits right."),
        ("Finishing &amp; delivery", "Careful pressing and finishing, then delivery — usually one to two weeks; express on request."),
    ]
    st = "".join(
        '<div class="step reveal"><div class="step__n">Step %02d</div><h3>%s</h3><p>%s</p></div>' % (i, n, d)
        for i, (n, d) in enumerate(steps, 1)
    )
    process = """
<section class="section section--ink">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow eyebrow--onink">How a commission works</span>
      <h2 class="section-title">Five honest steps, from first word to final press.</h2>
      <p>No mystery, no overpromising. This is exactly how your garment comes together.</p>
    </div>
    <div class="process">%(st)s</div>
  </div>
</section>""" % {"st": st}

    # Gallery preview
    gp = [
        plate("G · 01", "Storefront &amp; signage", "Exterior", "dark", "4 / 3", cls="g-span-2 plate--fill"),
        plate("G · 02", "Fabric wall detail", "Showroom", "chalk", "1 / 1"),
        plate("G · 03", "Finished suit on stand", "Garment", "dark", "1 / 1"),
        plate("G · 04", "Sherwani, close-up", "Ethnic", "dark", "1 / 1"),
        plate("G · 05", "Measuring in progress", "Craft", "chalk", "1 / 1"),
        plate("G · 06", "Shirt collar &amp; cuff", "Garment", "dark", "1 / 1"),
        plate("G · 07", "Consultation table", "Showroom", "chalk", "4 / 3", cls="g-span-2 plate--fill"),
    ]
    gallery = """
<section class="section section--deep">
  <div class="wrap">
    <div class="sec-head reveal" style="display:flex;justify-content:space-between;align-items:flex-end;max-width:none;gap:1rem;flex-wrap:wrap">
      <div style="max-width:40rem"><span class="eyebrow">The showroom</span><h2 class="section-title">Proof, not promises.</h2><p>Real fabric, real garments, real workmanship. A preview of the showroom and finished pieces.</p></div>
      <a class="tlink" href="gallery.html">See the full gallery %(arrow)s</a>
    </div>
    <div class="gallery gallery--home mt-3">%(gp)s</div>
  </div>
</section>""" % {"gp": "".join(gp), "arrow": icon("arrow")}

    # Location block
    location = location_section(depth=0)

    body = hero + trust_bar() + services + fabric + process + gallery + reviews_block("home") + location + cta_band()
    return page("index.html",
                "BespokeStudio — Bespoke Tailoring & Premium Fabrics in Basaveshwaranagar, Bengaluru",
                "Premium bespoke tailoring and Reid & Taylor fabric showroom in Basaveshwaranagar, Bengaluru. Custom suits, shirts, sherwani, women's formal wear. WhatsApp for a consultation.",
                body, "index.html", depth=0)

def location_section(depth=0):
    return """
<section class="section section--paper" id="visit">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Find us</span><h2 class="section-title">Basaveshwaranagar showroom.</h2></div>
    <div class="contact-grid mt-3">
      <div class="nap reveal">
        <div class="nap__row"><div class="nap__k">Address</div><div class="nap__v">568, Chord Rd, 3rd Stage,<br>Basaveshwar Nagar, Bengaluru,<br>Karnataka 560079<br><span style="color:var(--ink-52)">%(landmark)s</span></div></div>
        <div class="nap__row"><div class="nap__k">Hours</div><div class="nap__v"><span class="data">Mon&ndash;Sat &nbsp;11:00&ndash;21:00</span><br><span class="data">Sun &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;11:00&ndash;19:00</span></div></div>
        <div class="nap__row"><div class="nap__k">WhatsApp</div><div class="nap__v"><a href="%(wa)s" data-evt="whatsapp_click" data-p-position="location" target="_blank" rel="noopener" class="data">%(wa_disp)s</a></div></div>
        <div class="nap__row"><div class="nap__k">Call</div><div class="nap__v"><a href="%(tel)s" data-evt="call_click" data-p-position="location" class="data">%(phone)s</a></div></div>
        <div class="nap__row" style="border-bottom:0"><div class="nap__k">Email</div><div class="nap__v"><a href="%(mail)s" data-evt="email_click" data-p-position="location" class="data">%(email)s</a></div></div>
        <div class="cta-row">%(dirbtn)s</div>
      </div>
      <div class="map-embed reveal" data-map="%(mapembed)s" aria-label="Map showing BespokeStudio in Basaveshwaranagar"></div>
    </div>
  </div>
</section>""" % {
        "landmark": BIZ["landmark"], "wa": WA_DEFAULT, "wa_disp": BIZ["wa_display"], "tel": TEL,
        "phone": BIZ["phone_display"], "mail": MAILTO, "email": BIZ["email"],
        "dirbtn": '<a class="btn btn--brass" href="%s" data-evt="direction_click" data-p-section="location" target="_blank" rel="noopener">%s Get directions</a>' % (DIRECTIONS_URL, icon("pin")),
        "mapembed": MAP_EMBED_URL,
    }

# ============================================================
# BESPOKE TAILORING (services)
# ============================================================
def build_services():
    sub = "Custom clothing, cut to your measurements — men's suits, shirts and trousers, sherwani and ethnic wear, women's formal clothing, premium fabrics, and refitting. Every commission starts with a conversation."
    body = [phero('Bespoke Tailoring', "Bespoke tailoring in Basaveshwaranagar", sub)]

    services = [
        ("suits", "Men's Bespoke Suits", "custom suit tailor Basaveshwaranagar",
         "A structured suit is the sharpest thing in a wardrobe. We cut two- and three-piece suits to your measurements for the boardroom, the courtroom, weddings, and occasions — guided by fabric, posture, and the line you want through the shoulder and waist.",
         ["Business, wedding, reception, and formal occasions", "Reid &amp; Taylor and premium worsted suiting", "Collar, lapel, and trouser detail to your preference", "Trial fitting before finishing", "Usually 1&ndash;2 weeks; express on request"],
         "PL · 21", "Two-piece suit on stand — full length"),
        ("shirts", "Custom Shirts &amp; Trousers", "custom shirts Basaveshwaranagar; trouser tailoring near me",
         "The workhorses of a wardrobe, made to fit properly. Shirts built to your block with collar and cuff options, and trousers cut to sit clean through the seat and leg — ideal for building an office rotation that actually fits.",
         ["Collar, cuff, and placket options", "Cotton, linen, and blended shirtings", "Trousers cut for seat, rise, and break", "Office wardrobe combinations", "Usually 1&ndash;2 weeks"],
         "PL · 22", "Shirt collar &amp; cuff — close-up"),
        ("ethnic", "Sherwani &amp; Ethnic Wear", "custom sherwani Basaveshwaranagar; wedding tailor Bangalore",
         "Occasion clothing that looks rich without looking loud. Sherwani, bandh gala, and coordinated wedding and reception looks — with unhurried family fittings so the whole party is dressed to one standard.",
         ["Wedding, reception, and festive outfits", "Sherwani, bandh gala, and formal Indian wear", "Family consultations and group fittings", "Fabric and finish guidance for the occasion", "Express delivery available on request"],
         "PL · 23", "Sherwani — detail &amp; drape"),
        ("women", "Women's Formal Clothing", "women's formal tailor Basaveshwaranagar",
         "Formal clothing that fits well and feels premium. Tailored blazers, trousers, and formal sets cut for a clean line and a considered hand — for work, events, and occasions.",
         ["Blazers, trousers, and formal sets where applicable", "Premium suiting and formal fabrics", "Fit consultation for a confident line", "Made to your measurements", "Usually 1&ndash;2 weeks"],
         "PL · 24", "Women's blazer — tailored line"),
        ("alterations", "Alterations &amp; Refitting", "alterations Basaveshwaranagar; suit alteration near me",
         "Sometimes the right move is to refit what you own. We re-cut and refit existing garments — taking in, letting out, reshaping — to bring a good piece back to a sharp line.",
         ["Refit, take-in, and reshaping", "Restoring the line on existing garments", "Assessment before any work", "Priority turnaround on request"],
         "PL · 25", "Chalk marks on a jacket — refit"),
    ]
    for i, (anchor, name, kw, lede, points, code, cap) in enumerate(services):
        flip = " split--flip" if i % 2 else ""
        pts = "".join('<li>%s</li>' % p for p in points)
        variant = "char" if i % 2 == 0 else "paper"
        onink = variant == "char"
        eyebrow_cls = "eyebrow eyebrow--onink" if onink else "eyebrow"
        body.append("""
<section class="section section--%(variant)s%(weave)s" id="%(anchor)s">
  <div class="wrap">
    <div class="split%(flip)s">
      <div class="split__media reveal">%(plate)s</div>
      <div class="split__body reveal">
        <span class="%(eyebrow_cls)s">%(kw)s</span>
        <h2 class="section-title">%(name)s</h2>
        <p class="lede">%(lede)s</p>
        <ul class="flist mt-2">%(pts)s</ul>
        <div class="cta-row mt-3">%(wa)s</div>
      </div>
    </div>
  </div>
</section>""" % {
            "variant": variant, "weave": " weave" if onink else "", "anchor": anchor, "flip": flip,
            "plate": plate(code, cap, "Reserved for photography", "dark" if onink else "chalk", "4 / 3"),
            "eyebrow_cls": eyebrow_cls, "kw": kw, "name": name, "lede": lede, "pts": pts,
            "wa": '<a class="btn %s" href="%s" data-evt="whatsapp_click" data-p-service="%s" data-p-position="service" target="_blank" rel="noopener">%s Enquire on WhatsApp</a>' % (
                "btn--onink" if onink else "btn--wa", wa("Hello BespokeStudio, I would like to enquire about %s." % html.unescape(name.lower())), anchor, icon("wa")),
        })

    # pricing honesty block
    body.append("""
<section class="section section--deep">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">On pricing</span><h2 class="section-title">Priced by the work, not by a list.</h2>
    <p>Every garment is different, so a fixed price list would mislead more than it helps. What you pay depends on the fabric, the garment, the finish, and the delivery timeline. Tell us what you have in mind on WhatsApp and we will give you a clear, honest figure.</p></div>
    <div class="cta-row mt-2">%(wa)s</div>
  </div>
</section>""" % {"wa": cta_row("Hello BespokeStudio, I would like a pricing consultation for a bespoke garment.", on_ink=False)})

    body.append(cta_band())
    return page("bespoke-tailoring.html",
                "Bespoke Tailoring in Basaveshwaranagar — Custom Suits, Shirts, Sherwani | BespokeStudio",
                "Bespoke tailoring in Basaveshwaranagar, Bengaluru: custom men's suits, shirts and trousers, sherwani and ethnic wear, women's formal clothing, and alterations. WhatsApp for a consultation.",
                "".join(body), "bespoke-tailoring.html", depth=0, service="bespoke-tailoring")

# ============================================================
# FABRICS
# ============================================================
def build_fabrics():
    sub = "A fabric wall built around Reid & Taylor suiting and a considered range of wool, cotton, silk, linen, and refined blends — chosen for drape, season, and how they hold a press. Handle the cloth before you commit."
    body = [phero('Fabrics &amp; Materials', "Premium fabrics &amp; the Reid &amp; Taylor showroom", sub)]

    body.append("""
<section class="section section--char weave">
  <div class="wrap">
    <div class="split">
      <div class="split__body reveal">
        <span class="eyebrow eyebrow--onink">The house association</span>
        <h2 class="section-title">Reid &amp; Taylor suiting.</h2>
        <p class="lede">Reid &amp; Taylor is a premium suiting house long associated with worsted wool and a clean, formal finish. It anchors our fabric wall — the cloth we most often reach for when a suit needs to hold its line through a long day.</p>
        <p>We will show you the current lengths in the showroom and talk you through weight, weave, and season. Availability is always confirmed in person.</p>
        <div class="cta-row mt-3"><a class="btn btn--onink" href="%(wa)s" data-evt="whatsapp_click" data-p-service="fabrics" data-p-position="fabrics" target="_blank" rel="noopener">%(wa_ic)s Ask about fabric availability</a></div>
      </div>
      <div class="split__media reveal">%(plate)s</div>
    </div>
  </div>
</section>""" % {"wa": wa("Hello BespokeStudio, I would like to ask about Reid & Taylor fabric availability."),
                 "wa_ic": icon("wa"),
                 "plate": plate("PL · 31", "Reid &amp; Taylor lengths on the wall", "Reserved for showroom photography", "dark", "4 / 3")})

    fabrics = [
        ("Worsted wool", "The backbone of a good suit. Smooth, resilient, and quick to shed creases — ideal for structured suits and formal trousers that keep their shape."),
        ("Cotton", "Breathable and honest. A natural choice for shirts and warm-weather separates in the Bengaluru climate."),
        ("Linen", "Texture and coolness for occasion and summer wear. Relaxes beautifully and reads as considered, not careless."),
        ("Silk &amp; silk blends", "For sherwani, reception wear, and detailing where a subtle sheen lifts the whole garment."),
        ("Refined blends", "Wool-rich blends engineered for drape and travel — a practical middle ground for a working wardrobe."),
        ("Shirtings", "Fine cottons and blends for custom shirts, chosen for hand, weave, and how a collar sits."),
    ]
    cards = "".join(
        '<div class="review reveal" style="gap:.6rem"><div class="review__tag">Cloth</div><h3>%s</h3><p style="font-size:.95rem">%s</p></div>' % (n, d)
        for n, d in fabrics
    )
    body.append("""
<section class="section section--paper">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">The fabric wall</span><h2 class="section-title">Choose the cloth first. The garment follows.</h2>
    <p>A short guide to what lines our wall. In the showroom you can feel the weight and drape of each — the fastest way to know what is right for you.</p></div>
    <div class="reviews mt-3" style="grid-template-columns:repeat(3,1fr)">%(cards)s</div>
  </div>
</section>""" % {"cards": cards})

    # fabric care mini
    body.append("""
<section class="section section--deep">
  <div class="wrap">
    <div class="split">
      <div class="split__media reveal">%(plate)s</div>
      <div class="split__body reveal">
        <span class="eyebrow">Care, briefly</span>
        <h2 class="section-title">Look after good cloth and it looks after you.</h2>
        <ul class="flist mt-2">
          <li>Rest a suit a day between wears so the wool can recover.</li>
          <li>Brush, air, and hang on a shaped hanger — dry-clean sparingly.</li>
          <li>Press, don&rsquo;t crush; steam lifts most creases from worsted.</li>
          <li>Store linen and silk with room to breathe.</li>
        </ul>
        <div class="cta-row mt-3"><a class="tlink" href="craftsmanship.html">See how we finish a garment %(arrow)s</a></div>
      </div>
    </div>
  </div>
</section>""" % {"plate": plate("PL · 32", "Swatches &amp; grain — macro", "Reserved for fabric photography", "chalk", "4 / 3"), "arrow": icon("arrow")})

    body.append(cta_band())
    return page("fabrics.html",
                "Premium Fabrics & Reid & Taylor Showroom in Basaveshwaranagar | BespokeStudio",
                "Premium fabrics in Basaveshwaranagar, Bengaluru — Reid & Taylor suiting plus wool, cotton, silk, linen and refined blends. Fabric consultation at the showroom. WhatsApp to ask about availability.",
                "".join(body), "fabrics.html", depth=0, service="fabrics")

# ============================================================
# CRAFTSMANSHIP
# ============================================================
def build_craft():
    sub = "Quality is a set of small disciplines done consistently — measuring, cutting, stitching, fitting, and finishing. Here is exactly what we do, and what we don't claim."
    body = [phero('Craftsmanship', "Workmanship as discipline", sub)]

    steps = [
        ("Measurement", "We take a full set of measurements and read your posture — the stance, the shoulders, the way you actually stand — so the pattern starts from you, not a size chart."),
        ("Cutting", "The cloth is marked and cut with the grain respected, allowing enough for a clean fit and future adjustment."),
        ("Stitching", "Careful machine construction with attention to seams, balance, and the internal structure that lets a jacket hold its shape."),
        ("Fitting &amp; trial", "A trial fitting on the body to check line and comfort. We mark corrections and refine until it sits right through the shoulder and waist."),
        ("Fit correction", "Adjustments made and re-checked — the unglamorous step that separates a good fit from an almost-right one."),
        ("Finishing", "Pressing, detailing, and a final quality check before the garment leaves the atelier."),
    ]
    cards = "".join(
        '<div class="step reveal" style="background:var(--charcoal)"><div class="step__n">%02d</div><h3>%s</h3><p>%s</p></div>' % (i, n, d)
        for i, (n, d) in enumerate(steps, 1)
    )
    body.append("""
<section class="section section--ink">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow eyebrow--onink">Inside the atelier</span><h2 class="section-title">Six disciplines, done every time.</h2></div>
    <div class="process mt-3" style="grid-template-columns:repeat(3,1fr)">%(cards)s</div>
  </div>
</section>""" % {"cards": cards})

    # honesty block — what we don't claim
    body.append("""
<section class="section section--paper">
  <div class="wrap">
    <div class="split">
      <div class="split__body reveal">
        <span class="eyebrow">Plainly stated</span>
        <h2 class="section-title">What we promise — and what we won&rsquo;t pretend.</h2>
        <p class="lede">We would rather earn trust than inflate it. Our work is disciplined machine tailoring with careful fitting and finishing. We don&rsquo;t dress it up as something it isn&rsquo;t.</p>
        <div class="cols-2 mt-2">
          <div><h4 class="eyebrow" style="margin-bottom:.8rem">We do</h4>
          <ul class="flist"><li>Made-to-measure cutting and fitting</li><li>Trial fittings and fit corrections</li><li>Premium fabric guidance</li><li>Careful pressing and finishing</li></ul></div>
          <div><h4 class="eyebrow" style="margin-bottom:.8rem">We don&rsquo;t claim</h4>
          <ul class="flist"><li>Hand embroidery or hand finishing</li><li>&ldquo;Fastest&rdquo; or &ldquo;cheapest&rdquo; anything</li><li>Guaranteed search rankings</li><li>Credentials we don&rsquo;t hold</li></ul></div>
        </div>
      </div>
      <div class="split__media reveal">%(plate)s</div>
    </div>
  </div>
</section>""" % {"plate": plate("PL · 41", "Hands, chalk &amp; shears at the table", "Reserved for craft photography", "chalk", "3 / 4")})

    body.append(cta_band())
    return page("craftsmanship.html",
                "Craftsmanship & Tailoring Process in Basaveshwaranagar | BespokeStudio",
                "How BespokeStudio builds a garment in Basaveshwaranagar, Bengaluru — measurement, cutting, stitching, fitting, and finishing. Honest workmanship, no inflated claims.",
                "".join(body), "craftsmanship.html", depth=0, service="craftsmanship")

# ============================================================
# GALLERY
# ============================================================
def build_gallery():
    sub = "The showroom, the fabric wall, and finished work. These plates mark exactly what will be photographed for launch — real garments and real workmanship, never stock."
    body = [phero('Gallery', "The showroom &amp; the work", sub)]

    groups = [
        ("Storefront &amp; showroom", [
            ("G · 01", "Storefront &amp; signage — Chord Road", "Exterior", "dark", "3 / 2", "g-span-2 plate--fill"),
            ("G · 02", "Entrance &amp; window", "Exterior", "chalk", "1 / 1", ""),
            ("G · 03", "Fabric wall — wide", "Showroom", "dark", "1 / 1", ""),
            ("G · 04", "Consultation table", "Showroom", "chalk", "1 / 1", ""),
        ]),
        ("Fabrics", [
            ("G · 05", "Reid &amp; Taylor lengths", "Fabric", "dark", "1 / 1", ""),
            ("G · 06", "Wool &amp; worsted — macro", "Fabric", "chalk", "1 / 1", ""),
            ("G · 07", "Linen &amp; cotton shirtings", "Fabric", "dark", "1 / 1", ""),
            ("G · 08", "Silk &amp; blends detail", "Fabric", "chalk", "1 / 1", ""),
        ]),
        ("Finished garments", [
            ("G · 09", "Two-piece suit on stand", "Garment", "dark", "3 / 4", ""),
            ("G · 10", "Sherwani — full length", "Ethnic", "dark", "3 / 4", ""),
            ("G · 11", "Custom shirt — collar &amp; cuff", "Garment", "chalk", "3 / 4", ""),
            ("G · 12", "Women's blazer — line", "Women's", "dark", "3 / 4", ""),
        ]),
        ("The craft", [
            ("G · 13", "Measuring in progress", "Craft", "chalk", "1 / 1", ""),
            ("G · 14", "Chalk marks &amp; shears", "Craft", "dark", "1 / 1", ""),
            ("G · 15", "Trial fitting at the mirror", "Craft", "chalk", "1 / 1", ""),
            ("G · 16", "Final press &amp; finish", "Craft", "dark", "1 / 1", ""),
        ]),
    ]
    for i, (title, plates) in enumerate(groups):
        variant = "paper" if i % 2 == 0 else "deep"
        pl = "".join(plate(c, cap, tag, v, r, cls=cls) for c, cap, tag, v, r, cls in plates)
        body.append("""
<section class="section section--%(variant)s">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">%(title)s</span></div>
    <div class="gallery mt-2">%(pl)s</div>
  </div>
</section>""" % {"variant": variant, "title": title, "pl": pl})

    body.append(cta_band())
    return page("gallery.html",
                "Gallery — Showroom, Fabrics & Finished Work | BespokeStudio Basaveshwaranagar",
                "See BespokeStudio in Basaveshwaranagar, Bengaluru — showroom, Reid & Taylor fabric wall, custom suits, sherwani, shirts, women's formal wear, and the tailoring process.",
                "".join(body), "gallery.html", depth=0, service="gallery")

# ============================================================
# REVIEWS
# ============================================================
def build_reviews():
    sub = "Our customers rate us on Google. Read what they say about the fit, the fabric, and the finish — and add your own after your next commission."
    body = [phero('Reviews', "What customers say", sub)]
    body.append(reviews_block("page"))
    # review-invite
    write = GOOGLE["write_url"] or GOOGLE["profile_url"]
    body.append("""
<section class="section section--paper">
  <div class="wrap">
    <div class="split">
      <div class="split__body reveal">
        <span class="eyebrow">Leave a review</span>
        <h2 class="section-title">Wore something you love?</h2>
        <p class="lede">A few honest words help the next customer decide with confidence. If we made something for you, we&rsquo;d be grateful if you mentioned the garment and the occasion.</p>
        <div class="cta-row mt-3"><a class="btn btn--brass" href="%(write)s" target="_blank" rel="noopener">%(arrow)s Write a Google review</a></div>
      </div>
      <div class="split__media reveal">%(plate)s</div>
    </div>
  </div>
</section>""" % {"write": write, "arrow": icon("arrow"),
                 "plate": plate("PL · 51", "Happy customer at the mirror", "Reserved for photography (with consent)", "chalk", "4 / 3")})
    body.append(cta_band())
    return page("reviews.html",
                "Reviews — Rated on Google | BespokeStudio Basaveshwaranagar",
                "Read verified Google reviews for BespokeStudio, the bespoke tailoring and Reid & Taylor fabric showroom in Basaveshwaranagar, Bengaluru.",
                "".join(body), "reviews.html", depth=0, service="reviews")

# ============================================================
# ABOUT
# ============================================================
def build_about():
    sub = "Twenty years of dressing Basaveshwaranagar, more than twenty craftsmen at the bench, and a fabric wall anchored by Reid & Taylor. A private atelier, run on trust."
    body = [phero('About', "A private atelier in Basaveshwaranagar", sub)]
    body.append("""
<section class="section section--char weave">
  <div class="wrap">
    <div class="split split--flip">
      <div class="split__media reveal">%(plate)s</div>
      <div class="split__body reveal">
        <span class="eyebrow eyebrow--onink">Trust as heritage</span>
        <h2 class="section-title">Two decades, one standard.</h2>
        <p class="lede">For more than twenty years we have made clothing for the people of West Bengaluru — executives building a wardrobe, families dressing for a wedding, and customers who simply want something that fits properly and lasts.</p>
        <p>The work is done by a team of more than twenty craftsmen, in-house, where we can hold every garment to the same standard. We keep the room quiet, the advice honest, and the finish sharp.</p>
      </div>
    </div>
  </div>
</section>
<section class="section section--paper">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">What we stand for</span><h2 class="section-title">Fit, fabric, and workmanship — in that order.</h2></div>
    <div class="cols-3 mt-3">
      <div class="reveal"><h3>Fit as authority</h3><p class="mt-1">Clothing should sharpen posture, proportion, and presence. A good fit does more for how you look than any label.</p></div>
      <div class="reveal"><h3>Fabric as proof</h3><p class="mt-1">Premium Reid &amp; Taylor suiting, wool, cotton, silk, linen, and refined blends — chosen for how they fall and wear.</p></div>
      <div class="reveal"><h3>Workmanship as discipline</h3><p class="mt-1">Careful cutting, stitching, fitting, and finishing — without claiming handwork we don&rsquo;t offer.</p></div>
    </div>
  </div>
</section>""" % {"plate": plate("PL · 61", "The craftsmen — dignified portrait", "Reserved for team photography", "dark", "4 / 3")})

    body.append(trust_bar())
    body.append(location_section(depth=0))
    body.append(cta_band())
    return page("about.html",
                "About — 20+ Years of Bespoke Tailoring in Basaveshwaranagar | BespokeStudio",
                "BespokeStudio is a private bespoke tailoring atelier and Reid & Taylor fabric showroom in Basaveshwaranagar, Bengaluru — 20+ years, 20+ craftsmen, one standard.",
                "".join(body), "about.html", depth=0, service="about")

# ============================================================
# CONTACT
# ============================================================
def build_contact():
    sub = "Visit the showroom in Basaveshwaranagar, or reach us on WhatsApp for the fastest reply. We're open Monday to Saturday 11–9, and Sunday 11–7."
    body = [phero('Visit', "Visit &amp; contact", sub)]
    body.append(location_section(depth=0))
    # service areas + faq
    areas = "".join('<span class="chip">%s</span>' % a for a in
                    ["Basaveshwaranagar", "Rajajinagar", "Vijayanagar", "Malleshwaram", "Mahalakshmi Layout", "West Bengaluru"])
    faqs = [
        ("How do I book a consultation?", "The fastest way is WhatsApp — tap any WhatsApp button and tell us the occasion. You can also call the showroom on %s or simply visit during opening hours." % BIZ["phone_display"]),
        ("How long does a garment take?", "Most commissions are ready in one to two weeks. If you have a fixed date, tell us early — express work is available on request."),
        ("Do you work with Reid &amp; Taylor fabrics?", "Yes. Reid &amp; Taylor suiting anchors our fabric wall, alongside wool, cotton, silk, linen, and refined blends. Availability is confirmed at the showroom."),
        ("What does it cost?", "Pricing depends on the fabric, garment, finish, and timeline, so we don&rsquo;t publish a fixed list. Message us on WhatsApp with what you have in mind for a clear figure."),
        ("Is there parking or a landmark?", "We&rsquo;re on Chord Road, 3rd Stage, %s — easy to find, with the Post Office as a landmark." % BIZ["landmark"].lower().replace("near ", "")),
    ]
    faq_html = "".join('<details%s><summary>%s</summary><p>%s</p></details>' % (" open" if i == 0 else "", q, a) for i, (q, a) in enumerate(faqs))
    body.append("""
<section class="section section--deep">
  <div class="wrap">
    <div class="cols-2">
      <div class="reveal">
        <span class="eyebrow">Service areas</span>
        <h2 class="section-title">Dressing West Bengaluru.</h2>
        <p class="mt-1">Customers visit us from across the western neighbourhoods. If you&rsquo;re nearby, you&rsquo;re close enough.</p>
        <div class="chips mt-2">%(areas)s</div>
        <div class="cta-row mt-3">%(cta)s</div>
      </div>
      <div class="reveal">
        <span class="eyebrow">Questions</span>
        <div class="faq mt-2">%(faq)s</div>
      </div>
    </div>
  </div>
</section>""" % {"areas": areas, "cta": cta_row("Hello BespokeStudio, I would like to plan a visit / consultation.", on_ink=False), "faq": faq_html})
    body.append(cta_band())
    return page("contact.html",
                "Visit & Contact — Basaveshwaranagar Showroom | BespokeStudio",
                "Visit BespokeStudio at 568, Chord Rd, 3rd Stage, Basaveshwar Nagar, Bengaluru, Karnataka 560079. WhatsApp +91 99002 59407, call 080 4989 1288. Open Mon–Sat 11–9, Sun 11–7.",
                "".join(body), "contact.html", depth=0, service="contact")

# ============================================================
# GUIDES (SEO content cluster)
# ============================================================
def build_guides_index():
    sub = "Practical, local answers on custom suits, premium fabrics, and wedding tailoring in Basaveshwaranagar and West Bengaluru — written to help you decide before you visit."
    body = [phero('Guides', "Guides &amp; journal", sub)]
    guides = [
        ("guides/best-bespoke-tailor-basaveshwaranagar.html", "LG · 01", "Choosing a bespoke tailor in Basaveshwaranagar", "What to check on fabric, fit, and delivery before you commit to a tailor."),
        ("guides/custom-suits-fabric-fit-delivery.html", "LG · 02", "Custom suits: fabric, fit &amp; delivery, explained", "A plain guide to commissioning a suit that actually fits — and how long it takes."),
        ("guides/reid-and-taylor-fabrics-bengaluru.html", "LG · 03", "Reid &amp; Taylor fabrics: choosing your suiting", "How to pick the right suiting cloth for the occasion and the Bengaluru climate."),
    ]
    cards = "".join(
        '<a class="guide reveal" href="%s"><span class="guide__ref">%s</span><h3>%s</h3><p>%s</p><span class="tlink">Read the guide %s</span></a>' % (h, r, t, d, icon("arrow"))
        for h, r, t, d in guides
    )
    body.append('<section class="section section--paper"><div class="wrap"><div class="guide-list">%s</div>' % cards)
    # planned topics — listed honestly, not linked (avoids thin pages)
    planned = ["Executive wardrobe basics that work harder", "Cotton, linen, wool or silk in Bengaluru?",
               "How long does custom tailoring take?", "Why a custom shirt fits better than ready-made",
               "Women's formal tailoring in Basaveshwaranagar", "How to prepare for a tailoring consultation"]
    pl = "".join('<li>%s</li>' % p for p in planned)
    body.append('<div class="notice mt-3"><strong>More guides in progress.</strong> Planned topics: <ul class="flist mt-1" style="grid-template-columns:1fr 1fr">%s</ul></div></div></section>' % pl)
    body.append(cta_band())
    return page("guides.html",
                "Guides — Bespoke Tailoring, Fabrics & Suits in Basaveshwaranagar | BespokeStudio",
                "Local guides to bespoke tailoring, custom suits, and premium fabrics in Basaveshwaranagar, Bengaluru — from BespokeStudio.",
                "".join(body), "guides.html", depth=0, service="guides")

def guide_page(slug, title, meta, crumb, h1, intro, sections, related):
    depth = 1
    body = [phero(crumb, h1, intro, depth=depth)]
    secs = ""
    for h2, paras in sections:
        secs += "<h2>%s</h2>" % h2
        for p in paras:
            if isinstance(p, list):
                secs += "<ul>" + "".join("<li>%s</li>" % x for x in p) + "</ul>"
            else:
                secs += "<p>%s</p>" % p
    rel = "".join('<a class="tlink" style="margin-right:1.2rem" href="../%s">%s %s</a>' % (h, t, icon("arrow")) for h, t in related)
    body.append("""
<section class="section section--paper">
  <div class="wrap">
    <article class="prose reveal">%(secs)s
      <hr class="rule mt-3">
      <p class="mt-2"><strong>Ready to talk it through?</strong> Tell us the occasion on WhatsApp and we&rsquo;ll guide you on fabric, fit, and timing.</p>
      <div class="cta-row mt-2">%(cta)s</div>
      <p class="mt-3">%(rel)s</p>
    </article>
  </div>
</section>""" % {"secs": secs, "cta": cta_row("Hello BespokeStudio, I read your guide and would like a consultation.", on_ink=False), "rel": rel})
    body.append(cta_band())
    return page(slug, title, meta, "".join(body), "guides.html", depth=depth, service="guide")

def build_guide_1():
    return guide_page(
        "guides/best-bespoke-tailor-basaveshwaranagar.html",
        "Choosing a Bespoke Tailor in Basaveshwaranagar — What to Check | BespokeStudio",
        "How to choose a bespoke tailor in Basaveshwaranagar, Bengaluru: what to check on fabric, fit, trial fittings, and delivery before you commit.",
        "Guides &nbsp;/&nbsp; Choosing a tailor", "Choosing a bespoke tailor in Basaveshwaranagar",
        "A good tailor is worth keeping for years. Here is a practical, no-nonsense checklist for judging one — before you hand over your fabric or your wedding date.",
        [
            ("Start with the cloth", [
                "The fabric decides most of how a finished garment looks and lasts. A serious tailor will have a proper fabric wall and will let you handle the cloth, talk you through weight and weave, and be honest about what suits the occasion and the Bengaluru climate.",
                "Ask where the suiting comes from. Premium houses such as Reid &amp; Taylor are a good sign — but the real test is whether the tailor can explain <em>why</em> a particular length is right for you.",
            ]),
            ("Ask about fit and trial fittings", [
                "Fit is where bespoke earns its name. Look for a tailor who takes a full set of measurements, reads your posture, and offers a trial fitting before finishing.",
                ["A trial fitting on the body — not just measurements on paper", "A willingness to correct the fit and re-check it", "Clear talk about balance through the shoulder and waist"],
            ]),
            ("Get delivery in writing — roughly", [
                "Most quality commissions take one to two weeks. If you have a wedding or an event, say so early and ask whether express work is available. A trustworthy tailor gives you an honest window rather than an impossible promise.",
            ]),
            ("Judge the finish, and the reviews", [
                "Look at finished garments in the showroom, and read the tailor&rsquo;s Google reviews for what customers say about fit and follow-through. Beware anyone who guarantees they are the &lsquo;best&rsquo; or &lsquo;fastest&rsquo; — good tailors let the work and their customers speak.",
            ]),
        ],
        [("bespoke-tailoring.html", "Our bespoke tailoring"), ("reviews.html", "Read our reviews")],
    )

def build_guide_2():
    return guide_page(
        "guides/custom-suits-fabric-fit-delivery.html",
        "Custom Suits in Basaveshwaranagar — Fabric, Fit & Delivery Guide | BespokeStudio",
        "A plain guide to commissioning a custom suit in Basaveshwaranagar, Bengaluru — choosing fabric, getting the fit right, and how long delivery takes.",
        "Guides &nbsp;/&nbsp; Custom suits", "Custom suits: fabric, fit &amp; delivery",
        "Thinking about your first bespoke suit — or upgrading from ready-made? Here is what actually matters, in plain terms.",
        [
            ("Choosing the fabric", [
                "For a suit that holds its line through a long day, worsted wool is the classic choice — smooth, resilient, and quick to shed creases. Reid &amp; Taylor suiting is a dependable place to start.",
                "For warm Bengaluru months, consider lighter weights or wool-rich blends. Linen reads relaxed and cool for occasion wear; keep it for less formal moments.",
            ]),
            ("Getting the fit right", [
                "A suit fits when it sits clean on the shoulder, closes without strain, and lets you move. The route there is measurement, a pattern built from you, and a trial fitting where corrections are marked and re-checked.",
                ["Shoulder: clean, no divot or overhang", "Chest: closes with a flat drape, no X-pull", "Waist: shaped, not squeezed", "Trouser: sits at the seat with a break you choose"],
            ]),
            ("Two-piece or three-piece?", [
                "A two-piece is the versatile everyday choice. A three-piece adds a waistcoat for weddings and formal occasions, and lets you dress the look up or down through the day.",
            ]),
            ("How long it takes", [
                "Plan for one to two weeks for most commissions. If you have a fixed date, tell your tailor at the first meeting — express work is often possible on request, but earlier is always better.",
            ]),
        ],
        [("bespoke-tailoring.html#suits", "Men's bespoke suits"), ("fabrics.html", "Explore fabrics")],
    )

def build_guide_3():
    return guide_page(
        "guides/reid-and-taylor-fabrics-bengaluru.html",
        "Reid & Taylor Fabrics in Basaveshwaranagar — Choosing Your Suiting | BespokeStudio",
        "How to choose Reid & Taylor and other premium suiting fabrics in Basaveshwaranagar, Bengaluru — weight, weave, and season, explained simply.",
        "Guides &nbsp;/&nbsp; Reid &amp; Taylor fabrics", "Reid &amp; Taylor fabrics: choosing your suiting",
        "Standing at the fabric wall for the first time can be overwhelming. Here is how to narrow it down to the right length with confidence.",
        [
            ("Why the cloth matters most", [
                "Before cut and finish, the fabric sets the character of a suit — how it drapes, how formal it reads, and how it copes with heat and travel. Reid &amp; Taylor is a premium suiting house long associated with worsted wool and a clean, formal finish, which is why it anchors our wall.",
            ]),
            ("Weight and weave, briefly", [
                ["Lighter weights — better for Bengaluru&rsquo;s warmer months and travel", "Mid-weights — the versatile all-rounder for a working wardrobe", "Tighter worsted weaves — smoother, more formal, crease-resistant", "Textured weaves — more character, ideal for odd jackets"],
                "You don&rsquo;t need to memorise this. In the showroom, we put the lengths in your hands and translate weight and weave into what it means for <em>your</em> occasion.",
            ]),
            ("Match the cloth to the occasion", [
                "A boardroom suit and a reception outfit want different things. Tell us where the garment is going — work, wedding, court, festive — and we&rsquo;ll steer you to a length that fits the moment and the season.",
            ]),
            ("Confirm availability in person", [
                "Fabric ranges change, so we always confirm current lengths at the showroom. Message us before you visit and we&rsquo;ll tell you what&rsquo;s on the wall.",
            ]),
        ],
        [("fabrics.html", "The fabric showroom"), ("bespoke-tailoring.html#suits", "Commission a suit")],
    )

# ============================================================
# STATIC FILES
# ============================================================
FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="8" fill="#17150F"/>
<rect x="7" y="7" width="50" height="50" rx="4" fill="none" stroke="#9C7A44" stroke-width="1.4"/>
<text x="32" y="41" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-size="26" font-weight="600" letter-spacing="1" fill="#FBF8F1">BS</text>
<rect x="20" y="47" width="24" height="2" fill="#7A2E22"/>
</svg>"""

def build_sitemap(slugs):
    urls = ""
    for slug in slugs:
        loc = SITE_ORIGIN + "/" + slug
        pri = "1.0" if slug == "index.html" else ("0.9" if "/" not in slug else "0.6")
        urls += "  <url><loc>%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>\n" % (loc, pri)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls

ROBOTS = """User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE_ORIGIN

# Cloudflare Pages headers file (https://developers.cloudflare.com/pages/configuration/headers/).
# Long-cache immutable assets; always-revalidate HTML so content edits go live immediately.
HEADERS = """/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate
"""

# ============================================================
# WRITE
# ============================================================
def write(path, content):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(path) else None
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def main():
    pages = {
        "index.html": build_home(),
        "bespoke-tailoring.html": build_services(),
        "fabrics.html": build_fabrics(),
        "craftsmanship.html": build_craft(),
        "gallery.html": build_gallery(),
        "reviews.html": build_reviews(),
        "about.html": build_about(),
        "contact.html": build_contact(),
        "guides.html": build_guides_index(),
        "guides/best-bespoke-tailor-basaveshwaranagar.html": build_guide_1(),
        "guides/custom-suits-fabric-fit-delivery.html": build_guide_2(),
        "guides/reid-and-taylor-fabrics-bengaluru.html": build_guide_3(),
    }
    for slug, content in pages.items():
        write(slug, content)

    write("assets/img/favicon.svg", FAVICON)
    write("sitemap.xml", build_sitemap(list(pages.keys())))
    write("robots.txt", ROBOTS)
    write("_headers", HEADERS)

    print("Built %d pages + sitemap + robots + favicon + _headers (Cloudflare Pages)" % len(pages))
    for slug in pages:
        print("  ·", slug)

if __name__ == "__main__":
    main()

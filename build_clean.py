#!/usr/bin/env python3
"""Generate the Vyve landing page (index.html) + booking hub (book.html).

Plain, directly-editable HTML. No templating runtime, no design-system bundle:
real values, inlined design tokens, styled <a> buttons, logo from assets/,
fonts from Google Fonts.

Booking model: embedding Jane is blocked by Jane (X-Frame-Options: SAMEORIGIN),
so each therapist deep-links into their own Jane calendar (new tab), pre-selected
by staff_member id. Dual-office therapists get an office-picker modal. Jane
remains the single source of truth and tracks every booking.
"""

# Live subdomains (GitHub Pages custom domains; DNS CNAMEs live in Wix)
LANDING_URL = "https://landing.vyvepsychotherapy.ca"
BOOK_URL = "https://book.vyvepsychotherapy.ca"
BOOK_REPO_DIR = "../vyve-book"  # second repo: serves the booking hub as its index.html

JANE_BASE = "https://clearviewpsychotherapy.janeapp.com/locations"
LOC_SLUG = {
    "moncton": "vyve-psychotherapy-on-botsford-moncton-location",
    "richibucto": "vyve-psychotherapy-in-richibucto",
}
LOC_LABEL = {"moncton": "Moncton", "richibucto": "Richibucto"}

def loc_book_url(code):
    return f"{JANE_BASE}/{LOC_SLUG[code]}/book"

approaches = ["Person-centered", "ACT", "Solution-focused", "EMDR", "Somatic",
              "IFS", "CBT", "Massage Therapy", "Individual counselling", "Couples counselling"]

locations = [
    {"city": "Moncton", "code": "moncton", "addr": "187 Botsford St, Moncton, NB E1C 4X4",
     "phone": "506-524-8119", "telHref": "tel:+15065248119", "cta": "Book in Moncton"},
    {"city": "Richibucto", "code": "richibucto", "addr": "2-9333 Rue Main, Richibucto, NB E4W 4B6",
     "phone": "506-523-3359", "telHref": "tel:+15065233359", "cta": "Book in Richibucto"},
]

# name, initials, role, modality, jane staff_member id, offices, accepting-new-clients
team = [
    ("Petra Cross", "PC", "Canadian Certified Counsellor", "In person · Virtual", 30, ["moncton", "richibucto"], True),
    ("Carolina Mancipe", "CM", "Licensed Counselling Therapist", "In person · Virtual", 9, ["richibucto"], True),
    ("Tyler Curry", "TC", "Counselling Therapist — Candidate", "In person · Virtual", 16, ["moncton", "richibucto"], True),
    ("Lisa Johnson Thebeau", "LJ", "Licensed Counselling Therapist", "In person", 1, ["moncton", "richibucto"], False),
    ("Arianna Gaudreault", "AG", "Counselling Therapist — Candidate", "In person · Virtual", 34, ["moncton", "richibucto"], True),
    ("Charlene Savoie", "CS", "Trauma-Informed Naturotherapist", "In person · Virtual", 22, ["moncton", "richibucto"], True),
    ("Laura MacIsaac", "LM", "Counselling Therapist", "In person · Virtual", 10, ["moncton"], True),
    ("Stephanie Scripture", "SS", "Registered Social Worker", "In person · Virtual", 37, ["moncton"], True),
    ("Stephanie Perry", "SP", "Counselling Therapist — Candidate", "In person · Virtual", 21, ["moncton"], True),
    ("Terrell Sine", "TS", "Counselling Therapist — Candidate", "In person · Virtual", 13, ["moncton"], True),
    ("Mekayla Leger", "ML", "Registered Social Worker", "In person · Virtual", 29, ["moncton"], True),
    ("Joanne Gobeil", "JG", "Psychologist", "Virtual", 23, ["moncton"], True),
    ("Chelsea Steeves-Babineau", "CB", "Licensed Counselling Therapist", "In person · Virtual", 11, ["richibucto"], True),
    ("Julia Urbshot", "JU", "Counselling Therapist", "In person", 35, ["richibucto"], True),
    ("Janna Vassil", "JV", "Counsellor", "In person", 36, ["moncton", "richibucto"], True),
    ("Janine Daigle", "JD", "Counsellor", "In person", 4, ["richibucto"], True),
]


def office_label(offices):
    if len(offices) == 2:
        return "Both offices"
    return LOC_LABEL[offices[0]]


def team_card(t):
    name, initials, role, modality, jid, offices, accepting = t
    data_off = ",".join(offices)
    cls = "vyve-team-card reveal"
    attrs = f'data-card data-offices="{data_off}"'
    if accepting:
        cls += " is-bookable"
        attrs += (f' data-book data-jid="{jid}" data-name="{name}" '
                  f'role="button" tabindex="0" aria-label="Book with {name}"')
        footer_right = '<span style="font-size:13px; font-weight:800; color:var(--vyve-orange);">Book →</span>'
    else:
        footer_right = '<span style="font-size:11.5px; font-weight:700; color:var(--text-muted);">Not accepting new clients</span>'
    return f'''        <article class="{cls}" {attrs}>
          <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
            <div class="mono">
              <svg class="vyve-mono-ring" viewBox="0 0 66 66" width="66" height="66" aria-hidden="true">
                <circle cx="33" cy="33" r="27" fill="none" stroke="rgba(182,81,0,0.30)" stroke-width="2"></circle>
                <ellipse cx="33" cy="33" rx="13" ry="27" fill="none" stroke="rgba(182,81,0,0.45)" stroke-width="2"></ellipse>
              </svg>
              <span class="mono-initials">{initials}</span>
            </div>
            <span class="office-badge">{office_label(offices)}</span>
          </div>
          <div style="margin:18px 0 0;">
            <div style="font-family:var(--font-display); font-weight:var(--weight-black); font-size:20px; letter-spacing:-0.4px; color:var(--vyve-navy); line-height:1.1;">{name}</div>
            <div style="margin:5px 0 0; font-size:13.5px; font-weight:600; line-height:1.4; color:var(--vyve-orange-600);">{role}</div>
          </div>
          <div style="margin:16px 0 0; padding:14px 0 0; border-top:1px solid var(--border-soft); display:flex; align-items:center; justify-content:space-between; gap:10px;">
            <span style="font-size:12.5px; font-weight:600; color:var(--text-muted);">{modality}</span>
            {footer_right}
          </div>
        </article>'''


def team_cards():
    return "\n".join(team_card(t) for t in team)


def chips_html():
    return "\n".join(f'            <span class="chip">{a}</span>' for a in approaches)


def hero_loc_html():
    out = []
    for loc in locations:
        out.append(f'''          <div class="loc-card">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
              <span style="font-family:var(--font-display); font-weight:var(--weight-black); color:var(--vyve-white); font-size:19px; letter-spacing:-0.3px;">{loc["city"]}</span>
              <span style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:var(--vyve-peach); border:1px solid var(--border-on-dark); border-radius:var(--radius-pill); padding:4px 11px; white-space:nowrap;">In person</span>
            </div>
            <div style="margin:10px 0 0; font-size:14px; line-height:1.5; color:var(--vyve-grey);">{loc["addr"]}</div>
            <a href="{loc["telHref"]}" style="display:inline-block; margin:6px 0 16px; font-size:14px; font-weight:700; color:var(--vyve-peach); text-decoration:none;">{loc["phone"]}</a>
            <a href="{loc_book_url(loc["code"])}" target="_blank" rel="noopener" class="btn btn-md btn-accent btn-block">{loc["cta"]}</a>
          </div>''')
    return "\n".join(out)


def office_band_html():
    out = []
    for loc in locations:
        out.append(f'''          <div style="background:var(--vyve-white); border:1px solid var(--border-soft); border-radius:var(--radius-lg); box-shadow:var(--shadow-card); padding:28px 28px 26px; display:flex; flex-direction:column;">
            <div style="display:flex; align-items:center; gap:12px;">
              <h4 style="margin:0; font-family:var(--font-display); font-weight:var(--weight-black); color:var(--text-heading); font-size:26px; letter-spacing:-0.5px;">{loc["city"]}</h4>
              <span style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:var(--vyve-orange); border:1px solid var(--vyve-orange); border-radius:var(--radius-pill); padding:4px 11px; white-space:nowrap;">In-person office</span>
            </div>
            <div style="margin:12px 0 0; font-size:15px; line-height:1.5; color:var(--text-muted);">{loc["addr"]}</div>
            <a href="{loc["telHref"]}" style="display:inline-block; margin:6px 0 22px; font-size:15px; font-weight:700; color:var(--vyve-orange); text-decoration:none;">{loc["phone"]}</a>
            <div style="margin-top:auto;">
              <a href="{loc_book_url(loc["code"])}" target="_blank" rel="noopener" class="btn btn-md btn-primary">{loc["cta"]}</a>
            </div>
          </div>''')
    return "\n".join(out)


def office_book_cards_html():
    """Office cards for the dedicated book page."""
    out = []
    for loc in locations:
        out.append(f'''          <div style="background:var(--vyve-white); border:1px solid var(--border-soft); border-radius:var(--radius-lg); box-shadow:var(--shadow-card); padding:28px 28px 26px; display:flex; flex-direction:column;">
            <div style="display:flex; align-items:center; gap:12px;">
              <h3 style="margin:0; font-family:var(--font-display); font-weight:var(--weight-black); color:var(--text-heading); font-size:26px; letter-spacing:-0.5px;">{loc["city"]}</h3>
              <span style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:var(--vyve-orange); border:1px solid var(--vyve-orange); border-radius:var(--radius-pill); padding:4px 11px; white-space:nowrap;">In-person office</span>
            </div>
            <div style="margin:12px 0 0; font-size:15px; line-height:1.5; color:var(--text-muted);">{loc["addr"]}</div>
            <a href="{loc["telHref"]}" style="display:inline-block; margin:6px 0 4px; font-size:15px; font-weight:700; color:var(--vyve-orange); text-decoration:none;">{loc["phone"]}</a>
            <p style="margin:10px 0 20px; font-size:13.5px; line-height:1.5; color:var(--text-muted);">New here? A free 15-minute consult is the first option on Jane.</p>
            <div style="margin-top:auto;">
              <a href="{loc_book_url(loc["code"])}" target="_blank" rel="noopener" class="btn btn-md btn-primary">See all {loc["city"]} availability</a>
            </div>
          </div>''')
    return "\n".join(out)


def contact_links_html():
    out = []
    for loc in locations:
        out.append(f'          <a href="{loc["telHref"]}" class="contact-link" style="display:inline-flex; align-items:center; gap:9px; font-size:14px; font-weight:600; color:var(--vyve-grey); text-decoration:none;"><span style="font-weight:800; color:var(--vyve-cream);">{loc["city"]}</span> {loc["phone"]}</a>')
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Shared chrome
# ---------------------------------------------------------------------------

STYLE = """  <style>
    /* ============================================================
       DESIGN TOKENS  (edit brand colors / spacing here)
       ============================================================ */
    :root {
      --vyve-navy-deep:#08132E; --vyve-navy:#17294D; --vyve-white:#FFFFFF;
      --vyve-cream:#FAF6F2; --vyve-peach:#FAAC6F; --vyve-grey:#BEC3C5;
      --vyve-orange:#B65100; --vyve-orange-600:#9E551F; --vyve-sand:#ECE3D9;
      --vyve-slate:#677E82; --vyve-peach-tint:#FFE6C2;
      --text-on-dark:#FFFFFF; --text-body:#1C2533; --text-heading:#17294D; --text-muted:#677E82;
      --border-on-dark:rgba(255,255,255,0.22); --border-soft:rgba(28,37,51,0.12);
      --font-body:"Red Hat Display","Helvetica Neue",Arial,sans-serif;
      --font-display:"Red Hat Display","Helvetica Neue",Arial,sans-serif;
      --font-accent:"Cormorant Infant",Georgia,"Times New Roman",serif;
      --weight-black:900; --tracking-h1:-1.62px; --tracking-h2:-1.32px;
      --radius-xl:24px; --radius-lg:16px; --radius-chip:11px; --radius-pill:999px; --radius-sm:8px;
      --shadow-on-dark:0 20px 60px rgba(0,0,0,0.40);
      --shadow-card:0 12px 32px rgba(28,37,51,0.10);
      --shadow-sm:0 1px 2px rgba(8,19,46,0.06);
      --shadow-lg:0 18px 48px rgba(8,19,46,0.12);
      --blur-overlay:blur(8px);
      --bg-dark:radial-gradient(120% 90% at 18% 12%, rgba(46,123,175,0.10), transparent 55%), repeating-radial-gradient(circle at 30% 42%, transparent 0 78px, rgba(255,255,255,0.028) 78px 79px, transparent 79px 158px), radial-gradient(140% 120% at 80% 110%, #0c1f3d 0%, #08132E 55%, #041B32 100%);
      --bg-cream:radial-gradient(90% 70% at 85% -10%, rgba(250,172,111,0.14), transparent 60%), #FAF6F2;
      --site-width:1120px; --section-x:72px; --section-y:96px; --nav-height:90px;
      --dur-base:0.4s; --dur-fast:0.2s; --ease-soft:cubic-bezier(0.22,0.61,0.36,1);
    }

    *, *::before, *::after { box-sizing:border-box; }
    html, body { margin:0; padding:0; }
    body { font-family:var(--font-body); background:var(--vyve-navy-deep); background-image:var(--bg-dark); min-height:100vh; color:var(--text-on-dark); }
    ::selection { background:var(--vyve-peach); color:var(--vyve-navy); }

    /* ---- nav ---- */
    .nav-link { color:var(--vyve-cream); text-decoration:none; font-size:14px; font-weight:600; transition:color var(--dur-base) ease; }
    .nav-link:hover { color:var(--vyve-peach); }
    @media (max-width:560px) { .nav-link { display:none; } }

    /* ---- buttons ---- */
    .btn { display:inline-flex; align-items:center; justify-content:center; border-radius:var(--radius-pill);
      font-family:var(--font-body); font-weight:700; letter-spacing:0.2px; text-decoration:none; white-space:nowrap;
      border:1.5px solid transparent; cursor:pointer;
      transition:background var(--dur-base) ease, border-color var(--dur-base) ease, transform var(--dur-fast) ease; }
    .btn-sm { font-size:13px; padding:8px 18px; height:36px; }
    .btn-md { font-size:15px; padding:11px 24px; height:44px; }
    .btn-block { width:100%; }
    .btn-outline-light { background:transparent; color:var(--vyve-white); border-color:var(--border-on-dark); }
    .btn-outline-light:hover { border-color:rgba(250,172,111,0.6); background:rgba(255,255,255,0.06); }
    .btn-accent { background:var(--vyve-orange); color:var(--vyve-cream); border-color:var(--vyve-orange); }
    .btn-accent:hover { background:var(--vyve-orange-600); border-color:var(--vyve-orange-600); }
    .btn-primary { background:var(--vyve-navy); color:var(--vyve-cream); border-color:var(--vyve-navy); }
    .btn-primary:hover { background:#0F1E3A; border-color:#0F1E3A; }

    /* ---- hero chips ---- */
    .chip { display:inline-flex; align-items:center; font-size:13px; font-weight:600; color:var(--vyve-cream);
      background:rgba(255,255,255,0.06); border:1px solid var(--border-on-dark); border-radius:var(--radius-chip);
      padding:7px 14px; white-space:nowrap; transition:border-color var(--dur-base) ease, background var(--dur-base) ease; }
    .chip:hover { border-color:rgba(250,172,111,0.55); background:rgba(255,255,255,0.10); }

    /* ---- hero booking location cards ---- */
    .loc-card { background:rgba(255,255,255,0.05); border:1px solid var(--border-on-dark); border-radius:var(--radius-lg);
      padding:20px; transition:border-color var(--dur-base) ease, transform var(--dur-fast) ease; }
    .loc-card:hover { border-color:rgba(250,172,111,0.55); transform:translateY(-2px); }
    .virtual-link:hover { background:rgba(255,255,255,0.05); }
    .contact-link:hover { color:var(--vyve-peach); }

    /* ---- team grid + cards ---- */
    .vyve-team-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(258px, 1fr)); gap:20px; }
    .vyve-team-card { display:flex; flex-direction:column; background:var(--vyve-white);
      border:1px solid var(--border-soft); border-radius:var(--radius-lg); box-shadow:var(--shadow-card); padding:24px 22px 22px;
      transition:transform var(--dur-base) var(--ease-soft), box-shadow var(--dur-base) var(--ease-soft), border-color var(--dur-base) ease; }
    .vyve-team-card.is-bookable { cursor:pointer; }
    .vyve-team-card.is-bookable:hover { transform:translateY(-4px); box-shadow:var(--shadow-lg); border-color:rgba(182,81,0,0.35); }
    .vyve-team-card.is-bookable:focus-visible { outline:2px solid var(--vyve-orange); outline-offset:3px; }
    .vyve-team-card.is-bookable:hover .vyve-mono-ring { transform:rotate(-22deg) scale(1.05); }
    .mono { position:relative; width:66px; height:66px; flex:0 0 auto; display:grid; place-items:center; border-radius:50%;
      background:radial-gradient(120% 120% at 30% 25%, var(--vyve-peach-tint), var(--vyve-sand)); }
    .vyve-mono-ring { position:absolute; inset:0; transition:transform var(--dur-base) var(--ease-soft); transform:rotate(-22deg); }
    .mono-initials { position:relative; font-family:var(--font-accent); font-style:italic; font-weight:700; font-size:27px; line-height:1; color:var(--vyve-orange); }
    .office-badge { font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:var(--vyve-slate);
      border:1px solid var(--border-soft); border-radius:var(--radius-pill); padding:5px 10px; white-space:nowrap; }

    /* ---- offices band grid ---- */
    .vyve-office-grid { display:grid; grid-template-columns:1fr 1fr; gap:22px; }
    @media (max-width:720px) { .vyve-office-grid { grid-template-columns:1fr; } }

    /* ---- filter chips (book page) ---- */
    .filter-chip { display:inline-flex; align-items:center; cursor:pointer; font-family:var(--font-body);
      font-size:13px; font-weight:700; color:var(--text-muted); background:var(--vyve-white);
      border:1px solid var(--border-soft); border-radius:var(--radius-pill); padding:8px 16px;
      transition:border-color var(--dur-base) ease, background var(--dur-base) ease, color var(--dur-base) ease; }
    .filter-chip:hover { border-color:var(--vyve-orange); color:var(--vyve-orange); }
    .filter-chip.chip-active { border-color:var(--vyve-orange); background:rgba(182,81,0,0.10); color:var(--vyve-orange); }

    /* ---- office-picker modal ---- */
    .modal-overlay { position:fixed; inset:0; z-index:1000; display:none; align-items:center; justify-content:center;
      padding:20px; background:rgba(8,19,46,0.6); backdrop-filter:blur(6px); -webkit-backdrop-filter:blur(6px); }
    .modal-overlay.open { display:flex; }
    .modal-card { position:relative; width:100%; max-width:420px; background:var(--vyve-white);
      border-radius:var(--radius-xl); box-shadow:var(--shadow-lg); padding:32px 30px; animation:vyveReveal .35s var(--ease-soft); }
    .modal-close { position:absolute; top:12px; right:14px; width:34px; height:34px; border:0; background:transparent;
      font-size:26px; line-height:1; color:var(--text-muted); cursor:pointer; border-radius:50%; }
    .modal-close:hover { background:var(--vyve-sand); color:var(--vyve-navy); }

    /* ---- responsive (these elements carry inline styles, so !important is required to override) ---- */
    @media (max-width:860px) {
      .vyve-nav { padding-left:20px !important; padding-right:20px !important; }
      .vyve-hero { grid-template-columns:1fr !important; gap:34px !important; padding:32px 20px 52px !important; }
      .vyve-hero-h1 { font-size:clamp(34px, 9vw, 46px) !important; }
      .vyve-section-pad { padding-left:20px !important; padding-right:20px !important; }
      .vyve-section-y { padding-top:56px !important; padding-bottom:56px !important; }
    }
    @media (max-width:520px) {
      .vyve-book-panel { padding:22px !important; }
      .vyve-hero-p { font-size:17px !important; }
    }

    /* ---- motion ---- */
    @keyframes vyveHeroIn { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:none; } }
    .hero-anim { animation:vyveHeroIn 0.9s var(--ease-soft) 0.1s backwards; }
    @keyframes vyveReveal { from { opacity:0; transform:translateY(26px); } to { opacity:1; transform:none; } }
    .reveal.is-visible { animation:vyveReveal 0.7s var(--ease-soft) backwards; }
    @media (prefers-reduced-motion:reduce) { .hero-anim, .reveal.is-visible, .modal-card { animation:none; } }
  </style>"""

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
           "%3Crect width='100' height='100' rx='20' fill='%2308132E'/%3E"
           "%3Ccircle cx='50' cy='50' r='26' fill='none' stroke='%23B65100' stroke-width='7'/%3E"
           "%3Cellipse cx='50' cy='50' rx='13' ry='26' fill='none' stroke='%23FAAC6F' stroke-width='6' transform='rotate(-22 50 50)'/%3E%3C/svg%3E")


# Meta (Facebook) Pixel — Vyve Psychotherapy ad account dataset "vyvepsychotherapy.ca"
META_PIXEL_ID = "1741746813684532"
META_PIXEL = f'''  <!-- Meta Pixel Code -->
  <script>
  !function(f,b,e,v,n,t,s)
  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '{META_PIXEL_ID}');
  fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id={META_PIXEL_ID}&ev=PageView&noscript=1"/></noscript>
  <!-- End Meta Pixel Code -->'''


def head(title, desc):
    return f'''<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{desc}">
  <title>{title}</title>
  <link rel="icon" type="image/svg+xml" href="{FAVICON}">
{META_PIXEL}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Infant:ital,wght@1,700&family=Red+Hat+Display:wght@500;600;700;800;900&display=swap" rel="stylesheet">
{STYLE}
</head>'''


def nav(page):
    """page: 'landing' or 'book'. Each page lives on its own subdomain, so
    cross-page links are absolute; same-page links stay relative anchors."""
    if page == "landing":
        logo_href, team_href, offices_href, book_href = "/", "#team", "#offices", BOOK_URL
    else:  # book page (its own repo/subdomain)
        logo_href = LANDING_URL
        team_href = LANDING_URL + "/#team"
        offices_href = LANDING_URL + "/#offices"
        book_href = "/"
    return f'''  <header class="vyve-nav" style="position:sticky; top:0; z-index:50; height:var(--nav-height); display:flex; align-items:center; justify-content:space-between; padding:0 var(--section-x); background:rgba(8,19,46,0.55); backdrop-filter:var(--blur-overlay); -webkit-backdrop-filter:var(--blur-overlay); border-bottom:1px solid var(--border-on-dark);">
    <a href="{logo_href}" style="display:flex; align-items:center;">
      <img src="assets/vyve-logo.svg" alt="Vyve Psychotherapy" style="height:56px; width:auto; display:block;">
    </a>
    <nav style="display:flex; align-items:center; gap:24px;">
      <a href="{team_href}" class="nav-link">Our team</a>
      <a href="{offices_href}" class="nav-link">Offices</a>
      <a href="{book_href}" class="btn btn-sm btn-outline-light">Book appointment</a>
    </nav>
  </header>'''


def contact_bar():
    return f'''  <section style="background:var(--vyve-navy-deep); background-image:var(--bg-dark); border-top:1px solid var(--border-on-dark);">
    <div class="vyve-section-pad reveal" style="max-width:var(--site-width); margin:0 auto; padding:26px var(--section-x); display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:wrap;">
      <span style="font-family:var(--font-display); font-weight:var(--weight-black); color:var(--vyve-white); font-size:18px; letter-spacing:-0.3px;">Whatever you're facing, we're here to <span style="font-family:var(--font-accent); font-style:italic; font-weight:700; font-size:1.3em; color:var(--vyve-peach);">help</span>.</span>
      <div style="display:flex; align-items:center; gap:28px; flex-wrap:wrap;">
{contact_links_html()}
      </div>
    </div>
  </section>'''


MODAL_AND_JS = '''  <!-- office-picker modal (dual-office therapists) -->
  <div id="office-modal" class="modal-overlay" data-modal>
    <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="office-modal-title">
      <button class="modal-close" type="button" aria-label="Close" data-modal-close>&times;</button>
      <div style="text-transform:uppercase; letter-spacing:1.6px; font-size:11px; font-weight:800; color:var(--vyve-orange);">Choose an office</div>
      <h3 id="office-modal-title" style="margin:8px 0 6px; font-family:var(--font-display); font-weight:var(--weight-black); color:var(--vyve-navy); font-size:24px; letter-spacing:-0.4px;">Book with <span data-modal-name></span></h3>
      <p style="margin:0 0 20px; font-size:14.5px; line-height:1.5; color:var(--text-muted);">This therapist sees clients at both offices. Pick the one closest to you &mdash; you'll go straight to their live calendar.</p>
      <div data-modal-buttons style="display:flex; flex-direction:column; gap:12px;"></div>
    </div>
  </div>

  <script>
    (function () {
      var SLUGS = { moncton: "vyve-psychotherapy-on-botsford-moncton-location", richibucto: "vyve-psychotherapy-in-richibucto" };
      var LABEL = { moncton: "Moncton", richibucto: "Richibucto" };
      function janeUrl(office, jid) {
        return "https://clearviewpsychotherapy.janeapp.com/locations/" + SLUGS[office] + "/book#/staff_member/" + jid;
      }
      var modal = document.getElementById("office-modal");
      function openModal(name, jid, offices) {
        modal.querySelector("[data-modal-name]").textContent = name;
        var wrap = modal.querySelector("[data-modal-buttons]");
        wrap.innerHTML = "";
        offices.forEach(function (o) {
          var a = document.createElement("a");
          a.href = janeUrl(o, jid);
          a.target = "_blank"; a.rel = "noopener";
          a.className = "btn btn-md btn-accent btn-block";
          a.setAttribute("data-therapist", name);
          a.textContent = "Book in " + LABEL[o];
          a.addEventListener("click", closeModal);
          wrap.appendChild(a);
        });
        modal.classList.add("open");
        document.body.style.overflow = "hidden";
      }
      function closeModal() { modal.classList.remove("open"); document.body.style.overflow = ""; }
      modal.addEventListener("click", function (e) {
        if (e.target === modal || e.target.hasAttribute("data-modal-close")) closeModal();
      });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeModal(); });

      function book(el) {
        var jid = el.getAttribute("data-jid");
        var name = el.getAttribute("data-name");
        var offices = el.getAttribute("data-offices").split(",");
        if (offices.length === 1) { fireSchedule(name, "therapist_card", offices[0]); window.open(janeUrl(offices[0], jid), "_blank", "noopener"); }
        else { openModal(name, jid, offices); }
      }
      document.querySelectorAll("[data-book]").forEach(function (el) {
        el.addEventListener("click", function () { book(el); });
        el.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); book(el); }
        });
      });

      // ---- Meta Pixel click tracking ----------------------------------
      // Schedule       -> any click through to Jane (office buttons, therapist
      //                   cards, office-picker modal). The conversion event.
      // Contact        -> any phone-number (tel:) tap.
      // ClickToBookPage-> internal nav from landing to the book page (funnel).
      // Every event carries page + content_name (+ category/office) so each
      // button is identifiable in Events Manager breakdowns.
      var PAGE = location.hostname.indexOf("book.") === 0 ? "book" : "landing";
      function fireSchedule(name, category, office) {
        if (!window.fbq) return;
        var p = { content_name: name || "Booking", content_category: category || "appointment_booking", page: PAGE };
        if (office) p.office = office;
        fbq("track", "Schedule", p);
      }
      document.addEventListener("click", function (e) {
        var a = e.target.closest && e.target.closest("a");
        if (!a || !window.fbq) return;
        var href = a.getAttribute("href") || "";
        var label = (a.textContent || "").trim().replace(/\\s+/g, " ");
        if (href.indexOf("janeapp.com") > -1) {
          var inModal = !!(a.closest && a.closest("#office-modal"));
          var therapist = a.getAttribute("data-therapist");
          fireSchedule(therapist || label, inModal ? "office_modal" : "office_button",
                       label.indexOf("Moncton") > -1 ? "moncton" : (label.indexOf("Richibucto") > -1 ? "richibucto" : undefined));
        } else if (href.indexOf("tel:") === 0) {
          fbq("track", "Contact", { content_name: label, method: "phone", page: PAGE });
        } else if (href.indexOf("book.vyvepsychotherapy.ca") > -1) {
          fbq("trackCustom", "ClickToBookPage", { content_name: label, page: PAGE });
        }
      });

      // therapist filter (book page only)
      var chips = document.querySelectorAll("[data-filter]");
      if (chips.length) {
        chips.forEach(function (b) {
          b.addEventListener("click", function () {
            var f = b.getAttribute("data-filter");
            chips.forEach(function (x) { x.classList.toggle("chip-active", x === b); });
            document.querySelectorAll("[data-card]").forEach(function (c) {
              var show = (f === "all") || c.getAttribute("data-offices").split(",").indexOf(f) > -1;
              c.style.display = show ? "" : "none";
            });
          });
        });
      }
    })();
  </script>

  <script>
    (function () {
      function reveal() {
        var vh = window.innerHeight || document.documentElement.clientHeight;
        document.querySelectorAll(".reveal:not(.is-visible)").forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.top < vh * 0.9 && r.bottom > 0) el.classList.add("is-visible");
        });
      }
      reveal();
      window.addEventListener("scroll", reveal, { passive: true });
      window.addEventListener("resize", reveal);
      setTimeout(reveal, 150);
      setTimeout(reveal, 600);
    })();
  </script>'''


HERO_BG = ("background-color:var(--vyve-navy-deep); "
           "background-image:url('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22160%22 height=%22160%22%3E%3Cfilter id=%22n%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.9%22 numOctaves=%223%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23n)%22 opacity=%220.42%22/%3E%3C/svg%3E'), radial-gradient(120% 92% at 13% -8%, rgba(46,123,175,0.22), transparent 52%), radial-gradient(72% 80% at 97% -2%, rgba(182,81,0,0.12), transparent 60%), radial-gradient(150% 135% at 82% 118%, #0d2143 0%, #0a1733 48%, #06112a 100%); "
           "background-repeat:repeat, no-repeat, no-repeat, no-repeat; "
           "background-size:150px 150px, auto, auto, auto; "
           "background-blend-mode:overlay, normal, normal, normal;")

RINGS = '''    <svg viewBox="0 0 900 900" preserveAspectRatio="xMaxYMin slice" aria-hidden="true" style="position:absolute; top:-260px; right:-200px; width:900px; height:900px; pointer-events:none; opacity:0.55;">
      <g fill="none" stroke="rgba(250,172,111,0.16)">
        <circle cx="450" cy="450" r="120" stroke-width="1.5"></circle>
        <circle cx="450" cy="450" r="190" stroke-width="1.5"></circle>
        <circle cx="450" cy="450" r="262" stroke-width="1.25" stroke="rgba(255,255,255,0.10)"></circle>
        <circle cx="450" cy="450" r="338" stroke-width="1.25" stroke="rgba(255,255,255,0.08)"></circle>
        <circle cx="450" cy="450" r="418" stroke-width="1" stroke="rgba(255,255,255,0.06)"></circle>
      </g>
    </svg>'''


# ---------------------------------------------------------------------------
# index.html
# ---------------------------------------------------------------------------

index_html = f'''<!DOCTYPE html>
<html lang="en">
{head("Vyve Psychotherapy — Therapy that doesn't last forever", "Vyve Psychotherapy — real, licensed therapists and measurable progress. In-person and virtual counselling at our Moncton and Richibucto, NB offices.")}
<body>
{nav("landing")}

  <!-- ===== HERO ===== -->
  <section style="position:relative; overflow:hidden; {HERO_BG}">
{RINGS}
    <div class="vyve-hero" style="max-width:var(--site-width); margin:0 auto; width:100%; padding:64px var(--section-x) 88px; display:grid; grid-template-columns:1.05fr 0.95fr; gap:64px; align-items:center;">

      <div>
        <h1 class="vyve-hero-h1 hero-anim" style="margin:0; font-family:var(--font-display); font-weight:var(--weight-black); color:var(--text-on-dark); font-size:clamp(40px, 5.2vw, 60px); line-height:0.98; letter-spacing:var(--tracking-h1); text-wrap:balance;">
          We don't believe in therapy <span style="font-family:var(--font-accent); font-style:italic; font-weight:700; font-size:1.32em; line-height:0.8; color:var(--vyve-peach); padding:0 0.04em;">forever</span>.
        </h1>
        <p class="vyve-hero-p hero-anim" style="color:var(--vyve-cream); font-size:19px; line-height:1.6; font-weight:500; max-width:460px; margin:24px 0 0;">
          Real, licensed therapists and measurable progress.</p>
        <div class="hero-anim" style="margin:32px 0 0;">
          <div style="display:flex; flex-wrap:wrap; gap:9px; max-width:520px;">
{chips_html()}
          </div>
        </div>
      </div>

      <div id="book" class="vyve-book-panel hero-anim" style="background:rgba(255,255,255,0.06); backdrop-filter:var(--blur-overlay); -webkit-backdrop-filter:var(--blur-overlay); border:1px solid var(--border-on-dark); border-radius:var(--radius-xl); padding:30px; box-shadow:var(--shadow-on-dark);">
        <div style="display:flex; align-items:baseline; justify-content:space-between; gap:12px;">
          <h2 style="margin:0; font-family:var(--font-display); font-weight:var(--weight-black); color:var(--vyve-white); font-size:24px; letter-spacing:-0.4px;">Book your session</h2>
          <span style="font-size:13px; font-weight:700; color:var(--vyve-peach); text-transform:uppercase; letter-spacing:1.4px; white-space:nowrap;">2 offices</span>
        </div>
        <p style="margin:8px 0 22px; font-size:14.5px; line-height:1.5; color:var(--vyve-grey);">Choose the office closest to you. New patients welcome.</p>

        <div style="display:flex; flex-direction:column; gap:14px;">
{hero_loc_html()}
        </div>

        <a href="{BOOK_URL}" class="virtual-link" style="display:flex; align-items:center; justify-content:space-between; gap:10px; margin:16px 0 0; padding:14px 18px; border-radius:var(--radius-lg); background:transparent; border:1px dashed var(--border-on-dark); text-decoration:none; transition:background var(--dur-base) ease;">
          <span style="font-size:14px; font-weight:600; color:var(--vyve-cream);">Rather choose a specific therapist? Browse the full team.</span>
          <span style="color:var(--vyve-peach); font-weight:800; font-size:16px;">→</span>
        </a>
      </div>
    </div>
  </section>

  <!-- ===== TEAM DIRECTORY ===== -->
  <section id="team" style="background:var(--vyve-cream); background-image:var(--bg-cream); color:var(--text-body);">
    <div class="vyve-section-pad vyve-section-y" style="max-width:var(--site-width); margin:0 auto; padding:var(--section-y) var(--section-x);">

      <div class="reveal" style="display:flex; align-items:flex-end; justify-content:space-between; gap:28px; flex-wrap:wrap; margin:0 0 44px;">
        <div style="max-width:620px;">
          <span style="display:inline-block; text-transform:uppercase; letter-spacing:2px; font-size:12px; font-weight:800; color:var(--vyve-orange);">Our team · Notre équipe</span>
          <h2 style="margin:16px 0 0; font-family:var(--font-display); font-weight:var(--weight-black); color:var(--text-heading); font-size:clamp(30px, 4vw, 44px); line-height:0.98; letter-spacing:var(--tracking-h2); text-wrap:balance;">
            Find the therapist that's <span style="font-family:var(--font-accent); font-style:italic; font-weight:700; font-size:1.32em; line-height:0.8; color:var(--vyve-orange); padding:0 0.04em;">right</span> for you.
          </h2>
          <p style="margin:18px 0 0; font-size:17px; line-height:1.6; color:var(--text-muted); max-width:560px;">
            A full team of licensed counselling therapists, social workers and psychologists across our two New Brunswick offices. Tap any therapist to see their live availability and book through Jane.
          </p>
        </div>
        <div style="display:flex; align-items:center; gap:10px; padding:12px 18px; border:1px solid var(--border-soft); border-radius:var(--radius-pill); background:var(--vyve-white); box-shadow:var(--shadow-sm);">
          <span style="font-family:var(--font-display); font-weight:var(--weight-black); font-size:26px; color:var(--vyve-orange); letter-spacing:-0.5px;">{len(team)}</span>
          <span style="font-size:13.5px; font-weight:600; line-height:1.25; color:var(--text-muted);">therapists<br>ready to help</span>
        </div>
      </div>

      <div class="vyve-team-grid">
{team_cards()}
      </div>

    </div>
  </section>

  <!-- ===== OFFICES BAND ===== -->
  <section id="offices" style="background:var(--vyve-sand); color:var(--text-body);">
    <div class="vyve-section-pad" style="max-width:var(--site-width); margin:0 auto; padding:64px var(--section-x);">
      <div class="reveal" style="margin:0 0 26px;">
        <h3 style="margin:0; font-family:var(--font-display); font-weight:var(--weight-black); color:var(--text-heading); font-size:clamp(24px, 3vw, 32px); letter-spacing:-0.6px;">
          Two offices, both <span style="font-family:var(--font-accent); font-style:italic; font-weight:700; font-size:1.3em; color:var(--vyve-orange);">close</span> to home.</h3>
      </div>
      <div class="vyve-office-grid reveal">
{office_band_html()}
      </div>
    </div>
  </section>

{contact_bar()}

{MODAL_AND_JS}
</body>
</html>
'''


# ---------------------------------------------------------------------------
# book.html
# ---------------------------------------------------------------------------

book_html = f'''<!DOCTYPE html>
<html lang="en">
{head("Book an appointment — Vyve Psychotherapy", "Book your appointment with Vyve Psychotherapy. Choose a therapist or office in Moncton or Richibucto, NB and book instantly through Jane.")}
<body>
{nav("book")}

  <!-- ===== BOOK HERO ===== -->
  <section style="position:relative; overflow:hidden; {HERO_BG}">
{RINGS}
    <div class="vyve-section-pad" style="max-width:var(--site-width); margin:0 auto; padding:64px var(--section-x) 72px;">
      <span class="hero-anim" style="display:inline-block; text-transform:uppercase; letter-spacing:2px; font-size:12px; font-weight:800; color:var(--vyve-peach);">Book online</span>
      <h1 class="hero-anim" style="margin:14px 0 0; font-family:var(--font-display); font-weight:var(--weight-black); color:var(--text-on-dark); font-size:clamp(36px, 5vw, 54px); line-height:1.0; letter-spacing:var(--tracking-h1); text-wrap:balance; max-width:780px;">
        Book your <span style="font-family:var(--font-accent); font-style:italic; font-weight:700; font-size:1.3em; line-height:0.8; color:var(--vyve-peach);">appointment</span>.
      </h1>
      <p class="hero-anim" style="margin:20px 0 0; color:var(--vyve-cream); font-size:18px; line-height:1.6; font-weight:500; max-width:560px;">
        Pick a therapist or an office below. You'll go straight to their live calendar to choose a time &mdash; new patients welcome, and a free 15-minute consult is always available.
      </p>
    </div>
  </section>

  <!-- ===== BOOK BY OFFICE ===== -->
  <section style="background:var(--vyve-cream); background-image:var(--bg-cream); color:var(--text-body);">
    <div class="vyve-section-pad" style="max-width:var(--site-width); margin:0 auto; padding:72px var(--section-x) 40px;">
      <div class="reveal" style="margin:0 0 26px;">
        <h2 style="margin:0; font-family:var(--font-display); font-weight:var(--weight-black); color:var(--text-heading); font-size:clamp(24px, 3vw, 32px); letter-spacing:-0.6px;">Book by office</h2>
        <p style="margin:10px 0 0; font-size:16px; line-height:1.6; color:var(--text-muted); max-width:560px;">See everyone available at one location, including the free consult.</p>
      </div>
      <div class="vyve-office-grid reveal">
{office_book_cards_html()}
      </div>
    </div>
  </section>

  <!-- ===== BOOK BY THERAPIST ===== -->
  <section style="background:var(--vyve-sand); color:var(--text-body);">
    <div class="vyve-section-pad" style="max-width:var(--site-width); margin:0 auto; padding:48px var(--section-x) 80px;">
      <div class="reveal" style="display:flex; align-items:flex-end; justify-content:space-between; gap:24px; flex-wrap:wrap; margin:0 0 28px;">
        <div>
          <h2 style="margin:0; font-family:var(--font-display); font-weight:var(--weight-black); color:var(--text-heading); font-size:clamp(24px, 3vw, 32px); letter-spacing:-0.6px;">Book by therapist</h2>
          <p style="margin:10px 0 0; font-size:16px; line-height:1.6; color:var(--text-muted); max-width:560px;">Tap a therapist to open their live availability in Jane.</p>
        </div>
        <div style="display:flex; gap:9px; flex-wrap:wrap;">
          <button type="button" class="filter-chip chip-active" data-filter="all">All</button>
          <button type="button" class="filter-chip" data-filter="moncton">Moncton</button>
          <button type="button" class="filter-chip" data-filter="richibucto">Richibucto</button>
        </div>
      </div>

      <div class="vyve-team-grid">
{team_cards()}
      </div>
    </div>
  </section>

{contact_bar()}

{MODAL_AND_JS}
</body>
</html>
'''


import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK_DIR = os.path.normpath(os.path.join(HERE, BOOK_REPO_DIR))

# landing repo (this one) -> landing.vyvepsychotherapy.ca
with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
with open(os.path.join(HERE, "CNAME"), "w", encoding="utf-8") as f:
    f.write("landing.vyvepsychotherapy.ca\n")
open(os.path.join(HERE, ".nojekyll"), "w").close()

# book repo -> book.vyvepsychotherapy.ca (booking hub served as index.html)
os.makedirs(os.path.join(BOOK_DIR, "assets"), exist_ok=True)
with open(os.path.join(BOOK_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(book_html)
shutil.copy2(os.path.join(HERE, "assets", "vyve-logo.svg"), os.path.join(BOOK_DIR, "assets", "vyve-logo.svg"))
with open(os.path.join(BOOK_DIR, "CNAME"), "w", encoding="utf-8") as f:
    f.write("book.vyvepsychotherapy.ca\n")
open(os.path.join(BOOK_DIR, ".nojekyll"), "w").close()

print("wrote", os.path.join(HERE, "index.html"), len(index_html), "bytes  -> landing.vyvepsychotherapy.ca")
print("wrote", os.path.join(BOOK_DIR, "index.html"), len(book_html), "bytes  -> book.vyvepsychotherapy.ca")

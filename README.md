# Vyve Psychotherapy — Website + Booking Funnel

Plain, directly-editable HTML. No build step, no framework, no runtime. Open the files
in a browser to view; edit them in any text editor.

The site is a **booking funnel**: visitors browse your branded pages, then each "Book"
action sends them into **Jane** (the clinic's booking system) with the right therapist and
office pre-selected. Jane stays the single source of truth and tracks every appointment.

---

## Files

```
vyve-psychotherapy/
├── index.html          ← landing page (hero, team directory, offices, contact)
├── book.html           ← booking hub (book by office OR by therapist, with filter)
├── assets/
│   └── vyve-logo.svg   ← header logo
├── build_clean.py      ← regenerates index.html + book.html from the data at the top
├── README.md           ← you are here
└── _archive/           ← old formats, safe to ignore/delete
    ├── index.bundle.html   (original 850 KB JS bundle)
    └── source/             (original design-component template; needs a runtime)
```

**Deploy = upload `index.html`, `book.html`, and `assets/`.** Fonts load from Google Fonts
(needs internet for the exact typefaces); everything else is local.

---

## How booking works (important)

Each therapist deep-links into **their own Jane calendar**, opened in a new tab:

```
https://clearviewpsychotherapy.janeapp.com/locations/<office-slug>/book#/staff_member/<id>
```

- **Single-office therapists** → the card opens that office's calendar directly.
- **Dual-office therapists** → the card opens a small "Choose an office" pop-up, then Jane.
- **Offices** ("Book in Moncton/Richibucto") → that office's full Jane booking page (includes
  the free 15-minute consult as the first option).
- **Lisa Johnson Thebeau** is shown but marked *"Not accepting new clients"* (no booking),
  per Jane's current notice. When she reopens, set her `accepting` flag to `True` (below).

### Why the calendar isn't embedded *inside* the page
Jane sends `X-Frame-Options: SAMEORIGIN`, which makes browsers **refuse to load Jane's
booking page inside an iframe on any non-Jane site.** So the live calendar cannot be shown
on the Vyve domain — the booking step always happens on Jane (new tab). This is a Jane
policy, not a code limitation. The funnel (your UI → Jane handoff, pre-selected) is the
supported pattern.

---

## Editing

Everything is plain HTML with inline styles + a `<style>` block at the top of each file.

- **Brand colors / spacing / fonts** — the commented `:root { … }` token block (in both
  files; edit in `build_clean.py`'s `STYLE` to change both at once).
- **Copy** — search the file for the text and type over it.
- **Therapists / Jane IDs / offices** — the `team` list at the top of `build_clean.py`.
  Each row is: `(name, initials, role, modality, jane_id, [offices], accepting)`.
  After editing, run:
  ```
  python3 build_clean.py
  ```
  (writes both `index.html` and `book.html`). You can also hand-edit the HTML directly; the
  script is just a convenience for bulk changes.

### Therapist → Jane staff IDs (current)
Moncton + Richibucto share global staff IDs:
Petra Cross 30 · Carolina Mancipe 9 · Tyler Curry 16 · Lisa Johnson Thebeau 1 (closed) ·
Arianna Gaudreault 34 · Charlene Savoie 22 · Laura MacIsaac 10 · Stephanie Scripture 37 ·
Stephanie Perry 21 · Terrell Sine 13 · Mekayla Leger 29 · Joanne Gobeil 23 ·
Chelsea Steeves-Babineau 11 · Julia Urbshot 35 · Janna Vassil 36 · Janine Daigle 4.

---

## Still placeholders (`href="#"`) — set when you have them
- **Logo** link points to `index.html` (home). Change if your home route differs.
- No separate virtual-only booking link is wired; virtual sessions are booked through each
  therapist's normal Jane calendar (their modality shows "Virtual").

---

## Deploying

`index.html` + `book.html` + `assets/` is a static site. Netlify / Vercel / Cloudflare
Pages (drag-and-drop the folder), GitHub Pages, or any host / S3 bucket. Add your custom
domain in the host's dashboard. No server, database, or environment variables required.

---

## Design tokens (reference)
- **Colors:** cognac orange `#B65100`, deep navy `#08132E`–`#17294D`, peach `#FAAC6F`,
  cream `#FAF6F2`, sand `#ECE3D9`.
- **Type:** Red Hat Display (Black 900 headings); Cormorant Infant Bold Italic accent.
- **Shape/motion:** 16px card radius, pill buttons, soft navy shadows, ~0.4s soft ease.

All live as CSS variables in the `:root` block.

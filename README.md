# Drew League Digital Platform — MVP

**Official Digital Hub for The Drew League**
*53 Years of Summer Basketball · Los Angeles, California*
*No Excuse · Just Produce*

---

## What This Is

A full-featured sports media web app built in Streamlit (Python). This is the MVP for the Drew League's
digital platform — designed to match the experience of ESPN, NBA App, and Bleacher Report with
an original Drew League identity.

---

## Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- pip

### 2. Install Dependencies
```bash
cd "Drew League App"
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

### 4. Admin Dashboard
- Navigate to **Admin** in the sidebar
- Password: `drewleague2026`

---

## App Pages

| Page | Description |
|---|---|
| 🏠 Home | Dashboard with featured game, highlights, schedule, player spotlight, sponsors |
| 📊 Scores | Game results, standings, stat leaders, team charts |
| 📅 Schedule | Full season schedule with filters by team, week, status |
| 🎬 Highlights | Video hub with YouTube embeds, filters, Top 10 plays |
| 🎙️ Podcasts | Inside The Drew podcast with Spotify/Apple/YouTube links |
| 🎟️ Tickets | Game tickets, VIP passes, season passes, QR concept |
| 👕 Merch | Product catalog with Shopify integration placeholder |
| ⭐ Membership | 4-tier membership system with feature comparison |
| 🤝 Community | History, programs, sponsors, volunteer/newsletter signup |
| ⚙️ Admin | Content management, analytics, game/player/merch management |

---

## Membership Tiers

| Tier | Price | Members |
|---|---|---|
| Free Fan | Free | 12,500 |
| Drew Insider | $9.99/mo | 2,100 |
| Courtside Member | $24.99/mo | 480 |
| Legacy Member | $99.99/mo | 52 |

---

## File Structure

```
Drew League App/
├── app.py                   # Main entry point + navigation
├── requirements.txt
├── README.md
│
├── pages/
│   ├── home.py              # Home dashboard
│   ├── scores.py            # Scores, standings, stat leaders
│   ├── schedule.py          # Full schedule with filters
│   ├── highlights.py        # Video hub
│   ├── podcasts.py          # Podcast media hub
│   ├── tickets.py           # Ticket purchasing
│   ├── merch.py             # Merch store
│   ├── membership.py        # Membership tiers
│   ├── community.py         # Community & foundation
│   └── admin.py             # Admin dashboard
│
├── utils/
│   ├── data_loader.py       # Centralized CSV data loading
│   └── styles.py            # Global CSS + component helpers
│
├── data/
│   ├── teams.csv
│   ├── players.csv
│   ├── games.csv
│   ├── highlights.csv
│   ├── podcasts.csv
│   ├── merch.csv
│   ├── sponsors.csv
│   ├── memberships.csv
│   └── tickets.csv
│
├── database/
│   └── schema.sql           # Full production DB schema (Supabase-ready)
│
└── assets/                  # Logo, images (add your own)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Python) |
| Styling | Custom CSS injected via Streamlit |
| Charts | Plotly |
| Data | Pandas + CSV (dev) → Supabase (production) |
| Payments | Stripe (placeholder, ready to wire) |
| Commerce | Shopify (placeholder, ready to wire) |
| Video | YouTube iframe embeds |
| Podcast | Spotify / Apple Podcasts links |
| Database | SQLite → PostgreSQL / Supabase |
| Auth | Streamlit session state (MVP) → Supabase Auth (v2) |

---

## Monetization Streams

1. **Memberships** — Free, Insider ($9.99/mo), Courtside ($24.99/mo), Legacy ($99.99/mo)
2. **Tickets** — General ($20), VIP ($75), Season Pass ($299–$799)
3. **Merch** — Drew League Shop via Shopify integration
4. **Sponsorships** — Title ($50K+), Gold ($20–25K), Silver ($10–15K) per season
5. **Content Licensing** — Highlight packages, media rights
6. **Streaming** — Premium live game access (Phase 2)

---

## Integration Roadmap

### Ready to Wire (Placeholder Integrations)
- **Stripe** — `stripe` Python library. Add API keys in `.env`. Checkout sessions built into ticket and merch flows.
- **Shopify** — `shopify` Python library. Connect product catalog and cart to your Shopify storefront.
- **Supabase** — Drop-in PostgreSQL replacement. Use `supabase` Python client. Schema is at `database/schema.sql`.
- **YouTube Data API** — Pull real video stats and thumbnails for highlights.

### Phase 2 Additions
- Supabase Auth (email + social login)
- Real-time scores via websockets
- Push notifications (FCM)
- Live streaming integration
- Player profile pages
- Fantasy league module

---

## Mobile Conversion Roadmap

### Phase 1 (Now) — Streamlit Web App
- Fully functional web MVP
- Desktop + tablet optimized
- Dark mode, Drew League branding

### Phase 2 — React Native / Expo
- Convert each Streamlit page to React Native screen
- Same data layer (Supabase) — swap Pandas for Supabase client
- Add native features: push notifications, offline mode, biometrics
- App Store + Google Play submission

### Phase 3 — Native Features
- Live game tracker with real-time WebSocket updates
- Video player with native controls
- QR ticket scanner via device camera
- Apple Pay / Google Pay via Stripe React Native SDK
- Social sharing with Open Graph

---

## Environment Variables (`.env` file)
```
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
SHOPIFY_API_KEY=...
SHOPIFY_API_SECRET=...
SHOPIFY_STORE_URL=drewleague.myshopify.com
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJ...
YOUTUBE_API_KEY=AIza...
ADMIN_PASSWORD=drewleague2026
```

---

## Brand Identity

| Element | Value |
|---|---|
| Primary Color | `#C8102E` (Drew Red) |
| Accent | `#FFD700` (Gold) |
| Background | `#0A0A0A` (Near Black) |
| Card Background | `#1A1A1A` |
| Text | `#FFFFFF` / `#999999` |
| Font | Arial Black / Impact (headers), Arial (body) |
| Tone | Premium · Bold · Community-first |

---

## Credits

- **The Drew League** — Est. 1973, South Central Los Angeles
- **Platform Built by** — Miri LLC
- **Motto** — *No Excuse · Just Produce*

---

*This is a Miri LLC client project. All Drew League branding, trademarks, and intellectual property belong to The Drew League organization.*

# Drew League — Digital Platform

**Official digital hub for The Drew League.**  
Est. 1973 · South Central Los Angeles · No Excuse. Just Produce.

---

## Overview

Full-stack sports media platform for The Drew League — 53 years of summer basketball in Los Angeles. Built to match the experience of ESPN, The Athletic, and the NBA App with an original Drew League identity.

This repository contains the MVP prototype. It is the design and data blueprint for the production build.

---

## Stack

| Layer | Technology |
|---|---|
| Frontend (MVP) | Streamlit (Python) |
| Frontend (Production) | React / Next.js |
| Database | Supabase / PostgreSQL |
| Auth | Supabase Auth |
| Payments | Stripe |
| Commerce | Shopify |
| Video | YouTube Data API |
| Mobile | React Native (Expo) |

---

## Running the MVP

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`

Admin access: navigate to Admin in the nav bar. Password in `.env`.

---

## Pages

| Page | Description |
|---|---|
| Home | Hero, featured game, highlights, upcoming games, player spotlight |
| Schedule | Full season schedule with team and week filters |
| Stats | Scores, standings, stat leaders, team charts |
| Watch | Highlights hub with YouTube embeds and category filters |
| Fan Zone | Tickets, podcasts, community, newsletter signup |
| Shop | Merch catalog with Shopify integration placeholder |
| Members | 4-tier membership system with feature comparison |
| Admin | Content management, analytics, game and player data |

---

## Data

All data lives in `/data/` as CSVs for the MVP. Production replaces this with Supabase.

| File | Description |
|---|---|
| `teams.csv` | Team roster and records |
| `players.csv` | Player stats and profiles |
| `games.csv` | Game schedule, scores, recaps |
| `highlights.csv` | Video metadata and YouTube URLs |
| `memberships.csv` | Membership tier pricing and benefits |
| `tickets.csv` | Ticket inventory and pricing |
| `sponsors.csv` | Partner and sponsor directory |
| `merch.csv` | Product catalog |
| `podcasts.csv` | Episode list with platform links |

---

## Database

`/database/schema.sql` contains the full production schema — Supabase/PostgreSQL ready. Drop-in replacement for all CSV data.

---

## Environment Variables

Copy `.env` and fill in your keys:

```
ADMIN_PASSWORD=
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
SHOPIFY_API_KEY=
SHOPIFY_API_SECRET=
SHOPIFY_STORE_URL=
SUPABASE_URL=
SUPABASE_ANON_KEY=
YOUTUBE_API_KEY=
```

---

## Production Roadmap

**Phase 1 — Web App**  
Convert MVP to Next.js. Connect Supabase. Wire Stripe and Shopify. Ship admin CMS with real database writes.

**Phase 2 — Mobile**  
React Native (iOS + Android). Push notifications. QR ticket scanner. App Store submissions.

**Phase 3 — Advanced**  
Real-time live scores. Live streaming. Fantasy league module.

---

## Brand

| Element | Value |
|---|---|
| Primary | #FF5500 (Drew Orange) |
| Background | #080400 |
| Text | #FFFFFF |
| Secondary | #888888 |
| Font | Arial Black (headers), Arial (body) |

---

*Built by Miri LLC. All Drew League branding and intellectual property belong to The Drew League organization.*

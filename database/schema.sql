-- Drew League Platform — Database Schema
-- Compatible with SQLite (local dev) and PostgreSQL/Supabase (production)
-- Generated: 2026

-- ─── USERS & AUTH ────────────────────────────────────────────────────────────

CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    username        VARCHAR(100) UNIQUE,
    full_name       VARCHAR(255),
    avatar_url      TEXT,
    role            VARCHAR(50) DEFAULT 'fan',     -- fan, admin, staff, player
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE memberships (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    tier            VARCHAR(50) NOT NULL,           -- free, insider, courtside, legacy
    status          VARCHAR(50) DEFAULT 'active',   -- active, cancelled, expired
    price_paid      DECIMAL(10, 2),
    billing_cycle   VARCHAR(20),                    -- monthly, annual
    started_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at      TIMESTAMP WITH TIME ZONE,
    stripe_customer_id  VARCHAR(255),
    stripe_sub_id       VARCHAR(255),
    CONSTRAINT valid_tier CHECK (tier IN ('free', 'insider', 'courtside', 'legacy'))
);

-- ─── LEAGUE STRUCTURE ────────────────────────────────────────────────────────

CREATE TABLE teams (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    slug            VARCHAR(100) UNIQUE NOT NULL,
    logo_url        TEXT,
    wins            INTEGER DEFAULT 0,
    losses          INTEGER DEFAULT 0,
    division        VARCHAR(50),
    home_court      VARCHAR(200),
    head_coach      VARCHAR(100),
    founded_year    INTEGER,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE players (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) UNIQUE,
    team_id         INTEGER REFERENCES teams(id),
    position        VARCHAR(10),
    jersey_number   INTEGER,
    hometown        VARCHAR(100),
    status          VARCHAR(50) DEFAULT 'active',   -- active, inactive, alumni
    bio             TEXT,
    photo_url       TEXT,
    is_featured     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ─── GAMES & STATS ───────────────────────────────────────────────────────────

CREATE TABLE games (
    id              SERIAL PRIMARY KEY,
    home_team_id    INTEGER REFERENCES teams(id),
    away_team_id    INTEGER REFERENCES teams(id),
    home_score      INTEGER DEFAULT 0,
    away_score      INTEGER DEFAULT 0,
    game_date       DATE NOT NULL,
    game_time       TIME,
    season          INTEGER NOT NULL,
    week            INTEGER NOT NULL,
    status          VARCHAR(20) DEFAULT 'upcoming', -- upcoming, live, completed, cancelled
    location        VARCHAR(200),
    recap           TEXT,
    attendance      INTEGER DEFAULT 0,
    is_featured     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE player_stats (
    id              SERIAL PRIMARY KEY,
    player_id       INTEGER REFERENCES players(id),
    game_id         INTEGER REFERENCES games(id),
    points          INTEGER DEFAULT 0,
    assists         INTEGER DEFAULT 0,
    rebounds        INTEGER DEFAULT 0,
    steals          INTEGER DEFAULT 0,
    blocks          INTEGER DEFAULT 0,
    turnovers       INTEGER DEFAULT 0,
    fg_made         INTEGER DEFAULT 0,
    fg_attempted    INTEGER DEFAULT 0,
    three_made      INTEGER DEFAULT 0,
    three_attempted INTEGER DEFAULT 0,
    ft_made         INTEGER DEFAULT 0,
    ft_attempted    INTEGER DEFAULT 0,
    minutes_played  INTEGER DEFAULT 0,
    UNIQUE(player_id, game_id)
);

-- ─── CONTENT ─────────────────────────────────────────────────────────────────

CREATE TABLE highlights (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(500) NOT NULL,
    description     TEXT,
    player_id       INTEGER REFERENCES players(id),
    team_id         INTEGER REFERENCES teams(id),
    game_id         INTEGER REFERENCES games(id),
    youtube_url     TEXT,
    thumbnail_url   TEXT,
    views           INTEGER DEFAULT 0,
    week            INTEGER,
    season          INTEGER,
    category        VARCHAR(50),                    -- game_highlights, top_plays, player_spotlight, recap
    is_featured     BOOLEAN DEFAULT FALSE,
    published_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE podcasts (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(500) NOT NULL,
    guest           VARCHAR(255),
    host            VARCHAR(255),
    duration_min    INTEGER,
    description     TEXT,
    spotify_url     TEXT,
    apple_url       TEXT,
    youtube_url     TEXT,
    thumbnail_url   TEXT,
    category        VARCHAR(50),
    season          INTEGER,
    episode_number  INTEGER,
    release_date    DATE,
    published       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ─── COMMERCE ────────────────────────────────────────────────────────────────

CREATE TABLE merch_products (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) UNIQUE,
    category        VARCHAR(50),                    -- shirts, hoodies, hats, shorts, accessories
    price           DECIMAL(10, 2) NOT NULL,
    description     TEXT,
    sizes           TEXT,                           -- JSON array or comma-separated
    colors          TEXT,                           -- JSON array or comma-separated
    stock           INTEGER DEFAULT 0,
    image_url       TEXT,
    is_featured     BOOLEAN DEFAULT FALSE,
    is_collab       BOOLEAN DEFAULT FALSE,
    shopify_product_id  VARCHAR(255),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE orders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    status          VARCHAR(50) DEFAULT 'pending',  -- pending, paid, shipped, delivered, cancelled
    subtotal        DECIMAL(10, 2),
    tax             DECIMAL(10, 2),
    shipping        DECIMAL(10, 2),
    total           DECIMAL(10, 2),
    stripe_payment_id   VARCHAR(255),
    shopify_order_id    VARCHAR(255),
    shipping_address    JSONB,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE order_items (
    id              SERIAL PRIMARY KEY,
    order_id        UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_id      INTEGER REFERENCES merch_products(id),
    quantity        INTEGER NOT NULL,
    size            VARCHAR(20),
    color           VARCHAR(50),
    unit_price      DECIMAL(10, 2),
    total_price     DECIMAL(10, 2)
);

-- ─── TICKETING ───────────────────────────────────────────────────────────────

CREATE TABLE ticket_types (
    id              SERIAL PRIMARY KEY,
    game_id         INTEGER REFERENCES games(id),   -- NULL for season passes
    name            VARCHAR(100) NOT NULL,
    type            VARCHAR(50),                    -- general, vip, season_pass, courtside_season
    price           DECIMAL(10, 2) NOT NULL,
    description     TEXT,
    total_capacity  INTEGER,
    sold_count      INTEGER DEFAULT 0,
    perks           TEXT,
    is_active       BOOLEAN DEFAULT TRUE
);

CREATE TABLE tickets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    ticket_type_id  INTEGER REFERENCES ticket_types(id),
    game_id         INTEGER REFERENCES games(id),
    status          VARCHAR(50) DEFAULT 'valid',    -- valid, used, cancelled, refunded
    qr_code         VARCHAR(255) UNIQUE,
    seat_number     VARCHAR(50),
    stripe_payment_id   VARCHAR(255),
    purchased_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ─── COMMUNITY ───────────────────────────────────────────────────────────────

CREATE TABLE sponsors (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    tier            VARCHAR(50),                    -- title, gold, silver, community
    logo_url        TEXT,
    website         VARCHAR(500),
    description     TEXT,
    deal_type       VARCHAR(100),
    annual_value    DECIMAL(12, 2),
    category        VARCHAR(100),
    contract_start  DATE,
    contract_end    DATE,
    is_active       BOOLEAN DEFAULT TRUE
);

CREATE TABLE newsletter_signups (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    name            VARCHAR(255),
    interests       TEXT,                           -- comma-separated
    source          VARCHAR(100),                   -- home, community, podcast, etc.
    subscribed_at   TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active       BOOLEAN DEFAULT TRUE
);

CREATE TABLE volunteer_signups (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    email           VARCHAR(255) NOT NULL,
    interest        VARCHAR(100),
    message         TEXT,
    submitted_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status          VARCHAR(50) DEFAULT 'pending'   -- pending, contacted, active
);

-- ─── INDEXES FOR PERFORMANCE ─────────────────────────────────────────────────

CREATE INDEX idx_games_date ON games(game_date);
CREATE INDEX idx_games_season ON games(season);
CREATE INDEX idx_games_status ON games(status);
CREATE INDEX idx_player_stats_player ON player_stats(player_id);
CREATE INDEX idx_player_stats_game ON player_stats(game_id);
CREATE INDEX idx_highlights_season ON highlights(season, week);
CREATE INDEX idx_highlights_views ON highlights(views DESC);
CREATE INDEX idx_memberships_user ON memberships(user_id);
CREATE INDEX idx_memberships_tier ON memberships(tier);
CREATE INDEX idx_tickets_user ON tickets(user_id);
CREATE INDEX idx_tickets_game ON tickets(game_id);

-- ─── ROW LEVEL SECURITY (Supabase) ──────────────────────────────────────────
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE memberships ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tickets ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
-- Users can only read/update their own records.
-- Admins have full access via service role key.

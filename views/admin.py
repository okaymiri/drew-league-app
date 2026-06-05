"""
admin.py — Admin dashboard for Drew League content management.
Upload games, players, highlights, merch, podcasts; view analytics.
"""
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import (
    load_teams, load_players, load_games, load_highlights,
    load_merch, load_podcasts, load_memberships, get_standings
)
from utils.styles import section_header, badge

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "drewleague2026")


def render():
    st.markdown(section_header("Admin Dashboard", "Drew League Content Management"), unsafe_allow_html=True)

    # ─── AUTH GATE ────────────────────────────────────────────────────────────
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        st.markdown("""
        <div class="drew-card" style="max-width:400px;margin:40px auto;text-align:center;padding:40px;">
            <div style="font-size:48px;margin-bottom:16px;">🔐</div>
            <h3 style="font-size:22px;font-weight:900;margin:0 0 8px 0;">Admin Access</h3>
            <p style="color:#666;font-size:13px;margin:0 0 24px 0;">Drew League Staff Only</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            password = st.text_input("Admin Password", type="password")
            if st.button("Log In", use_container_width=True):
                if password == ADMIN_PASSWORD:
                    st.session_state.admin_auth = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
        return

    # ─── LOGOUT ──────────────────────────────────────────────────────────────
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Log Out"):
            st.session_state.admin_auth = False
            st.rerun()

    # ─── LOAD DATA ────────────────────────────────────────────────────────────
    teams = load_teams()
    players = load_players()
    games = load_games()
    highlights = load_highlights()
    merch = load_merch()
    podcasts = load_podcasts()
    memberships = load_memberships()

    # ─── KPI METRICS ─────────────────────────────────────────────────────────
    total_members = int(memberships["member_count"].sum()) if not memberships.empty else 0
    completed_games = len(games[games["status"] == "completed"]) if not games.empty else 0
    total_views = int(highlights["views"].sum()) if not highlights.empty else 0
    total_players = len(players)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Members", f"{total_members:,}", "+127 this week")
    c2.metric("Games Played", completed_games, f"+{completed_games} this season")
    c3.metric("Total Players", total_players)
    c4.metric("Highlight Views", f"{total_views:,}", "+8,200 this week")
    c5.metric("Active Teams", len(teams))

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "ANALYTICS", "GAMES", "PLAYERS", "HIGHLIGHTS", "MERCH", "MEMBERSHIPS"
    ])

    # ─── ANALYTICS ────────────────────────────────────────────────────────────
    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Membership distribution pie
            if not memberships.empty:
                fig = px.pie(
                    memberships,
                    values="member_count",
                    names="name",
                    title="Membership Distribution",
                    color_discrete_sequence=["#666666", "#C8102E", "#FFD700", "#C9A84C"],
                    hole=0.4,
                )
                fig.update_layout(
                    paper_bgcolor="#0A0A0A",
                    font_color="#FFFFFF",
                    title_font_color="#FFFFFF",
                    legend=dict(bgcolor="#1A1A1A"),
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Highlights views bar
            if not highlights.empty:
                fig2 = px.bar(
                    highlights.nlargest(6, "views"),
                    x="views",
                    y="title",
                    orientation="h",
                    title="Top Highlight Videos by Views",
                    color_discrete_sequence=["#C8102E"],
                )
                fig2.update_layout(
                    paper_bgcolor="#0A0A0A",
                    plot_bgcolor="#111111",
                    font_color="#FFFFFF",
                    title_font_color="#FFFFFF",
                    xaxis=dict(gridcolor="#2A2A2A"),
                    yaxis=dict(gridcolor="#2A2A2A"),
                )
                st.plotly_chart(fig2, use_container_width=True)

        # Revenue projection
        st.markdown(section_header("Revenue Projections"), unsafe_allow_html=True)

        revenue_data = {
            "Stream": ["Memberships", "Tickets", "Merch", "Sponsorships", "Content Licensing"],
            "Monthly Est.": [
                memberships[memberships["name"] != "Free Fan"]["price_monthly"].mean() * total_members * 0.1 if not memberships.empty else 0,
                25000,
                15000,
                12500,
                5000,
            ]
        }
        rev_df = pd.DataFrame(revenue_data)
        rev_df["Monthly Est."] = rev_df["Monthly Est."].round(0).astype(int)

        fig3 = px.bar(
            rev_df, x="Stream", y="Monthly Est.",
            title="Estimated Monthly Revenue by Stream ($)",
            color_discrete_sequence=["#C8102E"],
        )
        fig3.update_layout(
            paper_bgcolor="#0A0A0A",
            plot_bgcolor="#111111",
            font_color="#FFFFFF",
            title_font_color="#FFFFFF",
            xaxis=dict(gridcolor="#2A2A2A"),
            yaxis=dict(gridcolor="#2A2A2A", tickprefix="$"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ─── GAMES MANAGEMENT ─────────────────────────────────────────────────────
    with tab2:
        st.markdown("#### Current Game Data")
        if not games.empty:
            display = games[["game_id", "game_date", "home_team_id", "away_team_id",
                              "home_score", "away_score", "status", "week"]].copy()
            st.dataframe(display, use_container_width=True)

        st.markdown("---")
        st.markdown("#### Add / Update Game Result")
        col1, col2 = st.columns(2)
        with col1:
            team_names = teams["name"].tolist() if not teams.empty else []
            home_team = st.selectbox("Home Team", team_names, key="admin_home")
            home_score = st.number_input("Home Score", min_value=0, value=0)
            game_date = st.date_input("Game Date")
        with col2:
            away_team = st.selectbox("Away Team", team_names, key="admin_away")
            away_score = st.number_input("Away Score", min_value=0, value=0)
            week_num = st.number_input("Week", min_value=1, max_value=12, value=1)
        recap_text = st.text_area("Game Recap")
        if st.button("Save Game Result", use_container_width=True):
            st.success(f"Game saved: {home_team} {home_score} — {away_team} {away_score} (Week {week_num})")
            st.info("CSV persistence coming with Supabase integration")

    # ─── PLAYERS MANAGEMENT ───────────────────────────────────────────────────
    with tab3:
        st.markdown("#### Player Roster")
        if not players.empty:
            st.dataframe(
                players[["player_id", "name", "team_id", "position", "jersey_number",
                          "points_per_game", "assists_per_game", "rebounds_per_game", "status"]],
                use_container_width=True
            )

        st.markdown("---")
        st.markdown("#### Add Player")
        col1, col2, col3 = st.columns(3)
        with col1:
            new_name = st.text_input("Player Name")
            new_pos = st.selectbox("Position", ["PG", "SG", "SF", "PF", "C"])
        with col2:
            new_team = st.selectbox("Team", teams["name"].tolist() if not teams.empty else [], key="player_team")
            new_jersey = st.number_input("Jersey #", min_value=0, max_value=99, value=1)
        with col3:
            new_ppg = st.number_input("PPG", min_value=0.0, value=0.0)
            new_hometown = st.text_input("Hometown")

        new_bio = st.text_area("Player Bio")
        if st.button("Add Player", use_container_width=True):
            if new_name:
                st.success(f"Player '{new_name}' added to roster.")
                st.info("Database write coming with Supabase integration")
            else:
                st.error("Player name is required.")

    # ─── HIGHLIGHTS MANAGEMENT ────────────────────────────────────────────────
    with tab4:
        st.markdown("#### Highlights Library")
        if not highlights.empty:
            st.dataframe(
                highlights[["highlight_id", "title", "category", "views", "week", "season"]],
                use_container_width=True
            )

        st.markdown("---")
        st.markdown("#### Add Highlight")
        col1, col2 = st.columns(2)
        with col1:
            hl_title = st.text_input("Title")
            hl_cat = st.selectbox("Category", ["game_highlights", "top_plays", "player_spotlight", "recap"])
            hl_week = st.number_input("Week", min_value=1, max_value=12, value=1)
        with col2:
            hl_youtube = st.text_input("YouTube Embed URL")
            hl_views = st.number_input("Initial View Count", min_value=0, value=0)

        hl_desc = st.text_area("Description")
        if st.button("Add Highlight", use_container_width=True):
            if hl_title:
                st.success(f"Highlight '{hl_title}' added.")
                st.info("Database write coming with Supabase integration")
            else:
                st.error("Title is required.")

    # ─── MERCH MANAGEMENT ─────────────────────────────────────────────────────
    with tab5:
        st.markdown("#### Product Catalog")
        if not merch.empty:
            st.dataframe(
                merch[["product_id", "name", "category", "price", "stock", "is_featured", "is_collab"]],
                use_container_width=True
            )

        st.markdown("---")
        st.markdown("#### Add Product")
        col1, col2, col3 = st.columns(3)
        with col1:
            prod_name = st.text_input("Product Name", key="prod_name")
            prod_cat = st.selectbox("Category", ["shirts", "hoodies", "hats", "shorts", "accessories"])
        with col2:
            prod_price = st.number_input("Price ($)", min_value=0.0, value=35.0)
            prod_stock = st.number_input("Stock Quantity", min_value=0, value=100)
        with col3:
            prod_featured = st.checkbox("Featured Product")
            prod_collab = st.checkbox("Collab Drop")

        prod_desc = st.text_area("Product Description", key="prod_desc")
        prod_sizes = st.text_input("Sizes (comma separated)", value="S,M,L,XL,2XL")
        prod_colors = st.text_input("Colors (comma separated)", value="Black,White")
        if st.button("Add Product", use_container_width=True):
            if prod_name:
                st.success(f"Product '{prod_name}' added to catalog.")
                st.info("Shopify sync coming at launch")
            else:
                st.error("Product name is required.")

    # ─── MEMBERSHIP DASHBOARD ─────────────────────────────────────────────────
    with tab6:
        st.markdown("#### Membership Overview")
        if not memberships.empty:
            for _, tier in memberships.iterrows():
                is_free = tier["price_monthly"] == 0
                monthly_rev = 0 if is_free else tier["price_monthly"] * tier["member_count"]
                col1, col2, col3, col4 = st.columns(4)
                col1.markdown(f"**{tier['name']}**")
                col2.metric("Members", f"{int(tier['member_count']):,}", key=f"mem_{tier['tier_id']}")
                col3.metric("Monthly Rate", f"${tier['price_monthly']}", key=f"rate_{tier['tier_id']}")
                col4.metric("Monthly Rev", f"${monthly_rev:,.0f}", key=f"rev_{tier['tier_id']}")

        st.markdown("---")
        total_monthly_rev = sum(
            t["price_monthly"] * t["member_count"]
            for _, t in memberships.iterrows()
            if t["price_monthly"] > 0
        ) if not memberships.empty else 0
        st.markdown(f"""
        <div class="drew-card" style="text-align:center;border-color:#FFD700;">
            <div style="font-size:13px;color:#666;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">
                Total Estimated Monthly Membership Revenue
            </div>
            <div style="font-size:48px;font-weight:900;color:#FFD700;">${total_monthly_rev:,.0f}</div>
            <div style="font-size:13px;color:#999;margin-top:8px;">
                Based on current member counts × tier pricing
            </div>
        </div>
        """, unsafe_allow_html=True)

"""
admin.py — Admin dashboard.
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
from utils.styles import section_header

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "drewleague2026")

CHART_LAYOUT = dict(
    paper_bgcolor="#080400",
    plot_bgcolor="#0D0800",
    font_color="#888888",
    title_font_color="#FFFFFF",
    xaxis=dict(gridcolor="#1E1200"),
    yaxis=dict(gridcolor="#1E1200"),
    legend=dict(bgcolor="#0D0800", bordercolor="#1E1200"),
)


def render():
    st.markdown(section_header("Admin", "Drew League Content Management"), unsafe_allow_html=True)

    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        st.markdown("""
        <div class="drew-card" style="max-width:400px;margin:40px auto;text-align:center;padding:40px;
                                       border-top:2px solid #FF5500;">
            <h3 style="font-size:20px;font-weight:900;margin:0 0 8px 0;text-transform:uppercase;">
                Admin Access
            </h3>
            <p style="color:#555;font-size:13px;margin:0 0 24px 0;">Drew League Staff Only</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            password = st.text_input("Password", type="password")
            if st.button("Log In", use_container_width=True):
                if password == ADMIN_PASSWORD:
                    st.session_state.admin_auth = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
        return

    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Log Out"):
            st.session_state.admin_auth = False
            st.rerun()

    teams       = load_teams()
    players     = load_players()
    games       = load_games()
    highlights  = load_highlights()
    merch       = load_merch()
    podcasts    = load_podcasts()
    memberships = load_memberships()

    total_members   = int(memberships["member_count"].sum()) if not memberships.empty else 0
    completed_games = len(games[games["status"] == "completed"]) if not games.empty else 0
    total_views     = int(highlights["views"].sum()) if not highlights.empty else 0
    total_players   = len(players)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Members",    f"{total_members:,}",  "+127 this week")
    c2.metric("Games",      completed_games)
    c3.metric("Players",    total_players)
    c4.metric("Views",      f"{total_views:,}",    "+8,200 this week")
    c5.metric("Teams",      len(teams))

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "ANALYTICS", "GAMES", "PLAYERS", "HIGHLIGHTS", "MERCH", "MEMBERSHIPS"
    ])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            if not memberships.empty:
                fig = px.pie(
                    memberships, values="member_count", names="name",
                    title="Membership Distribution",
                    color_discrete_sequence=["#333", "#FF5500", "#888", "#555"],
                    hole=0.4,
                )
                fig.update_layout(**CHART_LAYOUT)
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            if not highlights.empty:
                fig2 = px.bar(
                    highlights.nlargest(6, "views"), x="views", y="title",
                    orientation="h", title="Top Highlights by Views",
                    color_discrete_sequence=["#FF5500"],
                )
                fig2.update_layout(**CHART_LAYOUT)
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown(section_header("Revenue Projections"), unsafe_allow_html=True)
        revenue_data = {
            "Stream":       ["Memberships", "Tickets", "Merch", "Sponsorships", "Content Licensing"],
            "Monthly Est.": [
                memberships[memberships["name"] != "Free Fan"]["price_monthly"].mean() * total_members * 0.1 if not memberships.empty else 0,
                25000, 15000, 12500, 5000,
            ]
        }
        rev_df = pd.DataFrame(revenue_data)
        rev_df["Monthly Est."] = rev_df["Monthly Est."].round(0).astype(int)
        fig3 = px.bar(rev_df, x="Stream", y="Monthly Est.",
                      title="Estimated Monthly Revenue ($)",
                      color_discrete_sequence=["#FFFFFF"])
        fig3.update_layout(**CHART_LAYOUT)
        fig3.update_layout(yaxis=dict(gridcolor="#1E1200", tickprefix="$"))
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        if not games.empty:
            st.dataframe(
                games[["game_id","game_date","home_team_id","away_team_id",
                        "home_score","away_score","status","week"]],
                use_container_width=True
            )
        st.markdown("---")
        st.markdown("#### Add / Update Game")
        col1, col2 = st.columns(2)
        team_names = teams["name"].tolist() if not teams.empty else []
        with col1:
            home_team  = st.selectbox("Home Team", team_names, key="admin_home")
            home_score = st.number_input("Home Score", min_value=0, value=0)
            game_date  = st.date_input("Game Date")
        with col2:
            away_team  = st.selectbox("Away Team", team_names, key="admin_away")
            away_score = st.number_input("Away Score", min_value=0, value=0)
            week_num   = st.number_input("Week", min_value=1, max_value=12, value=1)
        recap_text = st.text_area("Recap")
        if st.button("Save Game", use_container_width=True):
            st.success(f"Game saved: {home_team} {home_score} — {away_team} {away_score} (Week {week_num})")
            st.info("CSV persistence coming with Supabase integration.")

    with tab3:
        if not players.empty:
            st.dataframe(
                players[["player_id","name","team_id","position","jersey_number",
                          "points_per_game","assists_per_game","rebounds_per_game","status"]],
                use_container_width=True
            )
        st.markdown("---")
        st.markdown("#### Add Player")
        col1, col2, col3 = st.columns(3)
        with col1:
            new_name = st.text_input("Player Name")
            new_pos  = st.selectbox("Position", ["PG","SG","SF","PF","C"])
        with col2:
            new_team   = st.selectbox("Team", teams["name"].tolist() if not teams.empty else [], key="player_team")
            new_jersey = st.number_input("Jersey #", min_value=0, max_value=99, value=1)
        with col3:
            new_ppg      = st.number_input("PPG", min_value=0.0, value=0.0)
            new_hometown = st.text_input("Hometown")
        new_bio = st.text_area("Bio")
        if st.button("Add Player", use_container_width=True):
            if new_name:
                st.success(f"Player '{new_name}' added.")
                st.info("Database write coming with Supabase integration.")
            else:
                st.error("Player name is required.")

    with tab4:
        if not highlights.empty:
            st.dataframe(
                highlights[["highlight_id","title","category","views","week","season"]],
                use_container_width=True
            )
        st.markdown("---")
        st.markdown("#### Add Highlight")
        col1, col2 = st.columns(2)
        with col1:
            hl_title = st.text_input("Title")
            hl_cat   = st.selectbox("Category", ["game_highlights","top_plays","player_spotlight","recap"])
            hl_week  = st.number_input("Week", min_value=1, max_value=12, value=1)
        with col2:
            hl_youtube = st.text_input("YouTube URL")
            hl_views   = st.number_input("Initial Views", min_value=0, value=0)
        hl_desc = st.text_area("Description")
        if st.button("Add Highlight", use_container_width=True):
            if hl_title:
                st.success(f"Highlight '{hl_title}' added.")
                st.info("Database write coming with Supabase integration.")
            else:
                st.error("Title required.")

    with tab5:
        if not merch.empty:
            st.dataframe(
                merch[["product_id","name","category","price","stock","is_featured","is_collab"]],
                use_container_width=True
            )
        st.markdown("---")
        st.markdown("#### Add Product")
        col1, col2, col3 = st.columns(3)
        with col1:
            prod_name = st.text_input("Product Name", key="prod_name")
            prod_cat  = st.selectbox("Category", ["shirts","hoodies","hats","shorts","accessories"])
        with col2:
            prod_price = st.number_input("Price ($)", min_value=0.0, value=35.0)
            prod_stock = st.number_input("Stock", min_value=0, value=100)
        with col3:
            prod_featured = st.checkbox("Featured")
            prod_collab   = st.checkbox("Collab Drop")
        prod_desc   = st.text_area("Description", key="prod_desc")
        prod_sizes  = st.text_input("Sizes", value="S,M,L,XL,2XL")
        prod_colors = st.text_input("Colors", value="Black,White")
        if st.button("Add Product", use_container_width=True):
            if prod_name:
                st.success(f"Product '{prod_name}' added.")
                st.info("Shopify sync coming at launch.")
            else:
                st.error("Product name required.")

    with tab6:
        if not memberships.empty:
            for _, tier in memberships.iterrows():
                is_free     = tier["price_monthly"] == 0
                monthly_rev = 0 if is_free else tier["price_monthly"] * tier["member_count"]
                col1, col2, col3, col4 = st.columns(4)
                col1.markdown(f"**{tier['name']}**")
                col2.metric("Members",      f"{int(tier['member_count']):,}", key=f"mem_{tier['tier_id']}")
                col3.metric("Monthly Rate", f"${tier['price_monthly']}",     key=f"rate_{tier['tier_id']}")
                col4.metric("Monthly Rev",  f"${monthly_rev:,.0f}",          key=f"rev_{tier['tier_id']}")

        st.markdown("---")
        total_rev = sum(
            t["price_monthly"] * t["member_count"]
            for _, t in memberships.iterrows()
            if t["price_monthly"] > 0
        ) if not memberships.empty else 0

        st.markdown(f"""
        <div class="drew-card" style="text-align:center;border-top:2px solid #FFFFFF;padding:32px;">
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.15em;color:#555;margin-bottom:8px;">
                Estimated Monthly Membership Revenue
            </div>
            <div style="font-size:48px;font-weight:900;color:#FFFFFF;">${total_rev:,.0f}</div>
            <div style="font-size:12px;color:#444;margin-top:8px;">
                Based on current member counts × tier pricing
            </div>
        </div>
        """, unsafe_allow_html=True)

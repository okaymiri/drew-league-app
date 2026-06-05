"""
home.py — Drew League Home Dashboard.
Featured game, trending highlights, news, schedule preview, and sponsor spotlight.
"""
import streamlit as st
import pandas as pd
from utils.data_loader import (
    load_games, load_teams, load_players, load_highlights,
    load_sponsors, load_memberships, get_team_name
)
from utils.styles import section_header, badge


def render():
    games = load_games()
    teams = load_teams()
    players = load_players()
    highlights = load_highlights()
    sponsors = load_sponsors()
    memberships = load_memberships()

    # ─── HERO ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-hero">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
            <div>
                <div style="font-size:11px;letter-spacing:0.2em;color:#C8102E;text-transform:uppercase;margin-bottom:8px;font-weight:700;">
                    ● Live Season 2026
                </div>
                <h1 style="font-size:48px;font-weight:900;margin:0;line-height:1;text-transform:uppercase;">
                    DREW LEAGUE
                </h1>
                <p style="color:#999;font-size:16px;margin:8px 0 0 0;">
                    53 Years of Summer Basketball · Los Angeles, California
                </p>
                <p style="color:#FFD700;font-size:13px;font-weight:700;margin:6px 0 0 0;letter-spacing:0.1em;text-transform:uppercase;">
                    No Excuse · Just Produce
                </p>
            </div>
            <div style="text-align:right;">
                <div style="font-size:13px;color:#666;">Est. 1973</div>
                <div style="font-size:13px;color:#666;">South Central, LA</div>
                <div style="font-size:13px;color:#999;margin-top:4px;">Week 3 of 12</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── CTA BUTTONS ─────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("▶  Watch Highlights", use_container_width=True)
    with col2:
        st.button("🎟️  Buy Tickets", use_container_width=True)
    with col3:
        st.button("👕  Shop Merch", use_container_width=True)
    with col4:
        st.button("⭐  Join Membership", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── FEATURED GAME ────────────────────────────────────────────────────────
    st.markdown(section_header("Featured Game", "This week's must-watch matchup"), unsafe_allow_html=True)

    featured = games[games["is_featured"] == True]
    if not featured.empty:
        g = featured.iloc[0]
        home_name = get_team_name(teams, g["home_team_id"])
        away_name = get_team_name(teams, g["away_team_id"])

        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.markdown(f"""
            <div class="score-card">
                <div class="team-name">{home_name}</div>
                <div class="score">{int(g['home_score'])}</div>
                <div style="font-size:12px;color:#666;">HOME</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            status_badge = badge("FINAL", "default") if g["status"] == "completed" else badge("UPCOMING", "live")
            st.markdown(f"""
            <div style="text-align:center;padding:40px 0;">
                <div class="vs">VS</div>
                <div style="margin-top:16px;">{status_badge}</div>
                <div style="color:#666;font-size:12px;margin-top:8px;">
                    {g['game_date'].strftime('%b %d, %Y') if hasattr(g['game_date'], 'strftime') else g['game_date']}
                </div>
                <div style="color:#666;font-size:12px;">Week {g['week']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="score-card">
                <div class="team-name">{away_name}</div>
                <div class="score">{int(g['away_score'])}</div>
                <div style="font-size:12px;color:#666;">AWAY</div>
            </div>
            """, unsafe_allow_html=True)

        if g["recap"]:
            st.markdown(f"""
            <div class="drew-card" style="margin-top:16px;">
                <div style="font-size:12px;color:#C8102E;font-weight:700;text-transform:uppercase;
                             letter-spacing:0.1em;margin-bottom:8px;">Game Recap</div>
                <p style="color:#ccc;margin:0;line-height:1.6;">{g['recap']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── TWO COLUMN LAYOUT: HIGHLIGHTS + UPCOMING ─────────────────────────────
    left, right = st.columns([3, 2])

    with left:
        st.markdown(section_header("Trending Highlights"), unsafe_allow_html=True)
        top_highlights = highlights.nlargest(3, "views")
        for _, h in top_highlights.iterrows():
            views_fmt = f"{int(h['views']):,}"
            st.markdown(f"""
            <div class="highlight-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;">
                    <div style="flex:1;">
                        <div style="margin-bottom:6px;">
                            {badge(h['category'].replace('_', ' ').upper())}
                        </div>
                        <div style="font-size:16px;font-weight:700;color:#FFFFFF;margin-bottom:4px;line-height:1.3;">
                            {h['title']}
                        </div>
                        <div style="font-size:12px;color:#666;">
                            {views_fmt} views · Week {h['week']} · {h['season']}
                        </div>
                    </div>
                    <div style="background:#C8102E;border-radius:8px;padding:12px 16px;
                                font-size:20px;flex-shrink:0;">
                        ▶
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown(section_header("Upcoming Games"), unsafe_allow_html=True)
        upcoming = games[games["status"] == "upcoming"].head(4)
        for _, g in upcoming.iterrows():
            home_name = get_team_name(teams, g["home_team_id"])
            away_name = get_team_name(teams, g["away_team_id"])
            date_str = g['game_date'].strftime('%b %d') if hasattr(g['game_date'], 'strftime') else g['game_date']
            st.markdown(f"""
            <div class="drew-card">
                <div style="font-size:11px;color:#3B82F6;font-weight:700;text-transform:uppercase;
                             letter-spacing:0.1em;margin-bottom:8px;">
                    {date_str} · Week {g['week']}
                </div>
                <div style="font-size:15px;font-weight:700;color:#FFFFFF;">
                    {home_name} vs {away_name}
                </div>
                <div style="font-size:12px;color:#666;margin-top:4px;">Drew League Court · LA</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── FEATURED PLAYER ──────────────────────────────────────────────────────
    st.markdown(section_header("Featured Player"), unsafe_allow_html=True)
    featured_players = players[players["is_featured"] == True]
    if not featured_players.empty:
        player = featured_players.iloc[0]
        team_name = get_team_name(teams, player["team_id"])
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""
            <div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:12px;
                         padding:32px;text-align:center;">
                <div style="font-size:64px;">🏀</div>
                <div style="font-size:32px;font-weight:900;color:#FFD700;">#{player['jersey_number']}</div>
                <div style="font-size:12px;color:#666;text-transform:uppercase;letter-spacing:0.1em;">
                    {player['position']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="padding:8px 0;">
                <div style="font-size:11px;color:#C8102E;font-weight:700;text-transform:uppercase;
                             letter-spacing:0.1em;margin-bottom:8px;">Player Spotlight</div>
                <h2 style="font-size:36px;font-weight:900;margin:0 0 4px 0;">{player['name']}</h2>
                <div style="font-size:14px;color:#666;margin-bottom:16px;">{team_name}</div>
                <p style="color:#ccc;line-height:1.6;margin-bottom:16px;">{player['bio']}</p>
            </div>
            """, unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("PPG", f"{player['points_per_game']}")
            with m2:
                st.metric("APG", f"{player['assists_per_game']}")
            with m3:
                st.metric("RPG", f"{player['rebounds_per_game']}")
            with m4:
                st.metric("FG%", f"{int(player['field_goal_pct']*100)}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── SPONSOR SPOTLIGHT ────────────────────────────────────────────────────
    st.markdown(section_header("Official Partners", "Powering the Drew League community"), unsafe_allow_html=True)
    title_sponsors = sponsors[sponsors["tier"] == "title"]
    gold_sponsors = sponsors[sponsors["tier"] == "gold"]

    sponsor_html = ""
    for _, s in title_sponsors.iterrows():
        sponsor_html += f'<span class="sponsor-chip" style="border-color:#FFD700;color:#FFD700;">{s["name"]}</span>'
    for _, s in gold_sponsors.iterrows():
        sponsor_html += f'<span class="sponsor-chip">{s["name"]}</span>'

    st.markdown(f"""
    <div class="drew-card">
        <div style="font-size:11px;color:#666;font-weight:700;text-transform:uppercase;
                     letter-spacing:0.1em;margin-bottom:16px;">Season Partners</div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">{sponsor_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # ─── MEMBERSHIP CTA ───────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    total_members = memberships["member_count"].sum() if not memberships.empty else 0
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1A0000,#0A0A0A);border:1px solid #C8102E;
                border-radius:16px;padding:40px;text-align:center;">
        <div style="font-size:11px;color:#C8102E;font-weight:700;text-transform:uppercase;
                     letter-spacing:0.2em;margin-bottom:12px;">Drew League Membership</div>
        <h2 style="font-size:36px;font-weight:900;margin:0 0 12px 0;">
            Join {total_members:,}+ Drew League Members
        </h2>
        <p style="color:#999;font-size:16px;margin:0 0 24px 0;max-width:500px;margin-left:auto;margin-right:auto;">
            Exclusive content, VIP access, merch drops, and more.
            Be part of the legacy.
        </p>
        <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
            <div style="background:#C8102E;color:#FFF;padding:14px 32px;border-radius:8px;
                         font-weight:700;font-size:15px;text-transform:uppercase;letter-spacing:0.05em;">
                Start Free →
            </div>
            <div style="border:1px solid #FFD700;color:#FFD700;padding:14px 32px;border-radius:8px;
                         font-weight:700;font-size:15px;text-transform:uppercase;letter-spacing:0.05em;">
                View Plans
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

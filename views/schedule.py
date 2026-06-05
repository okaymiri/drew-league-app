"""
schedule.py — Full game schedule with team and player filters.
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_games, load_teams, load_players, get_team_name
from utils.styles import section_header, badge


def render():
    games = load_games()
    teams = load_teams()
    players = load_players()

    st.markdown(section_header("Schedule", "2026 Drew League Season · Week 3 of 12"), unsafe_allow_html=True)

    # ─── FILTER BAR ───────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        team_options = ["All Teams"] + teams["name"].tolist()
        team_filter = st.selectbox("Filter by Team", team_options)
    with col2:
        status_filter = st.selectbox("Status", ["All Games", "Upcoming", "Completed"])
    with col3:
        week_options = ["All Weeks"] + [f"Week {w}" for w in sorted(games["week"].unique())]
        week_filter = st.selectbox("Week", week_options)

    # ─── APPLY FILTERS ────────────────────────────────────────────────────────
    filtered = games.copy()

    if team_filter != "All Teams":
        team_id = teams[teams["name"] == team_filter]["team_id"].values
        if len(team_id) > 0:
            tid = team_id[0]
            filtered = filtered[(filtered["home_team_id"] == tid) | (filtered["away_team_id"] == tid)]

    if status_filter == "Upcoming":
        filtered = filtered[filtered["status"] == "upcoming"]
    elif status_filter == "Completed":
        filtered = filtered[filtered["status"] == "completed"]

    if week_filter != "All Weeks":
        week_num = int(week_filter.replace("Week ", ""))
        filtered = filtered[filtered["week"] == week_num]

    filtered = filtered.sort_values("game_date")

    # ─── QUICK STATS ──────────────────────────────────────────────────────────
    total = len(games)
    completed_count = len(games[games["status"] == "completed"])
    upcoming_count = len(games[games["status"] == "upcoming"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Games", total)
    c2.metric("Completed", completed_count)
    c3.metric("Upcoming", upcoming_count)
    c4.metric("Season Week", "3 of 12")

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── GAME LIST ────────────────────────────────────────────────────────────
    if filtered.empty:
        st.markdown("""
        <div class="drew-card" style="text-align:center;padding:48px;">
            <div style="font-size:48px;margin-bottom:16px;">📅</div>
            <div style="font-size:18px;font-weight:700;margin-bottom:8px;">No games found</div>
            <div style="color:#666;">Try adjusting your filters</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Group by week
    for week in sorted(filtered["week"].unique()):
        week_games = filtered[filtered["week"] == week]
        st.markdown(f"""
        <div style="margin:24px 0 12px 0;padding:12px 0;border-bottom:2px solid #C8102E;">
            <span style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.15em;color:#C8102E;">
                Week {week}
            </span>
            <span style="font-size:12px;color:#666;margin-left:12px;">
                {len(week_games)} game{'s' if len(week_games) != 1 else ''}
            </span>
        </div>
        """, unsafe_allow_html=True)

        for _, g in week_games.iterrows():
            home_name = get_team_name(teams, g["home_team_id"])
            away_name = get_team_name(teams, g["away_team_id"])
            date_str = g["game_date"].strftime("%A, %B %d, %Y") if hasattr(g["game_date"], "strftime") else g["game_date"]
            is_upcoming = g["status"] == "upcoming"
            status_color = "#3B82F6" if is_upcoming else "#22C55E"
            status_text = "UPCOMING" if is_upcoming else "FINAL"

            col1, col2 = st.columns([4, 1])
            with col1:
                if is_upcoming:
                    score_display = f"""
                    <div style="font-size:13px;color:#3B82F6;font-weight:700;">TBD</div>
                    """
                else:
                    home_score = int(g["home_score"])
                    away_score = int(g["away_score"])
                    home_win = home_score > away_score
                    hs = f"color:#FFD700;font-weight:900;" if home_win else "color:#999;"
                    as_ = f"color:#FFD700;font-weight:900;" if not home_win else "color:#999;"
                    score_display = f"""
                    <span style="font-size:24px;font-weight:900;{hs}">{home_score}</span>
                    <span style="color:#444;margin:0 8px;font-size:18px;">—</span>
                    <span style="font-size:24px;font-weight:900;{as_}">{away_score}</span>
                    """

                st.markdown(f"""
                <div class="drew-card" style="margin-bottom:8px;">
                    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
                        <div>
                            <div style="font-size:11px;color:#666;margin-bottom:6px;">{date_str}</div>
                            <div style="font-size:16px;font-weight:700;">
                                <span style="color:#FFFFFF;">{home_name}</span>
                                <span style="color:#444;margin:0 12px;">vs</span>
                                <span style="color:#FFFFFF;">{away_name}</span>
                            </div>
                            <div style="font-size:12px;color:#666;margin-top:4px;">{g['location']}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="margin-bottom:6px;">
                                <span style="background:{status_color};color:#FFF;padding:3px 10px;border-radius:20px;
                                              font-size:10px;font-weight:700;text-transform:uppercase;">{status_text}</span>
                            </div>
                            <div>{score_display}</div>
                        </div>
                    </div>
                    {f'<div style="margin-top:10px;padding-top:10px;border-top:1px solid #2A2A2A;color:#999;font-size:12px;">{g["recap"]}</div>' if g["recap"] and not is_upcoming else ""}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if is_upcoming:
                    st.button("🎟️ Tickets", key=f"ticket_{g['game_id']}", use_container_width=True)
                else:
                    st.button("📺 Highlights", key=f"hl_{g['game_id']}", use_container_width=True)

    # ─── SEASON CALENDAR VIEW ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_header("Season at a Glance"), unsafe_allow_html=True)

    all_weeks = sorted(games["week"].unique())
    cols = st.columns(len(all_weeks))
    for i, week in enumerate(all_weeks):
        week_g = games[games["week"] == week]
        completed_w = len(week_g[week_g["status"] == "completed"])
        upcoming_w = len(week_g[week_g["status"] == "upcoming"])
        with cols[i]:
            border = "#22C55E" if completed_w > 0 and upcoming_w == 0 else "#3B82F6" if upcoming_w > 0 else "#2A2A2A"
            st.markdown(f"""
            <div style="background:#1A1A1A;border:1px solid {border};border-radius:8px;
                         padding:12px;text-align:center;">
                <div style="font-size:10px;color:#666;text-transform:uppercase;letter-spacing:0.1em;">Wk</div>
                <div style="font-size:22px;font-weight:900;color:#FFFFFF;">{week}</div>
                <div style="font-size:11px;color:{'#22C55E' if completed_w>0 else '#3B82F6'};">
                    {'✓' if completed_w > 0 else '○'} {len(week_g)}g
                </div>
            </div>
            """, unsafe_allow_html=True)

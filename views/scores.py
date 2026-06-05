"""
scores.py — Scores, standings, stat leaders.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import (
    load_games, load_teams, load_players,
    get_team_name, get_standings, get_stat_leaders
)
from utils.styles import section_header

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
    games   = load_games()
    teams   = load_teams()
    players = load_players()

    st.markdown(section_header("Scores & Standings", "2026 Season"), unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["RESULTS", "STANDINGS", "STAT LEADERS", "TEAM STATS"])

    with tab1:
        completed = games[games["status"] == "completed"].sort_values("game_date", ascending=False)
        if completed.empty:
            st.info("No completed games yet.")
        for _, g in completed.iterrows():
            home_name  = get_team_name(teams, g["home_team_id"])
            away_name  = get_team_name(teams, g["away_team_id"])
            home_score = int(g["home_score"])
            away_score = int(g["away_score"])
            home_win   = home_score > away_score
            date_str   = g["game_date"].strftime("%b %d, %Y") if hasattr(g["game_date"], "strftime") else g["game_date"]
            hs  = "color:#FFFFFF;font-weight:900;" if home_win else "color:#555;"
            as_ = "color:#FFFFFF;font-weight:900;" if not home_win else "color:#555;"

            st.markdown(f"""
            <div class="drew-card" style="margin-bottom:8px;">
                <div style="font-size:10px;color:#444;text-transform:uppercase;
                             letter-spacing:0.1em;margin-bottom:12px;">
                    {date_str} · Week {g['week']}
                </div>
                <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
                    <div style="flex:1;min-width:120px;">
                        <div style="font-size:15px;font-weight:700;{hs}">{home_name}</div>
                        <div style="font-size:10px;color:#444;text-transform:uppercase;letter-spacing:0.08em;">Home</div>
                    </div>
                    <div style="text-align:center;min-width:90px;">
                        <div style="font-size:30px;font-weight:900;">
                            <span style="{hs}">{home_score}</span>
                            <span style="color:#2A1800;margin:0 6px;">–</span>
                            <span style="{as_}">{away_score}</span>
                        </div>
                        <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                                     letter-spacing:0.1em;color:#444;">Final</div>
                    </div>
                    <div style="flex:1;min-width:120px;text-align:right;">
                        <div style="font-size:15px;font-weight:700;{as_}">{away_name}</div>
                        <div style="font-size:10px;color:#444;text-transform:uppercase;letter-spacing:0.08em;">Away</div>
                    </div>
                </div>
                {f'<div style="margin-top:12px;padding-top:12px;border-top:1px solid #1E1200;color:#666;font-size:13px;line-height:1.6;">{g["recap"]}</div>' if g["recap"] else ""}
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        standings = get_standings(teams)
        standings["Rank"] = range(1, len(standings) + 1)
        standings["Win%"] = (standings["win_pct"] * 100).round(1).astype(str) + "%"

        for i, row in standings.iterrows():
            rank   = row["Rank"]
            border = "#FFFFFF" if rank == 1 else "#1E1200"
            st.markdown(f"""
            <div style="background:#0D0800;border:1px solid {border};padding:14px 20px;
                         margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                <div style="display:flex;align-items:center;gap:20px;">
                    <div style="font-size:14px;font-weight:900;color:{'#FFFFFF' if rank==1 else '#333'};
                                 min-width:24px;">#{rank}</div>
                    <div style="font-size:14px;font-weight:700;color:#FFFFFF;">{row['name']}</div>
                </div>
                <div style="display:flex;gap:28px;text-align:center;">
                    <div>
                        <div style="font-size:18px;font-weight:900;color:#FFFFFF;">{row['wins']}</div>
                        <div style="font-size:9px;color:#444;text-transform:uppercase;letter-spacing:0.1em;">W</div>
                    </div>
                    <div>
                        <div style="font-size:18px;font-weight:900;color:#FFFFFF;">{row['losses']}</div>
                        <div style="font-size:9px;color:#444;text-transform:uppercase;letter-spacing:0.1em;">L</div>
                    </div>
                    <div>
                        <div style="font-size:18px;font-weight:900;color:{'#FFFFFF' if rank==1 else '#888'};">{row['Win%']}</div>
                        <div style="font-size:9px;color:#444;text-transform:uppercase;letter-spacing:0.1em;">Win%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        col1, col2 = st.columns(2)
        stat_configs = [
            ("points_per_game",   "Scoring",  "PPG"),
            ("assists_per_game",  "Assists",  "APG"),
            ("rebounds_per_game", "Rebounds", "RPG"),
            ("steals_per_game",   "Steals",   "SPG"),
        ]
        for idx, (stat, title, label) in enumerate(stat_configs):
            col = col1 if idx % 2 == 0 else col2
            with col:
                leaders = get_stat_leaders(players, stat)
                st.markdown(f"""
                <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                             letter-spacing:0.15em;color:#555;margin:20px 0 10px 0;">{title} Leaders</div>
                """, unsafe_allow_html=True)
                for rank, (_, p) in enumerate(leaders.iterrows(), 1):
                    team_name = get_team_name(teams, p["team_id"])
                    st.markdown(f"""
                    <div style="background:#0D0800;border:1px solid #1E1200;padding:12px 16px;
                                 margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;">
                        <div style="display:flex;gap:12px;align-items:center;">
                            <div style="font-size:13px;font-weight:900;color:{'#FFFFFF' if rank==1 else '#333'};
                                         min-width:20px;">#{rank}</div>
                            <div>
                                <div style="font-size:13px;font-weight:700;color:#FFFFFF;">{p['name']}</div>
                                <div style="font-size:10px;color:#444;text-transform:uppercase;
                                             letter-spacing:0.08em;">{team_name}</div>
                            </div>
                        </div>
                        <div style="font-size:22px;font-weight:900;color:#FFFFFF;">{p[stat]}</div>
                    </div>
                    """, unsafe_allow_html=True)

    with tab4:
        if not teams.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=teams["name"], y=teams["wins"],   name="Wins",   marker_color="#FFFFFF"))
            fig.add_trace(go.Bar(x=teams["name"], y=teams["losses"], name="Losses", marker_color="#2A1800"))
            fig.update_layout(barmode="group", title="Win/Loss Records", **CHART_LAYOUT)
            fig.update_xaxes(tickangle=-35)
            st.plotly_chart(fig, use_container_width=True)

            fig2 = px.scatter(
                players, x="points_per_game", y="assists_per_game",
                size="rebounds_per_game", hover_name="name",
                title="Player Efficiency — PPG vs APG",
                color_discrete_sequence=["#FF5500"],
            )
            fig2.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig2, use_container_width=True)

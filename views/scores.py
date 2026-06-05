"""
scores.py — Scores page with box scores, team stats, and standings.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import (
    load_games, load_teams, load_players,
    get_team_name, get_standings, get_stat_leaders
)
from utils.styles import section_header, badge


def render():
    games = load_games()
    teams = load_teams()
    players = load_players()

    st.markdown(section_header("Scores & Standings", "2026 Drew League Season"), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["RESULTS", "STANDINGS", "STAT LEADERS", "TEAM STATS"])

    # ─── RESULTS ─────────────────────────────────────────────────────────────
    with tab1:
        completed = games[games["status"] == "completed"].sort_values("game_date", ascending=False)
        if completed.empty:
            st.info("No completed games yet.")
        else:
            for _, g in completed.iterrows():
                home_name = get_team_name(teams, g["home_team_id"])
                away_name = get_team_name(teams, g["away_team_id"])
                home_score = int(g["home_score"])
                away_score = int(g["away_score"])
                home_win = home_score > away_score
                date_str = g["game_date"].strftime("%b %d, %Y") if hasattr(g["game_date"], "strftime") else g["game_date"]

                home_style = "color:#FFD700;font-weight:900;" if home_win else "color:#FFFFFF;"
                away_style = "color:#FFD700;font-weight:900;" if not home_win else "color:#FFFFFF;"

                st.markdown(f"""
                <div class="drew-card" style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
                        <div style="flex:1;min-width:180px;">
                            <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">
                                {date_str} · Week {g['week']}
                            </div>
                            <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;">
                                <div style="flex:1;">
                                    <div style="font-size:16px;font-weight:700;{home_style}">{home_name}</div>
                                    <div style="font-size:12px;color:#666;">Home</div>
                                </div>
                                <div style="text-align:center;min-width:100px;">
                                    <div style="font-size:28px;font-weight:900;letter-spacing:0.05em;">
                                        <span style="{home_style}">{home_score}</span>
                                        <span style="color:#444;margin:0 8px;">-</span>
                                        <span style="{away_style}">{away_score}</span>
                                    </div>
                                    <div style="margin-top:4px;">{badge('FINAL')}</div>
                                </div>
                                <div style="flex:1;text-align:right;">
                                    <div style="font-size:16px;font-weight:700;{away_style}">{away_name}</div>
                                    <div style="font-size:12px;color:#666;">Away</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    {f'<div style="margin-top:12px;padding-top:12px;border-top:1px solid #2A2A2A;color:#999;font-size:13px;line-height:1.5;">{g["recap"]}</div>' if g["recap"] else ""}
                </div>
                """, unsafe_allow_html=True)

    # ─── STANDINGS ────────────────────────────────────────────────────────────
    with tab2:
        standings = get_standings(teams)
        standings["Rank"] = range(1, len(standings) + 1)
        standings["Record"] = standings["wins"].astype(str) + "-" + standings["losses"].astype(str)
        standings["Win%"] = (standings["win_pct"] * 100).round(1).astype(str) + "%"

        display_cols = ["Rank", "name", "Record", "Win%", "wins", "losses"]
        display_df = standings[display_cols].rename(columns={"name": "Team", "wins": "W", "losses": "L"})

        st.markdown("""
        <div style="margin-bottom:16px;">
            <div style="font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#FFD700;margin-bottom:8px;">
                2026 League Standings
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Color code rows
        for i, row in display_df.iterrows():
            rank = row["Rank"]
            border = "#FFD700" if rank == 1 else "#C8102E" if rank <= 3 else "#2A2A2A"
            rank_display = "🏆" if rank == 1 else f"#{rank}"
            st.markdown(f"""
            <div style="background:#1A1A1A;border:1px solid {border};border-radius:8px;padding:14px 20px;
                         margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
                <div style="display:flex;align-items:center;gap:16px;">
                    <div style="font-size:18px;font-weight:900;color:{'#FFD700' if rank==1 else '#999'};
                                 min-width:36px;">{rank_display}</div>
                    <div>
                        <div style="font-size:15px;font-weight:700;color:#FFFFFF;">{row['Team']}</div>
                    </div>
                </div>
                <div style="display:flex;gap:24px;text-align:center;">
                    <div>
                        <div style="font-size:18px;font-weight:900;color:#FFFFFF;">{row['W']}</div>
                        <div style="font-size:10px;color:#666;text-transform:uppercase;">W</div>
                    </div>
                    <div>
                        <div style="font-size:18px;font-weight:900;color:#FFFFFF;">{row['L']}</div>
                        <div style="font-size:10px;color:#666;text-transform:uppercase;">L</div>
                    </div>
                    <div>
                        <div style="font-size:18px;font-weight:900;color:#FFD700;">{row['Win%']}</div>
                        <div style="font-size:10px;color:#666;text-transform:uppercase;">Win%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ─── STAT LEADERS ─────────────────────────────────────────────────────────
    with tab3:
        col1, col2 = st.columns(2)

        stat_configs = [
            ("points_per_game", "Scoring Leaders", "PPG"),
            ("assists_per_game", "Assist Leaders", "APG"),
            ("rebounds_per_game", "Rebound Leaders", "RPG"),
            ("steals_per_game", "Steals Leaders", "SPG"),
        ]

        for idx, (stat, title, label) in enumerate(stat_configs):
            col = col1 if idx % 2 == 0 else col2
            with col:
                leaders = get_stat_leaders(players, stat)
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <div style="font-size:14px;font-weight:700;text-transform:uppercase;
                                 letter-spacing:0.1em;color:#FFD700;margin-bottom:12px;">{title}</div>
                """, unsafe_allow_html=True)
                for rank, (_, p) in enumerate(leaders.iterrows(), 1):
                    team_name = get_team_name(teams, p["team_id"])
                    st.markdown(f"""
                    <div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;
                                 padding:12px 16px;margin-bottom:6px;display:flex;
                                 justify-content:space-between;align-items:center;">
                        <div style="display:flex;gap:12px;align-items:center;">
                            <div style="font-size:16px;font-weight:900;color:{'#FFD700' if rank==1 else '#666'};
                                         min-width:24px;">#{rank}</div>
                            <div>
                                <div style="font-size:14px;font-weight:700;color:#FFFFFF;">{p['name']}</div>
                                <div style="font-size:11px;color:#666;">{team_name}</div>
                            </div>
                        </div>
                        <div style="font-size:22px;font-weight:900;color:#FFFFFF;">{p[stat]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # ─── TEAM STATS CHART ─────────────────────────────────────────────────────
    with tab4:
        if not teams.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=teams["name"],
                y=teams["wins"],
                name="Wins",
                marker_color="#C8102E",
            ))
            fig.add_trace(go.Bar(
                x=teams["name"],
                y=teams["losses"],
                name="Losses",
                marker_color="#333333",
            ))
            fig.update_layout(
                barmode="group",
                title="Team Win/Loss Records — 2026 Season",
                title_font_color="#FFFFFF",
                paper_bgcolor="#0A0A0A",
                plot_bgcolor="#111111",
                font_color="#FFFFFF",
                xaxis=dict(tickangle=-35, gridcolor="#2A2A2A"),
                yaxis=dict(gridcolor="#2A2A2A"),
                legend=dict(bgcolor="#1A1A1A", bordercolor="#2A2A2A"),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Player scoring scatter
            fig2 = px.scatter(
                players,
                x="points_per_game",
                y="assists_per_game",
                size="rebounds_per_game",
                hover_name="name",
                title="Player Efficiency — PPG vs APG (bubble = RPG)",
                color_discrete_sequence=["#C8102E"],
            )
            fig2.update_layout(
                paper_bgcolor="#0A0A0A",
                plot_bgcolor="#111111",
                font_color="#FFFFFF",
                xaxis=dict(gridcolor="#2A2A2A"),
                yaxis=dict(gridcolor="#2A2A2A"),
                title_font_color="#FFFFFF",
            )
            st.plotly_chart(fig2, use_container_width=True)

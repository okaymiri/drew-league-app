"""
schedule.py — Season schedule.
"""
import streamlit as st
from utils.data_loader import load_games, load_teams, get_team_name
from utils.styles import section_header


def render():
    games = load_games()
    teams = load_teams()

    st.markdown(section_header("Schedule", "2026 Season · Week 3 of 12"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        team_options = ["All Teams"] + teams["name"].tolist()
        team_filter = st.selectbox("Team", team_options)
    with col2:
        status_filter = st.selectbox("Status", ["All Games", "Upcoming", "Completed"])
    with col3:
        week_options = ["All Weeks"] + [f"Week {w}" for w in sorted(games["week"].unique())]
        week_filter = st.selectbox("Week", week_options)

    filtered = games.copy()
    if team_filter != "All Teams":
        tid = teams[teams["name"] == team_filter]["team_id"].values
        if len(tid):
            filtered = filtered[(filtered["home_team_id"] == tid[0]) | (filtered["away_team_id"] == tid[0])]
    if status_filter == "Upcoming":
        filtered = filtered[filtered["status"] == "upcoming"]
    elif status_filter == "Completed":
        filtered = filtered[filtered["status"] == "completed"]
    if week_filter != "All Weeks":
        filtered = filtered[filtered["week"] == int(week_filter.replace("Week ", ""))]
    filtered = filtered.sort_values("game_date")

    total    = len(games)
    done     = len(games[games["status"] == "completed"])
    upcoming = len(games[games["status"] == "upcoming"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Games", total)
    c2.metric("Completed",   done)
    c3.metric("Upcoming",    upcoming)
    c4.metric("Season Week", "3 of 12")

    st.markdown("<br>", unsafe_allow_html=True)

    if filtered.empty:
        st.markdown("""
        <div class="drew-card" style="text-align:center;padding:48px;">
            <div style="font-size:14px;font-weight:700;color:#555;">No games match your filters.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    for week in sorted(filtered["week"].unique()):
        week_games = filtered[filtered["week"] == week]
        st.markdown(f"""
        <div style="margin:28px 0 12px 0;padding-bottom:8px;border-bottom:2px solid #1E1200;">
            <span style="font-size:10px;font-weight:700;text-transform:uppercase;
                          letter-spacing:0.2em;color:#FF5500;">Week {week}</span>
            <span style="font-size:10px;color:#444;margin-left:12px;letter-spacing:0.05em;">
                {len(week_games)} game{'s' if len(week_games) != 1 else ''}
            </span>
        </div>
        """, unsafe_allow_html=True)

        for _, g in week_games.iterrows():
            home_name   = get_team_name(teams, g["home_team_id"])
            away_name   = get_team_name(teams, g["away_team_id"])
            date_str    = g["game_date"].strftime("%A, %B %d, %Y") if hasattr(g["game_date"], "strftime") else g["game_date"]
            is_upcoming = g["status"] == "upcoming"

            col1, col2 = st.columns([4, 1])
            with col1:
                if is_upcoming:
                    score_html = '<div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#FF5500;">Upcoming</div>'
                else:
                    hs  = home_score = int(g["home_score"])
                    as_ = away_score = int(g["away_score"])
                    hw  = home_score > away_score
                    hc  = "#FFFFFF" if hw else "#555"
                    ac  = "#FFFFFF" if not hw else "#555"
                    score_html = f'<div style="font-size:24px;font-weight:900;"><span style="color:{hc};">{home_score}</span><span style="color:#2A1800;margin:0 8px;">–</span><span style="color:{ac};">{away_score}</span></div>'

                st.markdown(f"""
                <div class="drew-card" style="margin-bottom:6px;">
                    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
                        <div>
                            <div style="font-size:10px;color:#444;text-transform:uppercase;
                                         letter-spacing:0.08em;margin-bottom:6px;">{date_str}</div>
                            <div style="font-size:16px;font-weight:700;color:#FFFFFF;">
                                {home_name} <span style="color:#333;margin:0 10px;font-size:12px;">vs</span> {away_name}
                            </div>
                        </div>
                        <div style="text-align:right;">{score_html}</div>
                    </div>
                    {f'<div style="margin-top:10px;padding-top:10px;border-top:1px solid #1E1200;color:#666;font-size:12px;line-height:1.6;">{g["recap"]}</div>' if g["recap"] and not is_upcoming else ""}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                label = "Tickets" if is_upcoming else "Highlights"
                st.button(label, key=f"btn_{g['game_id']}", use_container_width=True)

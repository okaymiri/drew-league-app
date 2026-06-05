"""
home.py — Drew League Home. Mobile-first feed.
"""
import streamlit as st
from utils.data_loader import (
    load_games, load_teams, load_players, load_highlights,
    load_sponsors, get_team_name
)
from utils.styles import section_header


def render():
    games      = load_games()
    teams      = load_teams()
    players    = load_players()
    highlights = load_highlights()
    sponsors   = load_sponsors()

    # ─── HERO ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin:0 -16px 24px -16px;padding:48px 24px 36px 24px;background:radial-gradient(ellipse at 60% 0%, #FF6600 0%, #CC3300 55%, #1A0800 100%);">
        <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.2em;color:rgba(255,255,255,0.5);margin-bottom:14px;">South Central Los Angeles · Est. 1973</div>
        <h1 style="font-size:60px;font-weight:900;margin:0;line-height:0.88;text-transform:uppercase;letter-spacing:-0.04em;color:#FFFFFF;text-shadow:0 2px 20px rgba(0,0,0,0.5);">NO<br>EXCUSE.<br>JUST<br>PRODUCE.</h1>
        <div style="margin-top:22px;display:flex;gap:8px;align-items:center;">
            <div style="background:#FFFFFF;color:#080400;padding:4px 10px;font-size:9px;font-weight:900;text-transform:uppercase;letter-spacing:0.15em;">LIVE</div>
            <div style="font-size:10px;color:rgba(255,255,255,0.6);text-transform:uppercase;letter-spacing:0.12em;">2026 Season · Week 3 of 12</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── FEATURED GAME ────────────────────────────────────────────────────────
    featured = games[games["is_featured"] == True]
    if not featured.empty:
        g = featured.iloc[0]
        hn = get_team_name(teams, g["home_team_id"])
        an = get_team_name(teams, g["away_team_id"])
        hs = int(g["home_score"])
        as_ = int(g["away_score"])
        hw  = hs > as_
        date_str = g['game_date'].strftime('%b %d') if hasattr(g['game_date'], 'strftime') else g['game_date']

        st.markdown(section_header("Featured Game"), unsafe_allow_html=True)
        st.markdown(f"""
        <div class="drew-card" style="border-top:2px solid #FFFFFF;padding:20px;">
            <div style="font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:14px;">
                Final · {date_str} · Week {g['week']}
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="flex:1;">
                    <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                                 letter-spacing:0.08em;color:{'#FFF' if hw else '#555'};">{hn}</div>
                    <div style="font-size:9px;color:#444;text-transform:uppercase;margin-top:2px;">Home</div>
                </div>
                <div style="text-align:center;padding:0 16px;">
                    <div style="font-size:38px;font-weight:900;letter-spacing:0.05em;line-height:1;">
                        <span style="color:{'#FFF' if hw else '#555'};">{hs}</span>
                        <span style="color:#2A1800;margin:0 8px;font-size:24px;">–</span>
                        <span style="color:{'#FFF' if not hw else '#555'};">{as_}</span>
                    </div>
                </div>
                <div style="flex:1;text-align:right;">
                    <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                                 letter-spacing:0.08em;color:{'#FFF' if not hw else '#555'};">{an}</div>
                    <div style="font-size:9px;color:#444;text-transform:uppercase;margin-top:2px;">Away</div>
                </div>
            </div>
            {f'<div style="margin-top:14px;padding-top:14px;border-top:1px solid #1E1200;font-size:13px;color:#666;line-height:1.6;">{g["recap"]}</div>' if g["recap"] else ""}
        </div>
        """, unsafe_allow_html=True)

    # ─── UPCOMING GAMES ───────────────────────────────────────────────────────
    st.markdown(section_header("Upcoming Games"), unsafe_allow_html=True)
    upcoming = games[games["status"] == "upcoming"].head(3)
    for _, g in upcoming.iterrows():
        hn = get_team_name(teams, g["home_team_id"])
        an = get_team_name(teams, g["away_team_id"])
        date_str = g['game_date'].strftime('%b %d') if hasattr(g['game_date'], 'strftime') else g['game_date']
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                     padding:14px 0;border-bottom:1px solid #1E1200;">
            <div>
                <div style="font-size:9px;color:#555;text-transform:uppercase;
                             letter-spacing:0.1em;margin-bottom:4px;">{date_str} · Wk {g['week']}</div>
                <div style="font-size:15px;font-weight:700;color:#FFF;">{hn} vs {an}</div>
            </div>
            <div style="font-size:9px;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.1em;color:#FF5500;">Upcoming</div>
        </div>
        """, unsafe_allow_html=True)
    st.button("Full Schedule", use_container_width=True, key="home_sched")

    # ─── HIGHLIGHTS ───────────────────────────────────────────────────────────
    st.markdown(section_header("Top Plays"), unsafe_allow_html=True)
    for _, h in highlights.nlargest(3, "views").iterrows():
        cat = h['category'].replace('_', ' ').upper()
        st.markdown(f"""
        <div style="padding:14px 0;border-bottom:1px solid #1E1200;">
            <div style="font-size:9px;color:#555;text-transform:uppercase;
                         letter-spacing:0.1em;margin-bottom:5px;">{cat} · Week {h['week']}</div>
            <div style="font-size:15px;font-weight:700;color:#FFF;line-height:1.3;margin-bottom:3px;">
                {h['title']}
            </div>
            <div style="font-size:10px;color:#444;">{int(h['views']):,} views</div>
        </div>
        """, unsafe_allow_html=True)
    st.button("All Highlights", use_container_width=True, key="home_hl")

    # ─── FEATURED PLAYER ──────────────────────────────────────────────────────
    featured_p = players[players["is_featured"] == True]
    if not featured_p.empty:
        p = featured_p.iloc[0]
        tn = get_team_name(teams, p["team_id"])
        st.markdown(section_header("Player Spotlight"), unsafe_allow_html=True)
        st.markdown(f"""
        <div class="drew-card" style="border-top:2px solid #FF5500;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
                <div>
                    <div style="font-size:20px;font-weight:900;color:#FFF;
                                 text-transform:uppercase;">{p['name']}</div>
                    <div style="font-size:9px;color:#555;text-transform:uppercase;
                                 letter-spacing:0.1em;margin-top:3px;">{tn} · #{p['jersey_number']} · {p['position']}</div>
                </div>
                <div style="font-size:40px;font-weight:900;color:#FFF;line-height:1;">
                    #{p['jersey_number']}
                </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0;border-top:1px solid #1E1200;">
                <div style="text-align:center;padding:12px 8px;border-right:1px solid #1E1200;">
                    <div style="font-size:22px;font-weight:900;color:#FFF;">{p['points_per_game']}</div>
                    <div style="font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.1em;">PPG</div>
                </div>
                <div style="text-align:center;padding:12px 8px;border-right:1px solid #1E1200;">
                    <div style="font-size:22px;font-weight:900;color:#FFF;">{p['assists_per_game']}</div>
                    <div style="font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.1em;">APG</div>
                </div>
                <div style="text-align:center;padding:12px 8px;border-right:1px solid #1E1200;">
                    <div style="font-size:22px;font-weight:900;color:#FFF;">{p['rebounds_per_game']}</div>
                    <div style="font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.1em;">RPG</div>
                </div>
                <div style="text-align:center;padding:12px 8px;">
                    <div style="font-size:22px;font-weight:900;color:#FFF;">{int(p['field_goal_pct']*100)}%</div>
                    <div style="font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.1em;">FG%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ─── PARTNERS ─────────────────────────────────────────────────────────────
    st.markdown(section_header("Partners"), unsafe_allow_html=True)
    sponsor_html = ""
    for _, s in sponsors[sponsors["tier"].isin(["title","gold"])].iterrows():
        sponsor_html += f'<span class="sponsor-chip">{s["name"]}</span>'
    st.markdown(f"""
    <div style="padding:12px 0;border-top:1px solid #1E1200;border-bottom:1px solid #1E1200;margin-bottom:24px;">
        {sponsor_html}
    </div>
    """, unsafe_allow_html=True)

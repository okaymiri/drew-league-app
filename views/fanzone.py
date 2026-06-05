"""
fanzone.py — Fan Zone. Podcasts, community, tickets, newsletter.
"""
import streamlit as st
from utils.data_loader import load_podcasts, load_tickets, load_games, load_teams, get_team_name
from utils.styles import section_header


def render():
    podcasts = load_podcasts()
    tickets  = load_tickets()
    games    = load_games()
    teams    = load_teams()

    st.markdown(section_header("Fan Zone", "Stay Connected"), unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["TICKETS", "PODCASTS", "COMMUNITY"])

    # ─── TICKETS ──────────────────────────────────────────────────────────────
    with tab1:
        upcoming = games[games["status"] == "upcoming"].head(4)
        for _, g in upcoming.iterrows():
            home_name = get_team_name(teams, g["home_team_id"])
            away_name = get_team_name(teams, g["away_team_id"])
            date_str  = g["game_date"].strftime("%b %d") if hasattr(g["game_date"], "strftime") else g["game_date"]
            game_tix  = tickets[tickets["game_id"] == g["game_id"]]

            st.markdown(f"""
            <div class="drew-card" style="margin-bottom:10px;">
                <div style="font-size:9px;color:#FF5500;font-weight:700;text-transform:uppercase;
                             letter-spacing:0.12em;margin-bottom:6px;">Upcoming · {date_str}</div>
                <div style="font-size:17px;font-weight:900;text-transform:uppercase;margin-bottom:10px;">
                    {home_name} vs {away_name}
                </div>
            """, unsafe_allow_html=True)

            if not game_tix.empty:
                for _, t in game_tix.iterrows():
                    avail = int(t["available"])
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                                 padding:10px 0;border-top:1px solid #1E1200;">
                        <div>
                            <div style="font-size:12px;font-weight:700;color:#FFF;text-transform:uppercase;">
                                {t['ticket_type'].replace('_',' ').title()}
                            </div>
                            <div style="font-size:10px;color:#555;">{avail} left</div>
                        </div>
                        <div style="font-size:22px;font-weight:900;color:#FFF;">${t['price']:.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
            st.button("Get Tickets", key=f"tix_{g['game_id']}", use_container_width=True)

        st.markdown("""
        <div class="drew-card" style="border-top:2px solid #FFFFFF;padding:20px;margin-top:16px;">
            <div style="font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:8px;">Best Value</div>
            <div style="font-size:20px;font-weight:900;text-transform:uppercase;margin-bottom:4px;">2026 Season Pass</div>
            <div style="font-size:13px;color:#666;margin-bottom:12px;">All games. All season.</div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:32px;font-weight:900;color:#FFF;">$299</div>
                <div style="font-size:10px;color:#555;">Courtside from $799</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Get Season Pass", use_container_width=True)

    # ─── PODCASTS ─────────────────────────────────────────────────────────────
    with tab2:
        if not podcasts.empty:
            sorted_pods = podcasts.sort_values("release_date", ascending=False)
            for _, ep in sorted_pods.iterrows():
                date_str = ep["release_date"].strftime("%b %d, %Y") if hasattr(ep["release_date"], "strftime") else ep["release_date"]
                cat      = ep["category"].replace("_", " ").upper()

                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"""
                    <div style="padding:14px 0;border-bottom:1px solid #1E1200;">
                        <div style="font-size:9px;color:#555;text-transform:uppercase;
                                     letter-spacing:0.1em;margin-bottom:5px;">
                            Ep {ep['episode_number']} · {cat} · {ep['duration_min']} min
                        </div>
                        <div style="font-size:15px;font-weight:700;color:#FFF;
                                     line-height:1.3;margin-bottom:4px;">
                            {ep['title']}
                        </div>
                        <div style="font-size:11px;color:#555;">{date_str}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.button("Play", key=f"p_{ep['episode_id']}", use_container_width=True)

    # ─── COMMUNITY ────────────────────────────────────────────────────────────
    with tab3:
        st.markdown("""
        <div class="drew-card" style="border-top:2px solid #FF5500;padding:20px;margin-bottom:10px;">
            <div style="font-size:9px;color:#555;text-transform:uppercase;
                         letter-spacing:0.15em;margin-bottom:8px;">Newsletter</div>
            <div style="font-size:18px;font-weight:900;text-transform:uppercase;margin-bottom:6px;">
                Stay Connected
            </div>
            <div style="font-size:13px;color:#666;">
                Game updates, drops, and Drew League stories. Every Friday.
            </div>
        </div>
        """, unsafe_allow_html=True)

        email = st.text_input("Email address", placeholder="your@email.com", key="fz_email")
        st.button("Subscribe", use_container_width=True, key="fz_sub")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(section_header("Get Involved"), unsafe_allow_html=True)

        options = [
            ("Volunteer",     "Help run game days and youth clinics."),
            ("Media",         "Photographers, videographers, and writers."),
            ("Coaching",      "Lead youth development programs."),
        ]
        for title, desc in options:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div style="padding:14px 0;border-bottom:1px solid #1E1200;">
                    <div style="font-size:13px;font-weight:700;color:#FFF;
                                 text-transform:uppercase;margin-bottom:3px;">{title}</div>
                    <div style="font-size:12px;color:#555;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.button("Join", key=f"fz_{title}", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(section_header("Become a Partner"), unsafe_allow_html=True)
        name  = st.text_input("Name",  key="fz_name")
        email2 = st.text_input("Email", key="fz_email2")
        co    = st.text_input("Company", key="fz_co")
        st.button("Request Sponsorship Info", use_container_width=True)

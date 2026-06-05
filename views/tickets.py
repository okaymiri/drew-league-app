"""
tickets.py — Ticket purchasing.
"""
import streamlit as st
from utils.data_loader import load_tickets, load_games, load_teams, get_team_name
from utils.styles import section_header


def render():
    tickets = load_tickets()
    games   = load_games()
    teams   = load_teams()

    st.markdown(section_header("Tickets", "2026 Season"), unsafe_allow_html=True)

    st.markdown("""
    <div class="drew-card" style="border-top:2px solid #FFFFFF;padding:28px;margin-bottom:28px;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px;">
            <div>
                <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                             letter-spacing:0.15em;color:#555;margin-bottom:10px;">Best Value</div>
                <h2 style="font-size:28px;font-weight:900;margin:0 0 8px 0;text-transform:uppercase;">
                    2026 Season Pass
                </h2>
                <p style="color:#888;margin:0;font-size:14px;">All games. All season. One price.</p>
            </div>
            <div style="text-align:right;">
                <div style="font-size:10px;color:#555;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;">From</div>
                <div style="font-size:40px;font-weight:900;color:#FFFFFF;">$299</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["UPCOMING GAMES", "SEASON PASSES", "MY TICKETS"])

    with tab1:
        upcoming_games = games[games["status"] == "upcoming"]
        if upcoming_games.empty:
            st.info("No upcoming games at this time.")
        else:
            for _, g in upcoming_games.iterrows():
                home_name    = get_team_name(teams, g["home_team_id"])
                away_name    = get_team_name(teams, g["away_team_id"])
                date_str     = g["game_date"].strftime("%A, %B %d, %Y") if hasattr(g["game_date"], "strftime") else g["game_date"]
                game_tickets = tickets[tickets["game_id"] == g["game_id"]]

                st.markdown(f"""
                <div class="drew-card" style="margin-bottom:16px;">
                    <div style="font-size:10px;color:#C8102E;font-weight:700;text-transform:uppercase;
                                 letter-spacing:0.1em;margin-bottom:8px;">Upcoming · {date_str}</div>
                    <div style="font-size:20px;font-weight:900;margin-bottom:4px;text-transform:uppercase;">
                        {home_name} vs {away_name}
                    </div>
                    <div style="font-size:11px;color:#555;text-transform:uppercase;
                                 letter-spacing:0.08em;margin-bottom:16px;">{g['location']} · Week {g['week']}</div>
                """, unsafe_allow_html=True)

                if not game_tickets.empty:
                    ticket_cols = st.columns(len(game_tickets))
                    for i, (_, t) in enumerate(game_tickets.iterrows()):
                        avail_pct   = (t["available"] / t["total"]) * 100 if t["total"] > 0 else 0
                        avail_color = "#FFFFFF" if avail_pct > 50 else "#888" if avail_pct > 20 else "#C8102E"
                        perks       = [p.strip() for p in str(t["perks"]).split(",")]

                        with ticket_cols[i]:
                            st.markdown(f"""
                            <div style="background:#0A0A0A;border:1px solid #1A1A1A;padding:16px;text-align:center;">
                                <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                                             letter-spacing:0.1em;color:#888;margin-bottom:8px;">
                                    {t['ticket_type'].replace('_', ' ').title()}
                                </div>
                                <div style="font-size:32px;font-weight:900;color:#FFFFFF;margin-bottom:4px;">
                                    ${t['price']:.0f}
                                </div>
                                <div style="font-size:10px;color:{avail_color};margin-bottom:12px;
                                             text-transform:uppercase;letter-spacing:0.08em;">
                                    {int(t['available'])} left
                                </div>
                                <div style="text-align:left;margin-bottom:8px;">
                                    {''.join([f'<div style="font-size:11px;color:#555;margin-bottom:3px;">{p}</div>' for p in perks])}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            st.button(f"${t['price']:.0f}", key=f"buy_{t['ticket_id']}", use_container_width=True)

                st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        season_tickets = tickets[tickets["game_id"] == 0]
        for _, t in season_tickets.iterrows():
            perks       = [p.strip() for p in str(t["perks"]).split(",")]
            is_court    = "courtside" in t["ticket_type"].lower()
            border      = "#FFFFFF" if is_court else "#1A1A1A"

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div style="background:#0A0A0A;border:1px solid {border};padding:24px;margin-bottom:12px;">
                    <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                                 letter-spacing:0.12em;color:#555;margin-bottom:8px;">Season Pass</div>
                    <div style="font-size:22px;font-weight:900;margin-bottom:8px;text-transform:uppercase;">
                        {t['ticket_type'].replace('_', ' ').title()}
                    </div>
                    <div style="font-size:13px;color:#666;margin-bottom:16px;">{t['description']}</div>
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="font-size:36px;font-weight:900;color:#FFFFFF;">${t['price']:.0f}</div>
                        <div style="font-size:11px;color:#444;text-transform:uppercase;letter-spacing:0.08em;">
                            {int(t['available'])} of {int(t['total'])} left
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.button("Purchase", key=f"pass_{t['ticket_id']}", use_container_width=True)

    with tab3:
        st.markdown("""
        <div class="drew-card" style="text-align:center;padding:48px;">
            <div style="font-size:14px;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.1em;margin-bottom:8px;">Sign In to View Your Tickets</div>
            <div style="color:#555;font-size:13px;">
                Your purchased tickets will appear here.
            </div>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("Sign In", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:16px 0;border-top:1px solid #1A1A1A;">
        <div style="font-size:11px;color:#444;">
            Secure checkout via Stripe. Accepts Visa, Mastercard, Apple Pay, and Google Pay.
        </div>
    </div>
    """, unsafe_allow_html=True)

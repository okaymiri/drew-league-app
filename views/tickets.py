"""
tickets.py — Ticket purchasing page with QR concept and Stripe placeholder.
"""
import streamlit as st
from utils.data_loader import load_tickets, load_games, load_teams, get_team_name
from utils.styles import section_header, badge
import datetime


def render():
    tickets = load_tickets()
    games = load_games()
    teams = load_teams()

    st.markdown(section_header("Tickets", "Secure your spot at the Drew"), unsafe_allow_html=True)

    # ─── SEASON PASS HERO ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1A0A00,#0A0A0A);border:2px solid #FFD700;
                 border-radius:16px;padding:36px;margin-bottom:32px;">
        <div style="font-size:11px;color:#FFD700;font-weight:700;text-transform:uppercase;
                     letter-spacing:0.2em;margin-bottom:12px;">🏆 Best Value</div>
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px;">
            <div>
                <h2 style="font-size:36px;font-weight:900;margin:0 0 8px 0;">2026 Season Pass</h2>
                <p style="color:#999;font-size:16px;margin:0 0 16px 0;">
                    All games. All season. One price. The ultimate Drew League experience.
                </p>
                <div style="display:flex;gap:16px;flex-wrap:wrap;">
                    <div>
                        <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:0.1em;">General</div>
                        <div style="font-size:28px;font-weight:900;color:#FFFFFF;">$299</div>
                    </div>
                    <div>
                        <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:0.1em;">Courtside</div>
                        <div style="font-size:28px;font-weight:900;color:#FFD700;">$799</div>
                    </div>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:13px;color:#999;margin-bottom:8px;">Limited passes available</div>
                <div style="background:#FFD700;color:#000;padding:14px 32px;border-radius:8px;
                             font-weight:700;font-size:15px;text-transform:uppercase;letter-spacing:0.05em;
                             display:inline-block;cursor:pointer;">
                    Get Season Pass →
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── TABS ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["UPCOMING GAMES", "SEASON PASSES", "MY TICKETS"])

    with tab1:
        upcoming_games = games[games["status"] == "upcoming"]

        if upcoming_games.empty:
            st.info("No upcoming games at this time. Check back soon.")
        else:
            for _, g in upcoming_games.iterrows():
                home_name = get_team_name(teams, g["home_team_id"])
                away_name = get_team_name(teams, g["away_team_id"])
                date_str = g["game_date"].strftime("%A, %B %d, %Y") if hasattr(g["game_date"], "strftime") else g["game_date"]
                game_tickets = tickets[tickets["game_id"] == g["game_id"]]

                st.markdown(f"""
                <div class="drew-card" style="margin-bottom:16px;">
                    <div style="margin-bottom:16px;">
                        <div style="font-size:11px;color:#3B82F6;font-weight:700;text-transform:uppercase;
                                     letter-spacing:0.1em;margin-bottom:6px;">UPCOMING · {date_str}</div>
                        <h3 style="font-size:22px;font-weight:900;margin:0 0 4px 0;">
                            {home_name} vs {away_name}
                        </h3>
                        <div style="font-size:13px;color:#666;">{g['location']} · Week {g['week']}</div>
                    </div>
                """, unsafe_allow_html=True)

                if not game_tickets.empty:
                    ticket_cols = st.columns(len(game_tickets))
                    for i, (_, t) in enumerate(game_tickets.iterrows()):
                        avail_pct = (t["available"] / t["total"]) * 100 if t["total"] > 0 else 0
                        avail_color = "#22C55E" if avail_pct > 50 else "#F59E0B" if avail_pct > 20 else "#C8102E"
                        perks = [p.strip() for p in str(t["perks"]).split(",")]

                        with ticket_cols[i]:
                            st.markdown(f"""
                            <div style="background:#0A0A0A;border:1px solid #2A2A2A;border-radius:10px;
                                         padding:16px;text-align:center;height:100%;">
                                <div style="font-size:13px;font-weight:700;text-transform:uppercase;
                                             letter-spacing:0.05em;color:#FFD700;margin-bottom:8px;">
                                    {t['ticket_type'].replace('_', ' ').title()}
                                </div>
                                <div style="font-size:32px;font-weight:900;color:#FFFFFF;margin-bottom:4px;">
                                    ${t['price']:.0f}
                                </div>
                                <div style="font-size:11px;color:{avail_color};margin-bottom:12px;">
                                    {int(t['available'])} left of {int(t['total'])}
                                </div>
                                <div style="text-align:left;margin-bottom:12px;">
                                    {''.join([f'<div style="font-size:11px;color:#999;margin-bottom:3px;">✓ {p}</div>' for p in perks])}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            st.button(f"Buy ${t['price']:.0f}", key=f"buy_{t['ticket_id']}", use_container_width=True)

                st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        season_tickets = tickets[tickets["game_id"] == 0]
        for _, t in season_tickets.iterrows():
            perks = [p.strip() for p in str(t["perks"]).split(",")]
            is_courtside = "courtside" in t["ticket_type"].lower()
            border = "#FFD700" if is_courtside else "#C8102E"

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div style="background:#1A1A1A;border:2px solid {border};border-radius:12px;
                             padding:24px;margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <div style="font-size:11px;color:{border};font-weight:700;text-transform:uppercase;
                                         letter-spacing:0.1em;margin-bottom:8px;">Season Pass</div>
                            <div style="font-size:22px;font-weight:900;margin-bottom:8px;">
                                {t['ticket_type'].replace('_', ' ').title()}
                            </div>
                            <div style="font-size:13px;color:#999;margin-bottom:16px;">{t['description']}</div>
                            <div style="display:flex;flex-wrap:wrap;gap:6px;">
                                {''.join([f'<span style="background:#1A1A1A;border:1px solid #2A2A2A;color:#CCC;padding:4px 10px;border-radius:20px;font-size:11px;">✓ {p}</span>' for p in perks])}
                            </div>
                        </div>
                        <div style="text-align:right;flex-shrink:0;margin-left:20px;">
                            <div style="font-size:40px;font-weight:900;color:{border};">${t['price']:.0f}</div>
                            <div style="font-size:12px;color:#666;">{int(t['available'])} of {int(t['total'])} left</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.button("Purchase Pass", key=f"pass_{t['ticket_id']}", use_container_width=True)

    with tab3:
        # Mock logged-in user ticket
        st.markdown("""
        <div class="drew-card" style="text-align:center;padding:48px;">
            <div style="font-size:48px;margin-bottom:16px;">🎟️</div>
            <div style="font-size:20px;font-weight:700;margin-bottom:8px;">Sign In to View Your Tickets</div>
            <div style="color:#666;margin-bottom:24px;">Your purchased tickets and QR codes will appear here.</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("Sign In / Create Account", use_container_width=True)

            st.markdown("---")

            # Demo QR ticket
            st.markdown("""
            <div style="border:2px dashed #C8102E;border-radius:12px;padding:24px;text-align:center;margin-top:16px;">
                <div style="font-size:11px;color:#C8102E;font-weight:700;text-transform:uppercase;letter-spacing:0.2em;margin-bottom:12px;">
                    Sample Ticket Preview
                </div>
                <div style="font-size:18px;font-weight:900;margin-bottom:4px;">Kings vs Legends</div>
                <div style="font-size:13px;color:#999;margin-bottom:12px;">June 28, 2026 · Drew League Court</div>
                <div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;padding:16px;
                             font-size:32px;letter-spacing:4px;font-family:monospace;color:#FFD700;">
                    ■■■■■<br>■□□□■<br>■□■□■<br>■□□□■<br>■■■■■
                </div>
                <div style="font-size:12px;color:#666;margin-top:8px;">QR Code · Seat: GA-087</div>
            </div>
            """, unsafe_allow_html=True)

    # ─── STRIPE PLACEHOLDER ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="drew-card" style="border-color:#2A2A2A;">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="font-size:24px;">🔒</div>
            <div>
                <div style="font-size:14px;font-weight:700;margin-bottom:2px;">Secure Checkout via Stripe</div>
                <div style="font-size:12px;color:#666;">All transactions are encrypted and secured by Stripe Payments.
                    Accepts Visa, Mastercard, Apple Pay, and Google Pay.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

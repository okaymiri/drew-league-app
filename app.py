"""
app.py — Drew League Digital Platform MVP
Entry point. Handles navigation and page routing.
"""
import streamlit as st
from utils.styles import inject_css

st.set_page_config(
    page_title="Drew League | Official Platform",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ─── NAV DEFINITIONS ───────────────────────────────────────────────────────────
NAV_ITEMS = [
    "🏠  Home",
    "📊  Scores",
    "📅  Schedule",
    "🎬  Highlights",
    "🎙️  Podcasts",
    "🎟️  Tickets",
    "👕  Merch",
    "⭐  Membership",
    "🤝  Community",
    "⚙️  Admin",
]

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 20px 0 24px 0; border-bottom: 1px solid #2A2A2A; margin-bottom: 16px;">
        <div style="font-size: 22px; font-weight: 900; letter-spacing: -0.02em; color: #FFFFFF;">
            DREW LEAGUE
        </div>
        <div style="font-size: 10px; letter-spacing: 0.2em; color: #C8102E; text-transform: uppercase; margin-top: 4px;">
            No Excuse · Just Produce
        </div>
        <div style="font-size: 10px; color: #666; margin-top: 2px;">
            Est. 1973 · Los Angeles, CA · 53 Years
        </div>
    </div>
    """, unsafe_allow_html=True)

    selection = st.radio(
        "Navigation",
        NAV_ITEMS,
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Live indicator
    st.markdown("""
    <div style="padding: 12px 0;">
        <span style="background:#22C55E;color:#000;padding:4px 10px;border-radius:20px;
                     font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">
            ● Season Live
        </span>
        <div style="color:#666;font-size:12px;margin-top:8px;">
            2026 Season · Week 3 of 12
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top: 40px; border-top: 1px solid #2A2A2A; padding-top: 16px;">
        <div style="color: #666; font-size: 11px; text-align: center;">
            © 2026 Drew League<br>
            Los Angeles, California<br>
            <span style="color:#C8102E;">drewleague.org</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── PAGE ROUTING ─────────────────────────────────────────────────────────────
if selection == "🏠  Home":
    from views import home
    home.render()
elif selection == "📊  Scores":
    from views import scores
    scores.render()
elif selection == "📅  Schedule":
    from views import schedule
    schedule.render()
elif selection == "🎬  Highlights":
    from views import highlights
    highlights.render()
elif selection == "🎙️  Podcasts":
    from views import podcasts
    podcasts.render()
elif selection == "🎟️  Tickets":
    from views import tickets
    tickets.render()
elif selection == "👕  Merch":
    from views import merch
    merch.render()
elif selection == "⭐  Membership":
    from views import membership
    membership.render()
elif selection == "🤝  Community":
    from views import community
    community.render()
elif selection == "⚙️  Admin":
    from views import admin
    admin.render()

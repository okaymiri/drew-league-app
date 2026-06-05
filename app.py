"""
app.py — Drew League. Mobile-first layout.
"""
import streamlit as st
from utils.styles import inject_css

st.set_page_config(
    page_title="Drew League",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_css()

# ─── APP HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div style="font-size:17px;font-weight:900;letter-spacing:0.06em;
                 color:#FFFFFF;text-transform:uppercase;">
        DREW LEAGUE
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
        <div style="background:#FF5500;color:#FFF;padding:3px 8px;font-size:9px;
                     font-weight:700;text-transform:uppercase;letter-spacing:0.12em;">
            LIVE
        </div>
        <div style="font-size:9px;color:#444;text-transform:uppercase;letter-spacing:0.1em;">
            Wk 3
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── NAV ──────────────────────────────────────────────────────────────────────
NAV_ITEMS = [
    "Home",
    "Schedule",
    "Stats",
    "Watch",
    "Fan Zone",
    "Shop",
    "Members",
    "Admin",
]

selection = st.radio("nav", NAV_ITEMS, horizontal=True, label_visibility="collapsed")

st.markdown('<div class="page-content">', unsafe_allow_html=True)

# ─── ROUTING ──────────────────────────────────────────────────────────────────
if selection == "Home":
    from views import home
    home.render()
elif selection == "Schedule":
    from views import schedule
    schedule.render()
elif selection == "Stats":
    from views import scores
    scores.render()
elif selection == "Watch":
    from views import highlights
    highlights.render()
elif selection == "Fan Zone":
    from views import fanzone
    fanzone.render()
elif selection == "Shop":
    from views import merch
    merch.render()
elif selection == "Members":
    from views import membership
    membership.render()
elif selection == "Admin":
    from views import admin
    admin.render()

st.markdown('</div>', unsafe_allow_html=True)

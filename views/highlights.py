"""
highlights.py — Highlights hub.
"""
import streamlit as st
from utils.data_loader import load_highlights, load_players, load_teams, get_player_name
from utils.styles import section_header


def render():
    highlights = load_highlights()
    players    = load_players()

    st.markdown(section_header("Highlights", "2026 Season"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        cats = ["All"] + sorted(highlights["category"].unique().tolist())
        cat_filter = st.selectbox("Category", cats)
    with col2:
        weeks = ["All Weeks"] + [f"Week {w}" for w in sorted(highlights["week"].dropna().unique())]
        week_filter = st.selectbox("Week", weeks)
    with col3:
        sort_by = st.selectbox("Sort By", ["Most Viewed", "Newest"])

    filtered = highlights.copy()
    if cat_filter != "All":
        filtered = filtered[filtered["category"] == cat_filter]
    if week_filter != "All Weeks":
        filtered = filtered[filtered["week"] == int(week_filter.replace("Week ", ""))]
    filtered = filtered.sort_values("views" if sort_by == "Most Viewed" else "week", ascending=False)

    st.markdown("<br>", unsafe_allow_html=True)

    for _, h in filtered.iterrows():
        cat_label  = h['category'].replace('_', ' ').upper()
        views_fmt  = f"{int(h['views']):,}"
        player_str = ""
        if h["player_id"] > 0:
            pname      = get_player_name(players, int(h["player_id"]))
            player_str = f'<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#FF5500;margin-bottom:4px;">{pname}</div>'

        title_html = f'<div style="font-size:15px;font-weight:700;color:#FFFFFF;line-height:1.3;margin-bottom:4px;">{h["title"]}</div>'
        meta_html  = f'<div style="font-size:10px;color:#555;">{views_fmt} views</div>'
        desc_html  = f'<div style="font-size:12px;color:#555;margin-top:6px;line-height:1.5;">{str(h["description"])[:100]}...</div>'
        label_html = f'<div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#664422;margin-bottom:6px;">{cat_label} · Wk {h["week"]}</div>'

        card = f'<div style="background:#0D0800;border:1px solid #1E1200;padding:14px;margin-bottom:8px;">{label_html}{player_str}{title_html}{meta_html}{desc_html}</div>'

        st.markdown(card, unsafe_allow_html=True)

        with st.expander(f"> Watch"):
            if h["youtube_url"] and str(h["youtube_url"]) != "nan":
                st.components.v1.iframe(h["youtube_url"], height=280)
            else:
                st.caption("Video coming soon.")

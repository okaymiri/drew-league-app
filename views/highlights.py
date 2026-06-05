"""
highlights.py — Highlights hub with video embeds, filters, and top plays.
"""
import streamlit as st
from utils.data_loader import load_highlights, load_players, load_teams, get_team_name, get_player_name
from utils.styles import section_header, badge


def render():
    highlights = load_highlights()
    players = load_players()
    teams = load_teams()

    st.markdown(section_header("Highlights Hub", "The best plays from the Drew League"), unsafe_allow_html=True)

    # ─── FILTERS ──────────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        cats = ["All"] + sorted(highlights["category"].unique().tolist())
        cat_filter = st.selectbox("Category", cats)
    with col2:
        weeks = ["All Weeks"] + [f"Week {w}" for w in sorted(highlights["week"].dropna().unique())]
        week_filter = st.selectbox("Week", weeks)
    with col3:
        sort_by = st.selectbox("Sort By", ["Most Viewed", "Newest", "Season"])

    # ─── APPLY FILTERS ────────────────────────────────────────────────────────
    filtered = highlights.copy()
    if cat_filter != "All":
        filtered = filtered[filtered["category"] == cat_filter]
    if week_filter != "All Weeks":
        week_num = int(week_filter.replace("Week ", ""))
        filtered = filtered[filtered["week"] == week_num]

    if sort_by == "Most Viewed":
        filtered = filtered.sort_values("views", ascending=False)
    elif sort_by == "Newest":
        filtered = filtered.sort_values("week", ascending=False)

    # ─── CATEGORY STATS ───────────────────────────────────────────────────────
    total_views = int(highlights["views"].sum())
    st.markdown(f"""
    <div style="display:flex;gap:16px;margin-bottom:24px;flex-wrap:wrap;">
        <div class="drew-card" style="flex:1;min-width:140px;text-align:center;">
            <div style="font-size:28px;font-weight:900;color:#FFD700;">{len(highlights)}</div>
            <div style="font-size:12px;color:#666;text-transform:uppercase;letter-spacing:0.1em;">Videos</div>
        </div>
        <div class="drew-card" style="flex:1;min-width:140px;text-align:center;">
            <div style="font-size:28px;font-weight:900;color:#C8102E;">{total_views:,}</div>
            <div style="font-size:12px;color:#666;text-transform:uppercase;letter-spacing:0.1em;">Total Views</div>
        </div>
        <div class="drew-card" style="flex:1;min-width:140px;text-align:center;">
            <div style="font-size:28px;font-weight:900;color:#FFFFFF;">{len(highlights['week'].unique())}</div>
            <div style="font-size:12px;color:#666;text-transform:uppercase;letter-spacing:0.1em;">Weeks Covered</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── TOP PLAYS SECTION ────────────────────────────────────────────────────
    top_plays = highlights[highlights["category"] == "top_plays"]
    if not top_plays.empty:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1A0000,#0A0A0A);border:1px solid #C8102E;
                     border-radius:16px;padding:24px;margin-bottom:24px;">
            <div style="font-size:11px;color:#C8102E;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.2em;margin-bottom:8px;">🔥 Weekly Feature</div>
            <div style="font-size:24px;font-weight:900;margin-bottom:4px;">Top 10 Plays</div>
            <div style="font-size:14px;color:#999;">The most insane moments from this week's games</div>
        </div>
        """, unsafe_allow_html=True)

        for _, h in top_plays.iterrows():
            views_fmt = f"{int(h['views']):,}"
            st.markdown(f"""
            <div class="highlight-card" style="margin-bottom:16px;">
                <div style="display:flex;gap:16px;align-items:flex-start;">
                    <div style="background:#C8102E;border-radius:8px;padding:16px;
                                 flex-shrink:0;font-size:24px;line-height:1;">▶</div>
                    <div style="flex:1;">
                        <div style="margin-bottom:8px;">{badge(h['category'].replace('_',' ').upper())}</div>
                        <div style="font-size:18px;font-weight:700;color:#FFFFFF;margin-bottom:6px;line-height:1.3;">
                            {h['title']}
                        </div>
                        <div style="font-size:13px;color:#666;margin-bottom:12px;">
                            {views_fmt} views · Week {h['week']} · 2026 Season
                        </div>
                        <div style="font-size:13px;color:#999;">{h['description']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Embed YouTube video
            if h["youtube_url"] and str(h["youtube_url"]) != "nan":
                with st.expander("▶ Watch Now"):
                    st.components.v1.iframe(h["youtube_url"], height=340)

    # ─── ALL HIGHLIGHTS GRID ──────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_header("All Highlights", f"{len(filtered)} videos"), unsafe_allow_html=True)

    if filtered.empty:
        st.info("No highlights match your filters.")
        return

    # Two-column grid
    cols = st.columns(2)
    for idx, (_, h) in enumerate(filtered.iterrows()):
        col = cols[idx % 2]
        views_fmt = f"{int(h['views']):,}"
        cat_label = h['category'].replace('_', ' ').title()

        with col:
            player_str = ""
            if h["player_id"] > 0:
                player_name = get_player_name(players, int(h["player_id"]))
                player_str = f'<div style="font-size:12px;color:#C8102E;font-weight:700;margin-bottom:4px;">{player_name}</div>'

            st.markdown(f"""
            <div class="highlight-card" style="min-height:160px;">
                <div style="display:flex;flex-direction:column;height:100%;gap:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        {badge(cat_label)}
                        <span style="font-size:11px;color:#666;">Wk {h['week']}</span>
                    </div>
                    {player_str}
                    <div style="font-size:15px;font-weight:700;color:#FFFFFF;line-height:1.3;flex:1;">
                        {h['title']}
                    </div>
                    <div style="font-size:12px;color:#666;">{views_fmt} views</div>
                    <div style="font-size:12px;color:#999;line-height:1.4;">{h['description'][:100]}...</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("▶ Watch"):
                if h["youtube_url"] and str(h["youtube_url"]) != "nan":
                    st.components.v1.iframe(h["youtube_url"], height=280)
                else:
                    st.info("Video coming soon")

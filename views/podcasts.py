"""
podcasts.py — Podcast and media hub.
"""
import streamlit as st
from utils.data_loader import load_podcasts
from utils.styles import section_header

CATEGORY_LABELS = {
    "history":        "History",
    "player_stories": "Player Stories",
    "community":      "Community",
    "business":       "Business",
}


def render():
    podcasts = load_podcasts()

    st.markdown(section_header("Inside The Drew", "Podcasts · Interviews · Stories"), unsafe_allow_html=True)

    latest = podcasts.sort_values("release_date", ascending=False).iloc[0] if not podcasts.empty else None
    if latest is not None:
        date_str  = latest["release_date"].strftime("%B %d, %Y") if hasattr(latest["release_date"], "strftime") else latest["release_date"]
        cat_label = CATEGORY_LABELS.get(latest["category"], latest["category"].title())

        st.markdown(f"""
        <div class="drew-card" style="border-top:2px solid #C8102E;padding:28px;margin-bottom:24px;">
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.15em;color:#555;margin-bottom:12px;">Latest Episode</div>
            <h2 style="font-size:26px;font-weight:900;margin:0 0 10px 0;line-height:1.2;">
                {latest['title']}
            </h2>
            <div style="font-size:12px;color:#555;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">
                {cat_label} · {latest['duration_min']} min · {date_str}
            </div>
            <div style="font-size:12px;color:#666;margin-bottom:12px;">
                With {latest['guest']} · Hosted by {latest['host']}
            </div>
            <p style="color:#888;line-height:1.7;margin:0 0 20px 0;font-size:14px;max-width:700px;">
                {latest['description']}
            </p>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <a href="{latest['spotify_url']}" target="_blank" style="text-decoration:none;">
                    <div style="border:1px solid #333;color:#FFFFFF;padding:8px 16px;font-size:10px;
                                 font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">Spotify</div>
                </a>
                <a href="{latest['apple_url']}" target="_blank" style="text-decoration:none;">
                    <div style="border:1px solid #333;color:#FFFFFF;padding:8px 16px;font-size:10px;
                                 font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">Apple Podcasts</div>
                </a>
                <div style="border:1px solid #333;color:#FFFFFF;padding:8px 16px;font-size:10px;
                             font-weight:700;text-transform:uppercase;letter-spacing:0.1em;cursor:pointer;">YouTube</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if latest["youtube_url"] and str(latest["youtube_url"]) != "nan":
            with st.expander("Watch on YouTube"):
                st.components.v1.iframe(latest["youtube_url"], height=340)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(section_header("All Episodes", f"{len(podcasts)} episodes"), unsafe_allow_html=True)
    with col2:
        cat_options = ["All Categories"] + list(CATEGORY_LABELS.values())
        cat_filter = st.selectbox("Filter", cat_options, label_visibility="collapsed")

    filtered = podcasts.copy()
    if cat_filter != "All Categories":
        reverse_map = {v: k for k, v in CATEGORY_LABELS.items()}
        if cat_filter in reverse_map:
            filtered = filtered[filtered["category"] == reverse_map[cat_filter]]
    filtered = filtered.sort_values("release_date", ascending=False)

    for _, ep in filtered.iterrows():
        date_str  = ep["release_date"].strftime("%B %d, %Y") if hasattr(ep["release_date"], "strftime") else ep["release_date"]
        cat_label = CATEGORY_LABELS.get(ep["category"], ep["category"].title())

        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="drew-card" style="margin-bottom:6px;">
                <div style="display:flex;gap:16px;align-items:flex-start;">
                    <div style="min-width:48px;text-align:center;padding-top:4px;">
                        <div style="font-size:10px;color:#444;text-transform:uppercase;letter-spacing:0.1em;">Ep</div>
                        <div style="font-size:22px;font-weight:900;color:#FFFFFF;">{ep['episode_number']}</div>
                    </div>
                    <div style="flex:1;">
                        <div style="font-size:10px;color:#444;text-transform:uppercase;
                                     letter-spacing:0.1em;margin-bottom:6px;">
                            {cat_label} · {ep['duration_min']} min · {date_str}
                        </div>
                        <div style="font-size:16px;font-weight:700;color:#FFFFFF;margin-bottom:4px;line-height:1.3;">
                            {ep['title']}
                        </div>
                        <div style="font-size:12px;color:#555;margin-bottom:8px;">
                            With {ep['guest']} · Hosted by {ep['host']}
                        </div>
                        <div style="font-size:13px;color:#666;line-height:1.5;">
                            {ep['description'][:140]}...
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.button("Play", key=f"play_{ep['episode_id']}", use_container_width=True)
            with st.expander("Links"):
                st.markdown(f"[Spotify]({ep['spotify_url']})")
                st.markdown(f"[Apple]({ep['apple_url']})")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="drew-card" style="border-top:1px solid #1A1A1A;text-align:center;padding:36px;">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                     letter-spacing:0.2em;color:#555;margin-bottom:10px;">Newsletter</div>
        <h3 style="font-size:22px;font-weight:900;margin:0 0 8px 0;text-transform:uppercase;">
            Never Miss an Episode
        </h3>
        <p style="color:#666;margin:0 0 0 0;font-size:14px;">New episodes every Friday.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("Email address", placeholder="you@email.com")
        if st.button("Subscribe", use_container_width=True):
            if email and "@" in email:
                st.success(f"Subscribed. Welcome to Inside The Drew.")
            else:
                st.error("Enter a valid email address.")

"""
podcasts.py — Podcast & media hub with episode pages and embedded links.
"""
import streamlit as st
from utils.data_loader import load_podcasts
from utils.styles import section_header, badge


CATEGORY_LABELS = {
    "history": "History",
    "player_stories": "Player Stories",
    "community": "Community",
    "business": "Business",
}


def render():
    podcasts = load_podcasts()

    st.markdown(section_header("Inside The Drew", "Podcasts · Interviews · Community Stories"), unsafe_allow_html=True)

    # ─── HERO PODCAST ──────────────────────────────────────────────────────────
    latest = podcasts.sort_values("release_date", ascending=False).iloc[0] if not podcasts.empty else None
    if latest is not None:
        date_str = latest["release_date"].strftime("%B %d, %Y") if hasattr(latest["release_date"], "strftime") else latest["release_date"]
        cat_label = CATEGORY_LABELS.get(latest["category"], latest["category"].title())
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1A1A0A,#0A0A0A);border:1px solid #FFD700;
                     border-radius:16px;padding:32px;margin-bottom:32px;">
            <div style="font-size:11px;color:#FFD700;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.2em;margin-bottom:12px;">🎙️ Latest Episode</div>
            <div style="font-size:12px;color:#666;margin-bottom:8px;">{badge(cat_label, 'gold')}</div>
            <h2 style="font-size:28px;font-weight:900;margin:0 0 8px 0;line-height:1.2;">{latest['title']}</h2>
            <div style="display:flex;gap:16px;margin-bottom:16px;flex-wrap:wrap;">
                <span style="color:#999;font-size:13px;">Guest: <strong style="color:#FFF;">{latest['guest']}</strong></span>
                <span style="color:#999;font-size:13px;">Host: <strong style="color:#FFF;">{latest['host']}</strong></span>
                <span style="color:#999;font-size:13px;">{latest['duration_min']} min</span>
                <span style="color:#999;font-size:13px;">{date_str}</span>
            </div>
            <p style="color:#ccc;line-height:1.6;margin:0 0 20px 0;max-width:700px;">{latest['description']}</p>
            <div style="display:flex;gap:12px;flex-wrap:wrap;">
                <a href="{latest['spotify_url']}" target="_blank">
                    <div style="background:#1DB954;color:#000;padding:10px 20px;border-radius:6px;
                                 font-weight:700;font-size:13px;display:inline-block;">▶ Spotify</div>
                </a>
                <a href="{latest['apple_url']}" target="_blank">
                    <div style="background:#FC3C44;color:#FFF;padding:10px 20px;border-radius:6px;
                                 font-weight:700;font-size:13px;display:inline-block;">▶ Apple Podcasts</div>
                </a>
                <div style="border:1px solid #666;color:#FFF;padding:10px 20px;border-radius:6px;
                             font-weight:700;font-size:13px;display:inline-block;cursor:pointer;">▶ YouTube</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Embed video
        if latest["youtube_url"] and str(latest["youtube_url"]) != "nan":
            with st.expander("▶ Watch on YouTube"):
                st.components.v1.iframe(latest["youtube_url"], height=340)

    # ─── PLATFORM LINKS ────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="drew-card" style="text-align:center;padding:24px;">
            <div style="font-size:32px;margin-bottom:8px;">🟢</div>
            <div style="font-size:16px;font-weight:700;margin-bottom:4px;">Spotify</div>
            <div style="font-size:12px;color:#666;margin-bottom:12px;">Stream all episodes</div>
            <div style="background:#1DB954;color:#000;padding:8px 16px;border-radius:6px;
                         font-weight:700;font-size:12px;text-align:center;">Follow on Spotify</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="drew-card" style="text-align:center;padding:24px;">
            <div style="font-size:32px;margin-bottom:8px;">🎵</div>
            <div style="font-size:16px;font-weight:700;margin-bottom:4px;">Apple Podcasts</div>
            <div style="font-size:12px;color:#666;margin-bottom:12px;">Subscribe and review</div>
            <div style="background:#FC3C44;color:#FFF;padding:8px 16px;border-radius:6px;
                         font-weight:700;font-size:12px;text-align:center;">Listen on Apple</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="drew-card" style="text-align:center;padding:24px;">
            <div style="font-size:32px;margin-bottom:8px;">▶️</div>
            <div style="font-size:16px;font-weight:700;margin-bottom:4px;">YouTube</div>
            <div style="font-size:12px;color:#666;margin-bottom:12px;">Watch with video</div>
            <div style="background:#FF0000;color:#FFF;padding:8px 16px;border-radius:6px;
                         font-weight:700;font-size:12px;text-align:center;">Subscribe on YouTube</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── FILTER BY CATEGORY ────────────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])
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

    # ─── EPISODE LIST ──────────────────────────────────────────────────────────
    for _, ep in filtered.iterrows():
        date_str = ep["release_date"].strftime("%B %d, %Y") if hasattr(ep["release_date"], "strftime") else ep["release_date"]
        cat_label = CATEGORY_LABELS.get(ep["category"], ep["category"].title())

        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="drew-card" style="margin-bottom:8px;">
                <div style="display:flex;gap:16px;align-items:flex-start;">
                    <div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;
                                 padding:16px;flex-shrink:0;text-align:center;min-width:60px;">
                        <div style="font-size:11px;color:#666;text-transform:uppercase;">Ep</div>
                        <div style="font-size:24px;font-weight:900;color:#FFD700;">{ep['episode_number']}</div>
                    </div>
                    <div style="flex:1;">
                        <div style="display:flex;gap:8px;align-items:center;margin-bottom:6px;flex-wrap:wrap;">
                            {badge(cat_label, 'gold')}
                            <span style="font-size:11px;color:#666;">{ep['duration_min']} min</span>
                            <span style="font-size:11px;color:#666;">{date_str}</span>
                        </div>
                        <div style="font-size:17px;font-weight:700;color:#FFFFFF;margin-bottom:4px;line-height:1.3;">
                            {ep['title']}
                        </div>
                        <div style="font-size:13px;color:#999;margin-bottom:8px;">
                            With {ep['guest']} · Hosted by {ep['host']}
                        </div>
                        <div style="font-size:13px;color:#999;line-height:1.5;">
                            {ep['description'][:150]}...
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.button("▶ Play", key=f"play_{ep['episode_id']}", use_container_width=True)
            with st.expander("Links"):
                st.markdown(f"[Spotify]({ep['spotify_url']})")
                st.markdown(f"[Apple]({ep['apple_url']})")

    # ─── NEWSLETTER SIGNUP ─────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="drew-card" style="text-align:center;padding:40px;border-color:#C8102E;">
        <div style="font-size:11px;color:#C8102E;font-weight:700;text-transform:uppercase;letter-spacing:0.2em;margin-bottom:12px;">
            Inside The Drew Newsletter
        </div>
        <h3 style="font-size:24px;font-weight:900;margin:0 0 8px 0;">Never Miss an Episode</h3>
        <p style="color:#999;margin:0 0 20px 0;">New episodes every Friday. Stories from the court, community, and beyond.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("Your email", placeholder="you@email.com")
        if st.button("Subscribe to Newsletter", use_container_width=True):
            if email and "@" in email:
                st.success(f"Subscribed! Welcome to Inside The Drew, {email}")
            else:
                st.error("Please enter a valid email address.")

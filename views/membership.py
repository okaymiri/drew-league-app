"""
membership.py — Membership tiers, benefits, and upgrade flows.
"""
import streamlit as st
from utils.data_loader import load_memberships
from utils.styles import section_header, badge


TIER_ICONS = {"Free Fan": "🏀", "Drew Insider": "⭐", "Courtside Member": "👑", "Legacy Member": "🏆"}
TIER_STYLES = {
    "Free Fan": {"border": "#2A2A2A", "bg": "#1A1A1A", "label_color": "#FFFFFF"},
    "Drew Insider": {"border": "#C8102E", "bg": "#1A0000", "label_color": "#C8102E"},
    "Courtside Member": {"border": "#FFD700", "bg": "#1A0F00", "label_color": "#FFD700"},
    "Legacy Member": {"border": "#C9A84C", "bg": "#0F0A00", "label_color": "#C9A84C"},
}


def render():
    memberships = load_memberships()

    st.markdown(section_header("Membership", "Join the Drew League community at your level"), unsafe_allow_html=True)

    # ─── MEMBER STATS ─────────────────────────────────────────────────────────
    total_members = memberships["member_count"].sum()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Members", f"{total_members:,}")
    col2.metric("Free Fans", f"{int(memberships[memberships['name']=='Free Fan']['member_count'].values[0]):,}" if not memberships.empty else "—")
    col3.metric("Insiders", f"{int(memberships[memberships['name']=='Drew Insider']['member_count'].values[0]):,}" if not memberships.empty else "—")
    col4.metric("Courtside+", f"{int(memberships[memberships['name'].isin(['Courtside Member','Legacy Member'])]['member_count'].sum()):,}" if not memberships.empty else "—")

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── TIER CARDS ───────────────────────────────────────────────────────────
    st.markdown(section_header("Choose Your Tier"), unsafe_allow_html=True)

    for _, tier in memberships.iterrows():
        style = TIER_STYLES.get(tier["name"], TIER_STYLES["Free Fan"])
        icon = TIER_ICONS.get(tier["name"], "🏀")
        benefits_list = [b.strip() for b in str(tier["benefits"]).split(",")]

        is_free = tier["price_monthly"] == 0
        price_display = "FREE" if is_free else f"${tier['price_monthly']}/mo"
        annual_display = "" if is_free else f"or ${tier['price_annual']}/year (save {int((1 - tier['price_annual']/(tier['price_monthly']*12))*100)}%)"

        available = int(tier["member_count"])
        popular_badge = ""
        if tier["name"] == "Drew Insider":
            popular_badge = f'<span style="background:#C8102E;color:#FFF;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-left:8px;">MOST POPULAR</span>'
        elif tier["name"] == "Legacy Member":
            popular_badge = f'<span style="background:#C9A84C;color:#000;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-left:8px;">LIMITED</span>'

        col1, col2 = st.columns([4, 1])
        with col1:
            benefits_html = "".join([
                f'<div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #2A2A2A;">'
                f'<span style="color:{style["label_color"]};font-size:14px;">✓</span>'
                f'<span style="color:#CCC;font-size:13px;">{b}</span></div>'
                for b in benefits_list
            ])

            st.markdown(f"""
            <div style="background:{style['bg']};border:2px solid {style['border']};border-radius:16px;
                         padding:28px;margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;margin-bottom:20px;">
                    <div>
                        <div style="display:flex;align-items:center;margin-bottom:8px;">
                            <span style="font-size:28px;margin-right:12px;">{icon}</span>
                            <span style="font-size:22px;font-weight:900;color:{style['label_color']};">{tier['name']}</span>
                            {popular_badge}
                        </div>
                        <div style="font-size:13px;color:#999;">{available:,} current members</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:36px;font-weight:900;color:{style['label_color']};">{price_display}</div>
                        <div style="font-size:12px;color:#666;">{annual_display}</div>
                    </div>
                </div>
                <div>{benefits_html}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            if is_free:
                st.button("Join Free", key=f"join_{tier['tier_id']}", use_container_width=True)
            else:
                st.button(f"Upgrade →", key=f"join_{tier['tier_id']}", use_container_width=True)
                if not is_free:
                    st.caption(f"${tier['price_annual']}/yr")

    # ─── COMPARISON TABLE ─────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_header("Feature Comparison"), unsafe_allow_html=True)

    features = [
        ("Scores & Schedule", True, True, True, True),
        ("Public Highlights", True, True, True, True),
        ("Exclusive Highlight Clips", False, True, True, True),
        ("Behind the Scenes", False, True, True, True),
        ("Monthly Newsletter", False, True, True, True),
        ("Member Discord", False, True, True, True),
        ("Merch Discount", False, "10%", "20%", "30%"),
        ("VIP Ticket Access", False, False, "2/mo", "Unlimited"),
        ("Player Interviews", False, False, True, True),
        ("Priority Event Access", False, False, True, True),
        ("Quarterly Merch Drop", False, False, False, True),
        ("Name in Program", False, False, False, True),
        ("Annual Gala Invite", False, False, False, True),
        ("Sponsor Recognition", False, False, False, True),
    ]

    header_html = """
    <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:4px;
                 margin-bottom:8px;padding:12px 16px;background:#1A1A1A;border-radius:8px;">
        <div style="font-size:12px;font-weight:700;color:#666;text-transform:uppercase;">Feature</div>
        <div style="font-size:12px;font-weight:700;color:#FFF;text-transform:uppercase;text-align:center;">Free</div>
        <div style="font-size:12px;font-weight:700;color:#C8102E;text-transform:uppercase;text-align:center;">Insider</div>
        <div style="font-size:12px;font-weight:700;color:#FFD700;text-transform:uppercase;text-align:center;">Courtside</div>
        <div style="font-size:12px;font-weight:700;color:#C9A84C;text-transform:uppercase;text-align:center;">Legacy</div>
    </div>
    """
    rows_html = ""
    for feature, *vals in features:
        cells = ""
        for v in vals:
            if v is True:
                cells += '<div style="text-align:center;color:#22C55E;font-size:16px;">✓</div>'
            elif v is False:
                cells += '<div style="text-align:center;color:#333;font-size:16px;">—</div>'
            else:
                cells += f'<div style="text-align:center;font-size:12px;font-weight:700;color:#FFD700;">{v}</div>'
        rows_html += f"""
        <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:4px;
                     padding:10px 16px;border-bottom:1px solid #1A1A1A;">
            <div style="font-size:13px;color:#CCC;">{feature}</div>
            {cells}
        </div>
        """

    st.markdown(f"""
    <div style="background:#111;border:1px solid #2A2A2A;border-radius:12px;overflow:hidden;">
        {header_html}
        {rows_html}
    </div>
    """, unsafe_allow_html=True)

    # ─── FINAL CTA ────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:40px;">
        <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:0.2em;margin-bottom:12px;">
            53 Years Strong
        </div>
        <h2 style="font-size:36px;font-weight:900;margin:0 0 12px 0;">Be Part of the Legacy</h2>
        <p style="color:#999;font-size:16px;max-width:500px;margin:0 auto 24px;">
            Every membership tier supports the Drew League community, youth programs, and
            the continuation of LA basketball culture.
        </p>
    </div>
    """, unsafe_allow_html=True)

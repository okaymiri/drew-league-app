"""
membership.py — Membership tiers.
"""
import streamlit as st
from utils.data_loader import load_memberships
from utils.styles import section_header

TIER_BORDER = {
    "Free Fan":         "#1E1200",
    "Drew Insider":     "#FF5500",
    "Courtside Member": "#FFFFFF",
    "Legacy Member":    "#555555",
}


def render():
    memberships = load_memberships()

    st.markdown(section_header("Membership", "Join the Drew League"), unsafe_allow_html=True)

    total = memberships["member_count"].sum()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Members", f"{total:,}")
    try:
        c2.metric("Free Fans",  f"{int(memberships[memberships['name']=='Free Fan']['member_count'].values[0]):,}")
        c3.metric("Insiders",   f"{int(memberships[memberships['name']=='Drew Insider']['member_count'].values[0]):,}")
        c4.metric("Courtside+", f"{int(memberships[memberships['name'].isin(['Courtside Member','Legacy Member'])]['member_count'].sum()):,}")
    except Exception:
        pass

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_header("Choose Your Tier"), unsafe_allow_html=True)

    for _, tier in memberships.iterrows():
        border   = TIER_BORDER.get(tier["name"], "#1E1200")
        is_free  = tier["price_monthly"] == 0
        price    = "FREE" if is_free else f"${tier['price_monthly']}/mo"
        annual   = "" if is_free else f"${tier['price_annual']}/yr"
        benefits = [b.strip() for b in str(tier["benefits"]).split(",")]
        count    = f"{int(tier['member_count']):,} members"

        popular = ""
        if tier["name"] == "Drew Insider":
            popular = '<span style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#FF5500;border:1px solid #FF5500;padding:2px 7px;margin-left:10px;">Most Popular</span>'
        elif tier["name"] == "Legacy Member":
            popular = '<span style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#555;border:1px solid #333;padding:2px 7px;margin-left:10px;">Limited</span>'

        benefit_rows = "".join([f'<div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #1E1200;"><span style="color:#444;font-size:11px;">+</span><span style="color:#888;font-size:13px;">{b}</span></div>' for b in benefits])

        card_html = f'<div style="background:#0D0800;border:1px solid {border};padding:20px;margin-bottom:10px;"><div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;"><div><div style="display:flex;align-items:center;margin-bottom:4px;"><span style="font-size:17px;font-weight:900;color:#FFFFFF;text-transform:uppercase;">{tier["name"]}</span>{popular}</div><div style="font-size:10px;color:#444;text-transform:uppercase;letter-spacing:0.08em;">{count}</div></div><div style="text-align:right;"><div style="font-size:28px;font-weight:900;color:#FFFFFF;">{price}</div><div style="font-size:10px;color:#444;">{annual}</div></div></div><div>{benefit_rows}</div></div>'

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(card_html, unsafe_allow_html=True)
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            btn_label = "Join Free" if is_free else "Upgrade"
            st.button(btn_label, key=f"join_{tier['tier_id']}", use_container_width=True)
            if not is_free:
                st.caption(f"${tier['price_annual']}/yr")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_header("Feature Comparison"), unsafe_allow_html=True)

    features = [
        ("Scores & Schedule",    True,  True,  True,      True),
        ("Public Highlights",    True,  True,  True,      True),
        ("Exclusive Clips",      False, True,  True,      True),
        ("Behind the Scenes",    False, True,  True,      True),
        ("Newsletter",           False, True,  True,      True),
        ("Merch Discount",       False, "10%", "20%",     "30%"),
        ("VIP Ticket Access",    False, False, "2/mo",    "Unlimited"),
        ("Player Interviews",    False, False, True,      True),
        ("Quarterly Merch Drop", False, False, False,     True),
        ("Gala Invite",          False, False, False,     True),
    ]

    header_html = '<div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;padding:10px 16px;background:#0D0800;border:1px solid #1E1200;border-bottom:none;"><div style="font-size:9px;font-weight:700;color:#444;text-transform:uppercase;letter-spacing:0.1em;">Feature</div><div style="font-size:9px;font-weight:700;color:#FFF;text-transform:uppercase;text-align:center;">Free</div><div style="font-size:9px;font-weight:700;color:#FF5500;text-transform:uppercase;text-align:center;">Insider</div><div style="font-size:9px;font-weight:700;color:#FFF;text-transform:uppercase;text-align:center;">Courtside</div><div style="font-size:9px;font-weight:700;color:#888;text-transform:uppercase;text-align:center;">Legacy</div></div>'

    rows_html = ""
    for feature, *vals in features:
        cells = ""
        for v in vals:
            if v is True:
                cells += '<div style="text-align:center;color:#FFF;font-size:13px;font-weight:700;">+</div>'
            elif v is False:
                cells += '<div style="text-align:center;color:#222;font-size:13px;">·</div>'
            else:
                cells += f'<div style="text-align:center;font-size:10px;font-weight:700;color:#888;">{v}</div>'
        rows_html += f'<div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;padding:9px 16px;border:1px solid #1E1200;border-top:none;"><div style="font-size:12px;color:#666;">{feature}</div>{cells}</div>'

    st.markdown(f'<div style="margin-bottom:32px;">{header_html}{rows_html}</div>', unsafe_allow_html=True)

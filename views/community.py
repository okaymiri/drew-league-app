"""
community.py — Community, history, foundation, and sponsorship.
"""
import streamlit as st
from utils.data_loader import load_sponsors
from utils.styles import section_header


def render():
    sponsors = load_sponsors()

    st.markdown(section_header("Community", "Rooted in South Central · Built for LA"), unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["HISTORY", "COMMUNITY IMPACT", "PARTNERS", "GET INVOLVED"])

    # ─── HISTORY ──────────────────────────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div style="padding:40px 0 32px 0;border-bottom:1px solid #1E1200;margin-bottom:32px;">
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.2em;color:#555;margin-bottom:12px;">Est. 1973</div>
            <h2 style="font-size:42px;font-weight:900;margin:0 0 12px 0;line-height:1;text-transform:uppercase;">
                53 Years of Summer Basketball in Los Angeles
            </h2>
            <p style="color:#666;font-size:14px;line-height:1.7;max-width:700px;margin:0;">
                The Drew League is more than a basketball league. It is a cultural institution
                that has shaped the identity of South Central Los Angeles since 1973.
            </p>
        </div>
        """, unsafe_allow_html=True)

        milestones = [
            ("1973", "The Beginning",        "The Drew League is founded in South Central Los Angeles with 6 original teams. A structured summer basketball outlet during a time of social and economic tension in LA."),
            ("1980s","Community Roots Deepen","The league grows into a cornerstone of South Central summer life. Local legends emerge and the competition level rises."),
            ("1990s","LA Basketball Culture", "The Drew becomes synonymous with Los Angeles basketball. No Excuse, Just Produce becomes a rallying cry for players and the entire community."),
            ("2000s","National Attention",    "NBA players, college stars, and overseas pros make the Drew a summer destination. National media attention follows."),
            ("2010s","Digital Era",           "Games stream on YouTube. Highlight clips go viral. The Drew League reaches global audiences."),
            ("2020", "Resilience",            "COVID-19 pauses the season. The community rallies and returns stronger."),
            ("2026", "53 Years Strong",       "The Drew League celebrates 53 years. A digital platform launches. The legacy continues."),
        ]

        for year, title, desc in milestones:
            st.markdown(f"""
            <div style="display:flex;gap:20px;margin-bottom:20px;">
                <div style="min-width:60px;text-align:right;padding-top:4px;">
                    <div style="font-size:12px;font-weight:900;color:#FF5500;">{year}</div>
                </div>
                <div class="drew-card" style="flex:1;margin-bottom:0;">
                    <div style="font-size:14px;font-weight:700;color:#FFFFFF;margin-bottom:6px;
                                 text-transform:uppercase;">{title}</div>
                    <div style="font-size:13px;color:#666;line-height:1.6;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ─── COMMUNITY IMPACT ─────────────────────────────────────────────────────
    with tab2:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Years of Service",    "53")
        col2.metric("Youth Served",        "10,000+")
        col3.metric("Teams in League",     "30+")
        col4.metric("Volunteer Hrs/Year",  "2,000+")

        st.markdown("<br>", unsafe_allow_html=True)

        programs = [
            ("Youth Basketball",  "Free summer clinics for ages 8-18. Skill development, teamwork, and life lessons on the court."),
            ("Academic Support",  "Partnerships with local schools. Player eligibility tied to academic performance."),
            ("Mentorship",        "Former players and community leaders serve as mentors for youth in the program."),
            ("Scholarship Fund",  "Annual scholarships for Drew League youth participants pursuing higher education."),
            ("Community Events",  "Cookouts, holiday giveback events, health fairs, and neighborhood projects."),
            ("Media Representation","Showcasing South Central Los Angeles through high-quality sports content."),
        ]

        cols = st.columns(2)
        for i, (title, desc) in enumerate(programs):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="drew-card" style="margin-bottom:10px;">
                    <div style="font-size:13px;font-weight:700;color:#FFFFFF;margin-bottom:6px;
                                 text-transform:uppercase;">{title}</div>
                    <div style="font-size:13px;color:#666;line-height:1.5;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="drew-card" style="text-align:center;padding:36px;border-top:1px solid #1E1200;">
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.2em;color:#555;margin-bottom:10px;">Support the Mission</div>
            <h3 style="font-size:26px;font-weight:900;margin:0 0 10px 0;text-transform:uppercase;">
                Make a Donation
            </h3>
            <p style="color:#666;font-size:14px;max-width:480px;margin:0 auto;">
                Your contribution funds youth programs, scholarships, and community events.
                Every dollar stays in Los Angeles.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            amount = st.radio("Amount", ["$25", "$50", "$100", "$250", "Custom"], horizontal=True)
            if amount == "Custom":
                st.number_input("Custom amount ($)", min_value=1, value=75)
            if st.button("Donate", use_container_width=True):
                st.success(f"Thank you for your {amount} donation. Stripe checkout coming soon.")

    # ─── PARTNERS ─────────────────────────────────────────────────────────────
    with tab3:
        st.markdown(section_header("Official Partners"), unsafe_allow_html=True)

        for tier_name, tier_label in [("title","Title Partners"), ("gold","Gold Partners"), ("silver","Silver Partners")]:
            tier_sponsors = sponsors[sponsors["tier"] == tier_name]
            if tier_sponsors.empty:
                continue
            st.markdown(f"""
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.15em;color:#555;margin:24px 0 12px 0;">{tier_label}</div>
            """, unsafe_allow_html=True)
            for _, s in tier_sponsors.iterrows():
                st.markdown(f"""
                <div class="drew-card" style="margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
                        <div>
                            <div style="font-size:16px;font-weight:700;color:#FFFFFF;margin-bottom:4px;
                                         text-transform:uppercase;">{s['name']}</div>
                            <div style="font-size:13px;color:#555;">{s['description']}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:10px;color:#444;text-transform:uppercase;
                                         letter-spacing:0.08em;margin-bottom:4px;">Annual Value</div>
                            <div style="font-size:22px;font-weight:900;color:#FFFFFF;">${int(s['annual_value']):,}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="drew-card" style="text-align:center;padding:36px;border-top:2px solid #FF5500;">
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.2em;color:#555;margin-bottom:10px;">Partnerships</div>
            <h3 style="font-size:26px;font-weight:900;margin:0 0 10px 0;text-transform:uppercase;">
                Sponsor the Drew League
            </h3>
            <p style="color:#666;font-size:14px;max-width:560px;margin:0 auto;">
                Reach a passionate audience connected to basketball, culture, and Los Angeles.
                Packages start at $10,000/season.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            contact_name    = st.text_input("Name")
            contact_email   = st.text_input("Business Email")
            contact_company = st.text_input("Company")
            if st.button("Request Partnership Info", use_container_width=True):
                if contact_email and "@" in contact_email:
                    st.success(f"Thank you, {contact_name}. The partnerships team will be in touch.")
                else:
                    st.error("Enter a valid email address.")

    # ─── GET INVOLVED ─────────────────────────────────────────────────────────
    with tab4:
        st.markdown(section_header("Get Involved"), unsafe_allow_html=True)

        options = [
            ("Volunteer",     "Help run game days, youth clinics, and community events."),
            ("Newsletter",    "Drew League community news, stories, and opportunities in your inbox."),
            ("Media",         "Photographers, videographers, and writers — help tell the Drew League story."),
            ("Become a Coach","Experienced players and coaches can apply to lead youth development programs."),
        ]

        for title, desc in options:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="drew-card" style="margin-bottom:8px;">
                    <div style="font-size:14px;font-weight:700;color:#FFFFFF;margin-bottom:4px;
                                 text-transform:uppercase;">{title}</div>
                    <div style="font-size:13px;color:#666;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.button("Sign Up", key=f"signup_{title}", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            signup_name = st.text_input("Full Name", key="community_name")
        with col2:
            signup_email = st.text_input("Email", key="community_email")
        interest = st.multiselect("Areas of Interest",
            ["Volunteer", "Media", "Coaching", "Youth Programs", "Sponsorship", "General Fan"])
        if st.button("Join the Community", use_container_width=True):
            if signup_email and "@" in signup_email:
                st.success(f"Welcome to the Drew League family, {signup_name}.")
            else:
                st.error("Enter a valid email.")

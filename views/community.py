"""
community.py — Community, history, foundation, youth programs, and sponsorship.
"""
import streamlit as st
from utils.data_loader import load_sponsors
from utils.styles import section_header, badge


def render():
    sponsors = load_sponsors()

    st.markdown(section_header("Community & Foundation", "Rooted in South Central · Built for LA"), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["HISTORY", "COMMUNITY IMPACT", "SPONSORS & PARTNERS", "GET INVOLVED"])

    # ─── HISTORY ──────────────────────────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div class="page-hero" style="margin-bottom:32px;">
            <div style="font-size:11px;color:#C8102E;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.2em;margin-bottom:12px;">Est. 1973</div>
            <h2 style="font-size:40px;font-weight:900;margin:0 0 12px 0;line-height:1.1;">
                53 Years of Summer<br>Basketball in Los Angeles
            </h2>
            <p style="color:#999;font-size:16px;line-height:1.6;max-width:700px;">
                The Drew League is more than a basketball league. It is a cultural institution
                that has shaped the identity of South Central Los Angeles since 1973.
            </p>
        </div>
        """, unsafe_allow_html=True)

        milestones = [
            ("1973", "The Beginning", "The Drew League is founded in South Central Los Angeles with 6 original teams. The league provides a structured summer basketball outlet for the community during a time of social and economic tension in LA."),
            ("1980s", "Community Roots Deepen", "The league grows into a cornerstone of South Central summer life. Word spreads through the neighborhood and beyond as the competition level rises and local legends emerge."),
            ("1990s", "LA Basketball Culture", "The Drew becomes synonymous with Los Angeles basketball culture. The 'No Excuse, Just Produce' motto becomes a rallying cry not just for players, but for the entire community."),
            ("2000s", "National Attention", "NBA players, college stars, and overseas pros begin making the Drew a summer destination. The league gains national media attention and becomes a proving ground for elite talent."),
            ("2010s", "Digital Era", "Games are streamed on YouTube and social media. The Drew League reaches global audiences. Highlight clips go viral. The league becomes a premier entertainment product."),
            ("2020", "Resilience", "The COVID-19 pandemic pauses the season. The community rallies. The Drew League demonstrates the resilience that has always defined South Central LA."),
            ("2026", "53 Years Strong", "The Drew League celebrates 53 years of summer basketball. A digital platform launches. The community continues to grow. The legacy endures."),
        ]

        for year, title, desc in milestones:
            st.markdown(f"""
            <div style="display:flex;gap:20px;margin-bottom:24px;">
                <div style="min-width:80px;text-align:right;">
                    <div style="font-size:14px;font-weight:900;color:#C8102E;line-height:1.2;">{year}</div>
                    <div style="width:2px;height:40px;background:#2A2A2A;margin:8px 0 0 auto;"></div>
                </div>
                <div class="drew-card" style="flex:1;">
                    <div style="font-size:16px;font-weight:700;color:#FFFFFF;margin-bottom:8px;">{title}</div>
                    <div style="font-size:13px;color:#999;line-height:1.6;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ─── COMMUNITY IMPACT ─────────────────────────────────────────────────────
    with tab2:
        # Impact stats
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Years of Service", "53")
        col2.metric("Youth Served (Est.)", "10,000+")
        col3.metric("Teams in League", "30+")
        col4.metric("Volunteer Hours/Yr", "2,000+")

        st.markdown("<br>", unsafe_allow_html=True)

        programs = [
            ("🏀", "Youth Basketball Programs", "Free summer basketball clinics for youth ages 8–18. Skill development, teamwork, and life lessons on the court."),
            ("📚", "Academic Support", "The Drew League partners with local schools to encourage academic achievement. Player eligibility tied to academic performance."),
            ("🤝", "Mentorship Network", "Former players and community leaders serve as mentors for youth in the program. Building the next generation of leaders."),
            ("🎓", "Scholarship Fund", "Annual scholarships awarded to Drew League youth participants pursuing higher education. Investing in futures."),
            ("🏙️", "Community Events", "Beyond basketball — community cookouts, holiday giveback events, health fairs, and neighborhood beautification projects."),
            ("📺", "Media & Representation", "Showcasing South Central Los Angeles to the world through high-quality sports content. Representation matters."),
        ]

        cols = st.columns(2)
        for i, (icon, title, desc) in enumerate(programs):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="drew-card" style="margin-bottom:12px;">
                    <div style="display:flex;gap:16px;align-items:flex-start;">
                        <div style="font-size:32px;flex-shrink:0;">{icon}</div>
                        <div>
                            <div style="font-size:16px;font-weight:700;color:#FFFFFF;margin-bottom:6px;">{title}</div>
                            <div style="font-size:13px;color:#999;line-height:1.5;">{desc}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Donation CTA
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0A1A00,#0A0A0A);border:1px solid #22C55E;
                     border-radius:16px;padding:36px;text-align:center;">
            <div style="font-size:11px;color:#22C55E;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.2em;margin-bottom:12px;">Support the Mission</div>
            <h3 style="font-size:28px;font-weight:900;margin:0 0 12px 0;">Make a Donation</h3>
            <p style="color:#999;font-size:15px;max-width:500px;margin:0 auto 24px;">
                Your contribution directly funds youth programs, scholarships, and community events.
                Every dollar stays in Los Angeles.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            donation_amounts = st.radio("Select amount", ["$25", "$50", "$100", "$250", "Custom"], horizontal=True)
            if donation_amounts == "Custom":
                custom_amount = st.number_input("Custom amount ($)", min_value=1, value=75)
            if st.button("Donate Now", use_container_width=True):
                amount = donation_amounts if donation_amounts != "Custom" else f"${custom_amount}"
                st.success(f"Thank you for your {amount} donation! Stripe checkout coming soon.")

    # ─── SPONSORS ─────────────────────────────────────────────────────────────
    with tab3:
        st.markdown(section_header("Official Partners & Sponsors"), unsafe_allow_html=True)

        for tier_name, tier_color in [("title", "#FFD700"), ("gold", "#C9A84C"), ("silver", "#AAAAAA")]:
            tier_sponsors = sponsors[sponsors["tier"] == tier_name]
            if tier_sponsors.empty:
                continue
            tier_label = f"{tier_name.title()} Partners"
            st.markdown(f"""
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.15em;
                         color:{tier_color};margin:24px 0 12px 0;">{tier_label}</div>
            """, unsafe_allow_html=True)

            for _, s in tier_sponsors.iterrows():
                st.markdown(f"""
                <div class="drew-card" style="border-color:{tier_color if tier_name != 'silver' else '#2A2A2A'};margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
                        <div>
                            <div style="font-size:18px;font-weight:700;color:#FFFFFF;margin-bottom:4px;">{s['name']}</div>
                            <div style="font-size:13px;color:#999;margin-bottom:6px;">{s['description']}</div>
                            <div style="display:flex;gap:8px;">
                                {badge(s['category'].replace('_',' ').title())}
                                {badge(s['deal_type'].replace('_',' ').title(), 'gold' if tier_name=='title' else 'default')}
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:13px;color:#666;">Partnership Value</div>
                            <div style="font-size:24px;font-weight:900;color:{tier_color};">${int(s['annual_value']):,}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Sponsorship CTA
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="drew-card" style="border-color:#C8102E;text-align:center;padding:36px;">
            <div style="font-size:11px;color:#C8102E;font-weight:700;text-transform:uppercase;letter-spacing:0.2em;margin-bottom:12px;">
                Become a Partner
            </div>
            <h3 style="font-size:28px;font-weight:900;margin:0 0 12px 0;">Sponsor the Drew League</h3>
            <p style="color:#999;font-size:15px;max-width:600px;margin:0 auto 20px;">
                Reach a passionate, loyal audience deeply connected to basketball, culture,
                and Los Angeles. Sponsorship packages start at $10,000/season.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            contact_name = st.text_input("Your Name")
            contact_email = st.text_input("Business Email")
            contact_company = st.text_input("Company")
            if st.button("Request Sponsorship Info", use_container_width=True):
                if contact_email and "@" in contact_email:
                    st.success(f"Thank you, {contact_name}! Drew League partnerships team will contact you at {contact_email}.")
                else:
                    st.error("Please enter a valid email address.")

    # ─── GET INVOLVED ─────────────────────────────────────────────────────────
    with tab4:
        st.markdown(section_header("Get Involved", "There are many ways to be part of the Drew League"), unsafe_allow_html=True)

        options = [
            ("🙋", "Volunteer", "Help run game days, youth clinics, and community events. No experience needed — just heart."),
            ("📰", "Newsletter", "Stay informed with the Drew League community newsletter. News, stories, and opportunities delivered to your inbox."),
            ("📸", "Media & Content", "Photographers, videographers, and writers — submit your work and help tell the Drew League story."),
            ("🎯", "Become a Coach", "Experienced players and coaches can apply to lead youth clinics and development programs."),
        ]

        for icon, title, desc in options:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="drew-card" style="margin-bottom:8px;">
                    <div style="display:flex;gap:16px;align-items:center;">
                        <div style="font-size:36px;">{icon}</div>
                        <div>
                            <div style="font-size:16px;font-weight:700;color:#FFFFFF;margin-bottom:4px;">{title}</div>
                            <div style="font-size:13px;color:#999;">{desc}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.button(f"Sign Up", key=f"signup_{title}", use_container_width=True)

        # General signup form
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Newsletter Signup**")
        col1, col2 = st.columns(2)
        with col1:
            signup_name = st.text_input("Full Name", key="community_name")
        with col2:
            signup_email = st.text_input("Email Address", key="community_email")
        interest = st.multiselect("Areas of Interest", ["Volunteer", "Media", "Coaching", "Youth Programs", "Sponsorship", "General Fan"])
        if st.button("Join the Drew League Community", use_container_width=True):
            if signup_email and "@" in signup_email:
                st.success(f"Welcome to the Drew League family, {signup_name}! You're now subscribed.")
            else:
                st.error("Please enter a valid email.")

"""
merch.py — Drew League Shop.
"""
import streamlit as st
from utils.data_loader import load_merch
from utils.styles import section_header


def render():
    merch = load_merch()

    st.markdown(section_header("Drew League Shop", "Official Merch · Limited Drops"), unsafe_allow_html=True)

    st.markdown("""
    <div class="drew-card" style="border-top:2px solid #FFFFFF;padding:28px;margin-bottom:28px;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px;">
            <div>
                <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                             letter-spacing:0.15em;color:#555;margin-bottom:10px;">New Drop</div>
                <h2 style="font-size:28px;font-weight:900;margin:0 0 8px 0;text-transform:uppercase;">
                    53 Years Collection
                </h2>
                <p style="color:#888;margin:0;font-size:14px;max-width:500px;">
                    Commemorating 53 years of Drew League basketball in Los Angeles.
                    Limited. Once it's gone, it's gone.
                </p>
            </div>
            <div style="text-align:right;">
                <div style="font-size:10px;color:#555;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;">From</div>
                <div style="font-size:40px;font-weight:900;color:#FFFFFF;">$45</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cats = ["All"] + sorted(merch["category"].unique().tolist())
        cat_filter = st.selectbox("Category", cats)
    with col2:
        price_filter = st.selectbox("Price", ["All Prices", "Under $40", "$40-$60", "Over $60"])
    with col3:
        sort_by = st.selectbox("Sort", ["Featured", "Price: Low to High", "Price: High to Low"])
    with col4:
        collab_only = st.checkbox("Collab Only")

    filtered = merch.copy()
    if cat_filter != "All":
        filtered = filtered[filtered["category"] == cat_filter]
    if price_filter == "Under $40":
        filtered = filtered[filtered["price"] < 40]
    elif price_filter == "$40-$60":
        filtered = filtered[(filtered["price"] >= 40) & (filtered["price"] <= 60)]
    elif price_filter == "Over $60":
        filtered = filtered[filtered["price"] > 60]
    if collab_only:
        filtered = filtered[filtered["is_collab"] == True]
    if sort_by == "Price: Low to High":
        filtered = filtered.sort_values("price")
    elif sort_by == "Price: High to Low":
        filtered = filtered.sort_values("price", ascending=False)
    else:
        filtered = filtered.sort_values("is_featured", ascending=False)

    st.markdown(f"""
    <div style="font-size:11px;color:#444;text-transform:uppercase;
                 letter-spacing:0.1em;margin-bottom:20px;">{len(filtered)} products</div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, (_, p) in enumerate(filtered.iterrows()):
        with cols[idx % 3]:
            labels = ""
            if p["is_featured"]:
                labels += '<span style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#888;border:1px solid #2A1800;padding:2px 6px;margin-right:6px;">Featured</span>'
            if p["is_collab"]:
                labels += '<span style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#FF5500;border:1px solid #FF5500;padding:2px 6px;">Collab</span>'

            stock_color = "#FFFFFF" if p['stock'] > 50 else "#888" if p['stock'] > 20 else "#FF5500"

            st.markdown(f"""
            <div style="background:#0D0800;border:1px solid #1E1200;margin-bottom:16px;">
                <div style="background:#111;height:180px;display:flex;align-items:center;
                             justify-content:center;border-bottom:1px solid #1E1200;">
                    <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                                 letter-spacing:0.2em;color:#2A1800;">{p['category'].upper()}</div>
                </div>
                <div style="padding:16px;">
                    <div style="margin-bottom:8px;">{labels}</div>
                    <div style="font-size:14px;font-weight:700;color:#FFFFFF;margin-bottom:4px;line-height:1.3;">
                        {p['name']}
                    </div>
                    <div style="font-size:12px;color:#555;margin-bottom:10px;">
                        {p['description'][:70]}...
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <div style="font-size:22px;font-weight:900;color:#FFFFFF;">${p['price']:.0f}</div>
                        <div style="font-size:10px;color:{stock_color};text-transform:uppercase;
                                     letter-spacing:0.08em;">{int(p['stock'])} in stock</div>
                    </div>
                    <div style="font-size:10px;color:#444;margin-bottom:2px;">Sizes: {p['sizes']}</div>
                    <div style="font-size:10px;color:#444;">Colors: {p['colors']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            ca, cb = st.columns(2)
            with ca:
                st.button("Add to Cart", key=f"cart_{p['product_id']}", use_container_width=True)
            with cb:
                st.button("View", key=f"view_{p['product_id']}", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:16px 0;border-top:1px solid #1E1200;">
        <div style="font-size:11px;color:#444;">
            Powered by Shopify · Secured by Stripe · Free shipping on orders over $75 · Ships from Los Angeles
        </div>
    </div>
    """, unsafe_allow_html=True)

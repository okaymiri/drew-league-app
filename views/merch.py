"""
merch.py — Official Drew League merch store with Shopify integration placeholder.
"""
import streamlit as st
from utils.data_loader import load_merch
from utils.styles import section_header, badge


def render():
    merch = load_merch()

    st.markdown(section_header("Drew League Shop", "Official Merch · Limited Drops · Collab Releases"), unsafe_allow_html=True)

    # ─── FEATURED BANNER ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1A0000,#0A0000);border:1px solid #C8102E;
                 border-radius:16px;padding:32px;margin-bottom:32px;
                 display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px;">
        <div>
            <div style="font-size:11px;color:#C8102E;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.2em;margin-bottom:8px;">🔥 New Drop</div>
            <h2 style="font-size:32px;font-weight:900;margin:0 0 8px 0;">53 Years Collection</h2>
            <p style="color:#999;margin:0;font-size:15px;">
                Commemorating 53 years of Drew League basketball in Los Angeles.
                Limited numbered print. Once it's gone, it's gone.
            </p>
        </div>
        <div style="text-align:center;">
            <div style="font-size:13px;color:#666;margin-bottom:4px;">Starting at</div>
            <div style="font-size:42px;font-weight:900;color:#C8102E;">$45</div>
            <div style="background:#C8102E;color:#FFF;padding:12px 28px;border-radius:8px;
                         font-weight:700;font-size:14px;text-transform:uppercase;margin-top:8px;">
                Shop Now →
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── FILTER BAR ───────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cats = ["All"] + sorted(merch["category"].unique().tolist())
        cat_filter = st.selectbox("Category", cats)
    with col2:
        price_filter = st.selectbox("Price", ["All Prices", "Under $40", "$40–$60", "Over $60"])
    with col3:
        sort_by = st.selectbox("Sort", ["Featured", "Price: Low to High", "Price: High to Low"])
    with col4:
        collab_only = st.checkbox("Collab Drops Only")

    # ─── APPLY FILTERS ────────────────────────────────────────────────────────
    filtered = merch.copy()
    if cat_filter != "All":
        filtered = filtered[filtered["category"] == cat_filter]
    if price_filter == "Under $40":
        filtered = filtered[filtered["price"] < 40]
    elif price_filter == "$40–$60":
        filtered = filtered[(filtered["price"] >= 40) & (filtered["price"] <= 60)]
    elif price_filter == "Over $60":
        filtered = filtered[filtered["price"] > 60]
    if collab_only:
        filtered = filtered[filtered["is_collab"] == True]
    if sort_by == "Price: Low to High":
        filtered = filtered.sort_values("price")
    elif sort_by == "Price: High to Low":
        filtered = filtered.sort_values("price", ascending=False)
    elif sort_by == "Featured":
        filtered = filtered.sort_values("is_featured", ascending=False)

    st.markdown(f"""
    <div style="font-size:13px;color:#666;margin-bottom:16px;">
        Showing {len(filtered)} of {len(merch)} products
    </div>
    """, unsafe_allow_html=True)

    # ─── PRODUCT GRID ─────────────────────────────────────────────────────────
    cols = st.columns(3)
    for idx, (_, product) in enumerate(filtered.iterrows()):
        col = cols[idx % 3]
        with col:
            featured_badge = badge("FEATURED") if product["is_featured"] else ""
            collab_badge = badge("COLLAB DROP", "gold") if product["is_collab"] else ""

            st.markdown(f"""
            <div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:12px;
                         margin-bottom:16px;overflow:hidden;transition:border-color 0.15s;">
                <!-- Product Image Placeholder -->
                <div style="background:linear-gradient(135deg,#2A2A2A,#1A1A1A);height:200px;
                             display:flex;align-items:center;justify-content:center;font-size:64px;">
                    {'👕' if product['category'] in ['shirts'] else '🧥' if product['category'] == 'hoodies' else '🧢' if product['category'] == 'hats' else '🩳'}
                </div>
                <div style="padding:16px;">
                    <div style="margin-bottom:8px;display:flex;gap:6px;flex-wrap:wrap;">
                        {featured_badge}{collab_badge}
                    </div>
                    <div style="font-size:15px;font-weight:700;color:#FFFFFF;margin-bottom:4px;line-height:1.3;">
                        {product['name']}
                    </div>
                    <div style="font-size:12px;color:#666;margin-bottom:8px;">
                        {product['description'][:80]}...
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                        <div style="font-size:24px;font-weight:900;color:#FFFFFF;">${product['price']:.0f}</div>
                        <div style="font-size:11px;color:{'#22C55E' if product['stock'] > 50 else '#F59E0B' if product['stock'] > 20 else '#C8102E'};">
                            {int(product['stock'])} in stock
                        </div>
                    </div>
                    <div style="font-size:11px;color:#666;margin-bottom:4px;">
                        Sizes: {product['sizes']}
                    </div>
                    <div style="font-size:11px;color:#666;">
                        Colors: {product['colors']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                st.button("Add to Cart", key=f"cart_{product['product_id']}", use_container_width=True)
            with col_b:
                st.button("View", key=f"view_{product['product_id']}", use_container_width=True)

    # ─── CART SUMMARY ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_header("Your Cart"), unsafe_allow_html=True)

    if "cart" not in st.session_state:
        st.session_state.cart = []

    st.markdown("""
    <div class="drew-card" style="text-align:center;padding:32px;border-style:dashed;">
        <div style="font-size:32px;margin-bottom:8px;">🛒</div>
        <div style="font-size:16px;font-weight:700;margin-bottom:4px;">Your cart is empty</div>
        <div style="color:#666;font-size:13px;">Add items above to start your order</div>
    </div>
    """, unsafe_allow_html=True)

    # ─── SHOPIFY & STRIPE NOTICE ──────────────────────────────────────────────
    st.markdown("""
    <div class="drew-card" style="margin-top:16px;">
        <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
            <div style="font-size:24px;">🔒</div>
            <div>
                <div style="font-size:14px;font-weight:700;margin-bottom:2px;">
                    Powered by Shopify · Secured by Stripe
                </div>
                <div style="font-size:12px;color:#666;">
                    Full Shopify store integration and Stripe checkout coming at launch.
                    Free shipping on orders over $75. Merch ships from Los Angeles.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

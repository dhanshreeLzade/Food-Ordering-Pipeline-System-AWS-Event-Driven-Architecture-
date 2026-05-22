import streamlit as st
import requests

st.set_page_config(page_title="Foodo", layout="wide")

# ======================
# ZOMATO STYLE UI + BIG TYPOGRAPHY
# ======================
st.markdown("""
<style>

/* background */
[data-testid="stAppViewContainer"] {
    background-color: #f5f5f5;
}

/* MAIN TITLE BIG */
.title {
    text-align:center;
    font-size:78px;
    font-weight:900;
    color:#e23744;
    letter-spacing:3px;
}

/* SUBTITLE BIGGER */
.subtitle {
    text-align:center;
    font-size:20px;
    color:#555;
    margin-bottom:25px;
}

/* NAV BAR STYLE */
.nav {
    display:flex;
    justify-content:center;
    gap:20px;
    margin-bottom:25px;
}

.nav-item {
    background:white;
    padding:10px 20px;
    border-radius:10px;
    border:1px solid #ddd;
    font-weight:600;
    cursor:pointer;
}

/* CARD */
.card {
    background:white;
    padding:25px;
    border-radius:16px;
    border:1px solid #eee;
    margin-bottom:20px;
}

/* SECTION TITLE BIG */
.section-title {
    font-size:22px;
    font-weight:800;
    color:#333;
    margin-bottom:15px;
}

/* INPUT */
.stTextInput>div>div>input {
    border-radius:10px;
    padding:12px;
    border:1px solid #ddd;
}

/* BUTTON */
.stButton>button {
    background-color:#e23744;
    color:white;
    border-radius:10px;
    padding:12px 20px;
    border:none;
    font-weight:700;
    font-size:15px;
}

.stButton>button:hover {
    background-color:#c81e35;
}

/* TEXT */
h1,h2,h3,h4,p,label {
    color:#333 !important;
}

</style>
""", unsafe_allow_html=True)

# ======================
# NAVIGATION (PRO STYLE)
# ======================
page = st.radio("Navigate", ["🏠 Home", "👨‍🍳 Restaurant", "🚚 Delivery"], horizontal=True)

# ======================
# HEADER
# ======================
st.markdown("<div class='title'>FOODO</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Fast • Fresh • Trusted Food Delivery System</div>", unsafe_allow_html=True)

st.divider()

# ======================
# HOME PAGE
# ======================
if page == "🏠 Home":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🛒 Place Order</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    customer_id = c1.text_input("Customer ID")
    phone = c2.text_input("Phone (+91XXXXXXXXXX)")
    food = c3.text_input("Food Item")

    if st.button("Place Order"):
        try:
            res = requests.post("http://127.0.0.1:5000/order", data={
                "customer_id": customer_id,
                "phone": phone,
                "order_name": food
            })
            st.success(res.text)
        except:
            st.error("Backend not running")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📦 Track Order</div>", unsafe_allow_html=True)

    order_id = st.text_input("Enter Order ID")

    if st.button("Track Order"):
        try:
            res = requests.post("http://127.0.0.1:5000/track", data={"order_id": order_id})
            st.info(res.text)
        except:
            st.error("Backend not running")

    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# RESTAURANT PAGE
# ======================
elif page == "👨‍🍳 Restaurant":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>👨‍🍳 Restaurant Panel</div>", unsafe_allow_html=True)

    rid = st.text_input("Order ID (Restaurant)")

    if st.button("Mark READY"):
        try:
            requests.post("http://127.0.0.1:5000/update", data={
                "order_id": rid,
                "status": "READY"
            })
            st.success("Order marked READY")
        except:
            st.error("Backend not running")

    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# DELIVERY PAGE
# ======================
elif page == "🚚 Delivery":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🚚 Delivery Panel</div>", unsafe_allow_html=True)

    did = st.text_input("Order ID (Delivery)")

    if st.button("Mark DELIVERED"):
        try:
            requests.post("http://127.0.0.1:5000/update", data={
                "order_id": did,
                "status": "DELIVERED"
            })
            st.success("Order marked DELIVERED")
        except:
            st.error("Backend not running")

    st.markdown("</div>", unsafe_allow_html=True)
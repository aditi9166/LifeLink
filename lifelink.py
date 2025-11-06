import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# ===================== PAGE CONFIG ======================
st.set_page_config(page_title="LifeLink Emergency Locator", layout="wide")

# ===================== CUSTOM UI STYLING ======================
custom_style = """
<style>

[data-testid="stAppViewContainer"] {
    background-color: #0b0f1a;
}

[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 2px solid rgba(255,0,0,0.4);
}

h1, h2, h3, h4, p, label, span, .stMarkdown, .css-1kyxreq {
    color: #ffffff !important;
    font-family: 'Arial', sans-serif;
}

.card {
    border-radius: 14px;
    padding: 18px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    margin-top: 10px;
}

.stButton>button {
    background: linear-gradient(90deg, #e60000, #ff4c4c);
    color: white;
    padding: 12px 26px;
    border-radius: 12px;
    font-size: 18px;
    border: none;
    transition: all 0.25s;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #ff4c4c, #e60000);
    transform: scale(1.05);
}

.feature-box {
    background: rgba(255,255,255,0.07);
    border-left: 5px solid #ff4c4c;
    padding: 18px;
    border-radius: 10px;
    margin-bottom: 12px;
}

.footer-text {
    text-align: center;
    color: #dddddd;
    font-size: 14px;
    margin-top: 30px;
}

</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

# ===================== SIDEBAR NAVIGATION ======================
st.sidebar.title("🚨 LifeLink Menu")
page = st.sidebar.radio("Menu",
                        ["🏠 Home", "🏥 Hospital Locator",
                         "🩹 First-Aid Guide", "👤 Medical Profile"])

# ===================== HOME ======================
if page == "🏠 Home":
    st.markdown("<h1>🚨 LifeLink Emergency Locator</h1>", unsafe_allow_html=True)
    st.write("Helping people reach medical help faster ❤️‍🩹")

    st.markdown("---")
    st.subheader("⚡ Quick Emergency Help")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("❤️ Heart Attack Help"):
            st.warning("Call 108 🚑 Give aspirin if available. Time is critical!")

    with col2:
        if st.button("🧠 Stroke Help"):
            st.warning("FAST → Face droop? Arm weak? Speech slurred? Act FAST & call 108!")

    with col3:
        if st.button("🚑 Accident Help"):
            st.warning("Check breathing + bleeding. Do not move victim unless needed!")

    st.markdown("---")
    st.subheader("📞 Emergency Numbers (India)")
    st.info("🚑 Ambulance: 108 | 👮 Police: 100 | 🔥 Fire: 101")

    st.markdown("---")
    st.subheader("✨ LifeLink Features")
    st.markdown("""
    ✅ Nearest Hospital Locator  
    ✅ Quick First-Aid Guidance  
    ✅ Store Emergency Profile  
    ✅ Clean & Fast UI  
    """)

# ===================== HOSPITAL LOCATOR ======================
elif page == "🏥 Hospital Locator":
    st.header("🏥 Find Nearest Hospitals")

    loc_input = st.text_input("Enter your location (City/Area)", placeholder="e.g., Mumbai, Pune, Delhi")

    if st.button("Search Hospital 🏥"):
        if not loc_input:
            st.error("Please enter a location!")
        else:
            geolocator = Nominatim(user_agent="lifelink-app")
            loc = geolocator.geocode(loc_input)

            if loc:
                st.success(f"📍 Found: {loc.address}")

                m = folium.Map(location=[loc.latitude, loc.longitude], zoom_start=13)
                folium.Marker(location=[loc.latitude, loc.longitude],
                              tooltip="You are here",
                              icon=folium.Icon(color="red")).add_to(m)

                st_folium(m, width=900, height=450)
            else:
                st.error("Location not found! Try another spelling.")

# ===================== FIRST AID GUIDE ======================
elif page == "🩹 First-Aid Guide":
    st.header("🩹 First Aid Guide")

    with st.expander("❤️ CPR - For Cardiac Arrest"):
        st.write("""
        ✅ Push hard & fast (Chest center)  
        ✅ 100–120 compressions per minute  
        ✅ Call 108 immediately  
        """)

    with st.expander("🩸 Severe Bleeding"):
        st.write("""
        ✅ Apply pressure immediately  
        ✅ Raise injured area  
        ✅ Do NOT remove soaked bandage  
        """)

    with st.expander("🔥 Burns"):
        st.write("""
        ✅ Cool under water for 20 min  
        ❌ Don't apply oil or toothpaste  
        ✅ Cover loosely with clean cloth  
        """)

# ===================== MEDICAL PROFILE ======================
elif page == "👤 Medical Profile":
    st.header("👤 Emergency Medical Profile")

    if "profile" not in st.session_state:
        st.session_state.profile = {}

    name = st.text_input("Full Name")
    age = st.number_input("Age", 1, 120)
    blood = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    conditions = st.text_area("Health Conditions (optional)")
    emergency = st.text_input("Emergency Contact Number")

    if st.button("💾 Save Profile"):
        st.session_state.profile = {
            "Name": name,
            "Age": age,
            "Blood Group": blood,
            "Health": conditions,
            "Emergency Contact": emergency
        }
        st.success("✅ Profile Saved Securely")

    if st.session_state.profile:
        st.subheader("📌 Saved Details")
        st.json(st.session_state.profile)

# Footer
st.markdown('<p class="footer-text">Made for India 🇮🇳 | LifeLink Emergency App</p>', unsafe_allow_html=True)
